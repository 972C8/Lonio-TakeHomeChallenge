---
# ── Identity ───────────────────────────────────────────────────────────────
id: US-NN                      # stable, never renumbered; withdrawn stories keep their id
title: <Outcome in plain language, verb first>
feature: <feature-id>          # folder name
persona: <persona-id>          # from the feature README's persona list, never free text
priority: 1                    # 1 urgent · 2 high · 3 normal · 4 low
# ── Readiness ──────────────────────────────────────────────────────────────
status: ready                  # ready | needs-decision | draft
blocked_by: []                 # open-question ids (OQ-NN) that must be decided first
depends_on: []                 # story ids whose information or rules this story reuses
# ── What this story owns (each rule is owned by exactly one story) ─────────
rules: []                      # rule ids decided in this story
# ── Provenance ─────────────────────────────────────────────────────────────
sources: []                    # fact / decision ids; resolved in traceability.md

# ── OPTIONAL: only for stories that collect information ───────────────────
# information: []              # information ids collected in this story (owned by exactly one story)
# receiving_parties: []        # who needs that information, from the feature README

# ── OPTIONAL: tooling metadata, not part of the spec ──────────────────────
# Added by a publisher (e.g. Linear) if one is configured. Never needed to
# read or build the story.
# milestone: <slice name>
# labels: []
# linear: { issue: null }      # filled by the publisher; never by hand
---

<!--
How to use this template
- Core sections (every story): story line, Why, Rules, Acceptance criteria,
  Open questions, Not in this story, Evidence.
- Optional sections: "Information collected" and "Question wording" apply
  only when the story collects data from someone (a form, a questionnaire,
  an import). Delete them otherwise, together with the optional front matter.
- Add other optional sections only when the story needs them, e.g. a
  "Decision table" when rules combine, or "States" for a workflow.
See example-US-03-source-tax-liability.md for a data-collection story.
-->

# <Title>

**As a** <persona>, **I want** <capability>, **so that** <benefit, in the persona's terms>.

## Why

<Two or three sentences on the problem today, with the stakeholder's own
words quoted and linked to the source (turn, screen, document, step).>

> "<verbatim quote>" (<source ref>)

## Information collected *(optional: only if this story collects data)*

One row per piece of information this story owns. The columns are the five
questions every collected piece of information must answer.

| Information | What, and in what form | Asked when | Required when | Depends on | Needed by |
|---|---|---|---|---|---|
| **<Label>** `<id>` | <type in business terms; the exact options, as the receiving party lists them; format> | always / <condition in plain words> | always when asked / <condition> | <other information or rule, linked> | <receiving party (their field name)> |

Question wording *(optional)*:
- `<id>`: "<question text>" (help text: "<help>")

## Rules

Business rules this story decides. One condition per rule. If there are more
than four, split the story or use a decision table.

- **R1** <rule> ([F-…](../traceability.md#f-))
- **R2** …

## Acceptance criteria

Each criterion is pass/fail and proves exactly one rule or one behaviour.
Use real cases from the sources where they exist (and say so); mark invented
values as *illustrative*.

**AC-1** (R1, <case name, source ref>)
- **Given** <the situation, inputs or prior state>
- **When** <the actor does something / an event happens>
- **Then** <the observable outcome>

**AC-2** …

## Open questions

- [OQ-NN](../open-questions.md#oq-nn) <question> · **Until decided:** <recommendation in effect>

## Not in this story

- <What a reader might expect here but belongs to another story (link) or is out of scope (link).>

## Evidence

| Item | Fact / decision | Quote | Source |
|---|---|---|---|
| R1, AC-1 | F-… | "…" | <source ref, speaker> |
