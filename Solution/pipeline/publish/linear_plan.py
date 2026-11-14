"""Linear publish stage - DRY RUN (design: docs/linear-publishing.md).

Computes deterministically what a sync of the feature specs to Linear would
do, and renders the exact issue payloads, without touching Linear. A real
publish hands this plan to a narrow publisher agent with the Linear MCP server
(https://mcp.linear.app/mcp) and verifies by reading the issues back.

Mapping
- problem        -> project; README / information catalogue / out of scope -> project documents
- feature        -> parent issue "[FEAT-..] title" (+ milestone of the same name)
- user story     -> sub-issue "[US-x.y] title"; criteria + examples in the description,
                    evidence in a collapsed "+++ Evidence +++" section
- open question  -> issue "[OQ-..] Decision needed: ...", label spec:needs-decision
Identity: problems/<p>/linear_map.yaml (committed) maps spec id -> Linear id + last published hash.
"""
from __future__ import annotations

import hashlib
import json

import yaml

from ..engine.context import Context
from ..engine.paths import REQUIREMENTS

PRIORITY = {"P1": "Urgent", "P2": "High", "P3": "Medium"}


def _h(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def _story_body(s: dict, names: dict, facts: dict, spec_link: str, who: dict) -> str:
    L = [f"**As** {who.get(s['as_a'], s['as_a'])}, **I want** {s['i_want']}, **so that** {s['so_that']}", "",
         f"Priority {s['priority']}: {s['priority_reason']}", "", "## Acceptance criteria", ""]
    for ac in s["acceptance_criteria"]:
        L += [f"**{ac['id']} {ac['title']}**", f"- Given {ac['given']}", f"- When {ac['when']}", f"- Then {ac['then']}"]
        if ac.get("examples"):
            cols_in = list(dict.fromkeys(g["item"] for ex in ac["examples"] for g in ex["given"]))
            cols_out = list(dict.fromkeys(t["target"] for ex in ac["examples"] for t in ex["then"]))
            L += ["", "| Example | " + " | ".join(names.get(c, c) for c in cols_in) + " | → | "
                  + " | ".join(names.get(c, c) for c in cols_out) + " |",
                  "|---" * (len(cols_in) + len(cols_out) + 2) + "|"]
            for ex in ac["examples"]:
                gi = {g["item"]: g["value"] for g in ex["given"]}
                th = {t["target"]: t["expect"] for t in ex["then"]}
                L.append(f"| {ex['name']} | " + " | ".join(gi.get(c, "–") for c in cols_in) + " | → | "
                         + " | ".join(th.get(c, "–") for c in cols_out) + " |")
        L.append("")
    refs = sorted(set(s["source_refs"]) | {r for ac in s["acceptance_criteria"] for r in ac["source_refs"]})
    L += ["+++ Evidence", ""]
    for r in refs:
        f = facts.get(r)
        L.append(f"- {r}: {f['statement']}" + "".join(f' — "{a["quote"]}" ({a["unit_id"]})' for a in f["anchors"])
                 if f else f"- {r}")
    L += ["", f"Spec: `{spec_link}`", "+++"]
    return "\n".join(L)


def plan(problem: str) -> str:
    ctx = Context(problem)
    spec = ctx.read("spec")
    facts = {f["id"]: f for f in ctx.read("facts")}
    km = spec["knowledge"]
    who = {k: str(v).split(" - ")[0].strip() for k, v in ctx.profile["stakeholders"].items()}
    names = {**{i["id"]: i["name"] for i in km["items"]}, **{r["id"]: r["name"] for r in km["rules"]}}
    map_path = ctx.problem_dir / "linear_map.yaml"
    current = (yaml.safe_load(map_path.read_text()) or {}).get("issues", {}) if map_path.exists() else {}
    out_dir = ctx.build / "linear"
    out_dir.mkdir(parents=True, exist_ok=True)
    req = REQUIREMENTS / problem

    items = {}
    for doc, title in (("README", "Overview"), ("information", "Information catalogue"), ("out-of-scope", "Out of scope")):
        body = (req / f"{doc}.md").read_text()
        items[f"document.{doc}"] = {"kind": "project document", "title": title, "body": body}
    for f in sorted(spec["features"], key=lambda f: f["order"]):
        fid = f["id"].split("-")[0] + "-" + f["id"].split("-")[1]
        body = (req / "features" / f"{f['id']}.md").read_text().split("## User stories")[0]
        items[f"feature.{f['id']}"] = {"kind": "parent issue + milestone", "title": f"[{fid}] {f['title']}",
                                       "labels": ["spec:feature"], "body": body}
        for s in f["stories"]:
            labels = [f"spec:{s['priority']}", f"spec:stakeholder/{s['as_a']}"] + (["spec:inferred"] if s["status"] == "inferred" else [])
            items[f"story.{s['id']}"] = {"kind": "sub-issue", "parent": f"feature.{f['id']}",
                                         "title": f"[{s['id']}] {s['title']}", "priority": PRIORITY[s["priority"]],
                                         "labels": labels,
                                         "body": _story_body(s, names, facts, f"requirements/{problem}/features/{f['id']}.md", who)}
    for q in km["open_questions"]:
        body = "\n".join([q["why_it_matters"], "", *[f"- {o}" for o in q.get("options", [])], "",
                          f"**Recommendation:** {q.get('recommendation', '')}"])
        items[f"open.{q['id']}"] = {"kind": "issue", "title": f"[{q['id']}] Decision needed: {q['question']}",
                                    "labels": ["spec:needs-decision"] + (["spec:blocking"] if q.get("blocking") else []),
                                    "assignee": "product owner", "body": body}
    for k, it in items.items():
        it["hash"] = _h(it["title"] + it["body"])
        (out_dir / f"{k.replace('/', '_')}.md").write_text(f"# {it['title']}\n\n{it['body']}\n")

    create = [k for k in items if k not in current]
    update = [k for k in items if k in current and current[k]["hash"] != items[k]["hash"]]
    same = [k for k in items if k in current and current[k]["hash"] == items[k]["hash"]]
    removed = [k for k in current if k not in items]

    L = [f"# Linear sync plan (DRY RUN) – {ctx.profile['title']}", "",
         f"Project: **{ctx.profile['title']}** · mapping file: `problems/{problem}/linear_map.yaml` "
         f"({'present' if map_path.exists() else 'none yet: first publish'})", "",
         "| Action | Count |", "|---|---|", f"| create | {len(create)} |", f"| update (+ change comment) | {len(update)} |",
         f"| cancel or flag (removed from spec) | {len(removed)} |", f"| unchanged | {len(same)} |", "",
         "Payload previews (exact titles and descriptions): `build/{problem}/linear/`".replace("{problem}", problem), ""]
    for title, keys in (("Create", create), ("Update", update)):
        if keys:
            L += [f"## {title}", ""]
            for k in keys:
                it = items[k]
                L.append(f"- {it['kind']} `{k}` → \"{it['title']}\""
                         + (f" · parent: `{it['parent']}`" if it.get("parent") else "")
                         + (f" · priority: {it['priority']}" if it.get("priority") else "")
                         + (f" · labels: {', '.join(it['labels'])}" if it.get("labels") else ""))
            L.append("")
    if removed:
        L += ["## Removed from the spec", "",
              "Not started → cancel with an explaining comment; in progress or done → comment + `spec:needs-decision` "
              "(never deleted).", ""] + [f"- `{k}` ({current[k].get('identifier', '?')})" for k in removed] + [""]
    L += ["Before applying, the publisher also compares each issue's current description with the last published "
          "hash; issues edited in Linear are not overwritten but flagged in review.md.", "",
          "Nothing was sent to Linear. The pipeline owns issue content and its `spec:` labels; engineering owns "
          "status, assignee, estimate, cycle and all other labels."]
    text = "\n".join(L) + "\n"
    (ctx.build / "linear-plan.md").write_text(text)
    (ctx.build / "linear-plan.json").write_text(json.dumps(
        {"create": create, "update": update, "removed": removed, "unchanged": same,
         "items": {k: {kk: vv for kk, vv in v.items() if kk != "body"} for k, v in items.items()}}, indent=2))
    return text
