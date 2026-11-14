"""Token savings on reruns (no LLM): incremental dev refinement and the section writer's knowledge slice."""
import json
import unittest
from pathlib import Path

from pipeline.engine.schemas import Spec
from pipeline.run import knowledge_slice, merge_refinement, refinement_scope
from pipeline.engine import incremental as I

SPEC = Path(__file__).resolve().parent.parent / "build" / "employee-onboarding" / "spec.json"


def spec():
    return Spec.model_validate(json.loads(SPEC.read_text()))


class TestRefinementScope(unittest.TestCase):
    def setUp(self):
        self.spec = spec()
        self.stories = {s.id: s for s in self.spec.stories()}
        self.sid = next(iter(self.stories))
        self.files = {f"stories/{i}-title.md": "h" + i for i in self.stories}
        self.files |= {"feature.md": "f", "information.md": "i", "open-questions.md": "o", "traceability.md": "t"}

    def test_nothing_changed(self):
        changed, removed, _ = refinement_scope(self.spec, self.files, dict(self.files))
        self.assertEqual((changed, removed), ([], []))

    def test_changed_story_brings_related_stories_as_context(self):
        now = dict(self.files)
        f = f"stories/{self.sid}-title.md"
        now[f] = "changed"
        now["feature.md"] = "changed"
        now["traceability.md"] = "changed"        # metadata: never reviewed
        changed, removed, context = refinement_scope(self.spec, self.files, now)
        self.assertEqual(changed, ["feature.md", f])
        self.assertNotIn("feature.md", context)
        self.assertIn("information.md", context)
        used = set(self.stories[self.sid].items + self.stories[self.sid].rules)
        related = {i for i, s in self.stories.items() if i != self.sid and used & set(s.items + s.rules)}
        self.assertEqual({c.split("/")[1].rsplit("-", 1)[0] for c in context if c.startswith("stories/")}, related)

    def test_renamed_story_is_removed_and_changed(self):
        now = dict(self.files)
        old = f"stories/{self.sid}-title.md"
        now.pop(old)
        now[f"stories/{self.sid}-new-title.md"] = "x"
        changed, removed, _ = refinement_scope(self.spec, self.files, now)
        self.assertEqual(removed, [old])
        self.assertEqual(changed, [f"stories/{self.sid}-new-title.md"])


class TestMergeRefinement(unittest.TestCase):
    def test_keeps_questions_on_unreviewed_files(self):
        prev = {"questions": [{"file": "stories/US-01.1-a.md", "question": "q1", "severity": "minor"},
                              {"file": "stories/US-08.1-b.md", "question": "q2", "severity": "major"},
                              {"file": "feature.md", "question": "q3", "severity": "major"}],
                "tech_leaks": [{"file": "stories/US-01.1-a.md", "quote": "x", "why": "y"},
                               {"file": "feature.md", "quote": "z", "why": "w"}],
                "already_flagged": ["OQ-1"]}
        new = {"questions": [{"file": "stories/US-08.1-b.md", "question": "q2", "severity": "major"},
                             {"file": "feature.md", "question": "q4", "severity": "minor"}],
               "tech_leaks": [], "already_flagged": ["OQ-1", "OQ-2"]}
        m = merge_refinement(prev, new, {"stories/US-08.1-b.md", "feature.md"})
        self.assertEqual([q["question"] for q in m["questions"]], ["q1", "q2", "q4"])
        self.assertEqual([t["quote"] for t in m["tech_leaks"]], ["x"])
        self.assertEqual(m["already_flagged"], ["OQ-1", "OQ-2"])

    def test_paths_are_normalised(self):
        prev = {"questions": [{"file": "/x/requirements/employee-onboarding/feature.md", "question": "q", "severity": "minor"}]}
        self.assertEqual(merge_refinement(prev, {"questions": []}, {"feature.md"})["questions"], [])


class TestKnowledgeSlice(unittest.TestCase):
    def test_slice_has_what_the_section_uses_and_indexes_the_rest(self):
        sp = spec()
        km = sp.knowledge
        sec = sp.feature.sections[1]
        rel = I.relevant_ids(sec, sec, km)
        text = knowledge_slice(km, rel)
        used = json.loads(text.split("):\n", 1)[1].split("\n\nThe other elements")[0])
        self.assertEqual({i["id"] for i in used["items"]}, {i.id for i in km.items if i.id in rel})
        self.assertEqual({r["id"] for r in used["rules"]}, {r.id for r in km.rules if r.id in rel})
        self.assertEqual(len(used["exclusions"]), len(km.exclusions))
        for i in km.items:
            self.assertTrue(f"`{i.id}`" in text or f"\"id\": \"{i.id}\"" in text)   # every element is at least named
        full = json.dumps(km.model_dump(exclude={"items": {"__all__": {"depends_on"}}, "rules": {"__all__": {"depends_on"}}}),
                          ensure_ascii=False, indent=1)
        self.assertLess(len(text), len(full) / 2)


if __name__ == "__main__":
    unittest.main()
