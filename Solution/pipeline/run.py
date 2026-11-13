"""The pipeline: stages, in order.

    1 normalize   per source, adapter      -> build/<p>/normalize/<src>.json   (Units)
    2 extract     per source, LLM agent    -> build/<p>/extract/<src>.json     (Facts)
    3 verify      anchors (code) + fact judge (LLM)  -> build/<p>/facts.json
    4 synthesize  LLM agent                -> build/<p>/spec.raw.json
    5 decide      decisions.yaml (code)    -> build/<p>/spec.json
    6 check       lint, coverage, personas, eval (code); trace judge (LLM)
    7 render      templates (code)         -> requirements/<p>/
    8 builder     naive builder agent reads requirements/ -> questions
    9 review      reviewer agent           -> build/<p>/review.md (verdict)

Every LLM stage is cached by a fingerprint of its inputs; unchanged inputs are
not recomputed. `--force <stage>` reruns a stage regardless.
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
from .engine.schemas import Fact, Finding, Spec, Unit
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


class BuilderQuestion(BaseModel):
    file: str
    question: str
    severity: Literal["blocker", "major", "minor"]


class BuilderReport(BaseModel):
    questions: list[BuilderQuestion]
    already_flagged: list[str] = F(default_factory=list)


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


async def stage_synthesize(ctx, facts: list[Fact]) -> Spec:
    usable = [f for f in facts if f.anchor_ok and f.judge != "unsupported"]
    sources = "\n".join(f"- `{s['id']}` ({s['type']}, precedence {s.get('precedence', 9)}): {s.get('authority', '')}"
                        for s in ctx.profile["sources"])
    consumers = "\n".join(f"- `{k}`: {v}" for k, v in ctx.profile["consumers"].items())
    prev = ctx.out("spec")
    existing = []
    if prev.exists():
        sp = json.loads(prev.read_text())
        existing = [f["id"] for f in sp["fields"]] + [r["id"] for r in sp.get("rules", [])]
    system = load_prompt(AGENTS / "synthesizer.md", goal=ctx.profile["goal"], consumers=consumers, sources=sources,
                         guidance=(ctx.problem_dir / "guidance.md").read_text(),
                         conventions=COND_LANG.read_text(), existing_ids=", ".join(existing) or "(none yet)")
    payload = [{"id": f.id, "source": f.source_id, "kind": f.kind, "subject": f.subject, "statement": f.statement,
                "basis": f.basis, "temporality": f.temporality, "superseded_by": f.superseded_by,
                "quotes": [a.quote for a in f.anchors]} for f in usable]

    async def go():
        return await run_agent("synthesize", system,
                               "Facts (JSON):\n" + json.dumps(payload, ensure_ascii=False, indent=1) +
                               "\n\nProduce the complete Spec.", Spec, model=ctx.model("synthesize"), max_turns=8)

    raw = await ctx.stage("spec.raw", [payload, system], go)
    return Spec.model_validate(raw)


async def stage_trace_judge(ctx, spec: Spec, facts: list[Fact]) -> tuple[dict, list[Finding]]:
    fb = {f.id: f for f in facts}
    guidance = ctx.guidance_items()
    items = []
    for kind, coll in (("field", spec.fields), ("rule", spec.rules), ("exclusion", spec.exclusions)):
        for it in coll:
            items.append({"id": f"{kind}.{it.id}",
                          "requirement": it.model_dump(exclude={"source_refs", "depends_on"}, exclude_none=True),
                          "cited": [{"id": r, "statement": fb[r].statement, "quotes": [a.quote for a in fb[r].anchors]}
                                    if r in fb else {"id": r, "statement": "product owner guidance: " + guidance[r]}
                                    if r in guidance else {"id": r, "statement": "product decision"}
                                    for r in it.source_refs]})
    system = load_prompt(AGENTS / "requirement_judge.md")

    async def go():
        batches = [items[i:i + 8] for i in range(0, len(items), 8)]
        res = await asyncio.gather(*[run_agent(f"judge_trace/batch{n}", system,
                                               json.dumps(b, ensure_ascii=False, indent=1), Verdicts,
                                               model=ctx.model("judge")) for n, b in enumerate(batches)])
        return [v for r in res for v in r["verdicts"]]

    verdicts = await ctx.stage("judge_trace", [items, AGENTS / "requirement_judge.md"], go)
    vmap = {v["id"]: v for v in verdicts}
    findings = [Finding(check="trace_judge", severity="warning" if v["verdict"] == "partial" else "error",
                        target=v["id"], message=f"{v['verdict']}: {v.get('note', '')}")
                for v in verdicts if v["verdict"] != "supported"]
    return vmap, findings


async def stage_builder(ctx, req_dir: Path) -> tuple[dict, list[Finding]]:
    async def go():
        return await run_agent("naive_builder", load_prompt(AGENTS / "naive_builder.md"),
                               f"The requirements folder is: {req_dir}\nRead every file in it, then answer.",
                               BuilderReport, model=ctx.model("builder"), tools=["Read", "Glob", "Grep"],
                               add_dirs=[req_dir], max_turns=60)

    rep = await ctx.stage("naive_builder", [req_dir, AGENTS / "naive_builder.md"], go)
    sev = {"blocker": "error", "major": "warning", "minor": "info"}
    return rep, [Finding(check="naive_builder", severity=sev[q["severity"]], target=q["file"], message=q["question"])
                 for q in rep["questions"]]


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

    ctx.log("[4] synthesize")
    spec = await stage_synthesize(ctx, facts)

    ctx.log("[5] apply decisions")
    spec, df = D.apply_to_spec(decisions, spec)
    findings += df
    M.compute_depends_on(spec)
    ctx.write("spec", spec.model_dump())

    ctx.log("[6] checks")
    valid_facts = {f.id for f in facts if f.anchor_ok and f.judge != "unsupported"}
    guidance = ctx.guidance_items()
    findings += M.lint(spec, valid_facts, {d.id for d in decisions} | set(guidance), set(ctx.profile["consumers"]))
    cov, cf = M.coverage(units, facts, spec, {d.id for d in decisions})
    findings += cf
    personas = yaml.safe_load((ctx.problem_dir / "personas.yaml").read_text())["personas"] \
        if (ctx.problem_dir / "personas.yaml").exists() else []
    presults, pf = M.persona_tests(spec, personas)
    findings += pf
    gold_path = ctx.problem_dir / "gold.yaml"
    metrics, ef = M.evaluate_gold(spec, yaml.safe_load(gold_path.read_text())) if gold_path.exists() else ({}, [])
    findings += ef
    judge = {}
    if not skip_llm_checks:
        judge, jf = await stage_trace_judge(ctx, spec, facts)
        findings += jf

    ctx.log("[7] render requirements")
    req_dir = REQUIREMENTS / problem
    render(req_dir, ctx, spec, facts, unit_by_id, decisions, judge, guidance)

    builder = {"questions": [], "already_flagged": []}
    if not skip_llm_checks:
        ctx.log("[8] naive builder")
        builder, bf = await stage_builder(ctx, req_dir)
        findings += bf

    report = {
        "problem": problem,
        "counts": {"units": len(units), "facts": len(facts), "steps": len(spec.steps), "fields": len(spec.fields),
                   "rules": len(spec.rules), "notices": len(spec.notices),
                   "open_questions": len(spec.open_questions), "exclusions": len(spec.exclusions)},
        "findings": {sev: [f.model_dump() for f in findings if f.severity == sev] for sev in ("error", "warning", "info")},
        "coverage": cov, "personas": presults, "eval": metrics,
        "open_questions": [q.model_dump() for q in spec.open_questions],
        "inferred_items": [f"field.{f.id}" for f in spec.fields if f.status == "inferred"] +
                          [f"rule.{r.id}" for r in spec.rules if r.status == "inferred"],
        "naive_builder": builder,
        "skipped_sources": [s["id"] for s in ctx.profile["sources"] if not any(u.source_id == s["id"] for u in units)],
    }
    review = None
    if not skip_llm_checks:
        ctx.log("[9] review")
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
        L += [f"**Verdict: {r['review']['verdict'].replace('_', ' ').upper()}**", "", r["review"]["summary"], ""]
        L += ["## Reviewer findings", ""]
        for i, f in enumerate(r["review"]["findings"], 1):
            L += [f"{i}. **{f['title']}** – {f['why']}  ", f"   Evidence: {f['evidence']}  ", f"   Action: {f['action']}"]
        L.append("")
    c = r["counts"]
    L += ["## Numbers", "", f"{c['units']} source units → {c['facts']} facts → {c['fields']} fields, {c['rules']} rules, "
          f"{c['notices']} notices in {c['steps']} steps; {c['open_questions']} open questions, {c['exclusions']} exclusions.", ""]
    if r["skipped_sources"]:
        L += [f"⚠ Sources without data (not explored / empty): {', '.join(r['skipped_sources'])}", ""]
    errs = r["findings"]["error"]
    L += [f"## Errors ({len(errs)})", ""] + [f"- [{f['check']}] `{f['target']}` {f['message']}" for f in errs] + [""]
    pr = r["personas"]
    L += [f"## Persona tests ({sum(p['pass'] for p in pr)}/{len(pr)} pass)", ""]
    for p in pr:
        L.append(f"- {'✅' if p['pass'] else '❌'} **{p['id']}** – {p['from']}" + ("" if p["pass"] else f": {'; '.join(p['failures'])}"))
    L.append("")
    if r["open_questions"]:
        L += ["## Open questions (need your decision)", ""]
        for q in r["open_questions"]:
            L.append(f"- **{q['id']}**{' (blocking)' if q['blocking'] else ''}: {q['question']} → recommended: {q['recommendation']}")
        L.append("")
    inferred = [f for f in facts if f.basis == "inferred" and f.anchor_ok]
    L += [f"## Inferred items to confirm", ""] + [f"- {i}" for i in r["inferred_items"]] + \
         [f"- fact {f.id}: {f.statement}" for f in inferred] + [""]
    nb = r["naive_builder"]["questions"]
    L += [f"## Naive builder questions ({len(nb)})", ""] + \
         [f"- [{q['severity']}] `{q['file']}` {q['question']}" for q in nb] + [""]
    if r["eval"]:
        L += ["## Eval against gold set", "", "```", yaml.safe_dump(r["eval"], sort_keys=False).strip(), "```", ""]
    cov = r["coverage"]
    L += [f"## Coverage", "", f"{cov['units_covered']}/{cov['units_total']} source units cited; "
          f"{cov['facts_used']}/{cov['facts_total']} facts used.", "",
          "Uncovered units (confirm they are irrelevant):", ""] + \
         [f"- {u['id']}: {u['text']}" for u in cov["uncovered_units"]] + [""]
    warns = r["findings"]["warning"]
    L += [f"## Warnings ({len(warns)})", ""] + [f"- [{f['check']}] `{f['target']}` {f['message']}" for f in warns] + [""]
    L += ["## Run", "", f"Stages run: {', '.join(r['stages']['ran']) or '-'}", "",
          f"Stages reused from cache: {', '.join(r['stages']['reused']) or '-'}", "",
          f"LLM cost this run: ${r['cost_usd_this_run']}"]
    (ctx.build / "review.md").write_text("\n".join(L) + "\n")
