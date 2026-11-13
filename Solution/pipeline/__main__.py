"""Command line interface.

    python -m pipeline run [--problem employee-onboarding] [--force STAGE ...] [--fast]
    python -m pipeline explore <source_id>      # crawl an interactive source (expensive, network)
    python -m pipeline status                   # what changed since the last run
    python -m pipeline publish --dry-run        # Linear sync plan, nothing is sent
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys

from .engine.context import Context

DEFAULT_PROBLEM = "employee-onboarding"


def main(argv=None):
    p = argparse.ArgumentParser(prog="pipeline")
    p.add_argument("--problem", default=DEFAULT_PROBLEM)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run the pipeline (cached stages are reused)")
    r.add_argument("--force", nargs="*", default=[], help="stage names to rerun, or 'all'")
    r.add_argument("--fast", action="store_true", help="skip LLM checks (trace judge, naive builder, reviewer)")
    e = sub.add_parser("explore", help="explore an interactive source (e.g. the tax calculator)")
    e.add_argument("source_id")
    sub.add_parser("status", help="show which stages are stale")
    pub = sub.add_parser("publish", help="publish to Linear")
    pub.add_argument("--dry-run", action="store_true", required=True,
                     help="only dry runs are supported in this version")
    a = p.parse_args(argv)

    if a.cmd == "run":
        from .run import run
        rep = asyncio.run(run(a.problem, set(a.force), skip_llm_checks=a.fast))
        _summary(rep, a.problem)
    elif a.cmd == "explore":
        from .adapters.base import get_adapter
        ctx = Context(a.problem)
        src = next(s for s in ctx.profile["sources"] if s["id"] == a.source_id)
        ad = get_adapter(src, ctx)
        if not hasattr(ad, "explore"):
            sys.exit(f"source type {src['type']} has nothing to explore")
        out = asyncio.run(ad.explore())
        print(f"explored {len(out['questions'])} questions, {len(out.get('vectors', []))} vectors -> {ad.cache}")
    elif a.cmd == "status":
        from .adapters.base import get_adapter
        from .engine.context import sha
        ctx = Context(a.problem)
        for s in ctx.profile["sources"]:
            ad = get_adapter(s, ctx)
            name = f"normalize/{s['id']}"
            fp = sha(*ad.normalize_inputs())
            state = "unchanged" if ctx.manifest.get(name, {}).get("fingerprint") == fp else "CHANGED -> will rerun"
            print(f"{s['id']:<28} {state}")
    elif a.cmd == "publish":
        from .publish.linear_plan import plan
        print(plan(a.problem))


def _summary(rep, problem):
    c = rep["counts"]
    errs, warns = len(rep["findings"]["error"]), len(rep["findings"]["warning"])
    pp = sum(p["pass"] for p in rep["personas"])
    print()
    print(f"{c['facts']} facts -> {c['fields']} fields, {c['rules']} rules, {c['open_questions']} open questions")
    print(f"errors {errs}, warnings {warns}, personas {pp}/{len(rep['personas'])}, "
          f"builder questions {len(rep['naive_builder']['questions'])}")
    if rep.get("review"):
        print(f"verdict: {rep['review']['verdict']}")
    print(f"cost this run: ${rep['cost_usd_this_run']}")
    print(f"review: build/{problem}/review.md   requirements: requirements/{problem}/")


if __name__ == "__main__":
    main()
