"""Deterministic tests for source-scoped ids and the id feedback loop (no LLM, no network).

Run from Solution/:  .venv/bin/python -m unittest discover -s tests -v
"""
import asyncio
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pipeline.run as R
from pipeline.adapters.base import ExtractedFact, build_facts, make_fact_id
from pipeline.adapters.transcript.adapter import TranscriptAdapter
from pipeline.checks import mechanical as M
from pipeline.engine.context import Context
from pipeline.engine.schemas import Anchor, Fact, FeaturePlan, KnowledgeModel, Section

FEATURE = "employee-onboarding"          # any feature folder works; only its profile is read


def run(coro):
    return asyncio.run(coro)


def two_transcripts(tmp: Path):
    """Two transcripts of the same type whose first turn is identical text."""
    (tmp / "kickoff.md").write_text("Leo: Hello Anna.\n\nAnna: We hire twenty people a year.\n")
    (tmp / "followup.md").write_text("Leo: Hello Anna.\n\nAnna: The start date moves often.\n")
    ctx = Context(FEATURE)
    srcs = [{"id": sid, "type": "transcript", "path": str(tmp / f"{sid}.md"), "speakers": ["Leo", "Anna"]}
            for sid in ("kickoff", "followup")]
    return ctx, srcs, [TranscriptAdapter(s, ctx) for s in srcs]


def fact(source, unit, quote, kind="field", local="f1", statement="s", supersedes=()):
    return ExtractedFact(local_id=local, kind=kind, subject="x", statement=statement,
                         anchors=[Anchor(unit_id=unit, quote=quote)], basis="explicit",
                         temporality="desired", supersedes=list(supersedes))


class SourceScopedIds(unittest.TestCase):
    def test_two_transcripts_do_not_collide(self):
        with tempfile.TemporaryDirectory() as t:
            ctx, srcs, adapters = two_transcripts(Path(t))
            units = [u for a in adapters for u in run(a.normalize())]
            ids = [u.id for u in units]
            self.assertEqual(len(ids), len(set(ids)), "unit ids must be unique across sources")
            self.assertIn("kickoff/T-001", ids)
            self.assertIn("followup/T-001", ids)          # same local id, different source
            self.assertTrue(all(u.id.startswith(u.source_id + "/") for u in units))

    def test_quote_checks_work_across_sources(self):
        with tempfile.TemporaryDirectory() as t:
            ctx, srcs, adapters = two_transcripts(Path(t))
            units = {u.id: u for a in adapters for u in run(a.normalize())}
            ad = {s["id"]: a for s, a in zip(srcs, adapters)}
            facts = (build_facts("kickoff", [fact("kickoff", "kickoff/T-001", "Hello Anna.")], set(units))
                     + build_facts("followup", [fact("followup", "followup/T-001", "Hello Anna.")], set(units)))
            self.assertEqual(M.verify_anchors(facts, units, ad), [])
            self.assertTrue(all(f.anchor_ok for f in facts))
            # a fact may not cite a unit of another source
            bad = build_facts("kickoff", [fact("kickoff", "followup/T-001", "Hello Anna.")], set(units))
            errs = M.verify_anchors(bad, units, ad)
            self.assertEqual(len(errs), 1)
            self.assertIn("another source", errs[0].message)

    def test_fact_ids_are_source_scoped_and_content_based(self):
        units = {"kickoff/T-001", "followup/T-001"}
        a = build_facts("kickoff", [fact("kickoff", "kickoff/T-001", "Hello Anna.")], units)[0]
        b = build_facts("followup", [fact("followup", "followup/T-001", "Hello Anna.")], units)[0]
        self.assertNotEqual(a.id, b.id)                                   # same quote, different source
        self.assertTrue(a.id.startswith("F-kickoff-") and b.id.startswith("F-followup-"))
        again = build_facts("kickoff", [fact("kickoff", "kickoff/T-001", "Hello Anna.", statement="reworded",
                                              local="other")], units)[0]
        self.assertEqual(a.id, again.id)                                  # stable across re-extraction
        other = build_facts("kickoff", [fact("kickoff", "kickoff/T-001", "Something else.")], units)[0]
        self.assertNotEqual(a.id, other.id)
        self.assertNotIn(".", a.id)                                       # decision targets split on the first dot

    def test_identical_anchors_get_numbered_ids_and_supersedes_resolve(self):
        units = {"kickoff/T-001"}
        fs = build_facts("kickoff", [fact("kickoff", "kickoff/T-001", "Hello Anna.", local="a"),
                                     fact("kickoff", "kickoff/T-001", "Hello Anna.", local="b", supersedes=["a"])], units)
        self.assertEqual(len({f.id for f in fs}), 2)
        self.assertEqual(fs[1].supersedes, [fs[0].id])
        self.assertEqual(make_fact_id("kickoff", "field", fs[0].anchors), fs[0].id)

    def test_agent_dropping_the_source_prefix_is_repaired(self):
        f = build_facts("kickoff", [fact("kickoff", "T-001", "Hello Anna.")], {"kickoff/T-001"})[0]
        self.assertEqual(f.anchors[0].unit_id, "kickoff/T-001")


