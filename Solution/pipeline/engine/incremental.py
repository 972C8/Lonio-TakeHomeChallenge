"""Incremental reruns: change only what the changed facts touch.

When only facts changed since the last run (same prompts, guidance and directives), the
agents get the previous result and return a delta; code applies it. Everything the delta
does not name stays exactly as it was - guaranteed by code, not by asking the agent.
A changed prompt, guidance or directive (or `--force <stage>`) still rebuilds in full.
"""
from __future__ import annotations

import json

from pydantic import BaseModel, Field as F

from . import conditions as C
from .schemas import BusinessRule, Exclusion, FeaturePlan, InfoItem, KnowledgeModel, OpenQuestion, Section


class KnowledgeDelta(BaseModel):
    items: list[InfoItem] = F(default_factory=list)            # added or changed (complete objects)
    rules: list[BusinessRule] = F(default_factory=list)
    open_questions: list[OpenQuestion] = F(default_factory=list)
    exclusions: list[Exclusion] = F(default_factory=list)
    remove: list[str] = F(default_factory=list)                # "item.<id>", "rule.<id>", "open.<id>", "exclusion.<id>"
    rationale: str = ""


class Assignment(BaseModel):
    id: str            # item / rule / open question id
    section: str       # existing section id


class Assignments(BaseModel):
    assignments: list[Assignment]


