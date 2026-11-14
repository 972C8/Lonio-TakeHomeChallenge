"""Deterministic rendering: spec JSON + facts -> requirements/<problem>/ feature specs.

The Markdown is never written by an LLM directly: agents produce structured
data, templates decide the format. The internal formalisation (expressions)
is deliberately NOT rendered - the output contains business knowledge only.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from ..engine.schemas import Decision, Fact, Spec, Unit

TEMPLATES = Path(__file__).parent / "templates"


def render(out_dir: Path, ctx, spec: Spec, facts: list[Fact], units: dict[str, Unit], decisions: list[Decision],
           judge: dict | None = None, guidance: dict | None = None, examples: list[dict] | None = None) -> list[Path]:
    env = Environment(loader=FileSystemLoader(TEMPLATES), undefined=StrictUndefined,
                      trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)
    env.filters["cell"] = lambda s: str(s).replace("|", "/").replace("\n", " ")
    km = spec.knowledge
    facts_by_id = {f.id: f for f in facts}
    dec_by_id = {d.id: d for d in decisions}
    guidance = guidance or {}
    items = {i.id: i for i in km.items}
    rules = {r.id: r for r in km.rules}
    names = {**{i.id: i.name for i in km.items}, **{r.id: r.name for r in km.rules}}
    owner = {x: f for f in spec.features for x in f.items + f.rules}
    used_in = {}
    for f in spec.features:
        for s in f.stories:
            for x in s.items + s.rules:
                used_in.setdefault(x, []).append((f, s))
    verified = {e["case"]: e["pass"] for e in (examples or [])}

    def evidence(refs):
        out = []
        for r in refs:
            if r in guidance:
                out.append({"id": r, "source": "product owner guidance", "statement": guidance[r], "quotes": [], "basis": ""})
            elif r in dec_by_id:
                d = dec_by_id[r]
                out.append({"id": r, "source": f"product decision ({d.by})", "statement": d.rationale, "quotes": [], "basis": ""})
            elif r in facts_by_id:
                f = facts_by_id[r]
                out.append({"id": r, "source": f.source_id, "statement": f.statement,
                            "basis": "inferred" if f.basis == "inferred" else "",
                            "quotes": [{"quote": a.quote, "where": _where(units.get(a.unit_id))} for a in f.anchors]})
        return out

    def feature_refs(f):
        refs = set(f.source_refs)
        for s in f.stories:
            refs |= set(s.source_refs)
            for ac in s.acceptance_criteria:
                refs |= set(ac.source_refs)
        for x in f.items:
            refs |= set(items[x].source_refs) if x in items else set()
        for x in f.rules:
            refs |= set(rules[x].source_refs) if x in rules else set()
        return sorted(refs)

    def example_table(ac):
        cols_in, cols_out = [], []
        for ex in ac.examples:
            for g in ex.given:
                if g.item not in cols_in:
                    cols_in.append(g.item)
            for t in ex.then:
                if t.target not in cols_out:
                    cols_out.append(t.target)
        rows = []
        for ex in ac.examples:
            gi = {g.item: g.value for g in ex.given}
            th = {t.target: t.expect for t in ex.then}
            ok = verified.get(f"{ac.id} / {ex.name}")
            rows.append({"name": ex.name + (" (illustrative)" if ex.illustrative else ""),
                         "in": [gi.get(c, "–") for c in cols_in], "out": [th.get(c, "–") for c in cols_out],
                         "ok": "✅" if ok else ("❌" if ok is False else "")})
        return {"in": [names.get(c, c) for c in cols_in], "out": [names.get(c, c) for c in cols_out], "rows": rows}

    # stakeholders: "id: short name - description" -> rendered by short name
    stakeholders = {k: str(v).split(" - ")[0].strip() for k, v in ctx.profile["stakeholders"].items()}
    common = dict(spec=spec, km=km, items=items, rules=rules, names=names, stakeholders=stakeholders,
                  owner=owner, used_in=used_in, evidence=evidence, judge=judge or {}, profile=ctx.profile,
                  oq={q.id: q for q in km.open_questions}, feature_refs=feature_refs, example_table=example_table,
                  features=sorted(spec.features, key=lambda f: f.order))
    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "features").mkdir(parents=True)
    written = []

    def w(path, tpl, **kw):
        p = out_dir / path
        p.write_text(env.get_template(tpl).render(**common, **kw))
        written.append(p)

    w("README.md", "index.md.j2")
    for f in common["features"]:
        w(f"features/{f.id}.md", "feature.md.j2", f=f)
    w("information.md", "information.md.j2")
    w("open-questions.md", "open_questions.md.j2")
    w("out-of-scope.md", "exclusions.md.j2")
    w("traceability.md", "traceability.md.j2", facts=facts)
    return written


def _where(u: Unit | None) -> str:
    if u is None:
        return "?"
    m = u.meta
    if "speaker" in m:
        return f"{u.id}, {m['speaker']}"
    if "file" in m:
        return f"{m['file']} ({u.id})"
    return u.id
