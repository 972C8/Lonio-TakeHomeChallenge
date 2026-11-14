---
name: update-source
description: Handle a source that changed or a new one that arrived: asks what happened, updates profile.yaml for a new source, shows what changed, runs the pipeline through /run-pipeline, then flags decisions whose evidence changed and what moved in the spec. Use when a transcript, screenshot set or other source was replaced, a live site changed, or a new source should be added.
---

# /update-source – after a source changes or a new one arrives

Lean on purpose: this skill only guides and hands off. Running is
`/run-pipeline`, a new kind of source is `/new-adapter`, deciding is
`/review` and `/decide`. Feature: the one the user names, default
`employee-onboarding`; commands from `Solution/` with `.venv/bin/python`.

## 1. Ask what happened
Ask (AskUserQuestion with these options):
- **A file of an existing source was replaced or updated**
- **A live site changed** (an explored source such as the Zurich calculator)
- **A new source of a known type** (`transcript`, `screenshots`, `web_calculator`)
- **A new kind of source** (emails, regulation PDFs, spreadsheets, …) →
  start `/new-adapter` for it first, then return here.

## 2. Prepare the source
- **Replaced file:** check the path in `features/<f>/profile.yaml`. The new
  file must be at that path (the old version stays in git; never delete it
  for the user). If it is elsewhere, ask whether to change the path in the
  profile.
- **Live site changed:** nothing to replace. `/run-pipeline` will offer to
  re-run the exploration (default no): tell the user to say yes there.
- **New source of a known type:** ask for the file or URL, and for the
  fields the profile needs: `id`, `type`, `path`/`url`, a one-line
  `description`, `authority` (what it is trusted for), `precedence` (lower
  wins a conflict; the product owner's decisions always win) and, for
  transcripts, `speakers`. Show the YAML entry for `sources:` and add it to
  `profile.yaml` only after the user confirms.

## 3. Show what the pipeline sees changed
Run `python -m pipeline --feature <f> status` and show which sources are
`CHANGED -> will rerun`. (Before the first run everything shows as changed.)

## 4. Run
Hand off to **`/run-pipeline`**; it asks about exploring live sources and
runs the pipeline. Do not run the pipeline yourself.

## 5. After the run
Read `build/<f>/review.md` and report, briefly:
1. **Decisions flagged for re-confirmation** (errors from the `decisions`
   check: "evidence … changed since this decision was made"). For each, show
   the decision, the old and the new source text of its `evidence` units
   (`build/<f>/normalize/<source>.json`) and ask: still valid, update, or
   drop? "Still valid" = clear that decision's `evidence_hash` in
   `decisions.yaml` so the next run re-stamps it (confirm before writing);
   update / drop follow `/decide`.
2. **New content not used:** uncited units of the changed or new source in
   the coverage section.
3. **What moved in the spec:** `git diff --stat -- requirements/<f>/` (and
   the diff of `feature.md` if short). If `requirements/<f>/` was not
   committed before, say there is nothing to compare against.

Then offer **`/review`** for everything else in the review.
