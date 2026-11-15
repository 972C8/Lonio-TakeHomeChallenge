"""The pipeline: stages, in order.

     1 normalize    per source, adapter          -> build/<f>/normalize/<src>.json  (Units)
     2 extract      per source, agent            -> build/<f>/extract/<src>.json    (Facts)
     3 verify       anchors (code) + fact judge  -> build/<f>/facts.json
     4 knowledge    agent                        -> build/<f>/knowledge.raw.json    (items, rules, open questions)
     5 feature      planner agent (sections of the ONE feature), then one writer agent
                    per section (parallel)       -> build/<f>/feature.plan.json, sections/<id>.json
     6 decide       decisions.yaml (code)        -> build/<f>/spec.json
                    (directives - action 'direct' - already steered stages 4-5)
     7 check        checklist lint, examples executed against the knowledge model,
                    coverage, tech-leak scan (code); trace judge (agent)
     8 render       templates (code)             -> requirements/<f>/
     9 refinement   a dev-refinement agent reads the rendered feature (feature.md + stories/)
    10 review       reviewer agent               -> build/<f>/review.md (verdict)

Every LLM stage is cached by a fingerprint of its inputs. `--force <stage>`
reruns a stage regardless.
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

from pydantic import BaseModel, Field as F
from typing import Literal

from .adapters.base import get_adapter
from .checks import mechanical as M
from .engine import decisions as D
from .engine import incremental as I
from .engine.context import Context, sha
from .engine.llm import COSTS, load_prompt, run_agent, usage_summary
from .engine.paths import PIPELINE, REQUIREMENTS
from .engine.schemas import (AcceptanceCriterion, BusinessRule, Fact, Feature, FeaturePlan, Finding, Flow, KnowledgeModel,
                             Section, Spec, Unit)
from .render.render import TEMPLATES, render

AGENTS = PIPELINE / "agents"
COND_LANG = PIPELINE / "engine" / "condition_language.md"


# ----------------------------------------------------------- judge schemas --

class Verdict(BaseModel):
    id: str
    verdict: Literal["supported", "partial", "unsupported"]
    note: str = ""


class Verdicts(BaseModel):
    verdicts: list[Verdict]


class RuleFixes(BaseModel):
    rules: list[BusinessRule]


class CriterionFixes(BaseModel):
    acceptance_criteria: list[AcceptanceCriterion]


class RefinementQuestion(BaseModel):
    file: str
    question: str
    severity: Literal["blocker", "major", "minor"]


class TechLeak(BaseModel):
    file: str
    quote: str
    why: str


class RefinementReport(BaseModel):
    questions: list[RefinementQuestion]
    already_flagged: list[str] = F(default_factory=list)
    tech_leaks: list[TechLeak] = F(default_factory=list)


class ReviewFinding(BaseModel):
    title: str
    why: str
    evidence: str
    action: str
    status: Literal["new", "still_open"] = F("new", description="still_open: the same problem was a finding of the "
                                                                 "previous review; new: it was not")


class ResolvedFinding(BaseModel):
    title: str = F(description="The previous finding's title, as it was")
    resolved_by: str = F(description="What resolved it: decision ids, or what changed in the spec")


class Review(BaseModel):
    verdict: Literal["ready", "ready_with_caveats", "not_ready"]
    summary: str
    findings: list[ReviewFinding]
    resolved: list[ResolvedFinding] = F(default_factory=list, description="Previous findings that no longer apply")


# ------------------------------------------------------------------ stages --

async def stage_sources(ctx: Context):
    """normalize + extract every source, in parallel across sources."""
    srcs = [s for s in ctx.profile["sources"] if s.get("enabled", True)]
    adapters = {s["id"]: get_adapter(s, ctx) for s in srcs}

    async def one(sid, ad):
        units_raw = await ctx.stage(f"normalize/{sid}", ad.normalize_inputs(),
                                    lambda: _dump(ad.normalize()))
        units = [Unit.model_validate(u) for u in units_raw]
        facts_raw = await ctx.stage(f"extract/{sid}", [units_raw, *ad.extract_inputs()],
                                    lambda: _dump(ad.extract(units)))
        return units, [Fact.model_validate(f) for f in facts_raw]

    results = await asyncio.gather(*[one(sid, ad) for sid, ad in adapters.items()])
    units = [u for us, _ in results for u in us]
    facts = [f for _, fs in results for f in fs]
    return adapters, units, facts


async def _dump(coro):
    return [x.model_dump() for x in await coro]


async def stage_verify_facts(ctx, adapters, units, facts) -> tuple[list[Fact], list[Finding]]:
    unit_by_id = {u.id: u for u in units}
    findings = M.verify_anchors(facts, unit_by_id, adapters)
    M.link_supersedes(facts)
    order = [u.id for u in units]

    system = load_prompt(AGENTS / "fact_judge.md")

    def item(f):
        ctx_units = set()
        for a in f.anchors:
            if a.unit_id in unit_by_id:
                i = order.index(a.unit_id)
                ctx_units |= {order[j] for j in range(max(0, i - 1), min(len(order), i + 2))}
        return {"id": f.id, "statement": f.statement, "basis": f.basis, "kind": f.kind,
                "units": {u: {"text": unit_by_id[u].text, "meta": unit_by_id[u].meta} for u in sorted(ctx_units)}}

    items = [item(f) for f in facts]

    # Verdicts are kept per fact: a fact whose statement and source context did not change keeps its verdict,
    # so a new source is judged on its own facts only (as the trace judge does for elements).
    def key(x):
        return sha(x, system)

    async def judge_all():
        known = _previous(ctx, "judge_facts.cache")
        if known is None:        # first run with this cache: verdicts of the previous run, for facts of sources not re-read
            prev_v = {v["id"]: v for v in (_previous(ctx, "judge_facts") or [])}
            reread = {n.split("/", 1)[1] for n in ctx.ran if n.startswith(("normalize/", "extract/"))}
            known = {key(x): prev_v[f.id] for f, x in zip(facts, items) if f.id in prev_v and f.source_id not in reread}
        todo = [x for x in items if key(x) not in known]
        batches = [todo[i:i + 15] for i in range(0, len(todo), 15)]

        async def judge(batch, n):
            out = await run_agent(f"judge_facts/batch{n}", system, json.dumps(batch, ensure_ascii=False, indent=1),
                                  Verdicts, model=ctx.model("judge"))
            return out["verdicts"]

        res = await asyncio.gather(*[judge(b, n) for n, b in enumerate(batches)])
        fresh = {v["id"]: v for r in res for v in r}
        ctx.log(f"  fact judge: {len(todo)} facts judged, {len(items) - len(todo)} verdicts reused")
        cache = {key(x): fresh[x["id"]] for x in todo if x["id"] in fresh}
        cache |= {key(x): known[key(x)] for x in items if key(x) in known}
        ctx.write("judge_facts.cache", cache)
        return [cache[key(x)] for x in items if key(x) in cache]

    verdicts = await ctx.stage("judge_facts", [[f.model_dump() for f in facts], AGENTS / "fact_judge.md"], judge_all)
    vmap = {v["id"]: v for v in verdicts}
    for f in facts:
        if f.id in vmap:
            f.judge, f.judge_note = vmap[f.id]["verdict"], vmap[f.id].get("note", "")
            if f.judge != "supported":
                findings.append(Finding(check="fact_judge", severity="warning" if f.judge == "partial" else "error",
                                        target=f.id, message=f"{f.judge}: {f.judge_note} | {f.statement}"))
    ctx.write("facts", [f.model_dump() for f in facts])
    return facts, findings


def _sources_text(sources: list[dict]) -> str:
    return "\n".join(f"- `{s['id']}` ({s['type']}, precedence {s.get('precedence', 9)}): {s.get('authority', '')}"
                     for s in sources)


def _profile_ctx(ctx: Context) -> dict:
    p = ctx.profile
    return dict(
        goal=p["goal"],
        stakeholders="\n".join(f"- `{k}`: {v}" for k, v in p["stakeholders"].items()),
        sources=_sources_text(p["sources"]),
        guidance=(ctx.feature_dir / "guidance.md").read_text(),
        directives=D.directives_prompt(D.load(ctx)),
        conventions=COND_LANG.read_text(),
    )


def _fact_payload(facts: list[Fact]) -> list[dict]:
    return [{"id": f.id, "source": f.source_id, "kind": f.kind, "subject": f.subject, "statement": f.statement,
             "basis": f.basis, "temporality": f.temporality, "superseded_by": f.superseded_by,
             "quotes": [a.quote for a in f.anchors]} for f in facts]


def _previous(ctx, name: str):
    """The saved output of an earlier run of stage `name` (None on the first run)."""
    p = ctx.out(name)
    return json.loads(p.read_text()) if p.exists() else None


def _existing(ids: list[str]) -> str:
    return ", ".join(ids) or "(none yet)"


async def stage_knowledge(ctx, facts: list[Fact], known_before: set[str] | None = None) -> KnowledgeModel:
    """Ids of items and rules are fed back from the last run (knowledge.raw) so reruns reuse them."""
    usable = [f for f in facts if f.anchor_ok and f.judge != "unsupported"]
    prev = _previous(ctx, "knowledge.raw")
    existing = [i["id"] for i in prev["items"]] + [r["id"] for r in prev.get("rules", [])] if prev else []
    args = dict(**_profile_ctx(ctx))
    system = load_prompt(AGENTS / "knowledge_modeler.md", **args, existing_ids=_existing(existing))
    # The ids fed back are not an input of the cache fingerprint: otherwise the first rerun would always recompute.
    # Nor is the list of sources: a new or removed source is new or removed facts (delta path); only a changed
    # trust level of an existing source (src_digest) forces a full rebuild.
    fingerprint_system = load_prompt(AGENTS / "knowledge_modeler.md", **{**args, "sources": ""}, existing_ids="")
    payload = _fact_payload(usable)

    system_fp = sha(fingerprint_system)
    digest = I.fact_digest(payload)
    dir_digest = I.directive_digest(D.load(ctx))
    src_digest = I.source_digest(ctx.profile["sources"])

    def same_prompt(prev_in: dict | None) -> bool:
        if prev_in is None:      # bootstrap: a model from before incremental runs; treat its prompt as unchanged
            return True
        if prev_in.get("system") == system_fp:
            return not I.sources_changed(prev_in, src_digest)
        if "sources" not in prev_in:   # recorded before sources were split out: rebuild the prompt it saw
            legacy = I.sources_with_facts(ctx.profile["sources"], prev_in.get("facts", {}))
            return prev_in.get("system") == sha(load_prompt(AGENTS / "knowledge_modeler.md",
                                                            **{**args, "sources": _sources_text(legacy)}, existing_ids=""))
        return False

    async def go():
        prev_in = _previous(ctx, "knowledge.input")
        ctx.write("knowledge.guard", {"reverted": []})
        # ...but never the directives: a new or changed one reshapes the model, not just the facts it cites
        full = (not prev or not same_prompt(prev_in) or (prev_in is None and known_before is None)
                or I.directives_changed(prev_in, dir_digest) or "all" in ctx.force or "knowledge.raw" in ctx.force)
        if full:
            out = await run_agent("knowledge", system, "Facts (JSON):\n" + json.dumps(payload, ensure_ascii=False, indent=1)
                                  + "\n\nProduce the complete KnowledgeModel.", KnowledgeModel,
                                  model=ctx.model("synthesize"), max_turns=8)
            km = KnowledgeModel.model_validate(out)
        else:
            if prev_in:
                new_ids, removed = I.fact_changes(prev_in["facts"], digest)
            else:                    # bootstrap: compare with the fact ids of the previous run
                new_ids = sorted(set(digest) - known_before)
                removed = sorted(known_before - set(digest))
            km = await _knowledge_delta(ctx, system, KnowledgeModel.model_validate(prev),
                                        [p for p in payload if p["id"] in set(new_ids)], removed)
        ctx.write("knowledge.input", {"system": system_fp, "facts": digest, "directives": dir_digest, "sources": src_digest})
        return await _repair_tables(ctx, system, km)

    return KnowledgeModel.model_validate(await ctx.stage("knowledge.raw", [payload, fingerprint_system, src_digest], go))


async def _knowledge_delta(ctx, system: str, prev: KnowledgeModel, new_facts: list[dict],
                           removed: list[str]) -> KnowledgeModel:
    """Incremental modelling: the agent returns only what the new / removed facts change; code applies it."""
    ctx.log(f"  delta: {len(new_facts)} new or changed facts, {len(removed)} removed")
    ctx.write("knowledge.guard", {"reverted": []})
    if not new_facts and not removed:
        return prev
    system = system + "\n\n" + load_prompt(AGENTS / "knowledge_delta.md")
    prompt = ("Previous knowledge model (JSON) - it stays exactly as it is except for what you return:\n"
              + prev.model_dump_json(indent=1, exclude={"items": {"__all__": {"depends_on"}}, "rules": {"__all__": {"depends_on"}}})
              + "\n\nNew or changed facts (JSON):\n" + json.dumps(new_facts, ensure_ascii=False, indent=1)
              + "\n\nRemoved fact ids (no longer valid; elements citing only them must change or go): "
              + (", ".join(removed) or "none")
              + "\n\nReturn a delta: every item, rule, open question or exclusion that must be ADDED or CHANGED because "
                "of these facts, as complete objects (keep the id when an element changes), and in `remove` the ids of "
                "elements to delete (item.<id>, rule.<id>, open.<id>, exclusion.<id>). An open question the new facts "
                "answer is removed or updated. Cite the new facts. Apply source precedence and corrections as usual. "
                "Return nothing for elements the facts do not affect.")
    out = await run_agent("knowledge_delta", system, prompt, I.KnowledgeDelta, model=ctx.model("synthesize"), max_turns=6)
    delta, reverted = I.guard_delta(prev, I.KnowledgeDelta.model_validate(out), {p["id"] for p in new_facts}, set(removed))
    for n in reverted:
        ctx.log(f"  guard: {n}")
    ctx.write("knowledge.guard", {"reverted": reverted})
    ctx.log(f"  delta: {len(delta.items)} items, {len(delta.rules)} rules, {len(delta.open_questions)} open questions "
            f"changed or added; {len(delta.remove)} removed")
    return I.apply_delta(prev, delta)


async def _repair_tables(ctx, system: str, km: KnowledgeModel) -> dict:
    """One repair round for decision tables whose rows do not have one cell per input (only the broken rules go back)."""
    errors = M.table_shape_errors(km)
    if not errors:
        return km.model_dump()
    broken = {e.split(":")[0].removeprefix("rule ") for e in errors}
    rules = [r for r in km.rules if r.id in broken]
    ctx.log(f"  repairing decision tables of {len(rules)} rules ...")
    out = await run_agent("knowledge_repair", system,
                          "These rules have decision-table rows without one cell per input:\n- " + "\n- ".join(errors)
                          + "\n\nRules (JSON):\n" + json.dumps([r.model_dump() for r in rules], ensure_ascii=False, indent=1)
                          + "\n\nReturn these rules corrected: every row exactly one cell per input, in column order "
                            "('any' / '-' where needed). Change nothing else.", RuleFixes, model=ctx.model("synthesize"), max_turns=4)
    fixed = {r["id"]: BusinessRule.model_validate(r) for r in out["rules"]}
    km.rules = [fixed.get(r.id, r) for r in km.rules]
    return km.model_dump()


async def _repair_examples(ctx, system: str, km: KnowledgeModel, sec: Section) -> Section:
    """One repair round for the section's acceptance criteria whose examples fail against the knowledge model."""
    failing = {}
    for s in sec.stories:
        for ac in s.acceptance_criteria:
            msgs = [f"{ex.name}: {m}" for ex in ac.examples
                    for m in M.check_example(km, {g.item: g.value for g in ex.given}, [(t.target, t.expect) for t in ex.then])[0]]
            if msgs:
                failing[ac.id] = (ac, msgs)
    if not failing:
        return sec
    ctx.log(f"  repairing {len(failing)} criteria of {sec.id} ...")
    items = [{"id": i.id, "asked_when_expr": i.asked_when_expr, "allowed_values": i.allowed_values} for i in km.items]
    prompt = ("These acceptance criteria have examples that fail when executed against the knowledge model:\n"
              + "\n".join(f"- {cid}: " + "; ".join(m) for cid, (_, m) in failing.items())
              + "\n\nCriteria (JSON):\n" + json.dumps([ac.model_dump() for ac, _ in failing.values()], ensure_ascii=False, indent=1)
              + "\n\nItems involved (JSON):\n" + json.dumps(items, ensure_ascii=False, indent=1)
              + "\n\nRules (JSON):\n" + json.dumps([{"id": r.id, "expression": r.expression} for r in km.rules], ensure_ascii=False, indent=1)
              + "\n\nReturn these criteria with corrected examples (usually missing inputs that make an item asked). "
                "Only change an expected outcome if the criterion's own text says otherwise. Change nothing else.")
    out = await run_agent(f"write_section_repair/{sec.id}", system, prompt, CriterionFixes,
                          model=ctx.model("synthesize"), max_turns=4)
    fixed = {a["id"]: AcceptanceCriterion.model_validate(a) for a in out["acceptance_criteria"]}
    stories = [s.model_copy(update={"acceptance_criteria": [fixed.get(a.id, a) for a in s.acceptance_criteria]})
               for s in sec.stories]
    return sec.model_copy(update={"stories": stories})


