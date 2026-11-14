"""Deterministic checks (no LLM). These run first and are the backbone of
"complete and correct"; LLM judges only cover what rules cannot.
"""
from __future__ import annotations

import datetime as dt
import re

from ..engine import conditions as C
from ..engine.schemas import Fact, Finding, KnowledgeModel, Spec, Unit


# ------------------------------------------------------------ facts ------

def verify_anchors(facts: list[Fact], units: dict[str, Unit], adapters: dict) -> list[Finding]:
    out = []
    for f in facts:
        notes = []
        oks = []
        for a in f.anchors:
            ok, note = adapters[f.source_id].verify_anchor(a, units)
            oks.append(ok)
            if not ok:
                notes.append(f"{a.unit_id}: {note} (quote: {a.quote!r})")
        f.anchor_ok = bool(f.anchors) and all(oks)
        if not f.anchors:
            notes.append("fact has no anchor")
        if notes:
            out.append(Finding(check="anchors", severity="error", target=f.id, message="; ".join(notes)))
    return out


def link_supersedes(facts: list[Fact]) -> None:
    by_id = {f.id: f for f in facts}
    for f in facts:
        for s in f.supersedes:
            if s in by_id and f.id not in by_id[s].superseded_by:
                by_id[s].superseded_by.append(f.id)


# --------------------------------------------------- knowledge + specs ----

TECH_WORDS = [  # generic signals of implementation decisions in business text
    "iso 3166", "iso 8601", "snake_case", "database", "api", "endpoint", "json", "enum", "boolean", "integer",
    "string", "null", "uuid", "regex", "frontend", "backend", "dropdown", "checkbox", "radio button",
    "text field", "input field", "local storage", "session", "microservice", "schema",
]


def compute_depends_on(km: KnowledgeModel) -> None:
    for item in [*km.items, *km.rules]:
        refs = set()
        exprs = [item.asked_when_expr, item.required_when_expr] if hasattr(item, "asked_when_expr") else [item.expression or "true"]
        for e in exprs:
            try:
                refs |= C.references(e)
            except C.ConditionError:
                pass
        item.depends_on = sorted(refs - {item.id})


