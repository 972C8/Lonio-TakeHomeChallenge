"""Linear publish stage - DRY RUN.

Computes what a sync of the feature specs to Linear would do, without touching
Linear. Git stays the source of truth; Linear is a projection.

Mapping (generic for any problem)
- problem            -> Linear project
- feature            -> project milestone (or parent issue)
- user story         -> issue: title "[US-x.y] <title>", description = story,
                        acceptance criteria and examples (rendered Markdown),
                        labels = priority, stakeholder, status
- open question      -> issue labelled `needs-decision`, assigned to the product owner
Idempotency: build/<problem>/linear_map.json maps id -> issue id + content hash.
Unchanged hash -> no-op; changed -> update + comment with the change reason;
removed -> cancel (never delete).

A real run hands this plan to a small publisher agent with the Linear MCP
server (https://mcp.linear.app) and reads the issues back to verify.
"""
from __future__ import annotations

import hashlib
import json

from ..engine.context import Context


def _h(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:12]


def plan(problem: str) -> str:
    ctx = Context(problem)
    spec = ctx.read("spec")
    map_path = ctx.build / "linear_map.json"
    current = json.loads(map_path.read_text()) if map_path.exists() else {}
    items = {}
    for f in sorted(spec["features"], key=lambda f: f["order"]):
        items[f"feature.{f['id']}"] = {"title": f["title"], "kind": "milestone", "labels": [], "hash": _h(f["goal"])}
        for s in f["stories"]:
            items[f"story.{s['id']}"] = {"title": f"[{s['id']}] {s['title']}", "kind": "issue", "milestone": f["title"],
                                         "labels": [s["priority"], s["as_a"], s["status"]], "hash": _h(s)}
    for q in spec["knowledge"]["open_questions"]:
        items[f"open.{q['id']}"] = {"title": f"[{q['id']}] Decision needed: {q['question']}", "kind": "issue",
                                    "labels": ["needs-decision"] + (["blocking"] if q["blocking"] else []),
                                    "assignee": "product owner", "hash": _h(q)}
    create = [k for k in items if k not in current]
    update = [k for k in items if k in current and current[k]["hash"] != items[k]["hash"]]
    cancel = [k for k in current if k not in items]
    same = [k for k in items if k in current and current[k]["hash"] == items[k]["hash"]]
    L = [f"# Linear sync plan (DRY RUN) – {ctx.profile['title']}", "", f"Project: **{ctx.profile['title']}**", "",
         "| Action | Count |", "|---|---|", f"| create | {len(create)} |", f"| update | {len(update)} |",
         f"| cancel | {len(cancel)} |", f"| unchanged | {len(same)} |", ""]
    for title, keys in (("Create", create), ("Update (description replaced, comment with change reason)", update),
                        ("Cancel (never delete)", cancel)):
        if keys:
            L += [f"## {title}", ""]
            for k in keys:
                it = items.get(k, current.get(k, {}))
                L.append(f"- {it.get('kind', '')} `{k}` → \"{it.get('title', '')}\""
                         + (f" · milestone: {it['milestone']}" if it.get("milestone") else "")
                         + (f" · labels: {', '.join(it['labels'])}" if it.get("labels") else ""))
            L.append("")
    L += ["Nothing was sent to Linear. The pipeline owns issue content; engineering owns status, assignee, "
          "estimate and cycle."]
    out = "\n".join(L) + "\n"
    (ctx.build / "linear-plan.md").write_text(out)
    return out
