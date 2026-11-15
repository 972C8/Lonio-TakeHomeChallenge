"""bench/report.md: per case and per stage, tokens before and after, and the gate."""
from __future__ import annotations

import json
from pathlib import Path


def _load(results: Path, label: str) -> dict:
    out = {}
    for f in sorted((results / label).glob("*/result.json")):
        r = json.loads(f.read_text())
        out[r["case"]] = r
    return out


def _tok(r: dict) -> dict:
    return (((r.get("metrics") or {}).get("usage")) or {}).get("total") or {}


def _stages(r: dict) -> dict:
    return (((r.get("metrics") or {}).get("usage")) or {}).get("by_stage") or {}


def _pct(a, b) -> str:
    return f"{(b - a) / a * 100:+.0f}%" if a else "-"


def gate(ref: dict, new: dict) -> tuple[bool, list[str]]:
    """A change passes a case when no check that held before fails now (hard or soft), the review verdict is the
    same, and the run used fewer tokens. Checks that already failed before are reported, not gated: they are
    findings about the pipeline, not regressions of the change."""
    why = []
    if "error" in new:
        why.append(new["error"])
    before = {c["check"]: c["ok"] for c in ref.get("checks", [])}
    for c in new.get("checks", []):
        if before.get(c["check"]) and not c["ok"]:
            why.append(f"regressed: {c['check']}")
    mr, mn = ref.get("metrics") or {}, new.get("metrics") or {}
    if mr and mn and mr.get("verdict") != mn.get("verdict"):
        why.append(f"verdict {mr.get('verdict')} -> {mn.get('verdict')}")
    tr, tn = _tok(ref).get("total_tokens"), _tok(new).get("total_tokens")
    if tr and tn is not None and tn >= tr:
        why.append("no fewer tokens")
    return not why, why


def write_report(results: Path, ref_label: str, new_label: str, path: Path) -> str:
    ref, new = _load(results, ref_label), _load(results, new_label)
    L = [f"# Benchmark: {ref_label} vs {new_label}", "",
         "Tokens are the SDK's counts summed over all agent calls of the run (input + output + cache read + cache "
         "write). Cost is the SDK's list-price estimate; the pipeline runs on a Max login, so it is not a bill.", "",
         "## Summary", "",
         f"| Case | Tokens {ref_label} | Tokens {new_label} | Change | Cost {ref_label} | Cost {new_label} | Verdict | Gate |",
         "|---|---:|---:|---:|---:|---:|---|---|"]
    for case in sorted(set(ref) | set(new)):
        r, n = ref.get(case, {}), new.get(case, {})
        tr, tn = _tok(r), _tok(n)
        ok, why = gate(r, n) if r and n else (n.get("ok", False), ["no reference"] if n else [f"not run in {new_label}"])
        vr = (r.get("metrics") or {}).get("verdict", "-")
        vn = (n.get("metrics") or {}).get("verdict", "-")
        L.append(f"| {case} | {tr.get('total_tokens', 0):,} | {tn.get('total_tokens', 0):,} | "
                 f"{_pct(tr.get('total_tokens', 0), tn.get('total_tokens', 0)) if n else '-'} | ${tr.get('cost_usd', 0):.2f} | "
                 f"${tn.get('cost_usd', 0):.2f} | {vr} → {vn} | {'PASS' if ok else ('- (' + why[0] + ')' if not n else 'FAIL: ' + '; '.join(why))} |")
    for case in sorted(set(ref) | set(new)):
        r, n = ref.get(case, {}), new.get(case, {})
        L += ["", f"## {case}", ""]
        sr, sn = _stages(r), _stages(n)
        if sr or sn:
            L += [f"| Stage | Calls | Tokens {ref_label} | Tokens {new_label} | Cost {ref_label} | Cost {new_label} |",
                  "|---|---:|---:|---:|---:|---:|"]
            for st in sorted(set(sr) | set(sn), key=lambda s: -(sr.get(s, {}).get("cost_usd", 0))):
                a, b = sr.get(st, {}), sn.get(st, {})
                L.append(f"| {st} | {a.get('calls', 0)} → {b.get('calls', 0)} | {a.get('total_tokens', 0):,} | "
                         f"{b.get('total_tokens', 0):,} | ${a.get('cost_usd', 0):.2f} | ${b.get('cost_usd', 0):.2f} |")
            L.append("")
        for lab, x in ((ref_label, r), (new_label, n)):
            if not x:
                continue
            m = x.get("metrics") or {}
            st = m.get("stories", {})
            L.append(f"**{lab}**: " + ("; ".join([
                f"stories changed {', '.join(st.get('changed', [])) or '-'}",
                f"added {', '.join(st.get('added', [])) or '-'}",
                f"errors {len(m.get('errors', []))}",
                f"examples {m.get('examples', {}).get('pass', '?')}/{m.get('examples', {}).get('total', '?')}",
                f"open questions {m.get('counts', {}).get('open_questions', '?')}",
                f"dev questions {m.get('dev_refinement', {}).get('questions', '?')}",
                f"verdict {m.get('verdict', '-')}",
                f"{m.get('seconds', x.get('seconds', '?'))} s"]) if m else "no metrics"))
            L.append("")
            for c in x.get("checks", []):
                L.append(f"- {'✅' if c['ok'] else '❌'} {'(soft) ' if c['soft'] else ''}{c['check']}"
                         + (f": {c['detail']}" if c.get("detail") else ""))
            L.append("")
    text = "\n".join(L) + "\n"
    path.write_text(text)
    return text