async def _plan_delta(ctx, system: str, prev: FeaturePlan, km: KnowledgeModel) -> dict:
    """Keep the previous sections; only new items, rules and open questions are assigned to one of them."""
    plan, unassigned = I.plan_update(prev, km)
    if unassigned:
        names = {x.id: getattr(x, "name", None) or getattr(x, "question", "") for x in [*km.items, *km.rules, *km.open_questions]}
        ctx.log(f"  plan: keeping {len(plan.sections)} sections, assigning {', '.join(unassigned)}")
        out = await run_agent("plan_assign", system,
                              "Existing sections (JSON):\n" + json.dumps([{"id": s.id, "title": s.title, "purpose": s.purpose}
                                                                           for s in plan.sections], ensure_ascii=False, indent=1)
                              + "\n\nNew elements to assign (id: name):\n" + "\n".join(f"- {i}: {names.get(i, '')}" for i in unassigned)
                              + "\n\nAssign each new element to the ONE existing section whose goal needs it most. "
                                "Do not create sections.", I.Assignments, model=ctx.model("assign", "synthesize"), max_turns=3)
        plan = I.assign(plan, km, I.Assignments.model_validate(out).assignments)
    return plan.model_dump()


async def stage_feature(ctx, km: KnowledgeModel, facts: list[Fact], prev_km: dict | None = None) -> Feature:
    """The whole feature: plan its sections, then one writer agent per section (parallel)."""
    pc = _profile_ctx(ctx)
    hints = ctx.profile.get("section_hints", "")
    prev_plan = _previous(ctx, "feature.plan")
    prev_sections = [f"{s['id']} ({s['title']})" for s in prev_plan["sections"]] if prev_plan else []
    plan_args = dict(**pc, plan_constraints=f"# Hints from the feature profile\n{hints}" if hints else "")
    plan_system = load_prompt(AGENTS / "feature_planner.md", **plan_args, existing_ids=_existing(prev_sections))
    plan_fingerprint_system = load_prompt(AGENTS / "feature_planner.md", **plan_args, existing_ids="")
    kmj = km.model_dump(exclude={"items": {"__all__": {"asked_when_expr", "required_when_expr", "depends_on"}},
                                 "rules": {"__all__": {"expression", "depends_on"}}})
    facts_by_id = {f.id: f for f in facts}

    plan_fp = sha(plan_fingerprint_system)
    write_fingerprint_system = load_prompt(AGENTS / "story_writer.md", **pc, existing_ids="")
    write_fp = sha(write_fingerprint_system)
    feat_in = _previous(ctx, "feature.input")            # None before the first incremental run: treat prompts as unchanged
    dir_digest = I.directive_digest(D.load(ctx))
    same_directives = not I.directives_changed(feat_in, dir_digest)   # ...but never the directives
    old_km = KnowledgeModel.model_validate(prev_km) if prev_km else None
    changed = I.changed_ids(old_km, km)                  # None = no previous model -> full rewrite
    changed_behaviour = I.behaviour_changed_ids(old_km, km)
    incremental_plan = (prev_plan is not None and changed is not None and same_directives
                        and (feat_in is None or feat_in["plan"] == plan_fp)
                        and not ({"all", "feature.plan"} & ctx.force))
    incremental_write = (changed is not None and same_directives and (feat_in is None or feat_in["write"] == write_fp)
                         and not ({"all", "sections"} & ctx.force))

    async def plan():
        if incremental_plan:
            return await _plan_delta(ctx, plan_system, FeaturePlan.model_validate(prev_plan), km)
        return await run_agent("plan_feature", plan_system,
                               "Knowledge model (JSON):\n" + json.dumps(kmj, ensure_ascii=False, indent=1),
                               FeaturePlan, model=ctx.model("synthesize"), max_turns=6)

    planned = FeaturePlan.model_validate(await ctx.stage("feature.plan", [kmj, plan_fingerprint_system], plan))
    ctx.write("feature.input", {"plan": plan_fp, "write": write_fp, "directives": dir_digest})
    head = {"title": ctx.profile["title"], "goal": planned.goal, "context": planned.context,
            "stakeholders": planned.stakeholders}

    async def write(sec: Section):
        refs = set(sec.source_refs)
        for i in km.items:
            if i.id in sec.items:
                refs |= set(i.source_refs)
        for r in km.rules:
            if r.id in sec.rules:
                refs |= set(r.source_refs)
        prev_sec = _previous(ctx, f"sections/{sec.id}")
        prev_obj = Section.model_validate(prev_sec) if prev_sec else None
        rel = I.relevant_ids(sec, prev_obj, km)
        rel_elements = [x.model_dump(exclude={"depends_on"}) for x in [*km.items, *km.rules, *km.open_questions] if x.id in rel]
        for x in [*km.items, *km.rules]:
            if x.id in rel:
                refs |= set(x.source_refs)
        cited = _fact_payload([facts_by_id[r] for r in sorted(refs) if r in facts_by_id])
        prev_stories = [f"{s['id']} ({s['title']})" for s in prev_sec["stories"]] if prev_sec else []
        write_system = load_prompt(AGENTS / "story_writer.md", **pc, existing_ids=_existing(prev_stories))
        prompt = ("Feature (JSON; you write the stories of ONE section of it):\n" + json.dumps(head, ensure_ascii=False, indent=1) +
                  "\n\nSection to write (JSON):\n" + sec.model_dump_json(indent=1) +
                  "\n\n" + knowledge_slice(km, rel) +
                  "\n\nCited facts (JSON):\n" + json.dumps(cited, ensure_ascii=False, indent=1) +
                  "\n\nReturn this Section with its stories written.")

        touched = I.touched_ids(sec, rel, changed, changed_behaviour) if changed is not None else None
        meta = sec.model_dump(exclude={"stories"})
        if prev_obj and incremental_write and not touched and prev_obj.model_dump(exclude={"stories"}) == meta:
            ctx.log(f"  reusing sections/{sec.id} (nothing it depends on changed)")
            return sec.model_copy(update={"stories": prev_obj.stories})

        async def go():
            if prev_obj and incremental_write:
                ctx.log(f"  updating sections/{sec.id}: {', '.join(sorted(touched)) or 'section changed'}")
                upd = (prompt + "\n\nThis section was written before. Previous version (JSON):\n" + prev_obj.model_dump_json(indent=1)
                       + "\n\n" + load_prompt(AGENTS / "section_update.md")
                       + "\n\nWhat changed in the knowledge model since then: " + (", ".join(sorted(touched)) or "the section's "
                       "own scope") + ".")
                out = await run_agent(f"write_section/{sec.id}", write_system, upd, Section,
                                      model=ctx.model("synthesize"), max_turns=6)
                new = I.keep_untouched(prev_obj, Section.model_validate(out), touched or set())
            else:
                out = await run_agent(f"write_section/{sec.id}", write_system, prompt, Section,
                                      model=ctx.model("synthesize"), max_turns=6)
                new = Section.model_validate(out)
            new = await _repair_examples(ctx, write_system, km, new)
            # store the section as planned (only the stories are the writer's), so the next run compares like with like
            return sec.model_copy(update={"stories": new.stories}).model_dump()

        # fingerprint: only what this section depends on (not the whole model), so a change elsewhere does not rewrite it
        fingerprint = [meta, rel_elements, cited, head, write_fingerprint_system]
        out = Section.model_validate(await ctx.stage(f"sections/{sec.id}", fingerprint, go))
        # ownership and metadata stay as planned; the writer only adds stories
        return sec.model_copy(update={"stories": out.stories})

    sections = list(await asyncio.gather(*[write(sec) for sec in sorted(planned.sections, key=lambda x: x.order)]))
    return Feature(id=ctx.feature_id, title=ctx.profile["title"], goal=planned.goal, context=planned.context,
                   stakeholders=planned.stakeholders, sections=sections)