class IdFeedback(unittest.TestCase):
    """The ids of the previous run reach the agents, without defeating the cache."""

    def setUp(self):
        self.ctx = Context(FEATURE)
        tmp = Path(tempfile.mkdtemp())
        self.ctx.build, self.ctx.manifest, self.ctx.manifest_path = tmp, {}, tmp / "manifest.json"
        self.calls, self.real = [], R.run_agent
        R.run_agent = self.fake

    def tearDown(self):
        R.run_agent = self.real

    async def fake(self, name, system, prompt, schema, **kw):
        self.calls.append((name, system))
        if name == "knowledge":
            return {"items": [{"id": "alpha", "name": "A", "description": "d", "asked_when": "always",
                               "required_when": "always", "needed_by": [{"stakeholder": "hr", "purpose": "p"}],
                               "source_refs": ["F-x-1"]}]}
        if name == "plan_feature":
            return FeaturePlan(goal="g", context="c", stakeholders=["hr"], sections=[
                Section(id="SEC-01-alpha", order=1, title="Alpha", purpose="p", items=["alpha"])]).model_dump()
        if name.startswith("write_section/"):
            return Section(id="SEC-01-alpha", order=1, title="Alpha", purpose="p", items=["alpha"], stories=[{
                "id": "US-01.1", "title": "Story", "as_a": "hr", "i_want": "x", "so_that": "y", "priority": "P1",
                "priority_reason": "r", "source_refs": ["F-x-1"], "acceptance_criteria": [{
                    "id": "AC-01.1.1", "title": "t", "given": "g", "when": "w", "then": "t",
                    "source_refs": ["F-x-1"]}]}]).model_dump()
        raise AssertionError(name)

    def facts(self, quote):
        return [Fact(id="F-x-1", source_id="x", kind="field", subject="s", statement=quote,
                     anchors=[Anchor(unit_id="x/T-001", quote=quote)], anchor_ok=True)]

    def system_of(self, name_prefix):
        return [s for n, s in self.calls if n.startswith(name_prefix)][-1]

    def test_knowledge_ids_are_fed_back_without_breaking_the_cache(self):
        run(R.stage_knowledge(self.ctx, self.facts("one")))
        self.assertIn("(none yet)", self.system_of("knowledge"))
        self.assertTrue((self.ctx.build / "knowledge.raw.json").exists())     # the file the loop reads
        n = len(self.calls)
        run(R.stage_knowledge(self.ctx, self.facts("one")))                   # plain rerun: cache hit
        self.assertEqual(len(self.calls), n, "fed-back ids must not invalidate the cache")
        run(R.stage_knowledge(self.ctx, self.facts("two")))                   # facts changed: reruns, with the ids
        self.assertIn("alpha", self.system_of("knowledge"))

    def test_section_and_story_ids_are_fed_back(self):
        km = KnowledgeModel.model_validate(run(self.fake("knowledge", "", "", None)))
        run(R.stage_feature(self.ctx, km, self.facts("one")))
        self.assertIn("(none yet)", self.system_of("plan_feature"))
        n = len(self.calls)
        run(R.stage_feature(self.ctx, km, self.facts("one")))                 # plain rerun: cache hit
        self.assertEqual(len(self.calls), n, "fed-back ids must not invalidate the cache")
        km2 = km.model_copy(deep=True)
        km2.items[0].description = "changed"                                  # forces plan and writers to rerun
        run(R.stage_feature(self.ctx, km2, self.facts("one")))
        self.assertIn("SEC-01-alpha", self.system_of("plan_feature"))
        self.assertIn("US-01.1", self.system_of("write_section/"))


if __name__ == "__main__":
    unittest.main()
