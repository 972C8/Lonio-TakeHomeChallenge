"""Command line interface.

    python -m pipeline run [--feature employee-onboarding] [--force STAGE ...] [--fast]
    python -m pipeline explore <source_id>      # crawl an interactive source (expensive, network)
    python -m pipeline status                   # what changed since the last run
    python -m pipeline reconfirm D-002 [...]    # decisions re-confirmed after "new evidence since this decision"
    python -m pipeline publish --team KEY [--dry-run]   # optional step 8: send feature specs to Linear
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys

from .engine.context import Context

DEFAULT_FEATURE = "employee-onboarding"


def main(argv=None):
    p = argparse.ArgumentParser(prog="pipeline")
    p.add_argument("--feature", default=DEFAULT_FEATURE)
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run the pipeline (cached stages are reused)")
    r.add_argument("--force", nargs="*", default=[], help="stage names to rerun, or 'all'")
    r.add_argument("--fast", action="store_true", help="skip LLM checks (trace judge, naive builder, reviewer)")
    e = sub.add_parser("explore", help="explore an interactive source (e.g. the tax calculator)")
    e.add_argument("source_id")
    sub.add_parser("status", help="show which stages are stale")
    rc = sub.add_parser("reconfirm", help="re-stamp decisions the product owner re-confirmed after new evidence")
    rc.add_argument("ids", nargs="+")
    pub = sub.add_parser("publish", help="optional step 8: send the feature specs to Linear (Linear MCP)")
    pub.add_argument("--team", required=True, help="Linear team key or name")
    pub.add_argument("--project", help="Linear project name (default: the feature title)")
    pub.add_argument("--dry-run", action="store_true", help="read-only: report what would be created/updated")
    a = p.parse_args(argv)

    if a.cmd == "run":
        from .run import run
        rep = asyncio.run(run(a.feature, set(a.force), skip_llm_checks=a.fast))
        _summary(rep, a.feature)
    elif a.cmd == "explore":
        from .adapters.base import get_adapter
        ctx = Context(a.feature)
        src = next(s for s in ctx.profile["sources"] if s["id"] == a.source_id)
        ad = get_adapter(src, ctx)
        if not hasattr(ad, "explore"):
            sys.exit(f"source type {src['type']} has nothing to explore")
        out = asyncio.run(ad.explore())
        print(f"explored {len(out['questions'])} questions, {len(out.get('vectors', []))} vectors -> {ad.cache}")
    elif a.cmd == "status":
        from .adapters.base import get_adapter
        from .engine.context import sha
        ctx = Context(a.feature)
        for s in ctx.profile["sources"]:
            ad = get_adapter(s, ctx)
            name = f"normalize/{s['id']}"
            fp = sha(*ad.normalize_inputs())
            state = "unchanged" if ctx.manifest.get(name, {}).get("fingerprint") == fp else "CHANGED -> will rerun"
            print(f"{s['id']:<28} {state}")
    elif a.cmd == "reconfirm":
        from .engine import decisions as D
        print("re-stamped against the current facts:", ", ".join(D.reconfirm(Context(a.feature), a.ids)))
    elif a.cmd == "publish":
        from .publish.linear import publish
        print(json.dumps(asyncio.run(publish(a.feature, a.team, a.project, a.dry_run)), indent=2, ensure_ascii=False))


def _summary(rep, feature_id):
    c = rep["counts"]
    errs, warns = len(rep["findings"]["error"]), len(rep["findings"]["warning"])
    ex = rep["examples"]
    print()
    print(f"{c['facts']} facts -> {c['items']} information items, {c['rules']} rules -> 1 feature with {c['sections']} sections, "
          f"{c['stories']} stories, {c['acceptance_criteria']} acceptance criteria; {c['open_questions']} open questions")
    print(f"errors {errs}, warnings {warns}, examples {sum(e['pass'] for e in ex)}/{len(ex)} pass, "
          f"dev refinement questions {len(rep['dev_refinement']['questions'])}, "
          f"tech leaks {len(rep['dev_refinement']['tech_leaks'])}")
    if rep.get("review"):
        print(f"verdict: {rep['review']['verdict']}")
    print(f"cost this run: ${rep['cost_usd_this_run']}")
    print(f"review: build/{feature_id}/review.md   requirements: requirements/{feature_id}/")


if __name__ == "__main__":
    main()
