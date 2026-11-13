---
name: decide
description: Record a product decision or override in decisions.yaml from plain language (e.g. "registered partners are asked the same as married people"). Use when the product owner resolves an open question, overrides a pipeline conclusion, adds or excludes a requirement, or accepts/rejects an inferred fact.
---

# /decide – write a product decision

The product owner's judgment enters the pipeline only through
`problems/<problem>/decisions.yaml`. Decisions are applied by code after
synthesis, cited like a source, and fingerprinted against their evidence.

1. Identify the problem (default `employee-onboarding`) and read
   `build/<problem>/spec.json`, `build/<problem>/facts.json` and the
   decisions file.
2. Translate the user's words into one or more entries:
   - `override` – change one attribute: `target: field.<id>.<attr>` (e.g.
     `ask_when`, `required_when`, `options`, `validation`, `step`, `order`) or
     `rule.<id>.expression`. `value` must be valid for that attribute; for
     conditions use the condition language in `pipeline/engine/condition_language.md`
     and only existing ids.
   - `add` – a new field/rule/notice: `target: field.<new_id>`, `value` = the
     full object following `pipeline/engine/schemas.py` (FieldReq / Rule / Notice).
   - `exclude` – `target: field.<id>` (moves it to out-of-scope).
   - `resolve` – `target: open.<id>` after the decision that answers it.
   - `accept` / `reject` – `target: fact.<id>`.
3. Fill `evidence` with the source unit ids (T-…, S..-E..) the decision is
   about, so it is re-flagged if those sources change. Leave `evidence_hash`
   empty; the pipeline stamps it.
4. Write `rationale` in one sentence, `by` = the user's name or role. Next
   free id: D-00N.
5. Show the user the YAML diff and ask for confirmation before saving.
6. Suggest `python -m pipeline run` (only the decide stage onward reruns).
