"""Apply product decisions (decisions.yaml) to facts and to the synthesized spec.

Decisions are data, not prompts: they are applied by code after the agents
ran, so no agent can reinterpret or ignore them. Each decision fingerprints the
evidence it is based on; if that evidence changes later, the decision is
flagged for re-confirmation instead of silently applied.
"""
from __future__ import annotations

import hashlib

import yaml

from .schemas import BusinessRule, Decision, Exclusion, Fact, Finding, InfoItem, OpenQuestion, Section, Spec, Story, Unit


def load(ctx) -> list[Decision]:
    path = ctx.feature_dir / ctx.profile.get("decisions_file", "decisions.yaml")
    data = yaml.safe_load(path.read_text()) or {}
    return [Decision.model_validate(d) for d in data.get("decisions") or []]


def evidence_hash(d: Decision, units: dict[str, Unit]) -> str:
    texts = [units[u].text if u in units else f"<missing {u}>" for u in sorted(d.evidence)]
    return hashlib.sha256("\n".join(texts).encode()).hexdigest()[:12]


def stamp_and_check(ctx, decisions: list[Decision], units: dict[str, Unit]) -> list[Finding]:
    """Fill missing evidence hashes (writes back to decisions.yaml); flag stale ones."""
    findings, changed = [], False
    for d in decisions:
        h = evidence_hash(d, units)
        if not d.evidence_hash:
            d.evidence_hash, changed = h, True
        elif d.evidence_hash != h:
            findings.append(Finding(check="decisions", severity="error", target=d.id,
                                    message=f"evidence {d.evidence} changed since this decision was made - re-confirm "
                                            f"(then clear evidence_hash to re-stamp)"))
    if changed:
        path = ctx.feature_dir / ctx.profile.get("decisions_file", "decisions.yaml")
        header = path.read_text().split("decisions:")[0]
        body = yaml.safe_dump({"decisions": [d.model_dump(exclude_defaults=False) for d in decisions]},
                              sort_keys=False, allow_unicode=True, width=100)
        path.write_text(header + body)
    return findings


def apply_to_facts(decisions: list[Decision], facts: list[Fact]) -> list[Fact]:
    by_id = {f.id: f for f in facts}
    for d in decisions:
        kind, _, rest = d.target.partition(".")
        if kind != "fact" or rest not in by_id:
            continue
        if d.action == "reject":
            by_id.pop(rest)
        elif d.action == "accept":
            by_id[rest].basis = "explicit"
            by_id[rest].judge_note += f" [accepted by {d.id}]"
    return list(by_id.values())


def apply_to_spec(decisions: list[Decision], spec: Spec) -> tuple[Spec, list[Finding]]:
    """Targets: item.<id>[.<attr>] | rule.<id>[.<attr>] | open.<id> | exclusion.<id>
    | section.<id>[.<attr>] | story.<id>[.<attr>] | feature[.<attr>]"""
    findings = []
    km, feat = spec.knowledge, spec.feature
    stories = {s.id: sec for sec in feat.sections for s in sec.stories}
    colls = {"item": (km.items, InfoItem), "rule": (km.rules, BusinessRule), "open": (km.open_questions, OpenQuestion),
             "exclusion": (km.exclusions, Exclusion), "section": (feat.sections, Section)}
    for d in decisions:
        kind, _, rest = d.target.partition(".")
        if kind == "fact":
            continue
        try:
            if kind == "feature":                       # feature.<attr>: only override
                if d.action != "override" or not rest:
                    raise ValueError("only 'override' on feature.<attribute> is supported")
                setattr(feat, rest, d.value)
                _cite(feat, d)
                continue
            known_ids = list(stories) if kind == "story" else [x.id for x in colls[kind][0]]
            item_id, attr = _split_target(rest, known_ids)   # ids may contain dots (US-02.1)
            if kind == "story":
                coll, model = (stories[item_id].stories if item_id in stories else None), Story
                if coll is None and d.action == "add":
                    coll = next(sec for sec in feat.sections if sec.id == (d.value or {}).get("section")).stories
            else:
                coll, model = colls[kind]
            item = next((x for x in coll if x.id == item_id), None) if coll is not None else None
            if d.action == "add":
                if item is not None:
                    coll.remove(item)
                val = {k: v for k, v in (d.value or {}).items() if k != "section" or kind == "section"}
                obj = model.model_validate({**val, "id": item_id})
                _cite(obj, d)
                coll.append(obj)
            elif item is None:
                findings.append(Finding(check="decisions", severity="error", target=d.id,
                                        message=f"target {d.target} not found in the spec (renamed?)"))
            elif d.action == "override":
                setattr(item, attr, d.value)
                _cite(item, d)
            elif d.action == "exclude":
                coll.remove(item)
                km.exclusions.append(Exclusion(id=f"X-{d.id}", item=f"{kind} {item_id}", reason=d.rationale,
                                               source_refs=[d.id]))
            elif d.action == "resolve":
                coll.remove(item)
                if kind == "open":                      # no dangling references in the sections
                    for sec in feat.sections:
                        sec.open_questions = [q for q in sec.open_questions if q != item_id]
        except Exception as e:  # noqa: BLE001
            findings.append(Finding(check="decisions", severity="error", target=d.id, message=f"could not apply: {e}"))
    return spec, findings


def _split_target(rest: str, ids: list[str]) -> tuple[str, str]:
    """Split '<id>[.<attribute>]' where the id itself may contain dots (e.g. story id US-02.1)."""
    for i in sorted(ids, key=len, reverse=True):
        if rest == i:
            return i, ""
        if rest.startswith(i + "."):
            return i, rest[len(i) + 1:]
    return rest, ""      # unknown id (e.g. for 'add'); reported later if it must exist


def _cite(obj, d):
    if hasattr(obj, "source_refs"):
        obj.source_refs = sorted(set(obj.source_refs) | {d.id})
    if hasattr(obj, "status"):
        obj.status = "decision"
