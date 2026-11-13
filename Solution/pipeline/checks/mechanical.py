"""Deterministic checks (no LLM). These run first and are the backbone of
"complete and correct"; LLM judges only cover what rules cannot.
"""
from __future__ import annotations

import datetime as dt
from collections import defaultdict

from ..engine import conditions as C
from ..engine.schemas import Fact, Finding, Spec, Unit


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


# ------------------------------------------------------------- spec ------

def compute_depends_on(spec: Spec) -> None:
    for item in [*spec.fields, *spec.rules]:
        refs = set()
        exprs = [item.ask_when, item.required_when] if hasattr(item, "ask_when") else [item.expression]
        for e in exprs:
            try:
                refs |= C.references(e)
            except C.ConditionError:
                pass
        item.depends_on = sorted(refs - {item.id})


def lint(spec: Spec, fact_ids: set[str], decision_ids: set[str], consumers: set[str]) -> list[Finding]:
    F = []
    ids = [f.id for f in spec.fields] + [r.id for r in spec.rules]
    dup = {i for i in ids if ids.count(i) > 1}
    for d in dup:
        F.append(Finding(check="lint", severity="error", target=d, message="duplicate id"))
    known = set(ids)
    steps = {s.id: s for s in spec.steps}
    position = {}
    for f in spec.fields:
        if f.step not in steps:
            F.append(Finding(check="lint", severity="error", target=f.id, message=f"unknown step {f.step!r}"))
        position[f.id] = (steps[f.step].order if f.step in steps else 99, f.order)

    def check_expr(target, label, expr):
        try:
            refs = C.references(expr)
        except C.ConditionError as e:
            F.append(Finding(check="lint", severity="error", target=target, message=f"{label}: {e}"))
            return set()
        unknown = refs - known
        if unknown:
            F.append(Finding(check="lint", severity="error", target=target,
                             message=f"{label} references unknown ids {sorted(unknown)}"))
        return refs

    rule_deps = {r.id: check_expr(f"rule.{r.id}", "expression", r.expression) for r in spec.rules}

    def field_deps(refs, seen=None):
        """Expand rule references to the fields they ultimately depend on."""
        seen = seen or set()
        out = set()
        for r in refs:
            if r in rule_deps and r not in seen:
                seen.add(r)
                out |= field_deps(rule_deps[r], seen)
            elif r in position:
                out.add(r)
        return out

    for f in spec.fields:
        t = f"field.{f.id}"
        # the five questions every field must answer
        if not f.label or not f.question:
            F.append(Finding(check="lint", severity="error", target=t, message="What? label/question missing"))
        if f.type == "enum" and not f.options:
            F.append(Finding(check="lint", severity="error", target=t, message="What? enum without options"))
        if f.type != "enum" and f.options:
            F.append(Finding(check="lint", severity="error", target=t,
                             message=f"What? type {f.type} must not have options (use enum)"))
        if not f.consumers:
            F.append(Finding(check="lint", severity="error", target=t, message="Who needs it? no consumer"))
        for c in f.consumers:
            if c.party not in consumers:
                F.append(Finding(check="lint", severity="error", target=t, message=f"unknown consumer {c.party!r}"))
        refs = check_expr(t, "ask_when", f.ask_when) | check_expr(t, "required_when", f.required_when)
        for dep in field_deps(refs):
            if dep == f.id:
                F.append(Finding(check="lint", severity="error", target=t, message="condition depends on itself"))
            elif position.get(dep, (0, 0)) >= position[f.id]:
                F.append(Finding(check="lint", severity="error", target=t,
                                 message=f"asked before {dep}, which its condition depends on"))
        _check_refs(F, t, f.source_refs, fact_ids, decision_ids)
    for r in spec.rules:
        _check_refs(F, f"rule.{r.id}", r.source_refs, fact_ids, decision_ids)
    for n in spec.notices:
        check_expr(f"notice.{n.id}", "show_when", n.show_when)
        _check_refs(F, f"notice.{n.id}", n.source_refs, fact_ids, decision_ids)
    for s in spec.steps:
        check_expr(f"step.{s.id}", "ask_when", s.ask_when)
    for q in spec.open_questions:
        _check_refs(F, f"open.{q.id}", q.source_refs, fact_ids, decision_ids, allow_empty=True)
    for x in spec.exclusions:
        _check_refs(F, f"exclusion.{x.id}", x.source_refs, fact_ids, decision_ids)
    return F