def lint(spec: Spec, valid_refs: set[str], stakeholders: set[str], checklist: list[dict]) -> list[Finding]:
    F, km = [], spec.knowledge
    ids = [i.id for i in km.items] + [r.id for r in km.rules]
    for d in {i for i in ids if ids.count(i) > 1}:
        F.append(Finding(check="lint", severity="error", target=d, message="duplicate id"))
    known = set(ids)

    def expr(target, label, e):
        try:
            unknown = C.references(e) - known
        except C.ConditionError as ex:
            F.append(Finding(check="lint", severity="error", target=target, message=f"{label}: {ex}"))
            return
        if unknown:
            F.append(Finding(check="lint", severity="error", target=target,
                             message=f"{label} references unknown ids {sorted(unknown)}"))

    for it in km.items:
        t = f"item.{it.id}"
        for c in checklist:  # the feature's checklist: every item must answer each question
            v = getattr(it, c["attribute"], None)
            if v in (None, "", []):
                F.append(Finding(check="checklist", severity="error", target=t,
                                 message=f"'{c['question']}' not answered ({c['attribute']} empty)"))
        for n in it.needed_by:
            if n.stakeholder not in stakeholders:
                F.append(Finding(check="lint", severity="error", target=t, message=f"unknown stakeholder {n.stakeholder!r}"))
        expr(t, "asked_when_expr", it.asked_when_expr)
        expr(t, "required_when_expr", it.required_when_expr)
        if _parses(it.asked_when_expr) and it.id in C.references(it.asked_when_expr):
            F.append(Finding(check="lint", severity="error", target=t, message="asked_when depends on itself"))
        _refs(F, t, it.source_refs, valid_refs)
    for r in km.rules:
        t = f"rule.{r.id}"
        if r.expression:
            expr(t, "expression", r.expression)
        else:
            F.append(Finding(check="lint", severity="warning", target=t, message="no internal expression: examples cannot be verified"))
        for row in r.table:
            if r.inputs and len(row.when) != len(r.inputs):
                F.append(Finding(check="lint", severity="error", target=t, message=f"decision row has {len(row.when)} cells for {len(r.inputs)} inputs"))
        _refs(F, t, r.source_refs, valid_refs)
    for q in km.open_questions:
        _refs(F, f"open.{q.id}", q.source_refs, valid_refs, allow_empty=True)
    for x in km.exclusions:
        _refs(F, f"exclusion.{x.id}", x.source_refs, valid_refs)

    owner = {}
    for f in spec.feature.sections:
        for i in f.items + f.rules:
            owner.setdefault(i, []).append(f.id)
            if i not in known:
                F.append(Finding(check="lint", severity="error", target=f.id, message=f"owns unknown item/rule {i}"))
        for s in f.stories:
            t = f"story.{s.id}"
            if s.as_a not in stakeholders:
                F.append(Finding(check="lint", severity="error", target=t, message=f"actor {s.as_a!r} is not a stakeholder"))
            if not s.acceptance_criteria:
                F.append(Finding(check="lint", severity="error", target=t, message="story without acceptance criteria"))
            for i in s.items + s.rules:
                if i not in known:
                    F.append(Finding(check="lint", severity="error", target=t, message=f"covers unknown item/rule {i}"))
            _refs(F, t, s.source_refs, valid_refs)
            for ac in s.acceptance_criteria:
                _refs(F, f"ac.{ac.id}", ac.source_refs, valid_refs)
        covered = {i for s in f.stories for i in s.items + s.rules}
        for i in f.items + f.rules:
            if i not in covered:
                F.append(Finding(check="coverage", severity="error", target=f.id, message=f"owns {i} but no story covers it"))
    for i in known:
        if i not in owner:
            F.append(Finding(check="coverage", severity="error", target=i, message="not owned by any section of the feature"))
        elif len(owner[i]) > 1:
            F.append(Finding(check="lint", severity="warning", target=i, message=f"owned by several sections {owner[i]}"))
    return F


def _parses(e):
    try:
        C.parse(e)
        return True
    except C.ConditionError:
        return False


def _refs(F, target, refs, valid, allow_empty=False):
    if not refs and not allow_empty:
        F.append(Finding(check="trace", severity="error", target=target, message="no source reference"))
    bad = [r for r in refs if r not in valid]
    if bad:
        F.append(Finding(check="trace", severity="error", target=target, message=f"cites unknown or invalid sources {bad}"))


def tech_leaks(spec: Spec, extra_words: list[str], allowed: list[str]) -> list[Finding]:
    """Deterministic scan of the business-language text for implementation vocabulary."""
    words = [w.lower() for w in TECH_WORDS + extra_words if w.lower() not in {a.lower() for a in allowed}]
    texts = []
    for it in spec.knowledge.items:
        texts += [(f"item.{it.id}", x) for x in (it.name, it.description, it.form, it.asked_when, it.required_when)]
    for r in spec.knowledge.rules:
        texts += [(f"rule.{r.id}", r.statement)]
    for f in spec.feature.sections:
        for s in f.stories:
            texts += [(f"story.{s.id}", x) for x in (s.i_want, s.so_that)]
            for ac in s.acceptance_criteria:
                texts += [(f"ac.{ac.id}", x) for x in (ac.given, ac.when, ac.then)]
    F = []
    for target, text in texts:
        low = f" {text.lower()} "
        hits = [w for w in words if re.search(rf"\b{re.escape(w)}\b", low)]
        if hits:
            F.append(Finding(check="tech_leak", severity="warning", target=target,
                             message=f"implementation vocabulary {hits}: {text[:140]}"))
    return F


