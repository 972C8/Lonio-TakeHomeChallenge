---
name: learn
description: Turn repeated human corrections into pipeline improvements. Use after several decisions/overrides have accumulated, or when the same kind of mistake keeps coming back.
---

# /learn

Every override in `decisions.yaml` is evidence that an agent got something
wrong. Make the pipeline stronger instead of correcting it forever.

1. Read `decisions.yaml` and group decisions by pattern (e.g. "condition too
   broad – asked of people who don't need it", "missing stakeholder", "used
   outside knowledge").
2. For each pattern propose exactly one of:
   - an entry in `examples.yaml` or `gold.yaml` that would have caught it (preferred –
     checks are cheaper than prompts),
   - a line in `guidance.md` (feature-specific) or an adapter/synthesizer
     prompt (general),
   - a new deterministic check in `pipeline/checks/mechanical.py`.
3. Show the proposals to the user; apply the accepted ones; rerun and confirm
   the decision is now redundant (the pipeline reaches the same result
   without it). Keep the decision anyway as documentation.