def fact_digest(payload: list[dict]) -> dict[str, str]:
    """Fact id -> hash of what the modeler sees of it."""
    import hashlib
    return {p["id"]: hashlib.sha256(json.dumps(p, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
            for p in payload}


def fact_changes(prev: dict[str, str], cur: dict[str, str]) -> tuple[list[str], list[str]]:
    """(new or changed fact ids, removed fact ids)."""
    return sorted(i for i, h in cur.items() if prev.get(i) != h), sorted(i for i in prev if i not in cur)


def apply_delta(km: KnowledgeModel, delta: KnowledgeDelta) -> KnowledgeModel:
    km = km.model_copy(deep=True)
    for attr, kind in (("items", "item"), ("rules", "rule"), ("open_questions", "open"), ("exclusions", "exclusion")):
        coll = getattr(km, attr)
        drop = {r.split(".", 1)[1] for r in delta.remove if r.startswith(kind + ".")}
        for new in getattr(delta, attr):
            drop.discard(new.id)
            idx = next((n for n, x in enumerate(coll) if x.id == new.id), None)
            if idx is None:
                coll.append(new)
            else:
                coll[idx] = new
        setattr(km, attr, [x for x in coll if x.id not in drop])
    return km


def _dump(x) -> str:
    return json.dumps(x.model_dump(exclude={"depends_on"}), sort_keys=True, ensure_ascii=False)


def changed_ids(prev: KnowledgeModel | None, cur: KnowledgeModel) -> set[str] | None:
    """Ids of items, rules and open questions that are new, changed or removed. None = no previous model."""
    if prev is None:
        return None
    def index(km):
        return {x.id: _dump(x) for x in [*km.items, *km.rules, *km.open_questions]}
    a, b = index(prev), index(cur)
    return {i for i in a.keys() | b.keys() if a.get(i) != b.get(i)}


# What an element DOES, as opposed to how it is described or cited. A change that only rewords a
# description or adds citations does not change behaviour.
BEHAVIOUR = {
    "item": ("asked_when", "asked_when_expr", "required_when", "required_when_expr", "allowed_values", "form"),
    "rule": ("inputs", "table", "expression"),
    "open": ("question", "options", "blocking"),
    "exclusion": ("item",),
}
_NOISE = {"source_refs", "status", "depends_on", "notes"}


def _strip(x):
    """Drop citation / status noise at every level (decision-table rows and criteria carry source_refs too)."""
    if isinstance(x, dict):
        return {k: _strip(v) for k, v in x.items() if k not in _NOISE}
    if isinstance(x, list):
        return [_strip(v) for v in x]
    return x


def behaviour(kind: str, obj) -> str:
    d = obj.model_dump() if hasattr(obj, "model_dump") else dict(obj)
    keys = BEHAVIOUR.get(kind)
    d = {k: d.get(k) for k in keys} if keys else d       # stories, criteria, sections: everything but the noise
    return json.dumps(_strip(d), sort_keys=True, ensure_ascii=False)


def behaviour_changed_ids(prev: KnowledgeModel | None, cur: KnowledgeModel) -> set[str] | None:
    """Ids of items, rules and open questions that are new, removed, or changed in behaviour."""
    if prev is None:
        return None
    def index(km):
        return {**{x.id: behaviour("item", x) for x in km.items}, **{x.id: behaviour("rule", x) for x in km.rules},
                **{x.id: behaviour("open", x) for x in km.open_questions}}
    a, b = index(prev), index(cur)
    return {i for i in a.keys() | b.keys() if a.get(i) != b.get(i)}


def touched_ids(sec: Section, relevant: set[str], changed: set[str], changed_behaviour: set[str]) -> set[str]:
    """What a section must react to: any change to what it owns; only behaviour changes to what it merely uses."""
    owned = set(sec.items + sec.rules + sec.open_questions)
    return (changed & owned) | (changed_behaviour & (relevant - owned))


def plan_update(prev: FeaturePlan, km: KnowledgeModel) -> tuple[FeaturePlan, list[str]]:
    """Keep the previous sections; drop ids that no longer exist. Returns the plan and the ids still unassigned."""
    plan = prev.model_copy(deep=True)
    items, rules, oqs = {i.id for i in km.items}, {r.id for r in km.rules}, {q.id for q in km.open_questions}
    for sec in plan.sections:
        sec.items = [i for i in sec.items if i in items]
        sec.rules = [r for r in sec.rules if r in rules]
        sec.open_questions = [q for q in sec.open_questions if q in oqs]
    owned = {x for sec in plan.sections for x in sec.items + sec.rules + sec.open_questions}
    unassigned = sorted((items | rules | oqs) - owned)
    return plan, unassigned


def assign(plan: FeaturePlan, km: KnowledgeModel, assignments: list[Assignment]) -> FeaturePlan:
    secs = {s.id: s for s in plan.sections}
    fallback = sorted(plan.sections, key=lambda s: s.order)[-1]
    items, rules = {i.id for i in km.items}, {r.id for r in km.rules}
    for a in assignments:
        sec = secs.get(a.section, fallback)
        lst = sec.items if a.id in items else sec.rules if a.id in rules else sec.open_questions
        if a.id not in lst:
            lst.append(a.id)
    return plan


def relevant_ids(sec: Section, prev_sec: Section | None, km: KnowledgeModel) -> set[str]:
    """What a section's stories depend on: owned items/rules/open questions, everything its previous stories
    covered or used in examples, and (two levels of) the ids their conditions and expressions reference."""
    ids = set(sec.items + sec.rules + sec.open_questions)
    if prev_sec:
        for s in prev_sec.stories:
            ids |= set(s.items + s.rules)
            for ac in s.acceptance_criteria:
                for ex in ac.examples:
                    ids |= {g.item for g in ex.given} | {t.target for t in ex.then}
    exprs = {i.id: [i.asked_when_expr, i.required_when_expr] for i in km.items}
    exprs |= {r.id: [r.expression or "true"] for r in km.rules}
    for _ in range(2):
        for i in list(ids):
            for e in exprs.get(i, []):
                try:
                    ids |= C.references(e)
                except C.ConditionError:
                    pass
    return ids


def story_touches(story, changed: set[str]) -> bool:
    used = set(story.items + story.rules)
    for ac in story.acceptance_criteria:
        for ex in ac.examples:
            used |= {g.item for g in ex.given} | {t.target for t in ex.then}
    text = json.dumps(story.model_dump(), ensure_ascii=False)
    return bool(used & changed) or any(i in text for i in changed)


def keep_untouched(prev: Section, new: Section, changed: set[str]) -> Section:
    """Previous stories the changes do not touch are kept word for word (and restored if the writer dropped them)."""
    keep = {s.id: s for s in prev.stories if not story_touches(s, changed)}
    stories = [keep.pop(s.id, s) for s in new.stories]
    stories += list(keep.values())                     # dropped by the writer although untouched
    order = {s.id: n for n, s in enumerate(prev.stories)}
    stories.sort(key=lambda s: (order.get(s.id, len(order)), s.id))
    return new.model_copy(update={"stories": stories})