def knowledge_slice(km: KnowledgeModel, rel: set[str]) -> str:
    """The part of the knowledge model a section writer needs: every element the section owns or uses (in full,
    with the formalisation its examples are checked against) and the exclusions; the rest as a one-line index."""
    used = {"items": [i.model_dump(exclude={"depends_on"}) for i in km.items if i.id in rel],
            "rules": [r.model_dump(exclude={"depends_on"}) for r in km.rules if r.id in rel],
            "open_questions": [q.model_dump() for q in km.open_questions if q.id in rel],
            "exclusions": [x.model_dump() for x in km.exclusions]}
    others = [f"- item `{i.id}`: {i.name} (asked: {i.asked_when})" for i in km.items if i.id not in rel]
    others += [f"- rule `{r.id}`: {r.name}" for r in km.rules if r.id not in rel]
    others += [f"- open question `{q.id}`: {q.question}" for q in km.open_questions if q.id not in rel]
    return ("Knowledge model, the elements this section owns or uses (JSON; *_expr/expression are the internal "
            "formalisation your examples are checked against):\n" + json.dumps(used, ensure_ascii=False, indent=1)
            + "\n\nThe other elements of the knowledge model (owned by other sections; reference them by id only "
              "where a story of this section needs them):\n" + ("\n".join(others) or "(none)"))


