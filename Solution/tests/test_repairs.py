"""Deterministic tests for the repair rounds and the clearer example errors (no LLM, no network).

Run from Solution/:  .venv/bin/python -m unittest discover -s tests -v
"""
import asyncio
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pipeline.run as R
from pipeline.checks import mechanical as M
from pipeline.engine.context import Context
from pipeline.engine.schemas import KnowledgeModel, Section

NEED = [{"stakeholder": "source_tax", "purpose": "p"}]


def km(rows=(["Germany", "yes"], ["Switzerland"])):
    return KnowledgeModel.model_validate({
        "items": [
            {"id": "country", "name": "c", "description": "d", "asked_when": "Always", "required_when": "Always",
             "allowed_values": ["Germany", "Switzerland"], "needed_by": NEED, "source_refs": ["F-1"]},
            {"id": "confession", "name": "c", "description": "d", "asked_when": "Only if living abroad",
             "required_when": "Always", "asked_when_expr": 'country == "Germany"',
             "allowed_values": ["Reformed", "None"], "needed_by": NEED, "source_refs": ["F-1"]}],
        "rules": [{"id": "suffix", "name": "s", "statement": "s", "inputs": ["Country", "Reformed"],
                   "table": [{"when": list(r), "then": "x"} for r in rows],
                   "expression": 'if_else(confession == "Reformed", "Y", if_else(confession == "None", "N", null))',
                   "source_refs": ["F-1"]}],
        "open_questions": [], "exclusions": []})


def section(given):
    return Section.model_validate({"id": "SEC-05", "order": 1, "title": "t", "purpose": "p", "stories": [{
        "id": "US-05.1", "title": "t", "as_a": "source_tax", "i_want": "x", "so_that": "y", "priority": "P1",
        "priority_reason": "r", "source_refs": ["F-1"], "acceptance_criteria": [{
            "id": "AC-05.1.1", "title": "t", "given": "g", "when": "w", "then": "t", "source_refs": ["F-1"],
            "examples": [{"name": "Reformed", "given": given, "then": [{"target": "suffix", "expect": "Y"}]}]}]}]})


class ClearerExampleErrors(unittest.TestCase):
    def test_unasked_input_is_named(self):
        fails, _ = M.check_example(km(), {"confession": "Reformed"}, [("suffix", "Y")])
        self.assertTrue(any("confession was given but is not asked" in f for f in fails), fails)

    def test_complete_example_passes_without_hint(self):
        fails, _ = M.check_example(km(), {"country": "Germany", "confession": "Reformed"}, [("suffix", "Y")])
        self.assertEqual(fails, [])


class RepairRounds(unittest.TestCase):
    def setUp(self):
        self.ctx = Context("employee-onboarding")
        tmp = Path(tempfile.mkdtemp())
        self.ctx.build, self.ctx.manifest, self.ctx.manifest_path = tmp, {}, tmp / "manifest.json"
        self.calls, self.real = [], R.run_agent
        R.run_agent = self.fake

    def tearDown(self):
        R.run_agent = self.real

    async def fake(self, name, system, prompt, schema, **kw):
        self.calls.append((name, prompt))
        if name == "knowledge_repair":
            return {"rules": [km(rows=(["Germany", "yes"], ["Switzerland", "-"])).rules[0].model_dump()]}
        if name.startswith("write_section_repair/"):
            return {"acceptance_criteria": [section([{"item": "country", "value": "Germany"},
                                                     {"item": "confession", "value": "Reformed"}])
                                            .stories[0].acceptance_criteria[0].model_dump()]}
        raise AssertionError(name)

    def test_short_table_rows_are_repaired_once(self):
        self.assertEqual(len(M.table_shape_errors(km())), 1)
        out = asyncio.run(R._repair_tables(self.ctx, "sys", km()))
        self.assertEqual(M.table_shape_errors(KnowledgeModel.model_validate(out)), [])
        self.assertEqual([n for n, _ in self.calls], ["knowledge_repair"])

    def test_good_tables_cost_nothing(self):
        asyncio.run(R._repair_tables(self.ctx, "sys", km(rows=(["Germany", "yes"], ["Switzerland", "-"]))))
        self.assertEqual(self.calls, [])

    def test_failing_examples_are_repaired_with_the_reason(self):
        sec = asyncio.run(R._repair_examples(self.ctx, "sys", km(), section([{"item": "confession", "value": "Reformed"}])))
        name, prompt = self.calls[0]
        self.assertIn("is not asked", prompt)
        ex = sec.stories[0].acceptance_criteria[0].examples[0]
        self.assertEqual(M.check_example(km(), {g.item: g.value for g in ex.given}, [("suffix", "Y")])[0], [])

    def test_passing_examples_cost_nothing(self):
        good = section([{"item": "country", "value": "Germany"}, {"item": "confession", "value": "Reformed"}])
        asyncio.run(R._repair_examples(self.ctx, "sys", km(), good))
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
