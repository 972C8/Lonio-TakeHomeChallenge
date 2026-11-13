"""Deterministic rendering: spec JSON + facts -> requirements/ Markdown.

The Markdown is never written by an LLM directly. Changing the format means
changing a template, and the whole package re-renders consistently.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from ..engine.paths import PIPELINE
from ..engine.schemas import Decision, Fact, Spec, Unit

TEMPLATES = Path(__file__).parent / "templates"


def _env():
    env = Environment(loader=FileSystemLoader(TEMPLATES), undefined=StrictUndefined,
                      trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)
    env.filters["cond"] = lambda e: "always" if e.strip() in ("true", "True") else ("never" if e.strip() in ("false", "False") else f"`{e}`")
    return env


def render(out_dir: Path, ctx, spec: Spec, facts: list[Fact], units: dict[str, Unit],
           decisions: list[Decision], judge: dict | None = None, guidance: dict | None = None) -> list[Path]:
    env = _env()
    facts_by_id = {f.id: f for f in facts}
    dec_by_id = {d.id: d for d in decisions}
    steps = sorted(spec.steps, key=lambda s: s.order)
    fields_by_step = {s.id: sorted([f for f in spec.fields if f.step == s.id], key=lambda f: f.order) for s in steps}
    used_by = {}
    for item in [*spec.fields, *spec.rules]:
        for dep in item.depends_on:
            used_by.setdefault(dep, []).append(item.id)
    sources = {s["id"]: s for s in ctx.profile["sources"]}

    def evidence(refs):
        out = []
        for r in refs:
            if guidance and r in guidance:
                out.append({"id": r, "kind": "guidance", "source": "product owner guidance",
                            "statement": guidance[r], "quotes": []})
            elif r in dec_by_id:
                d = dec_by_id[r]
                out.append({"id": r, "kind": "decision", "source": f"product decision ({d.by})",
                            "statement": d.rationale, "quotes": []})
            elif r in facts_by_id:
                f = facts_by_id[r]
                src = sources.get(f.source_id, {})
                out.append({"id": r, "kind": f.kind, "source": f.source_id, "basis": f.basis,
                            "statement": f.statement,
                            "quotes": [{"unit": a.unit_id, "quote": a.quote,
                                        "where": _where(units.get(a.unit_id))} for a in f.anchors],
                            "superseded_by": f.superseded_by, "src_type": src.get("type", "")})
        return out

    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "fields").mkdir(parents=True)
    (out_dir / "rules").mkdir()
    common = dict(spec=spec, steps=steps, fields_by_step=fields_by_step, profile=ctx.profile,
                  consumers=ctx.profile["consumers"], used_by=used_by, evidence=evidence, judge=judge or {},
                  condition_language=(PIPELINE / "engine" / "condition_language.md").read_text())
    written = []

    def w(path, tpl, **kw):
        p = out_dir / path
        p.write_text(env.get_template(tpl).render(**common, **kw))
        written.append(p)

    w("README.md", "index.md.j2")
    w("conventions.md", "conventions.md.j2")
    w("flow.md", "flow.md.j2")
    for s in steps:
        for f in fields_by_step[s.id]:
            w(f"fields/{f.id}.md", "field.md.j2", f=f, step=s)
    for r in spec.rules:
        w(f"rules/{r.id}.md", "rule.md.j2", r=r)
    w("notices.md", "notices.md.j2")
    w("open-questions.md", "open_questions.md.j2")
    w("out-of-scope.md", "exclusions.md.j2")
    w("traceability.md", "traceability.md.j2", facts=facts, units=units, sources=sources)
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