async def stage_flow(ctx, km: KnowledgeModel, feature: Feature) -> tuple[Flow | None, list[Finding]]:
    """The flow overview (steps over the asked items), only when the profile asks for one (`flow:`).
    On reruns the previous flow is updated, and code keeps every step whose items and rules did not change."""
    if not ctx.profile.get("flow"):
        return None, []
    pc = _profile_ctx(ctx)
    system = load_prompt(AGENTS / "flow_planner.md", **pc)
    elems = {"items": [{"id": i.id, "name": i.name, "asked_when": i.asked_when, "notes": i.notes} for i in km.items],
             "rules": [{"id": r.id, "name": r.name, "statement": r.statement} for r in km.rules],
             "stories": [{"id": s.id, "title": s.title, "items": s.items, "rules": s.rules}
                         for sec in feature.sections for s in sec.stories]}
    prev = _previous(ctx, "feature.flow")
    prev_in = _previous(ctx, "feature.flow.input")
    item_ids = {i.id for i in km.items}
    rule_ids = {r.id for r in km.rules}

    def digest(e):
        return {x["id"]: sha(x) for x in e["items"] + e["rules"]}

    async def go():
        cur = digest(elems)
        update = prev is not None and prev_in is not None and prev_in.get("system") == sha(system)
        if update:
            old = prev_in.get("elements", {})
            changed = sorted({i for i in cur.keys() | old.keys() if cur.get(i) != old.get(i)})
            prompt = ("Elements (JSON):\n" + json.dumps(elems, ensure_ascii=False, indent=1)
                      + "\n\nPrevious flow (JSON):\n" + json.dumps(prev, ensure_ascii=False, indent=1)
                      + "\n\nChanged, added or removed elements since then: " + (", ".join(changed) or "none")
                      + "\n\nReturn the updated Flow.")
        else:
            changed = None
            prompt = "Elements (JSON):\n" + json.dumps(elems, ensure_ascii=False, indent=1) + "\n\nReturn the Flow."
        if update and not changed:
            flow = Flow.model_validate(prev)
        else:
            flow = Flow.model_validate(await run_agent("flow", system, prompt, Flow, model=ctx.model("flow", "synthesize"), max_turns=4))
            missing = item_ids - {i for st in flow.steps for i in st.items}
            if missing:
                ctx.log(f"  flow: placing {len(missing)} items it left out ...")
                flow = Flow.model_validate(await run_agent(
                    "flow_repair", system, prompt + "\n\nYour flow:\n" + flow.model_dump_json(indent=1)
                    + "\n\nThese asked items are in no step: " + ", ".join(sorted(missing))
                    + ". Return the Flow with each of them in exactly one step.", Flow, model=ctx.model("flow", "synthesize"), max_turns=4))
            if update:                     # code keeps every step the changes do not touch
                before = {tuple(sorted(st["items"] + st["rules"])): st for st in prev["steps"]}
                steps = []
                for st in flow.steps:
                    old_st = before.get(tuple(sorted(st.items + st.rules)))
                    if old_st and not (set(st.items + st.rules) & set(changed)):
                        st = st.model_copy(update={k: old_st[k] for k in ("title", "asks", "shown_to")})
                    steps.append(st)
                flow = flow.model_copy(update={"steps": steps,
                                               "intro": prev["intro"] if len(steps) == len(prev["steps"]) else flow.intro})
        ctx.write("feature.flow.input", {"system": sha(system), "elements": cur})
        return flow.model_dump()

    flow = Flow.model_validate(await ctx.stage("feature.flow", [elems, system], go))
    placed = [i for st in flow.steps for i in st.items]
    F = [Finding(check="flow", severity="warning", target=f"item.{i}", message="asked item is in no step of the flow")
         for i in sorted(item_ids - set(placed))]
    F += [Finding(check="flow", severity="warning", target=f"item.{i}", message="item is in more than one step of the flow")
          for i in sorted({i for i in placed if placed.count(i) > 1})]
    F += [Finding(check="flow", severity="error", target=f"flow.{x}", message="unknown item or rule id in the flow")
          for st in flow.steps for x in st.items + st.rules if x not in item_ids | rule_ids]
    return flow, F


