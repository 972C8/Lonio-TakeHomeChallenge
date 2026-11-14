---
name: review
description: Walk the product owner through the latest pipeline review so they don't have to read review.md themselves. Gives the verdict in one line, then goes through failing examples, open questions, inferred items, uncited source units and dev-refinement questions one at a time, each with context, the source quote and a recommendation, and records every answer in decisions.yaml. Use after `pipeline run`, or when asked to "review the run", "go through the open questions" or "what do I need to decide".
---

# /review – a guided walk through the latest review

Goal: the product owner answers questions; they never have to open
`build/<feature>/review.md` themselves. You read it, explain, recommend, and
record their answers as decisions (the same mechanism as `/decide`).

## 0. Load
1. Feature: the one the user names, default `employee-onboarding`.
2. Read `build/<feature>/review.md`, `report.json`, `spec.json`,
   `facts.json` and `features/<feature>/decisions.yaml`. If `review.md` does
   not exist, say so and suggest `/run-pipeline` (a run costs money and takes
   minutes: never start it without asking).
3. If `review.md` says "Verdict: not available", the LLM checks did not run:
   tell the user, and still walk through what is there.
4. Say in **one line**: the verdict, the number of errors, failing examples and
   open questions. Then tell them the order you will go in and how many
   items each part has. Ask whether to start.

## 1. Walk through, in this order, one item at a time
For every item give: **what it is** (one sentence), **why it matters** (what
changes in the spec), **the evidence** (the verbatim source quote with its
unit id and speaker/file, found through the cited fact ids in `facts.json`),
and **your recommendation** (one of the options, with a reason). Then ask
for their answer (use AskUserQuestion with the options plus "skip", or ask in
plain text) and **wait**. Never batch several items into one question and
never answer for them.

1. **Errors** – anything that blocks the verdict that is not covered below.
2. **Failing examples** – for each: the case, what the rules produce versus
   what was expected, and your reading of who is wrong: the source, the
   example (`examples.yaml`, owned by the user) or the generated rule.
   Options: fix the example, add an override decision, or leave and rerun.
3. **Open questions** (`open_questions`, blocking ones first) – question, why
   it matters, options and the pipeline's recommendation, plus the quote that
   raised it. Record the answer as **two things**: the change itself
   (`override` / `add` / `exclude` of the affected item, rule, story or
   section) and `resolve` for `open.<id>`. A `resolve` alone only closes the
   question; it does not change the spec.
4. **Inferred items** – facts and elements that rest on interpretation: show
   the fact statement and the quote, say whether the reading is reasonable.
   Options: `accept` the fact, `reject` it, or override the element.
5. **Uncited source units** – group them (small talk, other topics, possibly
   relevant). Show only the groups that might matter. The user confirms they
   are irrelevant; nothing is recorded unless something was missed, in which
   case record an `add` decision or propose a line for `guidance.md`.
6. **Dev-refinement questions and technical vocabulary** – group duplicates,
   skip `minor` ones unless asked. An answer becomes a decision; a recurring
   technical choice by the agents becomes a proposed line for `guidance.md`
   (show it, save only after confirmation).
7. **Warnings** – only if the user asks. Mention how many there are.

If the user says "skip", move on and keep a list of skipped items.

## 2. Recording answers
- Build each decision exactly as `/decide` describes (targets `item.`, `rule.`,
  `story.`, `section.`, `feature.`, `open.`, `exclusion.`, `fact.`; story ids
  contain a dot; `evidence` = source unit ids; `rationale` in one sentence;
  `by` = the user's name or role; next free id `D-00N`). Change a business
  condition and its internal expression together, as two decisions.
- Collect the decisions as you go. After each part (not each item), show the
  YAML you are about to add and **ask for confirmation before writing** to
  `decisions.yaml`. Changes to `examples.yaml` or `guidance.md`
  also need confirmation and belong to the user: propose, never silently edit.
- Never edit anything under `requirements/` or `build/`.

## 3. Finish
- Summarise in a few lines: decisions written (ids and one-line meaning),
  items skipped, what remains open.
- Offer to rerun: `pipeline run` re-executes only the steps after the
  changed input, which costs a fraction of a first run. Say that it costs
  money and takes minutes, and run it only if the user agrees (use
  `/run-pipeline`).
