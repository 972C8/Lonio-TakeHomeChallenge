"""The review says which earlier findings are resolved, still open or new (no LLM)."""
import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from pipeline import run as R
from pipeline.engine.decisions import Decision

PREV = {"verdict": "not_ready", "summary": "s",
        "findings": [{"title": "Tariff code fails", "why": "w", "evidence": "AC-06.6.1", "action": "a"}]}


def dec(i, st="x"):
    return Decision(id=i, action="direct", target="", statement=st, rationale="r", by="Product owner")


class TestFollowupPrompt(unittest.TestCase):
    def test_first_review_has_no_followup(self):
        self.assertEqual(R.review_followup(None, None, [dec("D-001")]), "")

    def test_lists_previous_findings_and_only_new_decisions(self):
        seen = {"D-001": R._decision_digest(dec("D-001", "old")), "D-003": R._decision_digest(dec("D-003", "a"))}
        text = R.review_followup(PREV, {"decisions_seen": seen},
                                 [dec("D-001", "old"), dec("D-002", "new one"), dec("D-003", "changed")])
        self.assertIn("Tariff code fails", text)
        self.assertIn("D-002", text)
        self.assertIn("D-003", text)        # changed since
        self.assertNotIn("D-001", text)

    def test_unknown_previous_decisions_are_said_so(self):
        self.assertIn("not recorded", R.review_followup(PREV, {}, [dec("D-001")]))


class FakeCtx:
    def __init__(self, d):
        self.build, self.manifest, self.ran, self.reused, self.force = Path(d), {}, [], [], set()
        

    def out(self, name):
        return self.build / f"{name}.json"

    def model(self, *a):
        return "m"

    def log(self, *a):
        pass


class TestFingerprint(unittest.TestCase):
    def test_followup_and_decision_ids_do_not_change_the_review_fingerprint(self):
        seen = []

        async def stage(name, inputs, fn):
            seen.append(R.sha(*inputs) if hasattr(R, "sha") else repr(inputs))
            return {}

        with tempfile.TemporaryDirectory() as d:
            ctx = FakeCtx(d)
            ctx.stage = stage
            base = {"impact": None, "findings": {"error": [], "warning": [], "info": []}, "x": 1}
            asyncio.run(R.stage_review(ctx, {**base, "decisions_seen": {"D-001": "a"}}, [dec("D-001")]))
            asyncio.run(R.stage_review(ctx, {**base, "decisions_seen": {"D-001": "a", "D-002": "b"}}, [dec("D-001"), dec("D-002")]))
        self.assertEqual(seen[0], seen[1])


class TestRender(unittest.TestCase):
    def test_resolved_and_still_open_are_shown(self):
        with tempfile.TemporaryDirectory() as d:
            ctx = SimpleNamespace(build=Path(d))
            r = {"feature_id": "f", "review": {"verdict": "not_ready", "summary": "s",
                 "findings": [{"title": "A", "why": "w", "evidence": "e", "action": "a", "status": "still_open"}],
                 "resolved": [{"title": "Tariff code fails", "resolved_by": "D-052"}]},
                 "counts": {k: 0 for k in ("units", "facts", "items", "rules", "sections", "stories",
                                           "acceptance_criteria", "open_questions", "exclusions")},
                 "skipped_sources": [], "impact": None, "findings": {"error": [], "warning": [], "info": []},
                 "examples": [], "open_questions": [], "inferred_items": [], "dev_refinement": {"questions": []},
                 "coverage": {"units_cited": 0, "units_total": 0, "facts_used": 0, "facts_total": 0, "uncited_units": []},
                 "stages": {"ran": [], "reused": []}, "cost_usd_this_run": 0}
            R.write_review_md(ctx, r, [])
            md = (Path(d) / "review.md").read_text()
        self.assertIn("**A** (still open)", md)
        self.assertIn("## Resolved since the last review", md)
        self.assertIn("~~Tariff code fails~~ – D-052", md)


if __name__ == "__main__":
    unittest.main()
