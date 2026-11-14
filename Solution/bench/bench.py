"""Benchmark for pipeline reruns: token usage and quality per case, against one frozen baseline.

    python -m bench run B2 B3 B4 --label before      # each case: restore baseline, add its source, run, measure, restore
    python -m bench noop --label before              # B0: rerun the baseline with every agent call blocked
    python -m bench compare before after             # gate + bench/report.md

Every case starts from the same baseline (the build and requirements folders of the commit in
bench/BASELINE, with the feature folder of HEAD), adds one mock source from bench/cases/<case>/, runs `pipeline run`, and checks the result
against the case's expectations (case.yaml). Results go to bench/results/<label>/<case>/. The working tree is
restored to the baseline afterwards, so mock sources never stay in the feature folder.
"""
from __future__ import annotations

import argparse
import difflib
import fnmatch
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

SOLUTION = Path(__file__).resolve().parent.parent
BENCH = SOLUTION / "bench"
CASES = BENCH / "cases"
RESULTS = BENCH / "results"
FEATURE = "employee-onboarding"
STATE_DIRS = [f"build/{FEATURE}", f"requirements/{FEATURE}"]      # restored from the baseline commit
CONFIG_DIRS = [f"features/{FEATURE}"]                            # restored from HEAD: config is part of what is tested
PY = sys.executable


# ------------------------------------------------------------------ git state --

def baseline_ref() -> str:
    return (BENCH / "BASELINE").read_text().split()[0]


def git(*args: str, check=True) -> str:
    return subprocess.run(["git", *args], cwd=SOLUTION, check=check, capture_output=True, text=True).stdout


def restore(ref: str) -> None:
    """Build and requirements exactly as in `ref`, the feature folder as in HEAD (extra files removed)."""
    for d, src in [*((d, ref) for d in STATE_DIRS), *((d, "HEAD") for d in CONFIG_DIRS)]:
        shutil.rmtree(SOLUTION / d, ignore_errors=True)
        git("restore", f"--source={src}", "--staged", "--worktree", "--", d)
    shutil.rmtree(SOLUTION / "build" / "logs", ignore_errors=True)


def at_ref(ref: str, path: str):
    return json.loads(git("show", f"{ref}:Solution/{path}"))


def add_source(case_dir: Path, src: dict) -> None:
    """Copy the mock source into the feature folder and list it in profile.yaml (text insert, keeps the file as is)."""
    dest = SOLUTION / "features" / FEATURE / "sources"
    dest.mkdir(exist_ok=True)
    shutil.copy(case_dir / src["file"], dest / src["file"])
    entry = {k: v for k, v in src.items() if k != "file"} | {"path": f"features/{FEATURE}/sources/{src['file']}"}
    block = yaml.safe_dump([entry], sort_keys=False, allow_unicode=True, width=100)
    block = "\n".join("  " + line if line else line for line in block.splitlines()) + "\n"
    prof = SOLUTION / "features" / FEATURE / "profile.yaml"
    text = prof.read_text()
    marker = "\n# Stakeholders"
    assert marker in text, "profile.yaml: cannot find where the sources list ends"
    prof.write_text(text.replace(marker, block + marker, 1))


def run_pipeline(log: Path, no_agents=False) -> tuple[int, float]:
    env = dict(os.environ)
    if no_agents:
        env["PIPELINE_NO_AGENTS"] = "1"
    t0 = time.time()
    with log.open("w") as f:
        rc = subprocess.run([PY, "-m", "pipeline", "run"], cwd=SOLUTION, env=env, stdout=f, stderr=subprocess.STDOUT).returncode
    return rc, round(time.time() - t0)


# -------------------------------------------------------------------- metrics --

def _index(spec: dict) -> dict:
    k = spec["knowledge"]
    return {
        "stories": {s["id"]: s for sec in spec["feature"]["sections"] for s in sec["stories"]},
        "section_of": {s["id"]: sec["id"] for sec in spec["feature"]["sections"] for s in sec["stories"]},
        "elements": {**{f"item.{x['id']}": x for x in k["items"]}, **{f"rule.{x['id']}": x for x in k["rules"]},
                     **{f"open.{x['id']}": x for x in k["open_questions"]}},
    }


