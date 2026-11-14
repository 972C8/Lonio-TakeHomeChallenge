"""Incremental reruns and 'new evidence since a decision' (no LLM, no network).

Run from Solution/:  .venv/bin/python -m unittest discover -s tests -v
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.engine import decisions as D
from pipeline.engine import incremental as I
from pipeline.engine.context import Context
from pipeline.engine.schemas import Anchor, Decision, Fact, Feature, FeaturePlan, KnowledgeModel, Section, Spec

NEED = [{"stakeholder": "hr", "purpose": "p"}]


def item(id, refs=("F-a",), expr="true"):
    return {"id": id, "name": id, "description": "d", "asked_when": "Always", "required_when": "Always",
            "asked_when_expr": expr, "needed_by": NEED, "source_refs": list(refs)}


def km(items=(), rules=(), oqs=()):
    return KnowledgeModel.model_validate({"items": list(items), "rules": list(rules), "open_questions": list(oqs),
                                          "exclusions": []})


def story(id, items, refs=("F-a",)):
    return {"id": id, "title": id, "as_a": "hr", "i_want": "x", "so_that": "y", "priority": "P1",
            "priority_reason": "r", "items": list(items), "source_refs": list(refs),
            "acceptance_criteria": [{"id": f"AC-{id}", "title": "t", "given": "g", "when": "w", "then": "t",
                                     "source_refs": list(refs)}]}


def fact(id, text="s"):
    return Fact(id=id, source_id=id.split("-")[1], kind="rule", subject="s", statement=text,
                anchors=[Anchor(unit_id="x/T-1", quote="q")], anchor_ok=True)


class KnowledgeDelta(unittest.TestCase):
    def test_delta_changes_only_what_it_names(self):
        prev = km([item("a"), item("b"), item("c")], oqs=[{"id": "OQ-1", "question": "q", "why_it_matters": "w"}])
        delta = I.KnowledgeDelta(items=[I.InfoItem.model_validate(item("b", refs=("F-a", "F-new")))],
                                 remove=["open.OQ-1"])
        new = I.apply_delta(prev, delta)
        self.assertEqual([i.id for i in new.items], ["a", "b", "c"])
        self.assertEqual(new.items[0], prev.items[0])                       # untouched: identical
        self.assertIn("F-new", new.items[1].source_refs)
        self.assertEqual(new.open_questions, [])
        self.assertEqual(I.changed_ids(prev, new), {"b", "OQ-1"})

    def test_fact_changes(self):
        self.assertEqual(I.fact_changes({"F-1": "h", "F-2": "h"}, {"F-1": "h", "F-3": "h"}), (["F-3"], ["F-2"]))


class SectionsOnlyWhereNeeded(unittest.TestCase):
    def test_relevant_ids_follow_conditions(self):
        m = km([item("country"), item("canton", expr='country == "CH"'), item("other")])
        sec = Section(id="S1", order=1, title="t", purpose="p", items=["canton"])
        self.assertEqual(I.relevant_ids(sec, None, m), {"canton", "country"})

    def test_untouched_stories_are_kept_word_for_word(self):
        prev = Section.model_validate({"id": "S1", "order": 1, "title": "t", "purpose": "p",
                                       "stories": [story("US-1", ["canton"]), story("US-2", ["name"])]})
        rewritten = story("US-2", ["name"]) | {"title": "reworded by the writer"}
        new = Section.model_validate({"id": "S1", "order": 1, "title": "t", "purpose": "p",
                                      "stories": [story("US-1", ["canton"]) | {"title": "updated"}, rewritten]})
        out = I.keep_untouched(prev, new, {"canton"})
        self.assertEqual(out.stories[0].title, "updated")                   # touched: the writer's version
        self.assertEqual(out.stories[1], prev.stories[1])                   # untouched: previous version
        dropped = Section.model_validate({"id": "S1", "order": 1, "title": "t", "purpose": "p",
                                          "stories": [story("US-1", ["canton"])]})
        self.assertEqual([s.id for s in I.keep_untouched(prev, dropped, {"canton"}).stories], ["US-1", "US-2"])

    def test_plan_keeps_sections_and_lists_new_ids(self):
        prev = FeaturePlan(goal="g", context="c", stakeholders=["hr"], sections=[
            Section(id="S1", order=1, title="t", purpose="p", items=["a", "gone"])])
        plan, new = I.plan_update(prev, km([item("a"), item("b")]))
        self.assertEqual(plan.sections[0].items, ["a"])
        self.assertEqual(new, ["b"])
        plan = I.assign(plan, km([item("a"), item("b")]), [I.Assignment(id="b", section="S1")])
        self.assertEqual(plan.sections[0].items, ["a", "b"])


class BehaviourVsCitations(unittest.TestCase):
    def test_citations_and_descriptions_are_not_behaviour(self):
        prev = km([item("country"), item("canton", expr='country == "CH"')])
        cur = km([item("country", refs=("F-a", "F-new")) | {"description": "reworded"},
                  item("canton", expr='country == "CH" or country == "LI"')])
        self.assertEqual(I.changed_ids(prev, cur), {"country", "canton"})
        self.assertEqual(I.behaviour_changed_ids(prev, cur), {"canton"})

    def test_section_reacts_to_own_changes_but_only_to_behaviour_of_what_it_uses(self):
        sec = Section(id="S3", order=3, title="t", purpose="p", items=["civil_status"])
        rel = {"civil_status", "country"}
        self.assertEqual(I.touched_ids(sec, rel, changed={"country"}, changed_behaviour=set()), set())   # reuse
        self.assertEqual(I.touched_ids(sec, rel, changed={"country"}, changed_behaviour={"country"}), {"country"})
        self.assertEqual(I.touched_ids(sec, rel, changed={"civil_status"}, changed_behaviour=set()), {"civil_status"})


class NewEvidenceSinceDecision(unittest.TestCase):
    def setUp(self):
        self.ctx = Context("employee-onboarding")
        self.ctx.build = Path(tempfile.mkdtemp())

    def spec(self, item_refs):
        k = km([item("canton", refs=item_refs)])
        feat = Feature(id="f", title="t", goal="g", context="c", stakeholders=["hr"], sections=[])
        return Spec(knowledge=k, feature=feat)

    def test_directive_flagged_when_its_element_cites_a_new_fact(self):
        d = Decision(id="D-002", action="direct", statement="ask residents only", rationale="r")
        facts = [fact("F-hr-1"), fact("F-email-9", "Zurich for employees abroad")]
        # first seen in a run that knew only F-hr-1
        f = D.new_evidence(self.ctx, [d], self.spec(["F-hr-1", "F-email-9", "D-002"]), facts, {"F-hr-1"})
        self.assertEqual(len(f), 1)
        self.assertIn("F-email-9", f[0].message)
        self.assertIn("Zurich", f[0].message)

    def test_no_flag_without_new_facts_and_after_reconfirm(self):
        d = Decision(id="D-002", action="direct", statement="s", rationale="r")
        facts = [fact("F-hr-1"), fact("F-email-9")]
        self.assertEqual(D.new_evidence(self.ctx, [d], self.spec(["F-hr-1", "D-002"]), facts, {"F-hr-1"}), [])
        self.ctx.write("facts", [x.model_dump() for x in facts])
        D.reconfirm(self.ctx, ["D-002"])
        self.assertEqual(D.new_evidence(self.ctx, [d], self.spec(["F-hr-1", "F-email-9", "D-002"]), facts, None), [])

    def test_a_mere_new_citation_does_not_flag(self):
        d = Decision(id="D-011", action="accept", target="fact.F-hr-1", rationale="r")
        prev = self.spec(["F-hr-1"])
        cur = self.spec(["F-hr-1", "F-email-9"])                              # only a citation was added
        facts = [fact("F-hr-1"), fact("F-email-9")]
        self.assertEqual(D.new_evidence(self.ctx, [d], cur, facts, {"F-hr-1"}, prev), [])
        cur.knowledge.items[0].asked_when_expr = 'country == "CH"'          # now it changed in behaviour
        self.assertEqual(len(D.new_evidence(self.ctx, [d], cur, facts, {"F-hr-1"}, prev)), 1)

    def test_accepted_fact_flagged_through_the_elements_citing_it(self):
        d = Decision(id="D-012", action="accept", target="fact.F-hr-1", rationale="r")
        f = D.new_evidence(self.ctx, [d], self.spec(["F-hr-1", "F-email-9"]), [fact("F-hr-1"), fact("F-email-9")], {"F-hr-1"})
        self.assertEqual(len(f), 1)


class DirectivesForceFullRebuild(unittest.TestCase):
    """A new or changed directive must rebuild the model and rewrite every section (README, LIMITATIONS #4).
    Regression: with no input record yet (first incremental run), D-037/D-038 were treated as unchanged."""

    def directive(self, id="D-037", statement="Read-only after submission."):
        return Decision(id=id, action="direct", statement=statement, rationale="r")

    def test_no_record_rebuilds(self):
        self.assertTrue(I.directives_changed(None, I.directive_digest([self.directive()])))

    def test_record_from_before_directives_were_recorded_rebuilds(self):
        old = {"system": "x", "facts": {}}               # what the run before the fix wrote
        self.assertTrue(I.directives_changed(old, I.directive_digest([self.directive()])))
        self.assertTrue(I.directives_changed(old, I.directive_digest([])))

    def test_new_directive_rebuilds(self):
        rec = {"directives": I.directive_digest([self.directive("D-001", "a")])}
        now = I.directive_digest([self.directive("D-001", "a"), self.directive("D-037", "b")])
        self.assertTrue(I.directives_changed(rec, now))

    def test_changed_statement_rebuilds(self):
        rec = {"directives": I.directive_digest([self.directive(statement="a")])}
        self.assertTrue(I.directives_changed(rec, I.directive_digest([self.directive(statement="b")])))

    def test_same_directives_stay_incremental(self):
        rec = {"directives": I.directive_digest([self.directive()])}
        self.assertFalse(I.directives_changed(rec, I.directive_digest([self.directive()])))

    def test_patch_decision_does_not_rebuild(self):
        rec = {"directives": I.directive_digest([self.directive()])}
        patch = Decision(id="D-039", action="override", target="item.x", rationale="r")
        self.assertFalse(I.directives_changed(rec, I.directive_digest([self.directive(), patch])))


class NewSourceTakesTheDeltaPath(unittest.TestCase):
    SRC = [{"id": "hr", "type": "transcript", "precedence": 2, "authority": "policy"},
           {"id": "fund", "type": "screenshots", "precedence": 1, "authority": "fields"}]

    def test_added_or_removed_source_is_not_a_change(self):
        rec = {"sources": I.source_digest(self.SRC[:1])}
        self.assertFalse(I.sources_changed(rec, I.source_digest(self.SRC)))       # added
        rec = {"sources": I.source_digest(self.SRC)}
        self.assertFalse(I.sources_changed(rec, I.source_digest(self.SRC[:1])))   # removed

    def test_changed_trust_level_rebuilds(self):
        rec = {"sources": I.source_digest(self.SRC)}
        changed = [dict(self.SRC[0], precedence=0), self.SRC[1]]
        self.assertTrue(I.sources_changed(rec, I.source_digest(changed)))

    def test_previous_sources_from_fact_ids(self):
        self.assertEqual([s["id"] for s in I.sources_with_facts(self.SRC, ["F-hr-1a2b3c", "D-001"])], ["hr"])


class DeltaGuard(unittest.TestCase):
    def guard(self, delta, new=("F-new",), removed=()):
        prev = km([item("a"), item("b", refs=("F-old",))])
        return I.guard_delta(prev, delta, set(new), set(removed))

    def test_change_citing_a_new_fact_is_kept(self):
        d, notes = self.guard(I.KnowledgeDelta(items=[I.InfoItem.model_validate(item("a", refs=("F-a", "F-new")))]))
        self.assertEqual([i.id for i in d.items], ["a"])
        self.assertEqual(notes, [])

    def test_change_without_cause_is_reverted(self):
        changed = dict(item("a"), description="reworded")
        d, notes = self.guard(I.KnowledgeDelta(items=[I.InfoItem.model_validate(changed)]))
        self.assertEqual(d.items, [])
        self.assertIn("item.a", notes[0])

    def test_rename_is_reverted_but_change_kept(self):
        changed = dict(item("a", refs=("F-a", "F-new")), name="New label")
        d, notes = self.guard(I.KnowledgeDelta(items=[I.InfoItem.model_validate(changed)]))
        self.assertEqual(d.items[0].name, "a")
        self.assertIn("rename", notes[0])

    def test_addition_must_cite_a_new_fact(self):
        d, notes = self.guard(I.KnowledgeDelta(items=[I.InfoItem.model_validate(item("c")),
                                                      I.InfoItem.model_validate(item("e", refs=("F-new",)))]))
        self.assertEqual([i.id for i in d.items], ["e"])
        self.assertEqual(len(notes), 1)

    def test_removal_only_of_elements_citing_a_removed_fact(self):
        d, notes = self.guard(I.KnowledgeDelta(remove=["item.a", "item.b"]), removed=("F-old",))
        self.assertEqual(d.remove, ["item.b"])
        self.assertIn("item.a", notes[0])


class StoryImpact(unittest.TestCase):
    def test_changed_story_without_changed_element_is_flagged(self):
        a = Section.model_validate({"id": "S", "order": 1, "title": "t", "purpose": "p",
                                    "stories": [story("US-1", ["item_a"]), story("US-2", ["item_b"])]})
        b = a.model_copy(deep=True)
        b.stories[0].title = "changed"
        b.stories[1].title = "changed too"
        b.stories.append(Section.model_validate({"id": "S", "order": 1, "title": "t", "purpose": "p",
                                                 "stories": [story("US-3", ["item_c"])]}).stories[0])
        imp = I.story_impact(a.stories, b.stories, {"item_a", "item_c"})
        self.assertEqual(imp["added"], ["US-3"])
        self.assertEqual(imp["changed"], ["US-1", "US-2"])
        self.assertEqual(imp["changed_without_cause"], ["US-2"])


if __name__ == "__main__":
    unittest.main()
