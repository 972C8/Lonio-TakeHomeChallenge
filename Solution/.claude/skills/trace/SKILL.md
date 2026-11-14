---
name: trace
description: Explain why a requirement says what it says, down to the verbatim source quotes. Use when asked "where does X come from", "why is Y required", or to audit a field, rule, notice, open question or fact id.
---

# /trace <id>

1. Read `build/<feature>/spec.json` and find the element: a story (`US-…`),
   acceptance criterion (`AC-…`), information item, business rule or open
   question. Also accept a fact id `F-…`, guidance `G-…` or decision `D-…`.
2. For each id in `source_refs`: look it up in `build/<feature>/facts.json`
   (or `decisions.yaml` for `D-…`). Show statement, kind, basis, the judge
   verdict, and each anchor quote with its unit id.
3. For each anchor, show the full unit text from
   `build/<feature>/normalize/<source>.json` (speaker / screenshot file), so
   the quote is seen in context. Mention superseded facts and what superseded
   them.
4. Show the trace-judge verdict from `build/<feature>/judge_trace.json` and,
   for acceptance criteria, whether their examples pass (`report.json`).
5. Conclude in two sentences: is the requirement fully backed, and what (if
   anything) rests on inference or a decision.
