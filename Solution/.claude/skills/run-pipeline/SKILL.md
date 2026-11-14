---
name: run-pipeline
description: Run the requirements pipeline and summarize the review for the product owner. Always asks about exploring live sources (e.g. the Zurich calculator) first. Use when asked to run, rerun or refresh the requirements, or after sources/guidance/decisions changed.
---

# /run-pipeline

Feature: the one the user names, default `employee-onboarding`. Commands run
from `Solution/` with `.venv/bin/python`.

1. `python -m pipeline --feature <f> status` – report which sources changed.
2. **Always ask about exploration before running**, even if the user said
   "just run it". For every source in `features/<f>/profile.yaml` with
   `type: web_calculator` (a live site that must be explored), look for its
   cache `build/<f>/cache/<source_id>/tree.json`:
   - **No cache (never explored):** ask whether to run `pipeline explore
     <source_id>` first. Say it takes about 20–60 minutes and a few dollars,
     and that without it the source is skipped and reported as an open
     question in the review.
   - **Cache exists:** read `explored_at` and the number of questions from
     `tree.json`, and ask whether to **re-run** the exploration. The default
     is **no**; only re-run on a clear yes (e.g. the site changed).

   Ask one question per source (AskUserQuestion with yes / no, or plain
   text). If there is no such source, skip this step. Run the approved
   explorations first, one at a time and in the background:
   `python -m pipeline --feature <f> explore <source_id>`, and wait until they
   finish before step 3.
3. `python -m pipeline --feature <f> run` (add `--force <stage>` only if
   asked; `--fast` skips LLM checks for quick iterations on decisions or
   templates). Runs take minutes; run in the background.
4. Read `build/<f>/review.md` and summarize: verdict, failing examples,
   errors, open questions needing a decision, dev-refinement blockers and
   technical leaks.
5. For each open question, propose a decision (then use /decide on the
   user's answer). Never edit `requirements/` by hand.