def _behaviour(eid: str, el: dict) -> str:
    sys.path.insert(0, str(SOLUTION))
    from pipeline.engine.incremental import behaviour
    return behaviour({"item": "item", "rule": "rule", "open": "open"}[eid.split(".")[0]], el)


def measure(ref: str) -> dict:
    """Everything the gate and the report need, from the current build compared with the baseline."""
    b = SOLUTION / "build" / FEATURE
    rep = json.loads((b / "report.json").read_text())
    spec = json.loads((b / "spec.json").read_text())
    base_spec = at_ref(ref, f"build/{FEATURE}/spec.json")
    base_rep = at_ref(ref, f"build/{FEATURE}/report.json")
    cur, base = _index(spec), _index(base_spec)
    s_cur, s_base = cur["stories"], base["stories"]
    e_cur, e_base = cur["elements"], base["elements"]
    errors = rep["findings"]["error"]
    ex = rep["examples"]
    req = SOLUTION / "requirements" / FEATURE
    files_changed = _changed_files(ref, req)
    return {
        "usage": rep.get("usage_this_run"),
        "cost_usd": rep.get("cost_usd_this_run"),
        "stages_ran": rep["stages"]["ran"],
        "counts": rep["counts"],
        "verdict": (rep.get("review") or {}).get("verdict"),
        "baseline_verdict": (base_rep.get("review") or {}).get("verdict"),
        "errors": [{"check": e["check"], "target": e["target"], "message": e["message"][:300]} for e in errors],
        "warnings": len(rep["findings"]["warning"]),
        "examples": {"pass": sum(e["pass"] for e in ex), "total": len(ex)},
        "dev_refinement": {"questions": len(rep["dev_refinement"]["questions"]),
                           "by_severity": {s: sum(q["severity"] == s for q in rep["dev_refinement"]["questions"])
                                           for s in ("blocker", "major", "minor")},
                           "tech_leaks": len(rep["dev_refinement"]["tech_leaks"])},
        "review_findings": len((rep.get("review") or {}).get("findings", [])),
        "stories": {
            "added": sorted(set(s_cur) - set(s_base)),
            "removed": sorted(set(s_base) - set(s_cur)),
            "changed": sorted(i for i in set(s_cur) & set(s_base) if s_cur[i] != s_base[i]),
            "unchanged": sum(1 for i in set(s_cur) & set(s_base) if s_cur[i] == s_base[i]),
            "added_sections": {i: cur["section_of"][i] for i in sorted(set(s_cur) - set(s_base))},
        },
        "elements": {
            "added": sorted(set(e_cur) - set(e_base)),
            "removed": sorted(set(e_base) - set(e_cur)),
            "changed_behaviour": sorted(i for i in set(e_cur) & set(e_base)
                                        if _behaviour(i, e_cur[i]) != _behaviour(i, e_base[i])),
        },
        "files_changed": files_changed,
        "impact": rep.get("impact"),
    }


def _changed_files(ref: str, req: Path) -> list[str]:
    base = set(git("ls-tree", "-r", "--name-only", ref, f"requirements/{FEATURE}").split())
    cur = {str(p.relative_to(SOLUTION)) for p in req.rglob("*") if p.is_file()}
    out = []
    for f in sorted(base | cur):
        if f not in cur or f not in base:
            out.append(f)
        elif git("show", f"{ref}:Solution/{f}") != (SOLUTION / f).read_text():
            out.append(f)
    return out


def diff_patch(ref: str, files: list[str]) -> str:
    chunks = []
    for f in files:
        old = git("show", f"{ref}:Solution/{f}", check=False).splitlines(keepends=True)
        p = SOLUTION / f
        new = p.read_text().splitlines(keepends=True) if p.exists() else []
        chunks += difflib.unified_diff(old, new, f"baseline/{f}", f"run/{f}")
    return "".join(chunks)


# ---------------------------------------------------------------- expectations --