async def stage_trace_judge(ctx, spec: Spec, facts: list[Fact], prev_spec: Spec | None = None) -> tuple[dict, list[Finding]]:
    fb = {f.id: f for f in facts}
    guidance = ctx.guidance_items()
    dec = {d.id: d for d in D.load(ctx)}

    def cite(refs):
        return [{"id": r, "statement": fb[r].statement, "quotes": [a.quote for a in fb[r].anchors]} if r in fb
                else {"id": r, "statement": "product owner guidance: " + guidance[r]} if r in guidance
                else {"id": r, "statement": "product decision: " + (dec[r].statement or dec[r].rationale)} if r in dec
                else {"id": r, "statement": "product decision"} for r in refs]

    def elements(spec):
        items = [{"id": f"item.{i.id}", "element": i.model_dump(exclude={"source_refs", "depends_on"}), "cited": cite(i.source_refs)}
                 for i in spec.knowledge.items]
        items += [{"id": f"rule.{r.id}", "element": r.model_dump(exclude={"source_refs", "depends_on"}), "cited": cite(r.source_refs)}
                  for r in spec.knowledge.rules]
        for s in spec.stories():
            refs = sorted(set(s.source_refs) | {r for ac in s.acceptance_criteria for r in ac.source_refs})
            items.append({"id": f"story.{s.id}", "element": s.model_dump(exclude={"source_refs"}), "cited": cite(refs)})
        return items

    items = elements(spec)
    system = load_prompt(AGENTS / "requirement_judge.md")

    # Verdicts are kept per element: an element whose content and cited evidence did not change keeps its
    # previous verdict, so an unchanged story does not get a different trace note by chance.
    def key(x):
        return sha(x["element"], x["cited"], system)

    async def go():
        known = _previous(ctx, "judge_trace.cache")
        if known is None:        # bootstrap: verdicts of the previous run, for elements that did not change since
            prev_v = {v["id"]: v for v in (_previous(ctx, "judge_trace") or [])}
            known = {key(x): prev_v[x["id"]] for x in (elements(prev_spec) if prev_spec else []) if x["id"] in prev_v}
        todo = [x for x in items if key(x) not in known]
        batches = [todo[i:i + 6] for i in range(0, len(todo), 6)]
        res = await asyncio.gather(*[run_agent(f"judge_trace/batch{n}", system, json.dumps(b, ensure_ascii=False, indent=1),
                                               Verdicts, model=ctx.model("judge")) for n, b in enumerate(batches)])
        fresh = {v["id"]: v for r in res for v in r["verdicts"]}
        ctx.log(f"  trace judge: {len(todo)} elements judged, {len(items) - len(todo)} verdicts reused")
        cache = {key(x): fresh[x["id"]] for x in todo if x["id"] in fresh}
        cache |= {key(x): known[key(x)] for x in items if key(x) in known}
        ctx.write("judge_trace.cache", cache)
        return [cache[key(x)] for x in items if key(x) in cache]

    verdicts = await ctx.stage("judge_trace", [items, system], go)
    vmap = {v["id"]: v for v in verdicts}
    return vmap, [Finding(check="trace_judge", severity="warning" if v["verdict"] == "partial" else "error",
                          target=v["id"], message=f"{v['verdict']}: {v.get('note', '')}")
                  for v in verdicts if v["verdict"] != "supported"]


