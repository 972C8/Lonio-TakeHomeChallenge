"""Linear publish stage - DRY RUN.

Computes what a sync of requirements/<problem>/ to Linear would do, without
touching Linear. Git stays the source of truth; Linear is a projection.

Mapping
- problem profile  -> Linear project
- step             -> project milestone
- field / rule     -> issue  (title "[<id>] <label>", body = rendered Markdown)
- open question    -> issue labelled `needs-decision`
Idempotency: build/<problem>/linear_map.json maps requirement id -> issue id +
content hash. Unchanged hash -> no-op; changed -> update + comment with diff
reason; removed -> cancel (never delete).

A real run would hand this plan to a small publisher agent with the Linear MCP
server (https://mcp.linear.app) and read the issues back to verify.
"""
from __future__ import annotations

import hashlib
import json

from ..engine.context import Context
from ..engine.paths import REQUIREMENTS


def plan(problem: str) -> str:
    ctx = Context(problem)
    spec = ctx.read("spec")
    req = REQUIREMENTS / problem
    map_path = ctx.build / "linear_map.json"
    current = json.loads(map_path.read_text()) if map_path.exists() else {}

    items = {}
    steps = {s["id"]: s["title"] for s in spec["steps"]}
    for f in spec["fields"]:
        body = (req / "fields" / f"{f['id']}.md").read_text()
        items[f"field.{f['id']}"] = {"title": f"[{f['id']}] {f['label']}", "milestone": steps.get(f["step"]),
                                     "labels": ["requirement", f["status"], *[c["party"] for c in f["consumers"]]],
                                     "hash": hashlib.sha256(body.encode()).hexdigest()[:12]}
    for r in spec["rules"]:
        body = (req / "rules" / f"{r['id']}.md").read_text()
        items[f"rule.{r['id']}"] = {"title": f"[{r['id']}] Derived rule", "milestone": None,
                                    "labels": ["requirement", "derived-rule", r["status"]],
                                    "hash": hashlib.sha256(body.encode()).hexdigest()[:12]}
    for q in spec["open_questions"]:
        items[f"open.{q['id']}"] = {"title": f"[{q['id']}] Decision needed: {q['question']}", "milestone": None,
                                    "labels": ["needs-decision"] + (["blocking"] if q["blocking"] else []),
                                    "assignee": "product owner",
                                    "hash": hashlib.sha256(json.dumps(q, sort_keys=True).encode()).hexdigest()[:12]}

    create = [k for k in items if k not in current]
    update = [k for k in items if k in current and current[k]["hash"] != items[k]["hash"]]
    cancel = [k for k in current if k not in items]
    same = [k for k in items if k in current and current[k]["hash"] == items[k]["hash"]]

    L = [f"# Linear sync plan (DRY RUN) – {ctx.profile['title']}", "",
         f"Project: **{ctx.profile['title']}**  ", f"Milestones: {', '.join(steps.values())}", "",
         f"| Action | Count |", "|---|---|", f"| create | {len(create)} |", f"| update | {len(update)} |",
         f"| cancel | {len(cancel)} |", f"| unchanged | {len(same)} |", ""]
    for title, keys in (("Create", create), ("Update (body replaced, comment with change reason)", update),
                        ("Cancel (never delete)", cancel)):
        if keys:
            L += [f"## {title}", ""]
            for k in keys:
                it = items.get(k, current.get(k, {}))
                L.append(f"- `{k}` → \"{it.get('title', '')}\"" + (f" · milestone: {it['milestone']}" if it.get("milestone") else "")
                         + f" · labels: {', '.join(it.get('labels', []))}")
            L.append("")
    L += ["Nothing was sent to Linear. Ownership: the pipeline owns issue content; engineering owns status, "
          "assignee, estimate and cycle."]
    out = "\n".join(L) + "\n"
    (ctx.build / "linear-plan.md").write_text(out)
    return out
