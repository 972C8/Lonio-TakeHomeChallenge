# Improvements

Two tests with mock sources (a pension fund email with a new 2027 rule and an
answered open question; an HR follow-up call that contradicts decision D-007)
showed one root cause: the pipeline treats a rerun as *regenerate, then
compare*. Incremental reruns (only affected sections rewritten) and the
"new evidence since this decision" flag reduce the damage, but a newer source
can still change the spec before the product owner has seen it (test 2: HR's
statement overrode D-007), and the flags are based on citations, so they are
coarse (12 decisions flagged in test 2, about half of them noise).

The two most valuable next steps:

## 1. Treat the approved spec as a baseline

Once the product owner approves a run, freeze it as the baseline. A new or
changed source then produces a **proposed diff** against that baseline
(elements added, changed or contradicted, with the facts behind each change),
never a silent rewrite. The product owner approves or rejects the diff, like a
pull request; only approved changes enter the baseline.

- Covers both failures seen in the tests: a decision overridden by a newer
  source (D-007), and stories drifting although nothing relevant changed.
- Makes "nothing changes without the product owner's OK" structural instead of
  best-effort.
- The approved diff is also the natural unit to publish to Linear.

## 2. Classify each new fact before modelling

Before a new fact reaches the modeler, classify it against the existing facts
**and** the decisions: *new information*, *confirmation*, *correction* or
*contradiction*.

- Contradictions (of a fact or a decision) become questions for the product
  owner; they do not flow into the model until answered.
- New information, confirmations and corrections flow in as today.
- Replaces the citation-based decision flagging, which cannot tell "this new
  fact contradicts D-007" from "this element merely gained a citation".

Together, 1 and 2 turn a new source into a reviewable change request: the
classification decides what may flow in, the baseline diff shows what it did.
