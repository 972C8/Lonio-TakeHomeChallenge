"""Deterministic tests for directive decisions (action: direct). No LLM, no network.

Run from Solution/:  .venv/bin/python -m unittest discover -s tests -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.engine import decisions as D
from pipeline.engine.llm import load_prompt
from pipeline.engine.schemas import (BusinessRule, Decision, Feature, KnowledgeModel, Section, Spec)

AGENTS = Path(__file__).resolve().parents[1] / "pipeline" / "agents"


def directive(id="D-001", statement="Lonio computes the full tariff code."):
    return Decision(id=id, action="direct", statement=statement, rationale="product choice", evidence=["hr/T-012"])


def spec(rule_refs=("F-x",)):
    km = KnowledgeModel(items=[], rules=[BusinessRule(id="r", name="r", statement="s", source_refs=list(rule_refs))],
                        open_questions=[], exclusions=[])
    feat = Feature(id="f", title="t", goal="g", context="c", stakeholders=[],
                   sections=[Section(id="SEC-01", title="t", order=1, purpose="p", items=[], rules=["r"],
                                     open_questions=[], source_refs=[], stories=[])])
    return Spec(knowledge=km, feature=feat)


class Directives(unittest.TestCase):
    def test_directive_needs_statement_but_no_target(self):
        self.assertEqual(D.validate([directive()]), [])
        self.assertEqual(len(D.validate([directive(statement=" ")])), 1)
        bad = Decision(id="D-002", action="override", rationale="x")
        self.assertIn("needs a target", D.validate([bad])[0].message)

    def test_prompt_block_lists_only_directives(self):
        patch = Decision(id="D-002", action="exclude", target="item.photo", rationale="not needed")
        block = D.directives_prompt([directive(), patch])
        self.assertIn("[D-001] Lonio computes the full tariff code.", block)
        self.assertNotIn("D-002", block)
        self.assertEqual(D.directives_prompt([patch]), "")   # no directives: no prompt change

    def test_directive_reaches_every_writing_agent(self):
        block = D.directives_prompt([directive()])
        for name in ("knowledge_modeler.md", "feature_planner.md", "story_writer.md"):
            text = load_prompt(AGENTS / name, directives=block)
            self.assertIn("[D-001]", text, name)
            self.assertNotIn("{{directives}}", text, name)

    def test_directive_is_not_applied_as_a_patch(self):
        s, findings = D.apply_to_spec([directive()], spec())
        self.assertEqual(findings, [])
        self.assertEqual(s.knowledge.rules[0].source_refs, ["F-x"])

    def test_uncited_directive_is_reported(self):
        self.assertEqual(len(D.check_directives([directive()], spec())), 1)
        self.assertEqual(D.check_directives([directive()], spec(rule_refs=("F-x", "D-001"))), [])


class Stamping(unittest.TestCase):
    def test_stamping_keeps_a_header_that_mentions_decisions(self):
        import tempfile
        from types import SimpleNamespace
        from pipeline.engine.schemas import Unit
        with tempfile.TemporaryDirectory() as t:
            path = Path(t) / "decisions.yaml"
            path.write_text("# Product decisions: the override layer.\ndecisions:\n"
                            "- id: D-001\n  action: direct\n  statement: s\n  rationale: r\n  evidence: [hr/T-1]\n")
            ctx = SimpleNamespace(feature_dir=Path(t), profile={})
            ds = D.load(ctx)
            units = {"hr/T-1": Unit(id="hr/T-1", source_id="hr", kind="turn", text="hello")}
            D.stamp_and_check(ctx, ds, units)
            text = path.read_text()
            self.assertTrue(text.startswith("# Product decisions: the override layer.\ndecisions:\n"))
            self.assertTrue(D.load(ctx)[0].evidence_hash)


if __name__ == "__main__":
    unittest.main()
