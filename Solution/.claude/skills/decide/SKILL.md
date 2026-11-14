---
name: decide
description: Record a product decision or override in decisions.yaml from plain language (e.g. "registered partners are asked the same as married people"). Use when the product owner resolves an open question, overrides a pipeline conclusion, adds or excludes a requirement, or accepts/rejects an inferred fact.
---

# /decide – write a product decision

The product owner's judgment enters the pipeline only through
`problems/<problem>/decisions.yaml`. Decisions are applied by code after
synthesis, cited like a source, and fingerprinted against their evidence.

1. Identify the problem (default `employee-onboarding`) and read
   `build/<problem>/spec.json` (knowledge model + features),
   `build/<problem>/facts.json` and the decisions file.
2. Translate the user's words into one or more entries:
   - `override` – change one attribute: `target: item.<id>.<attr>` (e.g.
     `asked_when` + `asked_when_expr` – always change the business text AND
     the internal expression together, as two decisions), `rule.<id>.<attr>`,
     `story.<id>.<attr>` or `feature.<id>.<attr>`. For expressions use
     `pipeline/engine/condition_language.md` and only existing ids.
   - `add` – a new item/rule/story: `target: item.<new_id>` etc., `value` =
     the full object following `pipeline/engine/schemas.py` (InfoItem /
     BusinessRule / Story; for a story also `feature: <feature id>`).
   - `exclude` – `target: item.<id>` / `story.<id>` (moves it to out of scope).
   - `resolve` – `target: open.<id>` after the decision that answers it.
   - `accept` / `reject` – `target: fact.<id>`.
3. Fill `evidence` with the source unit ids (T-…, S..-E..) the decision is
   about, so it is re-flagged if those sources change. Leave `evidence_hash`
   empty; the pipeline stamps it.
4. Write `rationale` in one sentence, `by` = the user's name or role. Next
   free id: D-00N.
5. Show the user the YAML diff and ask for confirmation before saving.
6. Suggest `python -m pipeline run` (only the decide stage onward reruns).