REFINE_SHARED = ("feature.md", "information.md", "open-questions.md", "out-of-scope.md")
REFINE_SKIP = ("traceability.md", "README.md")     # tool metadata and an index: not what an engineer refines


def requirement_files(req_dir: Path) -> dict[str, str]:
    """Rendered files (path relative to the requirements folder -> content hash): what dev refinement read."""
    return {str(p.relative_to(req_dir)): sha(p) for p in sorted(req_dir.rglob("*.md"))} if req_dir.exists() else {}


def _story_id(rel: str) -> str:
    """'stories/US-01.2-complete-home-address.md' -> 'US-01.2'."""
    return "-".join(Path(rel).stem.split("-")[:2])


async def stage_dev_refinement(ctx, req_dir: Path, spec: Spec, files_before: dict[str, str] | None = None
                               ) -> tuple[dict, list[Finding]]:
    """One engineer agent reads the rendered feature (feature.md, stories/, shared files) and reports what it would ask.
    First run (or a changed prompt, or --force): the agent reads every file with tools. Later runs: one call without
    tools that gets only the files that changed (plus feature.md and the stories sharing their items as context);
    the questions on unchanged files are kept by code."""
    system = load_prompt(AGENTS / "dev_refinement.md")
    path = req_dir / "feature.md"
    story_files = sorted((req_dir / "stories").glob("*.md"))
    files_now = requirement_files(req_dir)

    async def full():
        return await run_agent("dev_refinement", system,
                               f"Feature file: {path}\nStory files are in: {req_dir / 'stories'}\n"
                               f"Shared files are in: {req_dir}\nRead them all, then answer.",
                               RefinementReport, model=ctx.model("builder"), tools=["Read", "Glob", "Grep"],
                               add_dirs=[req_dir], max_turns=60)

    async def go():
        prev = _previous(ctx, "dev_refinement")
        rec = _previous(ctx, "dev_refinement.input")
        # files the previous refinement saw: recorded, or (first run with this code) the folder as it was before render
        base = (rec["files"] if rec.get("system") == sha(system) else None) if rec else files_before
        if prev is None or not base or {"all", "dev_refinement"} & ctx.force:
            rep = await full()
        else:
            rep = await _refine_delta(ctx, system, req_dir, spec, prev, base, files_now)
        ctx.write("dev_refinement.input", {"system": sha(system), "files": files_now})
        return rep

    rep = await ctx.stage("dev_refinement", [path, *story_files, req_dir / "information.md", req_dir / "open-questions.md", system], go)
    merged = {"questions": rep["questions"], "already_flagged": rep.get("already_flagged", []),
              "tech_leaks": rep.get("tech_leaks", [])}
    sev = {"blocker": "error", "major": "warning", "minor": "info"}
    F = [Finding(check="dev_refinement", severity=sev[q["severity"]], target=q["file"], message=q["question"])
         for q in merged["questions"]]
    F += [Finding(check="tech_leak", severity="warning", target=t["file"], message=f"\"{t['quote']}\" - {t['why']}")
          for t in merged["tech_leaks"]]
    return merged, F


def refinement_scope(spec: Spec, base: dict[str, str], now: dict[str, str]) -> tuple[list[str], list[str], list[str]]:
    """(changed files to review, removed files, unchanged files given as context) for an incremental refinement.
    Context: feature.md and the shared files, and every unchanged story that shares an item or rule with a changed one."""
    changed = sorted(f for f in now if base.get(f) != now[f] and f not in REFINE_SKIP)
    removed = sorted(f for f in base if f not in now)
    changed_ids = {_story_id(f) for f in changed if f.startswith("stories/")}
    stories = {s.id: s for s in spec.stories()}
    used = {x for i in changed_ids if i in stories for x in stories[i].items + stories[i].rules}
    related = {s.id for s in stories.values() if s.id not in changed_ids and used & set(s.items + s.rules)}
    context = [f for f in REFINE_SHARED if f in now and f not in changed]
    context += sorted(f for f in now if f.startswith("stories/") and _story_id(f) in related and f not in changed)
    return changed, removed, context


def merge_refinement(prev: dict, new: dict, reviewed: set[str]) -> dict:
    """Questions and leaks on files that were not reviewed again are kept; the agent's answer replaces the rest."""
    def norm(f: str) -> str:
        return f.split("employee-onboarding/")[-1].lstrip("./") if f else f
    keep_q = [q for q in prev.get("questions", []) if norm(q["file"]) not in reviewed]
    keep_t = [t for t in prev.get("tech_leaks", []) if norm(t["file"]) not in reviewed]
    seen, questions = set(), []
    for q in keep_q + new.get("questions", []):
        k = (norm(q["file"]), q["question"])
        if k not in seen:
            seen.add(k)
            questions.append(q)
    return {"questions": questions,
            "already_flagged": new.get("already_flagged") or prev.get("already_flagged", []),
            "tech_leaks": keep_t + new.get("tech_leaks", [])}


async def _refine_delta(ctx, system: str, req_dir: Path, spec: Spec, prev: dict, base: dict, now: dict) -> dict:
    changed, removed, context = refinement_scope(spec, base, now)
    if not changed and not removed:
        ctx.log("  dev refinement: no rendered file changed, previous questions kept")
        return prev
    reviewed = set(changed) | set(removed)
    ctx.log(f"  dev refinement (incremental): {len(changed)} changed, {len(removed)} removed, {len(context)} context files")

    def block(rel):
        return f"### {rel}\n\n{(req_dir / rel).read_text()}"

    prev_on = {"questions": [q for q in prev.get("questions", []) if q["file"] in reviewed],
               "tech_leaks": [t for t in prev.get("tech_leaks", []) if t["file"] in reviewed],
               "already_flagged": prev.get("already_flagged", [])}
    prompt = ("You refined this feature before. Since then these files changed: " + ", ".join(changed)
              + (". Removed: " + ", ".join(removed) if removed else "") + ".\n\n"
              + "## Files to review again (changed)\n\n" + "\n\n".join(block(f) for f in changed)
              + "\n\n## Context (unchanged; read them to find contradictions, but their own questions are kept as they are)\n\n"
              + "\n\n".join(block(f) for f in context)
              + "\n\n## Your previous answer for the changed and removed files (JSON)\n\n"
              + json.dumps(prev_on, ensure_ascii=False, indent=1)
              + "\n\n" + load_prompt(AGENTS / "dev_refinement_delta.md"))
    out = await run_agent("dev_refinement", system, prompt, RefinementReport, model=ctx.model("builder"), max_turns=4)
    return merge_refinement(prev, out, reviewed)