def _check_refs(F, target, refs, fact_ids, decision_ids, allow_empty=False):
    if not refs and not allow_empty:
        F.append(Finding(check="trace", severity="error", target=target, message="no source reference"))
    bad = [r for r in refs if r not in fact_ids and r not in decision_ids]
    if bad:
        F.append(Finding(check="trace", severity="error", target=target, message=f"cites unknown or invalid facts {bad}"))


def coverage(units: list[Unit], facts: list[Fact], spec: Spec, decisions_refs: set[str]) -> tuple[dict, list[Finding]]:
    used_facts = set()
    for coll in (spec.fields, spec.rules, spec.notices, spec.open_questions, spec.exclusions):
        for item in coll:
            used_facts |= set(item.source_refs)
    # a superseded fact counts as covered when its successor is used
    for f in facts:
        if any(s in used_facts for s in f.superseded_by):
            used_facts.add(f.id)
    covered_units = {a.unit_id for f in facts for a in f.anchors}
    unused_facts = [f for f in facts if f.id not in used_facts and f.kind != "context" and f.temporality == "desired"]
    uncovered_units = [u for u in units if u.id not in covered_units and not u.id.endswith("-E00")]
    findings = [Finding(check="coverage", severity="warning", target=f.id,
                        message=f"fact not used by any requirement, exclusion or open question: {f.statement}")
                for f in unused_facts]
    stats = {
        "units_total": len(units), "units_covered": len(units) - len(uncovered_units),
        "facts_total": len(facts), "facts_used": len([f for f in facts if f.id in used_facts]),
        "uncovered_units": [{"id": u.id, "text": u.text[:160]} for u in uncovered_units],
    }
    return stats, findings


# --------------------------------------------------------- personas ------

def evaluate_persona(spec: Spec, answers: dict) -> dict:
    """Simulate the questionnaire for one person. Returns asked/required fields and rule values."""
    steps = {s.id: s for s in spec.steps}
    known = {f.id for f in spec.fields}
    visible = {k: v for k, v in answers.items() if k in known}
    for _ in range(4):                           # iterate to a fixpoint: answers -> rules -> asked -> answers
        env = dict(visible)
        for _ in range(len(spec.rules) + 1):      # rules may depend on rules
            for r in spec.rules:
                try:
                    env[r.id] = C.evaluate(r.expression, env)
                except Exception as e:  # noqa: BLE001
                    env[r.id] = f"ERROR: {e}"
        asked, required = [], []
        for f in spec.fields:                     # in flow order: only answers of asked fields exist
            step_ok = C.evaluate(steps[f.step].ask_when, env) if f.step in steps else True
            if step_ok and C.evaluate(f.ask_when, env):
                asked.append(f.id)
                if C.evaluate(f.required_when, env):
                    required.append(f.id)
            else:
                env[f.id] = None                  # not asked -> no value, even if the persona has one
        new_visible = {k: v for k, v in answers.items() if k in asked}
        if new_visible == visible:
            break
        visible = new_visible
    rules = {r.id: (v.isoformat() if isinstance(v := env.get(r.id), dt.date) else v) for r in spec.rules}
    return {"asked": asked, "required": required, "rules": rules}


