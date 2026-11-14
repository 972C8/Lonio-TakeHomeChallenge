"""The rendered output: one feature.md plus one file per story (no LLM, no network).

Run from Solution/:  .venv/bin/python -m unittest discover -s tests -v
"""
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.engine.context import Context
from pipeline.render.render import render, story_file
from pipeline.engine.schemas import Feature, KnowledgeModel, Spec


def spec():
    story = lambda n, title: {"id": f"US-01.{n}", "title": title, "as_a": "hr", "i_want": "x", "so_that": "y",
                              "priority": "P1", "priority_reason": "r", "source_refs": ["G-01"],
                              "acceptance_criteria": [{"id": f"AC-01.{n}.1", "title": "t", "given": "g", "when": "w",
                                                       "then": "t", "source_refs": ["G-01"]}]}
    feat = Feature.model_validate({"id": "f", "title": "Feature", "goal": "g", "context": "c", "stakeholders": ["hr"],
                                   "sections": [{"id": "SEC-01", "order": 1, "title": "One", "purpose": "p",
                                                 "stories": [story(1, "First story"), story(2, "Second: story!")]}]})
    return Spec(knowledge=KnowledgeModel(items=[], rules=[], open_questions=[], exclusions=[]), feature=feat)


class SplitOutput(unittest.TestCase):
    def test_one_file_per_story_linked_from_the_feature(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / "f"
            ctx = Context("employee-onboarding")                          # real profile, fake spec
            render(out, ctx, spec(), [], {}, [], guidance={"G-01": "ask once"})
            files = sorted(p.name for p in (out / "stories").glob("*.md"))
            self.assertEqual(files, ["US-01.1-first-story.md", "US-01.2-second-story.md"])
            feature = (out / "feature.md").read_text()
            self.assertIn("(stories/US-01.2-second-story.md)", feature)
            self.assertNotIn("AC-01.1.1", feature)                       # criteria live in the story files only
            story = (out / "stories" / files[0]).read_text()
            self.assertTrue(story.startswith("---\nid: US-01.1\n"))
            self.assertIn("AC-01.1.1", story)
            self.assertIn("(../feature.md#SEC-01)", story)
            self.assertIn("**G-01**", story)                              # the story's own evidence

    def test_long_titles_are_cut_at_a_word(self):
        s = SimpleNamespace(id="US-09.1", title="Ask custody and alternating care for a minor child not living with the employee")
        name = story_file(s)
        self.assertTrue(name.startswith("US-09.1-ask-custody"))
        self.assertFalse(name.endswith("-.md"))
        self.assertTrue(name.endswith("-child-not.md"), name)             # cut at a whole word
        self.assertLessEqual(len(name), len("US-09.1-") + 60 + len(".md"))


if __name__ == "__main__":
    unittest.main()