def review_followup(prev_review: dict | None, prev_report: dict | None, decisions: list) -> str:
    """The previous review's findings and the decisions taken since, so the reviewer can say which findings
    are resolved, still open or new. Empty on the first review."""
    if not prev_review or not prev_review.get("findings"):
        return ""
    known = prev_report.get("decision_ids") if prev_report else None
    new = [d for d in decisions if known is not None and d.id not in set(known)]
    L = ["", "## Follow-up to the previous review", "",
         "Below are the findings of the previous review. For each one, decide from the report above whether it "
         "still applies. If it no longer applies, list it under `resolved` with what resolved it (decision ids "
         "or what changed). If it still applies, keep it as a finding with status `still_open` (keep its title "
         "unless the problem itself changed). Every other finding has status `new`. Do not invent resolutions: "
         "a finding is resolved only when the report no longer shows the problem.", "", "Previous findings:"]
    L += [f"- {f['title']}: {f['why']} (evidence: {f['evidence']})" for f in prev_review["findings"]]
    if known is None:
        L += ["", "Decisions taken since the previous review: not recorded for that review; use the report."]
    else:
        L += ["", "Decisions taken since the previous review:"] + \
             ([f"- {d.id} ({d.action}{' ' + d.target if d.target else ''}): {d.statement}" for d in new] or ["- none"])
    return "\n".join(L)


async def stage_review(ctx, report: dict, decisions: list | None = None) -> dict:
    # read before this run overwrites them: the previous review and the report it was based on
    followup = review_followup(_previous(ctx, "review"), _previous(ctx, "report"), decisions or [])

    async def go():
        return await run_agent("review", load_prompt(AGENTS / "reviewer.md"),
                               json.dumps(report, ensure_ascii=False, indent=1, default=str) + followup, Review,
                               model=ctx.model("review"), max_turns=6)
    # the impact section says what the last run changed; on a rerun with nothing new it only flips to "nothing
    # changed", which is no reason to review again. The follow-up block is not part of the fingerprint either:
    # it changes with every review, and an unchanged report needs no new review.
    stable = {k: v for k, v in report.items() if k not in ("impact", "decision_ids")}
    stable["findings"] = {sev: [f for f in fs if f["check"] != "impact"] for sev, fs in report["findings"].items()}
    return await ctx.stage("review", [stable, AGENTS / "reviewer.md"], go)


# -------------------------------------------------------------------- main --

async def run(feature_id: str, force: set[str] | None = None, skip_llm_checks: bool = False) -> dict:
    ctx = Context(feature_id, force=force or set())
    ctx.log(f"Pipeline for feature '{feature_id}'")
    ctx.log("[1-2] normalize + extract sources")
    adapters, units, facts = await stage_sources(ctx)
    unit_by_id = {u.id: u for u in units}

    # what the previous run knew (read before this run overwrites it): for decisions and incremental reruns
    prev_facts = _previous(ctx, "facts")
    known_before = {f["id"] for f in prev_facts} if prev_facts else None
    prev_km = _previous(ctx, "knowledge.raw")
    prev_spec = _previous(ctx, "spec")
    prev_spec = Spec.model_validate(prev_spec) if prev_spec else None

    ctx.log("[3] verify facts")
    decisions = D.load(ctx)
    findings = D.validate(decisions) + D.stamp_and_check(ctx, decisions, unit_by_id)
    facts, ff = await stage_verify_facts(ctx, adapters, units, facts)
    findings += ff
    facts = D.apply_to_facts(decisions, facts)

    ctx.log("[4] knowledge model")
    km = await stage_knowledge(ctx, facts, known_before)
    ctx.log("[5] feature: sections and stories")
    feature = await stage_feature(ctx, km, facts, prev_km)
    flow, flf = await stage_flow(ctx, km, feature)
    feature = feature.model_copy(update={"flow": flow})
    findings += flf
    spec = Spec(knowledge=km, feature=feature)

    ctx.log("[6] apply decisions")
    spec, df = D.apply_to_spec(decisions, spec)
    findings += df + D.check_directives(decisions, spec) + D.new_evidence(ctx, decisions, spec, facts, known_before, prev_spec)
    M.compute_depends_on(spec.knowledge)
    ctx.write("spec", spec.model_dump())

    # impact: what this run changed compared to the previous one, and whether each change has a cause
    impact = None
    if prev_spec:
        impact = I.story_impact(prev_spec.stories(), spec.stories(), I.changed_ids(prev_spec.knowledge, spec.knowledge) or set())
        impact["guard_reverted"] = (_previous(ctx, "knowledge.guard") or {}).get("reverted", []) if "knowledge.raw" in ctx.ran else []
        findings += [Finding(check="impact", severity="warning", target=f"story.{i}",
                             message="changed although no element it uses changed") for i in impact["changed_without_cause"]]
        findings += [Finding(check="impact", severity="warning", target=n.split(":")[0], message=n.split(": ", 1)[-1])
                     for n in impact["guard_reverted"]]

    ctx.log("[7] checks")
    guidance = ctx.guidance_items()
    valid = {f.id for f in facts if f.anchor_ok and f.judge != "unsupported"} | {d.id for d in decisions} | set(guidance)
    checklist = ctx.profile.get("item_checklist", [])
    findings += M.lint(spec, valid, set(ctx.profile["stakeholders"]), checklist)
    leak_cfg = ctx.profile.get("tech_vocabulary", {})
    findings += M.tech_leaks(spec, leak_cfg.get("flag", []), leak_cfg.get("allow", []))
    cov, cf = M.coverage(units, facts, spec)
    findings += cf
    examples, ef = M.run_examples(spec)
    findings += ef
    judge = {}
    if not skip_llm_checks:
        judge, jf = await stage_trace_judge(ctx, spec, facts, prev_spec)
        findings += jf

    ctx.log("[8] render feature specs")
    req_dir = REQUIREMENTS / feature_id
    files_before = requirement_files(req_dir)        # what the previous dev refinement read (incremental refinement)
    render(req_dir, ctx, spec, facts, unit_by_id, decisions, judge, guidance, examples)

    refinement = {"questions": [], "already_flagged": [], "tech_leaks": []}
    if not skip_llm_checks:
        ctx.log("[9] dev refinement")
        refinement, rf = await stage_dev_refinement(ctx, req_dir, spec, files_before)
        findings += rf

    stories = spec.stories()
    report = {
        "feature_id": feature_id,
        "counts": {"units": len(units), "facts": len(facts), "items": len(km.items), "rules": len(km.rules),
                   "sections": len(spec.feature.sections), "stories": len(stories),
                   "acceptance_criteria": sum(len(s.acceptance_criteria) for s in stories),
                   "open_questions": len(km.open_questions), "exclusions": len(km.exclusions)},
        "findings": {sev: [f.model_dump() for f in findings if f.severity == sev] for sev in ("error", "warning", "info")},
        "coverage": cov, "examples": examples,
        "open_questions": [q.model_dump() for q in km.open_questions],
        "inferred_items": [f"item.{i.id}" for i in km.items if i.status == "inferred"] +
                          [f"rule.{r.id}" for r in km.rules if r.status == "inferred"] +
                          [f"story.{s.id}" for s in stories if s.status == "inferred"],
        "dev_refinement": refinement,
        "impact": impact,
        "skipped_sources": [s["id"] for s in ctx.profile["sources"] if not any(u.source_id == s["id"] for u in units)],
        "decision_ids": [d.id for d in decisions],     # the next review lists the decisions taken since this one
    }
    review = None
    if not skip_llm_checks:
        ctx.log("[10] review")
        review = await stage_review(ctx, report, decisions)
    report["review"] = review
    report["stages"] = {"ran": ctx.ran, "reused": ctx.reused}
    report["cost_usd_this_run"] = round(sum(c["cost_usd"] for c in COSTS), 2)
    report["usage_this_run"] = usage_summary(COSTS)
    ctx.write("report", report)
    write_review_md(ctx, report, facts)
    return report