def _matches(sid: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(sid, p) for p in patterns)


def _condition(cond: dict, m: dict, spec_idx: dict) -> tuple[bool, str]:
    if "open_question_removed" in cond:
        q = cond["open_question_removed"]
        return f"open.{q}" in m["elements"]["removed"], f"open question {q} closed"
    if "decision_flagged" in cond:
        d = cond["decision_flagged"]
        hit = any(e["check"] == "decisions" and e["target"] == d and "new evidence" in e["message"] for e in m["errors"])
        return hit, f"decision {d} flagged for re-confirmation"
    if "open_question_mentions" in cond:
        words = cond["open_question_mentions"]
        new_or_changed = set(m["elements"]["added"]) | set(m["elements"]["changed_behaviour"])
        hit = any(i.startswith("open.") and any(w.lower() in json.dumps(spec_idx["elements"][i]).lower() for w in words)
                  for i in new_or_changed if i in spec_idx["elements"])
        return hit, f"new or changed open question mentions {words}"
    raise ValueError(f"unknown condition {cond}")


def check(case: dict, m: dict) -> list[dict]:
    """Hard checks gate the case; soft checks are gated as 'not worse than the reference label'."""
    exp = case.get("expect", {})
    spec_idx = _index(json.loads((SOLUTION / "build" / FEATURE / "spec.json").read_text()))
    R = []

    def add(name, ok, soft=False, detail=""):
        R.append({"check": name, "ok": bool(ok), "soft": soft, "detail": detail})

    allowed = set(exp.get("allowed_error_checks", []))
    bad = [e for e in m["errors"] if e["check"] not in allowed]
    add("no errors (other than expected flags)", not bad, detail="; ".join(f"{e['check']} {e['target']}" for e in bad))
    add("all examples pass", m["examples"]["pass"] == m["examples"]["total"], detail=f"{m['examples']['pass']}/{m['examples']['total']}")
    st = m["stories"]
    may = exp.get("stories_may_change", []) + exp.get("stories_must_change", [])
    stray = [i for i in st["changed"] + st["removed"] if not _matches(i, may)]
    add("only expected stories changed", not stray, detail=", ".join(stray) or ", ".join(st["changed"]) or "none changed")
    for p in exp.get("stories_must_change", []):
        add(f"story {p} changed", any(fnmatch.fnmatch(i, p) for i in st["changed"]))
    if "stories_added" in exp:
        lo, hi = exp["stories_added"].get("min", 0), exp["stories_added"].get("max", 99)
        add(f"{lo}-{hi} stories added", lo <= len(st["added"]) <= hi, detail=", ".join(st["added"]) or "none")
    if exp.get("added_stories_mention_any"):
        words = [w.lower() for w in exp["added_stories_mention_any"]]
        texts = [json.dumps(spec_idx["stories"][i]).lower() for i in st["added"]]
        add(f"an added story mentions {exp['added_stories_mention_any']}", any(any(w in t for w in words) for t in texts))
    for e in exp.get("elements_must_mention", []):
        el = spec_idx["elements"].get(e["element"])
        add(f"{e['element']} mentions {e['any']}", el is not None and any(w.lower() in json.dumps(el).lower() for w in e["any"]))
    for e in exp.get("elements_must_exist", []):
        add(f"{e} still exists", e in spec_idx["elements"])
    for e in exp.get("elements_unchanged_behaviour", []):
        add(f"{e} unchanged in behaviour", e not in m["elements"]["changed_behaviour"] and e not in m["elements"]["removed"])
    if exp.get("any_of"):
        res = [_condition(c, m, spec_idx) for c in exp["any_of"]]
        add("one of: " + " / ".join(d for _, d in res), any(ok for ok, _ in res),
            detail=", ".join(d for ok, d in res if ok))
    if exp.get("soft_any_of"):
        res = [_condition(c, m, spec_idx) for c in exp["soft_any_of"]]
        add("one of: " + " / ".join(d for _, d in res), any(ok for ok, _ in res), soft=True,
            detail=", ".join(d for ok, d in res if ok))
    return R


