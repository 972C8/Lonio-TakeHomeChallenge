---
name: run-pipeline
description: Run the requirements pipeline and summarize the review for the product owner. Use when asked to run, rerun or refresh the requirements, or after sources/guidance/decisions changed.
---

# /run-pipeline

1. `python -m pipeline status` – report which sources changed.
2. `python -m pipeline run` (add `--force <stage>` only if asked; `--fast`
   skips LLM checks for quick iterations on decisions/templates).
   Runs take minutes; run in the background.
3. Read `build/<problem>/review.md` and summarize: verdict, failing examples,
   errors, open questions needing a decision, dev-refinement blockers and
   technical leaks.
4. For each open question, propose a decision (then use /decide on the
   user's answer). Never edit `requirements/` by hand.