def write_review_md(ctx: Context, r: dict, facts: list[Fact]) -> None:
    L = [f"# Review: {r['feature_id']}", ""]
    if r.get("review"):
        L += [f"**Verdict: {r['review']['verdict'].replace('_', ' ').upper()}**", "", r["review"]["summary"], "",
              "## Reviewer findings", ""]
        for i, f in enumerate(r["review"]["findings"], 1):
            tag = " (still open)" if f.get("status") == "still_open" else ""
            L += [f"{i}. **{f['title']}**{tag} – {f['why']}  ", f"   Evidence: {f['evidence']}  ", f"   Action: {f['action']}"]
        L.append("")
        if r["review"].get("resolved"):
            L += ["## Resolved since the last review", ""] + \
                 [f"- ~~{f['title']}~~ – {f['resolved_by']}" for f in r["review"]["resolved"]] + [""]
    else:
        L += ["**Verdict: not available** – the LLM checks (trace judge, dev refinement, review) did not run for this "
              "report. Run `pipeline run` for the full review.", ""]
    c = r["counts"]
    L += ["## Numbers", "", f"{c['units']} source units → {c['facts']} facts → {c['items']} information items, "
          f"{c['rules']} business rules → one feature with {c['sections']} sections, {c['stories']} stories, "
          f"{c['acceptance_criteria']} acceptance criteria; {c['open_questions']} open questions, {c['exclusions']} exclusions.", ""]
    if r["skipped_sources"]:
        L += [f"⚠ Sources without data (not explored / empty): {', '.join(r['skipped_sources'])}", ""]
    imp = r.get("impact")
    if imp:
        L += ["## Impact of this run", "",
              f"Stories added: {', '.join(imp['added']) or '-'}; changed: {', '.join(imp['changed']) or '-'}; "
              f"removed: {', '.join(imp['removed']) or '-'}; unchanged: {imp['unchanged']}.", "",
              f"Knowledge elements changed: {', '.join(imp['changed_elements']) or '-'}", ""]
        if imp["changed_without_cause"]:
            L += [f"⚠ Changed although nothing they use changed: {', '.join(imp['changed_without_cause'])}", ""]
        if imp["guard_reverted"]:
            L += ["Changes the update guard reverted (force with `--force knowledge.raw` if they are wanted):", ""] + \
                 [f"- {n}" for n in imp["guard_reverted"]] + [""]
    errs = r["findings"]["error"]
    L += [f"## Errors ({len(errs)})", ""] + [f"- [{f['check']}] `{f['target']}` {f['message']}" for f in errs] + [""]
    ex = r["examples"]
    L += [f"## Examples executed against the knowledge model ({sum(e['pass'] for e in ex)}/{len(ex)} pass)", ""]
    L += [f"- {'✅' if e['pass'] else '❌'} {e['case']} ({e['origin']})" + ("" if e["pass"] else f": {'; '.join(e['failures'])}")
          for e in ex] + [""]
    if r["open_questions"]:
        L += ["## Open questions (need your decision)", ""]
        L += [f"- **{q['id']}**{' (blocking)' if q['blocking'] else ''}: {q['question']} → recommended: {q['recommendation']}"
              for q in r["open_questions"]] + [""]
    inferred = [f for f in facts if f.basis == "inferred" and f.anchor_ok]
    L += ["## Inferred items to confirm", ""] + [f"- {i}" for i in r["inferred_items"]] + \
         [f"- fact {f.id}: {f.statement}" for f in inferred] + [""]
    dr = r["dev_refinement"]
    if r.get("review"):
        L += [f"## Dev refinement questions ({len(dr['questions'])})", ""] + \
             [f"- [{q['severity']}] `{q['file']}` {q['question']}" for q in dr["questions"]] + [""]
    leaks = [f for f in r["findings"]["warning"] if f["check"] == "tech_leak"]
    L += [f"## Technical vocabulary found in the spec ({len(leaks)})", ""] + \
         [f"- `{f['target']}` {f['message']}" for f in leaks] + [""]
    cov = r["coverage"]
    L += ["## Coverage", "", f"{cov['units_cited']}/{cov['units_total']} source units cited; "
          f"{cov['facts_used']}/{cov['facts_total']} facts used.", "", "Uncited units (confirm they are irrelevant):", ""] + \
         [f"- {u['id']}: {u['text']}" for u in cov["uncited_units"]] + [""]
    warns = [f for f in r["findings"]["warning"] if f["check"] != "tech_leak"]
    L += [f"## Other warnings ({len(warns)})", ""] + [f"- [{f['check']}] `{f['target']}` {f['message']}" for f in warns] + [""]
    L += ["## Run", "", f"Stages run: {', '.join(r['stages']['ran']) or '-'}", "",
          f"Stages reused from cache: {', '.join(r['stages']['reused']) or '-'}", "", f"LLM cost this run: ${r['cost_usd_this_run']}"]
    u = (r.get("usage_this_run") or {}).get("total")
    if u:
        L += ["", f"Tokens this run: {u['total_tokens']:,} in {u['calls']} agent calls ({u['input_tokens']:,} input, "
              f"{u['cache_read_input_tokens']:,} cache read, {u['cache_creation_input_tokens']:,} cache write, "
              f"{u['output_tokens']:,} output)"]
    (ctx.build / "review.md").write_text("\n".join(L) + "\n")