# ------------------------------------------------------------------- commands --

def run_case(name: str, label: str, ref: str, noop_after: bool) -> dict:
    case_dir = next(CASES.glob(f"{name}*"))
    case = yaml.safe_load((case_dir / "case.yaml").read_text())
    out = RESULTS / label / case["id"]
    out.mkdir(parents=True, exist_ok=True)
    restore(ref)
    try:
        add_source(case_dir, case["source"])
        print(f"[{case['id']}] running pipeline ...", flush=True)
        rc, secs = run_pipeline(out / "run.log")
        if rc != 0:
            res = {"case": case["id"], "label": label, "ok": False, "error": f"pipeline exited {rc}", "seconds": secs}
        else:
            m = measure(ref)
            m["seconds"] = secs
            checks = check(case, m)
            (out / "diff.patch").write_text(diff_patch(ref, m["files_changed"]))
            shutil.copy(SOLUTION / "build" / FEATURE / "review.md", out / "review.md")
            res = {"case": case["id"], "label": label, "ok": all(c["ok"] for c in checks if not c["soft"]),
                   "checks": checks, "metrics": m}
            if noop_after:                     # B0: nothing changed since -> no agent call
                rc0, _ = run_pipeline(out / "noop.log", no_agents=True)
                res["noop_after"] = rc0 == 0
                res["checks"].append({"check": "no-op rerun calls no agent (B0)", "ok": rc0 == 0, "soft": False, "detail": ""})
                res["ok"] = res["ok"] and rc0 == 0
        (out / "result.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
        _print(res)
        return res
    finally:
        restore(ref)


def noop(label: str, ref: str) -> dict:
    out = RESULTS / label / "B0"
    out.mkdir(parents=True, exist_ok=True)
    restore(ref)
    try:
        rc, secs = run_pipeline(out / "run.log", no_agents=True)
        res = {"case": "B0", "label": label, "ok": rc == 0, "seconds": secs,
               "checks": [{"check": "no-op rerun calls no agent", "ok": rc == 0, "soft": False, "detail": ""}]}
        (out / "result.json").write_text(json.dumps(res, indent=1))
        _print(res)
        return res
    finally:
        restore(ref)


def _print(res: dict) -> None:
    print(f"[{res['case']}] {'PASS' if res['ok'] else 'FAIL'}" + (f" - {res['error']}" if "error" in res else ""))
    for c in res.get("checks", []):
        print(f"   {'ok ' if c['ok'] else 'NO '}{'(soft) ' if c['soft'] else ''}{c['check']}" + (f": {c['detail']}" if c["detail"] else ""))
    u = (res.get("metrics") or {}).get("usage")
    if u:
        t = u["total"]
        print(f"   tokens {t['total_tokens']:,} ({t['input_tokens']:,} in, {t['cache_read_input_tokens']:,} cache read, "
              f"{t['cache_creation_input_tokens']:,} cache write, {t['output_tokens']:,} out), SDK est. ${t['cost_usd']:.2f}, "
              f"{t['calls']} calls")


def compare(ref_label: str, new_label: str) -> str:
    from .report import write_report
    return write_report(RESULTS, ref_label, new_label, BENCH / "report.md")


def main(argv=None):
    p = argparse.ArgumentParser(prog="bench")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("cases", nargs="+")
    r.add_argument("--label", required=True)
    r.add_argument("--noop-after", action="store_true", help="also check that a rerun right after calls no agent (B0)")
    n = sub.add_parser("noop")
    n.add_argument("--label", required=True)
    c = sub.add_parser("compare")
    c.add_argument("ref_label")
    c.add_argument("new_label")
    sub.add_parser("restore")
    a = p.parse_args(argv)
    ref = baseline_ref()
    if a.cmd == "run":
        for name in a.cases:
            run_case(name, a.label, ref, a.noop_after)
    elif a.cmd == "noop":
        noop(a.label, ref)
    elif a.cmd == "compare":
        print(compare(a.ref_label, a.new_label))
    elif a.cmd == "restore":
        restore(ref)


if __name__ == "__main__":
    main()
