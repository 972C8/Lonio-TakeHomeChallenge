"""Source adapter contract.

An adapter turns one kind of source into the two shared types the rest of the
pipeline understands:

    normalize()       -> list[Unit]   addressable pieces of the source, exact text
    extract(units)    -> list[Fact]   atomic, cited claims (default: LLM agent with agent.md)
    verify_anchor()   -> (ok, note)   proof that a cited quote really is in the source

To add a new source type, create pipeline/adapters/<type>/ with adapter.py
(subclass Adapter), agent.md (extraction prompt) and config.yaml, then register
the type in REGISTRY below. Nothing downstream changes.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field as F

from ..engine.context import Context
from ..engine.llm import load_prompt, run_agent
from ..engine.schemas import Anchor, Fact, FactKind, Unit


class ExtractedFact(BaseModel):
    local_id: str = F(description="Your own id for this fact, e.g. f1, f2 ...")
    kind: FactKind
    subject: str = F(description="snake_case topic, e.g. civil_status, source_tax_liability")
    statement: str = F(description="One atomic, self-contained claim in plain English")
    anchors: list[Anchor] = F(description="Exact verbatim quotes from the units that prove the claim")
    basis: Literal["explicit", "inferred"]
    temporality: Literal["desired", "current_state"]
    supersedes: list[str] = F(default_factory=list, description="local_ids of earlier facts this one corrects or retracts")


class Extraction(BaseModel):
    facts: list[ExtractedFact]


def norm_ws(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


def make_fact_id(source_id: str, kind: str, anchors: list[Anchor]) -> str:
    """Source-scoped, content-based id: F-<source id>-<hash of kind + anchors>.

    Two sources can never clash, and the id survives re-extraction as long as
    the fact is anchored on the same quotes (decisions on facts keep working).
    The statement is deliberately not part of the hash: the agent words it
    differently on every run.
    """
    key = "|".join(sorted(f"{a.unit_id}\u241f{norm_ws(a.quote)}" for a in anchors))
    h = hashlib.sha1(f"{kind}\u241e{key}".encode()).hexdigest()[:6]
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", source_id)      # no dots: decision targets split on the first dot
    return f"F-{safe}-{h}"


def build_facts(source_id: str, extracted: list[ExtractedFact], unit_ids: set[str]) -> list[Fact]:
    """Turn the agent's output into Facts: full unit ids in anchors, source-scoped ids, resolved supersedes."""
    facts, local_to_id, used = [], {}, set()
    for ef in extracted:
        d = ef.model_dump(exclude={"local_id"})
        for a in d["anchors"]:       # agents sometimes drop the source prefix; repair it (same source only)
            if a["unit_id"] not in unit_ids and f"{source_id}/{a['unit_id']}" in unit_ids:
                a["unit_id"] = f"{source_id}/{a['unit_id']}"
        fact = Fact(source_id=source_id, local_id=ef.local_id, **d)
        base = make_fact_id(source_id, fact.kind, fact.anchors)
        fid, n = base, 1
        while fid in used:            # identical anchors and kind: keep both, numbered in extraction order
            n += 1
            fid = f"{base}-{n}"
        used.add(fid)
        fact.id = fid
        local_to_id[ef.local_id] = fid
        facts.append(fact)
    for f in facts:
        f.supersedes = [local_to_id[s] for s in f.supersedes if s in local_to_id]
    return facts


class Adapter:
    type: str = "base"

    def uid(self, local_id: str) -> str:
        """Unit ids are scoped by the source id (e.g. hr_transcript/T-044), so sources never clash."""
        return f"{self.src['id']}/{local_id}"

    def __init__(self, src: dict, ctx: Context):
        self.src = src
        self.ctx = ctx
        self.dir = Path(__file__).parent / self.type
        cfg = self.dir / "config.yaml"
        self.config = yaml.safe_load(cfg.read_text()) if cfg.exists() else {}

    # -- fingerprint inputs: anything that, if changed, must trigger a rerun
    def normalize_inputs(self) -> list:
        return [self.ctx.source_path(self.src), self.config, self.src]

    def extract_inputs(self) -> list:
        return [self.dir / "agent.md", self.ctx.feature_dir / "guidance.md"]

    async def normalize(self) -> list[Unit]:
        raise NotImplementedError

    async def extract(self, units: list[Unit]) -> list[Fact]:
        if not units:
            return []
        system = load_prompt(
            self.dir / "agent.md",
            guidance=(self.ctx.feature_dir / "guidance.md").read_text(),
            source_description=self.src.get("description", ""),
        )
        payload = json.dumps([u.model_dump() for u in units], ensure_ascii=False, indent=1)
        prompt = (
            f"Source id: {self.src['id']}\n\nUnits (JSON):\n{payload}\n\n"
            "Extract all facts as instructed. Return the structured output only."
        )
        out = await run_agent(f"extract/{self.src['id']}", system, prompt, Extraction,
                              model=self.ctx.model(self.config.get("model_role", "extract")))
        return build_facts(self.src["id"], Extraction.model_validate(out).facts, {u.id for u in units})

    def verify_anchor(self, anchor: Anchor, units: dict[str, Unit]) -> tuple[bool, str]:
        """Default: the quote must be a verbatim (whitespace/case-insensitive) substring of the unit."""
        u = units.get(anchor.unit_id)
        if u is None:
            return False, f"unit {anchor.unit_id} does not exist"
        if u.source_id != self.src["id"]:
            return False, f"unit {anchor.unit_id} belongs to another source"
        if not anchor.quote.strip():
            return False, "empty quote"
        if norm_ws(anchor.quote) in norm_ws(u.text):
            return True, ""
        return False, f"quote not found in {anchor.unit_id}"


def get_adapter(src: dict, ctx: Context) -> Adapter:
    from .screenshots.adapter import ScreenshotsAdapter
    from .transcript.adapter import TranscriptAdapter
    from .web_calculator.adapter import WebCalculatorAdapter
    registry = {a.type: a for a in (TranscriptAdapter, ScreenshotsAdapter, WebCalculatorAdapter)}
    if src["type"] not in registry:
        raise KeyError(f"no adapter for source type {src['type']!r}; known: {sorted(registry)}")
    return registry[src["type"]](src, ctx)
