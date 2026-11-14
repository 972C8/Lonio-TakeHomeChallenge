"""The pipeline: stages, in order.

     1 normalize    per source, adapter          -> build/<p>/normalize/<src>.json  (Units)
     2 extract      per source, agent            -> build/<p>/extract/<src>.json    (Facts)
     3 verify       anchors (code) + fact judge  -> build/<p>/facts.json
     4 knowledge    agent                        -> build/<p>/knowledge.raw.json    (items, rules, open questions)
     5 features     planner agent, then one writer agent per feature (parallel)
                                                 -> build/<p>/features.plan.json, features/<id>.json
     6 decide       decisions.yaml (code)        -> build/<p>/spec.json
     7 check        checklist lint, examples executed against the knowledge model,
                    coverage, tech-leak scan, gold eval (code); trace judge (agent)
     8 render       templates (code)             -> requirements/<p>/
     9 refinement   one dev-refinement agent per feature reads the rendered spec
    10 review       reviewer agent               -> build/<p>/review.md (verdict)

Every LLM stage is cached by a fingerprint of its inputs. `--force <stage>`
reruns a stage regardless.
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

import yaml
from pydantic import BaseModel, Field as F
from typing import Literal

from .adapters.base import get_adapter
from .checks import mechanical as M
from .engine import decisions as D
from .engine.context import Context, sha
from .engine.llm import COSTS, load_prompt, run_agent
from .engine.paths import PIPELINE, REQUIREMENTS
from .engine.schemas import Fact, Feature, FeaturePlan, Finding, KnowledgeModel, Spec, Unit
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


class Review(BaseModel):
    verdict: Literal["ready", "ready_with_caveats", "not_ready"]
    summary: str
    findings: list[ReviewFinding]


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

    async def judge_all():
        batches = [facts[i:i + 15] for i in range(0, len(facts), 15)]
        system = load_prompt(AGENTS / "fact_judge.md")

        async def judge(batch, n):
            items = []
            for f in batch:
                ctx_units = set()
                for a in f.anchors:
                    if a.unit_id in unit_by_id:
                        i = order.index(a.unit_id)
                        ctx_units |= {order[j] for j in range(max(0, i - 1), min(len(order), i + 2))}
                items.append({"id": f.id, "statement": f.statement, "basis": f.basis, "kind": f.kind,
                              "units": {u: {"text": unit_by_id[u].text, "meta": unit_by_id[u].meta}
                                        for u in sorted(ctx_units)}})
            out = await run_agent(f"judge_facts/batch{n}", system, json.dumps(items, ensure_ascii=False, indent=1),
                                  Verdicts, model=ctx.model("judge"))
            return out["verdicts"]

        res = await asyncio.gather(*[judge(b, n) for n, b in enumerate(batches)])
        return [v for r in res for v in r]

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


def _profile_ctx(ctx: Context) -> dict:
    p = ctx.profile
    return dict(
        goal=p["goal"],
        stakeholders="\n".join(f"- `{k}`: {v}" for k, v in p["stakeholders"].items()),
        sources="\n".join(f"- `{s['id']}` ({s['type']}, precedence {s.get('precedence', 9)}): {s.get('authority', '')}"
                          for s in p["sources"]),
        guidance=(ctx.problem_dir / "guidance.md").read_text(),
        conventions=COND_LANG.read_text(),
    )


def _fact_payload(facts: list[Fact]) -> list[dict]:
    return [{"id": f.id, "source": f.source_id, "kind": f.kind, "subject": f.subject, "statement": f.statement,
             "basis": f.basis, "temporality": f.temporality, "superseded_by": f.superseded_by,
             "quotes": [a.quote for a in f.anchors]} for f in facts]


async def stage_knowledge(ctx, facts: list[Fact]) -> KnowledgeModel:
    usable = [f for f in facts if f.anchor_ok and f.judge != "unsupported"]
    prev = ctx.out("knowledge")
    existing = []
    if prev.exists():
        km = json.loads(prev.read_text())
        existing = [i["id"] for i in km["items"]] + [r["id"] for r in km.get("rules", [])]
    system = load_prompt(AGENTS / "knowledge_modeler.md", **_profile_ctx(ctx), existing_ids=", ".join(existing) or "(none yet)")
    payload = _fact_payload(usable)

    async def go():
        return await run_agent("knowledge", system, "Facts (JSON):\n" + json.dumps(payload, ensure_ascii=False, indent=1)
                               + "\n\nProduce the complete KnowledgeModel.", KnowledgeModel,
                               model=ctx.model("synthesize"), max_turns=8)

    return KnowledgeModel.model_validate(await ctx.stage("knowledge.raw", [payload, system], go))


async def stage_features(ctx, km: KnowledgeModel, facts: list[Fact]) -> list[Feature]:
    pc = _profile_ctx(ctx)
    constraints = ctx.profile.get("feature_constraints", "")
    plan_system = load_prompt(AGENTS / "feature_planner.md", **pc,
                              plan_constraints=f"# Constraints from the problem profile\n{constraints}" if constraints else "")
    kmj = km.model_dump(exclude={"items": {"__all__": {"asked_when_expr", "required_when_expr", "depends_on"}},
                                 "rules": {"__all__": {"expression", "depends_on"}}})
    facts_by_id = {f.id: f for f in facts}

    async def plan():
        return await run_agent("plan_features", plan_system,
                               "Knowledge model (JSON):\n" + json.dumps(kmj, ensure_ascii=False, indent=1),
                               FeaturePlan, model=ctx.model("synthesize"), max_turns=6)

    planned = FeaturePlan.model_validate(await ctx.stage("features.plan", [kmj, plan_system], plan)).features
    write_system = load_prompt(AGENTS / "feature_writer.md", **pc)
    full_km = km.model_dump(exclude={"items": {"__all__": {"depends_on"}}, "rules": {"__all__": {"depends_on"}}})

    async def write(feat: Feature):
        refs = set(feat.source_refs)
        for i in km.items:
            if i.id in feat.items:
                refs |= set(i.source_refs)
        for r in km.rules:
            if r.id in feat.rules:
                refs |= set(r.source_refs)
        cited = _fact_payload([facts_by_id[r] for r in sorted(refs) if r in facts_by_id])
        prompt = ("Feature to write (JSON):\n" + feat.model_dump_json(indent=1) +
                  "\n\nFull knowledge model (JSON; *_expr/expression are the internal formalisation your examples are "
                  "checked against):\n" + json.dumps(full_km, ensure_ascii=False, indent=1) +
                  "\n\nCited facts (JSON):\n" + json.dumps(cited, ensure_ascii=False, indent=1) +
                  "\n\nReturn this Feature with its stories written.")

        async def go():
            return await run_agent(f"write_feature/{feat.id}", write_system, prompt, Feature,
                                   model=ctx.model("synthesize"), max_turns=6)

        out = Feature.model_validate(await ctx.stage(f"features/{feat.id}", [prompt, write_system], go))
        # ownership and metadata stay as planned; the writer only adds stories
        return feat.model_copy(update={"stories": out.stories})

    return list(await asyncio.gather(*[write(f) for f in sorted(planned, key=lambda f: f.order)]))


async def stage_trace_judge(ctx, spec: Spec, facts: list[Fact]) -> tuple[dict, list[Finding]]:
    fb = {f.id: f for f in facts}
    guidance = ctx.guidance_items()

    def cite(refs):
        return [{"id": r, "statement": fb[r].statement, "quotes": [a.quote for a in fb[r].anchors]} if r in fb
                else {"id": r, "statement": "product owner guidance: " + guidance[r]} if r in guidance
                else {"id": r, "statement": "product decision"} for r in refs]

    items = [{"id": f"item.{i.id}", "element": i.model_dump(exclude={"source_refs", "depends_on"}), "cited": cite(i.source_refs)}
             for i in spec.knowledge.items]
    items += [{"id": f"rule.{r.id}", "element": r.model_dump(exclude={"source_refs", "depends_on"}), "cited": cite(r.source_refs)}
              for r in spec.knowledge.rules]
    for f in spec.features:
        for s in f.stories:
            refs = sorted(set(s.source_refs) | {r for ac in s.acceptance_criteria for r in ac.source_refs})
            items.append({"id": f"story.{s.id}", "element": s.model_dump(exclude={"source_refs"}), "cited": cite(refs)})
    system = load_prompt(AGENTS / "requirement_judge.md")

    async def go():
        batches = [items[i:i + 6] for i in range(0, len(items), 6)]
        res = await asyncio.gather(*[run_agent(f"judge_trace/batch{n}", system, json.dumps(b, ensure_ascii=False, indent=1),
                                               Verdicts, model=ctx.model("judge")) for n, b in enumerate(batches)])
        return [v for r in res for v in r["verdicts"]]

    verdicts = await ctx.stage("judge_trace", [items, system], go)
    vmap = {v["id"]: v for v in verdicts}
    return vmap, [Finding(check="trace_judge", severity="warning" if v["verdict"] == "partial" else "error",
                          target=v["id"], message=f"{v['verdict']}: {v.get('note', '')}")
                  for v in verdicts if v["verdict"] != "supported"]


async def stage_dev_refinement(ctx, req_dir: Path, spec: Spec) -> tuple[dict, list[Finding]]:
    system = load_prompt(AGENTS / "dev_refinement.md")

    async def one(f: Feature):
        path = next((p for p in (req_dir / "features").glob(f"{f.id}*.md")), req_dir / "features")

        async def go():
            return await run_agent(f"dev_refinement/{f.id}", system,
                                   f"Feature file: {path}\nShared files are in: {req_dir}\nRead them, then answer.",
                                   RefinementReport, model=ctx.model("builder"), tools=["Read", "Glob", "Grep"],
                                   add_dirs=[req_dir], max_turns=40)
        return await ctx.stage(f"dev_refinement/{f.id}", [path, req_dir / "information.md", system], go)

    reps = await asyncio.gather(*[one(f) for f in spec.features])
    merged = {"questions": [q for r in reps for q in r["questions"]],
              "already_flagged": [q for r in reps for q in r.get("already_flagged", [])],
              "tech_leaks": [t for r in reps for t in r.get("tech_leaks", [])]}
    sev = {"blocker": "error", "major": "warning", "minor": "info"}
    F = [Finding(check="dev_refinement", severity=sev[q["severity"]], target=q["file"], message=q["question"])
         for q in merged["questions"]]
    F += [Finding(check="tech_leak", severity="warning", target=t["file"], message=f"\"{t['quote']}\" - {t['why']}")
          for t in merged["tech_leaks"]]
    return merged, F


async def stage_review(ctx, report: dict) -> dict:
    async def go():
        return await run_agent("review", load_prompt(AGENTS / "reviewer.md"),
                               json.dumps(report, ensure_ascii=False, indent=1, default=str), Review,
                               model=ctx.model("review"), max_turns=6)
    return await ctx.stage("review", [report, AGENTS / "reviewer.md"], go)


# -------------------------------------------------------------------- main --

async def run(problem: str, force: set[str] | None = None, skip_llm_checks: bool = False) -> dict:
    ctx = Context(problem, force=force or set())
    ctx.log(f"Pipeline for problem '{problem}'")
    ctx.log("[1-2] normalize + extract sources")
    adapters, units, facts = await stage_sources(ctx)
    unit_by_id = {u.id: u for u in units}

    ctx.log("[3] verify facts")
    decisions = D.load(ctx)
    findings = D.stamp_and_check(ctx, decisions, unit_by_id)
    facts, ff = await stage_verify_facts(ctx, adapters, units, facts)
    findings += ff
    facts = D.apply_to_facts(decisions, facts)

    ctx.log("[4] knowledge model")
    km = await stage_knowledge(ctx, facts)
    ctx.log("[5] features and stories")
    features = await stage_features(ctx, km, facts)
    spec = Spec(knowledge=km, features=features)

    ctx.log("[6] apply decisions")
    spec, df = D.apply_to_spec(decisions, spec)
    findings += df
    M.compute_depends_on(spec.knowledge)
    ctx.write("spec", spec.model_dump())

    ctx.log("[7] checks")
    guidance = ctx.guidance_items()
    valid = {f.id for f in facts if f.anchor_ok and f.judge != "unsupported"} | {d.id for d in decisions} | set(guidance)
    checklist = ctx.profile.get("item_checklist", [])
    findings += M.lint(spec, valid, set(ctx.profile["stakeholders"]), checklist)
    leak_cfg = ctx.profile.get("tech_vocabulary", {})
    findings += M.tech_leaks(spec, leak_cfg.get("flag", []), leak_cfg.get("allow", []))
    cov, cf = M.coverage(units, facts, spec)
    findings += cf
    ex_path = ctx.problem_dir / "examples.yaml"
    profile_examples = (yaml.safe_load(ex_path.read_text()) or {}).get("examples", []) if ex_path.exists() else []
    examples, ef = M.run_examples(spec, profile_examples)
    findings += ef
    gold_path = ctx.problem_dir / "gold.yaml"
    metrics, gf = M.evaluate_gold(spec, yaml.safe_load(gold_path.read_text())) if gold_path.exists() else ({}, [])
    findings += gf
    judge = {}
    if not skip_llm_checks:
        judge, jf = await stage_trace_judge(ctx, spec, facts)
        findings += jf

    ctx.log("[8] render feature specs")
    req_dir = REQUIREMENTS / problem
    render(req_dir, ctx, spec, facts, unit_by_id, decisions, judge, guidance, examples)

    refinement = {"questions": [], "already_flagged": [], "tech_leaks": []}
    if not skip_llm_checks:
        ctx.log("[9] dev refinement")
        refinement, rf = await stage_dev_refinement(ctx, req_dir, spec)
        findings += rf

    stories = [s for f in spec.features for s in f.stories]
    report = {
        "problem": problem,
        "counts": {"units": len(units), "facts": len(facts), "items": len(km.items), "rules": len(km.rules),
                   "features": len(spec.features), "stories": len(stories),
                   "acceptance_criteria": sum(len(s.acceptance_criteria) for s in stories),
                   "open_questions": len(km.open_questions), "exclusions": len(km.exclusions)},
        "findings": {sev: [f.model_dump() for f in findings if f.severity == sev] for sev in ("error", "warning", "info")},
        "coverage": cov, "examples": examples, "eval": metrics,
        "open_questions": [q.model_dump() for q in km.open_questions],
        "inferred_items": [f"item.{i.id}" for i in km.items if i.status == "inferred"] +
                          [f"rule.{r.id}" for r in km.rules if r.status == "inferred"] +
                          [f"story.{s.id}" for s in stories if s.status == "inferred"],
        "dev_refinement": refinement,
        "skipped_sources": [s["id"] for s in ctx.profile["sources"] if not any(u.source_id == s["id"] for u in units)],
    }
    review = None
    if not skip_llm_checks:
        ctx.log("[10] review")
        review = await stage_review(ctx, report)
    report["review"] = review
    report["stages"] = {"ran": ctx.ran, "reused": ctx.reused}
    report["cost_usd_this_run"] = round(sum(c["cost_usd"] for c in COSTS), 2)
    ctx.write("report", report)
    write_review_md(ctx, report, facts)
    return report


def write_review_md(ctx: Context, r: dict, facts: list[Fact]) -> None:
    L = [f"# Review: {r['problem']}", ""]
    if r.get("review"):
        L += [f"**Verdict: {r['review']['verdict'].replace('_', ' ').upper()}**", "", r["review"]["summary"], "",
              "## Reviewer findings", ""]
        for i, f in enumerate(r["review"]["findings"], 1):
            L += [f"{i}. **{f['title']}** – {f['why']}  ", f"   Evidence: {f['evidence']}  ", f"   Action: {f['action']}"]
        L.append("")
    c = r["counts"]
    L += ["## Numbers", "", f"{c['units']} source units → {c['facts']} facts → {c['items']} information items, "
          f"{c['rules']} business rules → {c['features']} features, {c['stories']} stories, "
          f"{c['acceptance_criteria']} acceptance criteria; {c['open_questions']} open questions, {c['exclusions']} exclusions.", ""]
    if r["skipped_sources"]:
        L += [f"⚠ Sources without data (not explored / empty): {', '.join(r['skipped_sources'])}", ""]
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
    L += [f"## Dev refinement questions ({len(dr['questions'])})", ""] + \
         [f"- [{q['severity']}] `{q['file']}` {q['question']}" for q in dr["questions"]] + [""]
    leaks = [f for f in r["findings"]["warning"] if f["check"] == "tech_leak"]
    L += [f"## Technical decisions leaking into the spec ({len(leaks)})", ""] + \
         [f"- `{f['target']}` {f['message']}" for f in leaks] + [""]
    if r["eval"]:
        L += ["## Eval against gold set", "", "```", yaml.safe_dump(r["eval"], sort_keys=False).strip(), "```", ""]
    cov = r["coverage"]
    L += ["## Coverage", "", f"{cov['units_cited']}/{cov['units_total']} source units cited; "
          f"{cov['facts_used']}/{cov['facts_total']} facts used.", "", "Uncited units (confirm they are irrelevant):", ""] + \
         [f"- {u['id']}: {u['text']}" for u in cov["uncited_units"]] + [""]
    warns = [f for f in r["findings"]["warning"] if f["check"] != "tech_leak"]
    L += [f"## Other warnings ({len(warns)})", ""] + [f"- [{f['check']}] `{f['target']}` {f['message']}" for f in warns] + [""]
    L += ["## Run", "", f"Stages run: {', '.join(r['stages']['ran']) or '-'}", "",
          f"Stages reused from cache: {', '.join(r['stages']['reused']) or '-'}", "", f"LLM cost this run: ${r['cost_usd_this_run']}"]
    (ctx.build / "review.md").write_text("\n".join(L) + "\n")
