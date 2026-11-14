"""Meeting transcripts (PDF, .md or .txt) -> one Unit per speaker turn (<source id>/T-001 ...).

Normalization is deterministic (no LLM), so turn ids are stable across runs and
quotes can be checked by exact substring match.
"""
from __future__ import annotations

import re
from pathlib import Path

from ...engine.schemas import Unit
from ..base import Adapter


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        return "\n".join(p.extract_text() or "" for p in PdfReader(str(path)).pages)
    return path.read_text()


class TranscriptAdapter(Adapter):
    type = "transcript"

    async def normalize(self) -> list[Unit]:
        text = re.sub(r"\s+", " ", read_text(self.ctx.source_path(self.src))).strip()
        speakers = self.src.get("speakers") or self.config.get("speakers") or []
        if not speakers:
            raise ValueError(f"source {self.src['id']}: list the speakers in profile.yaml (speakers: [...])")
        pattern = re.compile(r"\b(" + "|".join(map(re.escape, speakers)) + r"):\s")
        parts = pattern.split(text)
        units = []
        preamble = parts[0].strip()
        if preamble:
            units.append(Unit(id=self.uid("T-000"), source_id=self.src["id"], text=preamble, meta={"speaker": "(document header)"}))
        for i in range(1, len(parts) - 1, 2):
            n = len(units) if preamble else len(units) + 1
            units.append(Unit(id=self.uid(f"T-{n:03d}"), source_id=self.src["id"], text=parts[i + 1].strip(),
                              meta={"speaker": parts[i]}))
        return units
