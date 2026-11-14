"""Interactive web calculators/forms (e.g. the Zurich source tax tariff calculator).

Two phases, deliberately separated:

1. `explore` (expensive, run on demand: `pipeline explore <source_id>`):
   an agent drives the live site through Playwright MCP, walks every branch
   and records a question tree + test vectors to
   build/<problem>/cache/<source_id>/tree.json, with a snapshot of each
   question's visible text. This is the only step that touches the network.
2. `normalize` (cheap, every run): turns the cached tree into Units
   (C-Q01 per question, C-V01 per test vector). If the site changes, rerun
   explore; the tree's fingerprint changes and everything downstream reruns.
"""
from __future__ import annotations

import json

from pydantic import BaseModel, Field as F

from ...engine.llm import load_prompt, run_agent
from ...engine.schemas import Unit
from ..base import Adapter


class Question(BaseModel):
    id: str = F(description="Q01, Q02 ... in order of first appearance")
    page_text: str = F(description="Verbatim question text as shown on the site")
    control: str = F(description="dropdown | radio | checkbox | date | number | text")
    options: list[str] = F(default_factory=list, description="Verbatim option labels, all of them")
    help_text: str = ""
    shown_when: str = F(default="always", description="Which earlier answers make this question appear, e.g. 'Q02 = Married'")
    required: str = F(default="unknown", description="yes | no | unknown, as observed")


class Vector(BaseModel):
    id: str
    answers: dict[str, str] = F(description="question id -> chosen option label")
    result: str = F(description="Verbatim result shown, e.g. the tariff code")


class Tree(BaseModel):
    url: str
    explored_at: str
    questions: list[Question]
    vectors: list[Vector] = F(default_factory=list)
    notes: list[str] = F(default_factory=list, description="Anything unexplored or ambiguous")


class WebCalculatorAdapter(Adapter):
    type = "web_calculator"
    prefix = "CA"

    @property
    def cache(self):
        return self.ctx.build / "cache" / self.src["id"] / "tree.json"

    def normalize_inputs(self) -> list:
        return [self.cache, self.src]

    async def explore(self) -> dict:
        system = load_prompt(self.dir / "explorer.md", hints=self.src.get("explore_hints", "(none)"))
        out = await run_agent(
            f"explore/{self.src['id']}", system,
            f"Explore this calculator exhaustively: {self.src['url']}",
            Tree, model=self.ctx.model("explore"),
            tools=["mcp__playwright__*"],
            mcp_servers={"playwright": {"command": "npx", "args": ["@playwright/mcp@latest", "--headless"]}},
            max_turns=self.config.get("max_turns", 300),
        )
        self.cache.parent.mkdir(parents=True, exist_ok=True)
        self.cache.write_text(json.dumps(out, indent=2, ensure_ascii=False))
        return out

    async def normalize(self) -> list[Unit]:
        if not self.cache.exists():
            self.ctx.log(f"  ! {self.src['id']}: not explored yet (run `pipeline explore {self.src['id']}`); skipping")
            return []
        tree = Tree.model_validate_json(self.cache.read_text())
        units = []
        for q in tree.questions:
            text = q.page_text
            if q.options:
                text += " Options: " + " | ".join(q.options)
            if q.help_text:
                text += " Help: " + q.help_text
            units.append(Unit(id=f"C-{q.id}", source_id=self.src["id"], text=text,
                              meta={"control": q.control, "shown_when": q.shown_when, "required": q.required}))
        for v in tree.vectors:
            units.append(Unit(id=f"C-{v.id}", source_id=self.src["id"],
                              text=f"Answers {json.dumps(v.answers, ensure_ascii=False)} -> result {v.result}",
                              meta={"kind": "test_vector"}))
        for i, n in enumerate(tree.notes, 1):
            units.append(Unit(id=f"C-N{i:02d}", source_id=self.src["id"], text=n, meta={"kind": "explorer_note"}))
        return units
