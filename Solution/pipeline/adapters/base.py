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


class Adapter:
    type: str = "base"
    prefix: str = "X"

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
        return [self.dir / "agent.md", self.ctx.problem_dir / "guidance.md"]

    async def normalize(self) -> list[Unit]:
        raise NotImplementedError

    async def extract(self, units: list[Unit]) -> list[Fact]:
        if not units:
            return []
        system = load_prompt(
            self.dir / "agent.md",
            guidance=(self.ctx.problem_dir / "guidance.md").read_text(),
            source_description=self.src.get("description", ""),
        )
        payload = json.dumps([u.model_dump() for u in units], ensure_ascii=False, indent=1)
        prompt = (
            f"Source id: {self.src['id']}\n\nUnits (JSON):\n{payload}\n\n"
            "Extract all facts as instructed. Return the structured output only."
        )
        out = await run_agent(f"extract/{self.src['id']}", system, prompt, Extraction,
                              model=self.ctx.model(self.config.get("model_role", "extract")))
        facts = []
        local_to_id = {}
        for i, ef in enumerate(Extraction.model_validate(out).facts, 1):
            fid = f"F-{self.prefix}-{i:03d}"
            local_to_id[ef.local_id] = fid
            facts.append(Fact(id=fid, source_id=self.src["id"], local_id=ef.local_id,
                              **ef.model_dump(exclude={"local_id"})))
        for f in facts:  # resolve supersedes to global ids
            f.supersedes = [local_to_id[s] for s in f.supersedes if s in local_to_id]
        return facts

    def verify_anchor(self, anchor: Anchor, units: dict[str, Unit]) -> tuple[bool, str]:
        """Default: the quote must be a verbatim (whitespace/case-insensitive) substring of the unit."""
        u = units.get(anchor.unit_id)
        if u is None:
            return False, f"unit {anchor.unit_id} does not exist"
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
