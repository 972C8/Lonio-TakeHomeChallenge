"""Portal screenshots -> one Unit per visible UI element (S01-E01 ...).

A vision agent transcribes every visible element *verbatim* (labels, values,
options, hints, errors) and tags it with structural metadata. Facts may only
quote this visible text, so every claim about the portal is anchored to
something a human can see on the screenshot.

Optional double read: two independent transcriptions per screenshot are
compared; disagreements are reported so a human can look at that screenshot.
"""
from __future__ import annotations

import asyncio
import re
from collections import Counter
from typing import Literal

from pydantic import BaseModel, Field as F

from ...engine.llm import load_prompt, run_agent
from ...engine.schemas import Unit
from ..base import Adapter, norm_ws

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


class Element(BaseModel):
    kind: Literal["title", "breadcrumb", "section_heading", "field_label", "field_value", "placeholder",
                  "dropdown_option", "hint", "error", "button", "footnote", "other"]
    text: str = F(description="The exact visible text, character for character")
    field: str = F(default="", description="Label of the form field this element belongs to, if any")
    control: Literal["", "text_input", "dropdown", "checkbox", "radio", "button"] = ""
    state: Literal["", "empty", "filled", "open", "error_highlight"] = ""
    required_marker: bool = F(default=False, description="True if the label shows a required marker such as *")


class ScreenRead(BaseModel):
    screen_summary: str = F(description="One sentence: what this screenshot shows (state of the form)")
    elements: list[Element]


class ScreenshotsAdapter(Adapter):
    type = "screenshots"
    prefix = "SC"

    def normalize_inputs(self) -> list:
        return super().normalize_inputs() + [self.dir / "reader.md"]

    def files(self):
        d = self.ctx.source_path(self.src)
        return sorted(p for p in d.iterdir() if p.suffix.lower() in IMAGE_EXT)

    async def _read(self, path, attempt: int) -> ScreenRead:
        system = load_prompt(self.dir / "reader.md")
        out = await run_agent(
            f"normalize/{self.src['id']}/{path.stem}/read{attempt}", system,
            f"Transcribe the screenshot at this absolute path (use the Read tool): {path}",
            ScreenRead, model=self.ctx.model("vision"), tools=["Read"], add_dirs=[path.parent], max_turns=6)
        return ScreenRead.model_validate(out)

    async def normalize(self) -> list[Unit]:
        files = self.files()
        double = self.config.get("double_read", False)
        reads = await asyncio.gather(*[self._read(f, 1) for f in files])
        checks = await asyncio.gather(*[self._read(f, 2) for f in files]) if double else [None] * len(files)
        units, self.disagreements = [], []
        for n, (f, r, c) in enumerate(zip(files, reads, checks), 1):
            screen = f"S{n:02d}"
            units.append(Unit(id=f"{screen}-E00", source_id=self.src["id"], text=r.screen_summary,
                              meta={"file": f.name, "kind": "screen_summary (reader's description, not visible text)"}))
            for i, e in enumerate(r.elements, 1):
                units.append(Unit(id=f"{screen}-E{i:02d}", source_id=self.src["id"], text=e.text,
                                  meta={"file": f.name, **e.model_dump(exclude={"text"})}))
            if c is not None:
                # compare the words read, not how they were segmented into elements
                words = lambda els: Counter(re.findall(r"[\w'*.]+", " ".join(norm_ws(e.text) for e in els)))
                a, b = words(r.elements), words(c.elements)
                if a != b:
                    self.disagreements.append({"file": f.name, "only_in_read1": sorted((a - b).elements()),
                                               "only_in_read2": sorted((b - a).elements())})
        if double:
            self.ctx.write(f"normalize/{self.src['id']}.double_read", self.disagreements)
        return units

    def verify_anchor(self, anchor, units):
        ok, note = super().verify_anchor(anchor, units)
        if ok and anchor.unit_id.endswith("-E00"):
            return False, "screen summaries are the reader's words, not visible text; quote a visible element"
        return ok, note
