"""Run context: loaded feature profile, build directory, and the stage cache.

The cache is what makes reruns cheap and source changes traceable: every stage
output is stored with a fingerprint of everything that went into it (source
files, prompts, upstream outputs, config). A stage is re-executed only when
that fingerprint changes.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Awaitable, Callable

import yaml

from .paths import BUILD, FEATURES, ROOT


def sha(*parts: Any) -> str:
    h = hashlib.sha256()
    for p in parts:
        if isinstance(p, Path):
            if p.is_dir():
                for f in sorted(p.rglob("*")):
                    if f.is_file() and f.name != ".DS_Store":
                        h.update(f.name.encode()); h.update(f.read_bytes())
            elif p.exists():
                h.update(p.read_bytes())
            else:
                h.update(f"missing:{p}".encode())
        else:
            h.update(json.dumps(p, sort_keys=True, default=str).encode())
    return h.hexdigest()[:16]


@dataclass
class Context:
    feature_id: str
    force: set[str] = field(default_factory=set)       # stage names to force-rerun ("all" for everything)
    log: Callable[[str], None] = print

    def __post_init__(self):
        self.feature_dir = FEATURES / self.feature_id
        self.profile = yaml.safe_load((self.feature_dir / "profile.yaml").read_text())
        self.build = BUILD / self.feature_id
        self.build.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.build / "manifest.json"
        self.manifest = json.loads(self.manifest_path.read_text()) if self.manifest_path.exists() else {}
        self.ran: list[str] = []
        self.reused: list[str] = []

    # ------------------------------------------------------------ helpers --
    def model(self, role: str) -> str:
        models = self.profile.get("models", {})
        return models.get(role, models.get("default", "claude-opus-5-5"))

    def guidance_items(self) -> dict[str, str]:
        """Product-owner statements tagged [G-nn] in guidance.md (citable like facts)."""
        import re
        text = (self.feature_dir / "guidance.md").read_text()
        items = {}
        for m in re.finditer(r"\[(G-\d+)\]\s*(.+?)(?=\n\s*-|\n\n|\Z)", text, re.S):
            items[m.group(1)] = re.sub(r"\s+", " ", m.group(2)).strip()
        return items

    def source_path(self, src: dict) -> Path:
        return (ROOT / src["path"]).resolve() if "path" in src else Path("/nonexistent")

    def out(self, name: str) -> Path:
        p = self.build / f"{name}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def read(self, name: str) -> Any:
        return json.loads(self.out(name).read_text())

    def write(self, name: str, data: Any) -> None:
        self.out(name).write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str))

    def save_manifest(self) -> None:
        self.manifest_path.write_text(json.dumps(self.manifest, indent=2))

    # -------------------------------------------------------------- cache --
    async def stage(self, name: str, inputs: list[Any], fn: Callable[[], Awaitable[Any]]) -> Any:
        """Run `fn` unless its inputs are unchanged since the last run; persist result as build/<name>.json."""
        fp = sha(*inputs)
        forced = "all" in self.force or name in self.force or name.split("/")[0] in self.force
        if not forced and self.manifest.get(name, {}).get("fingerprint") == fp and self.out(name).exists():
            self.reused.append(name)
            return self.read(name)
        self.log(f"  running {name} ...")
        data = await fn()
        self.write(name, data)
        self.manifest[name] = {"fingerprint": fp}
        self.save_manifest()
        self.ran.append(name)
        return data