def persona_tests(spec: Spec, personas: list[dict]) -> tuple[list[dict], list[Finding]]:
    results, F = [], []
    field_ids = {f.id for f in spec.fields}
    for p in personas:
        try:
            sim = evaluate_persona(spec, p["answers"])
        except Exception as e:  # noqa: BLE001
            F.append(Finding(check="personas", severity="error", target=p["id"], message=f"evaluation failed: {e}"))
            continue
        exp, fails = p.get("expect", {}), []
        fields = {f.id: f for f in spec.fields}
        for k, v in p["answers"].items():   # a persona answer must be a value the form can produce
            if k in fields and fields[k].type == "enum" and v not in {o.value for o in fields[k].options}:
                fails.append(f"answer {k}={v!r} is not an option value {[o.value for o in fields[k].options]} "
                             f"(fixture or option vocabulary out of sync)")
        for rid, want in exp.get("rules", {}).items():
            if rid not in sim["rules"]:
                fails.append(f"rule {rid} does not exist")
            elif sim["rules"][rid] != want:
                fails.append(f"{rid} = {sim['rules'][rid]!r}, expected {want!r}")
        for fid in exp.get("asked", []):
            if fid not in field_ids:
                fails.append(f"field {fid} does not exist")
            elif fid not in sim["asked"]:
                fails.append(f"{fid} should be asked")
        for fid in exp.get("not_asked", []):
            if fid in sim["asked"]:
                fails.append(f"{fid} should NOT be asked (data minimisation)")
        for fid in exp.get("required", []):
            if fid in field_ids and fid not in sim["required"]:
                fails.append(f"{fid} should be required")
        ignored = sorted(set(p["answers"]) - field_ids)
        results.append({"id": p["id"], "from": p.get("from", ""), "pass": not fails, "failures": fails,
                        "simulation": sim, "unused_inputs_alias_or_not_in_spec": ignored})
        for msg in fails:
            F.append(Finding(check="personas", severity="error", target=p["id"], message=f"{msg}  [{p.get('from', '')}]"))
    return results, F


# ------------------------------------------------------------- eval ------

def evaluate_gold(spec: Spec, gold: dict) -> tuple[dict, list[Finding]]:
    F = []
    spec_fields = {f.id: f for f in spec.fields}
    spec_rules = {r.id for r in spec.rules}
    matched_spec = set()
    hits = 0
    consumer_hits = consumer_total = 0
    for g in gold.get("fields", []):
        names = [g["id"], *g.get("aliases", [])]
        hit = next((n for n in names if n in spec_fields or n in spec_rules), None)
        if hit:
            hits += 1
            matched_spec.add(hit)
            if hit in spec_fields:
                have = {c.party for c in spec_fields[hit].consumers}
                for c in g.get("consumers", []):
                    consumer_total += 1
                    consumer_hits += c in have
                    if c not in have:
                        F.append(Finding(check="eval", severity="warning", target=hit, message=f"missing consumer {c}"))
        else:
            F.append(Finding(check="eval", severity="warning", target=g["id"], message="gold field not in spec"))
    for r in gold.get("rules", []):
        if r not in spec_rules:
            F.append(Finding(check="eval", severity="warning", target=r, message="gold rule not in spec"))

    def kw(items, text_of, keys, label):
        found = 0
        for k in keys:
            if any(k.lower() in text_of(i).lower() for i in items):
                found += 1
            else:
                F.append(Finding(check="eval", severity="warning", target=label, message=f"no {label} mentions {k!r}"))
        return found

    ex = kw(spec.exclusions, lambda x: f"{x.item} {x.reason}", gold.get("exclusions", []), "exclusion")
    no = kw(spec.notices, lambda x: x.text, gold.get("notices", []), "notice")
    oq = kw(spec.open_questions, lambda x: f"{x.question} {x.why_it_matters}", gold.get("open_questions", []), "open question")
    extra = sorted(set(spec_fields) - matched_spec)
    n_gold = len(gold.get("fields", []))
    metrics = {
        "field_recall": round(hits / n_gold, 2) if n_gold else None,
        "field_precision": round(len(matched_spec & set(spec_fields)) / len(spec_fields), 2) if spec_fields else None,
        "consumer_recall": round(consumer_hits / consumer_total, 2) if consumer_total else None,
        "rules_found": f"{len([r for r in gold.get('rules', []) if r in spec_rules])}/{len(gold.get('rules', []))}",
        "exclusions_found": f"{ex}/{len(gold.get('exclusions', []))}",
        "notices_found": f"{no}/{len(gold.get('notices', []))}",
        "open_questions_found": f"{oq}/{len(gold.get('open_questions', []))}",
        "fields_not_in_gold": extra,
    }
    return metrics, F