# ------------------------------------------------------- simulation ------

def simulate(km: KnowledgeModel, given: dict) -> dict:
    """Which items are asked/required and what the rules yield, for one case."""
    known = {i.id for i in km.items}
    context = {k: v for k, v in given.items() if k in C.BUILTINS}
    visible = {k: v for k, v in given.items() if k in known}
    asked, required, env = [], [], {}
    for _ in range(6):                            # fixpoint: answers -> rules -> asked -> answers
        env = {**context, **visible}
        for _ in range(len(km.rules) + 1):
            for r in km.rules:
                if r.expression:
                    try:
                        env[r.id] = C.evaluate(r.expression, env)
                    except Exception as e:  # noqa: BLE001
                        env[r.id] = f"ERROR: {e}"
        asked, required = [], []
        for it in km.items:
            if C.evaluate(it.asked_when_expr or "true", env):
                asked.append(it.id)
                if C.evaluate(it.required_when_expr or "true", env):
                    required.append(it.id)
        new_visible = {k: v for k, v in given.items() if k in asked}
        if new_visible == visible:
            break
        visible = new_visible
    rules = {r.id: env.get(r.id) for r in km.rules}
    return {"asked": asked, "required": required, "rules": rules}


def _norm(v):
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, dt.date):
        return v.isoformat()
    s = str(v).strip().lower()
    if s in ("true", "yes", "ja"):
        return "yes"
    if s in ("false", "no", "nein"):
        return "no"
    try:
        return C._as_date(s).isoformat()
    except Exception:  # noqa: BLE001
        return s


def check_example(km: KnowledgeModel, given: dict, then: list[tuple[str, str]]) -> tuple[list[str], dict]:
    sim = simulate(km, given)
    items, rules = {i.id for i in km.items}, {r.id for r in km.rules}
    fails = []
    for target, expect in then:
        e = expect.strip().lower()
        if target in items:
            if e == "asked" and target not in sim["asked"]:
                fails.append(f"{target} should be asked")
            elif e == "not asked" and target in sim["asked"]:
                fails.append(f"{target} should NOT be asked")
            elif e == "required" and target not in sim["required"]:
                fails.append(f"{target} should be required")
            elif e == "optional" and (target not in sim["asked"] or target in sim["required"]):
                fails.append(f"{target} should be asked and optional")
            elif e not in ("asked", "not asked", "required", "optional"):
                fails.append(f"unknown expectation {expect!r} for item {target}")
        elif target in rules:
            got = sim["rules"].get(target)
            if _norm(got) != _norm(expect):
                fails.append(f"{target} = {got!r}, expected {expect!r}")
        else:
            fails.append(f"unknown target {target}")
    for k in given:
        if k in C.BUILTINS:
            continue
        if k not in items:
            fails.append(f"input {k} is not an information item")
        else:
            it = next(i for i in km.items if i.id == k)
            if it.allowed_values and given[k] not in it.allowed_values:
                fails.append(f"input {k}={given[k]!r} not in allowed values {it.allowed_values}")
    return fails, sim


def run_examples(spec: Spec, profile_examples: list[dict]) -> tuple[list[dict], list[Finding]]:
    """Execute every acceptance-criterion example and every profile example against the knowledge model."""
    results, F = [], []
    km = spec.knowledge
    cases = []
    for f in spec.feature.sections:
        for s in f.stories:
            for ac in s.acceptance_criteria:
                for ex in ac.examples:
                    cases.append((f"{ac.id} / {ex.name}", "spec", {g.item: g.value for g in ex.given},
                                  [(t.target, t.expect) for t in ex.then]))
    for p in profile_examples:
        then = [(k, str(v)) for k, v in p.get("expect", {}).items()]
        cases.append((p["id"], f"profile: {p.get('from', '')}", {k: str(v) for k, v in p["given"].items()}, then))
    for name, origin, given, then in cases:
        fails, sim = check_example(km, given, then)
        results.append({"case": name, "origin": origin, "pass": not fails, "failures": fails})
        for m in fails:
            F.append(Finding(check="examples", severity="error", target=name, message=m))
    return results, F


