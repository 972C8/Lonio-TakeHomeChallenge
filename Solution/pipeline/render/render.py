"""Deterministic rendering: spec JSON + facts -> requirements/<feature>/ (feature.md, one file per story in
stories/, shared files).

The Markdown is never written by an LLM directly: agents produce structured
data, templates decide the format. The internal formalisation (expressions)
is deliberately NOT rendered - the output contains business knowledge only.
"""
from __future__ import annotations

import re
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
    feature = spec.feature
    sections = sorted(feature.sections, key=lambda x: x.order)
    owner = {x: sec for sec in sections for x in sec.items + sec.rules}
    verified = {e["case"]: e["pass"] for e in (examples or [])}

    def evidence(refs):
        out = []
        for r in refs:
            if r in guidance:
                out.append({"id": r, "source": "product owner guidance", "statement": guidance[r], "quotes": [], "basis": ""})
            elif r in dec_by_id:
                d = dec_by_id[r]
                out.append({"id": r, "source": f"product decision ({d.by})", "statement": d.statement or d.rationale, "quotes": [], "basis": ""})
            elif r in facts_by_id:
                f = facts_by_id[r]
                out.append({"id": r, "source": f.source_id, "statement": f.statement,
                            "basis": "inferred" if f.basis == "inferred" else "",
                            "quotes": [{"quote": a.quote, "where": _where(units.get(a.unit_id))} for a in f.anchors]})
        return out

    def story_refs(st):
        refs = set(st.source_refs)
        for ac in st.acceptance_criteria:
            refs |= set(ac.source_refs)
        return sorted(refs)

    def feature_refs(stories=True):
        refs = set(feature.source_refs)
        for sec in sections:
            refs |= set(sec.source_refs)
            if stories:
                for st in sec.stories:
                    refs |= set(story_refs(st))
        for i in km.items:
            refs |= set(i.source_refs)
        for r in km.rules:
            refs |= set(r.source_refs)
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
    story_path = {s.id: f"stories/{story_file(s)}" for sec in sections for s in sec.stories}
    all_stories = [s for sec in sections for s in sec.stories]
    flow_stories, flow_derived = {}, []
    if feature.flow:
        placed = set()
        for st in feature.flow.steps:
            placed |= set(st.rules)
            flow_stories[st.order] = [s.id for s in all_stories
                                      if set(s.items) & set(st.items) or set(s.rules) & set(st.rules)]
        flow_derived = [{"name": r.name, "stories": [s.id for s in all_stories if r.id in s.rules]}
                        for r in km.rules if r.id not in placed]
    flow_title = (ctx.profile.get("flow") or {}).get("title", "Flow") if isinstance(ctx.profile.get("flow"), dict) else "Flow"
    common = dict(flow_stories=flow_stories, flow_derived=flow_derived, flow_title=flow_title, spec=spec, km=km, items=items, rules=rules, names=names, stakeholders=stakeholders,
                  owner=owner, evidence=evidence, feature=feature, sections=sections, judge=judge or {}, profile=ctx.profile,
                  oq={q.id: q for q in km.open_questions}, feature_refs=feature_refs, story_refs=story_refs,
                  example_table=example_table, story_path=story_path)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    written = []

    def w(path, tpl, **kw):
        p = out_dir / path
        p.write_text(env.get_template(tpl).render(**common, **kw))
        written.append(p)

    w("README.md", "index.md.j2")
    w("feature.md", "feature.md.j2")
    (out_dir / "stories").mkdir()
    for sec in sections:
        for s in sec.stories:
            w(story_path[s.id], "story.md.j2", sec=sec, s=s)
    w("information.md", "information.md.j2")
    w("open-questions.md", "open_questions.md.j2")
    w("out-of-scope.md", "exclusions.md.j2")
    w("traceability.md", "traceability.md.j2", facts=facts)
    return written


def story_file(s) -> str:
    """stories/US-02.1-confirm-the-first-working-day.md - id first so the files sort in story order."""
    slug = re.sub(r"[^a-z0-9]+", "-", s.title.lower()).strip("-")
    if len(slug) > 60:                                  # cut at a word boundary
        slug = slug[:61].rsplit("-", 1)[0]
    return f"{s.id}-{slug}.md"


def _where(u: Unit | None) -> str:
    if u is None:
        return "?"
    m = u.meta
    if "speaker" in m:
        return f"{u.id}, {m['speaker']}"
    if "file" in m:
        return f"{m['file']} ({u.id})"
    return u.id