def coverage(units: list[Unit], facts: list[Fact], spec: Spec) -> tuple[dict, list[Finding]]:
    km = spec.knowledge
    used = set()
    for coll in (km.items, km.rules, km.open_questions, km.exclusions):
        for x in coll:
            used |= set(x.source_refs)
    used |= set(spec.feature.source_refs)
    for f in spec.feature.sections:
        used |= set(f.source_refs)
        for s in f.stories:
            used |= set(s.source_refs)
            for ac in s.acceptance_criteria:
                used |= set(ac.source_refs)
    for f in facts:
        if any(s in used for s in f.superseded_by):
            used.add(f.id)
    cited_units = {a.unit_id for f in facts if f.id in used for a in f.anchors}
    unused = [f for f in facts if f.id not in used and f.kind != "context" and f.temporality == "desired"]
    uncovered = [u for u in units if u.id not in cited_units and not u.id.endswith("-E00")]
    findings = [Finding(check="coverage", severity="warning", target=f.id,
                        message=f"fact not used anywhere in the spec: {f.statement}") for f in unused]
    return {"units_total": len(units), "units_cited": len(units) - len(uncovered),
            "facts_total": len(facts), "facts_used": len([f for f in facts if f.id in used]),
            "uncited_units": [{"id": u.id, "text": u.text[:160]} for u in uncovered]}, findings


def evaluate_gold(spec: Spec, gold: dict) -> tuple[dict, list[Finding]]:
    F, km = [], spec.knowledge
    items = {i.id: i for i in km.items}
    rules = {r.id for r in km.rules}
    matched, hits, ch, ct = set(), 0, 0, 0
    for g in gold.get("items", []):
        hit = next((n for n in [g["id"], *g.get("aliases", [])] if n in items or n in rules), None)
        if not hit:
            F.append(Finding(check="eval", severity="warning", target=g["id"], message="gold item missing"))
            continue
        hits += 1
        matched.add(hit)
        if hit in items:
            have = {n.stakeholder for n in items[hit].needed_by}
            for c in g.get("needed_by", []):
                ct += 1
                ch += c in have
                if c not in have:
                    F.append(Finding(check="eval", severity="warning", target=hit, message=f"missing stakeholder {c}"))
    for r in gold.get("rules", []):
        if r not in rules:
            F.append(Finding(check="eval", severity="warning", target=r, message="gold rule missing"))

    def kw(texts, keys, label):
        n = 0
        for k in keys:
            if any(k.lower() in t.lower() for t in texts):
                n += 1
            else:
                F.append(Finding(check="eval", severity="warning", target=label, message=f"no {label} mentions {k!r}"))
        return f"{n}/{len(keys)}"

    story_texts = [f"{s.title} {s.i_want} {s.so_that}" for f in spec.feature.sections for s in f.stories]
    n_gold = len(gold.get("items", []))
    return {
        "item_recall": round(hits / n_gold, 2) if n_gold else None,
        "item_precision": round(len(matched & set(items)) / len(items), 2) if items else None,
        "stakeholder_recall": round(ch / ct, 2) if ct else None,
        "rules_found": f"{len([r for r in gold.get('rules', []) if r in rules])}/{len(gold.get('rules', []))}",
        "exclusions_found": kw([f"{x.item} {x.reason}" for x in km.exclusions], gold.get("exclusions", []), "exclusion"),
        "open_questions_found": kw([f"{q.question} {q.why_it_matters}" for q in km.open_questions], gold.get("open_questions", []), "open question"),
        "stories_found": kw(story_texts, gold.get("stories", []), "story"),
        "items_not_in_gold": sorted(set(items) - matched),
    }, F
