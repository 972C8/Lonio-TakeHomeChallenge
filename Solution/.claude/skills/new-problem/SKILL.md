---
name: new-problem
description: Start a new investigation (a new process to extract requirements for) by scaffolding a problem profile. Use when the user has a new problem/process, not just a new source.
---

# /new-problem <name>

Everything problem-specific lives in `problems/<name>/`; engine and adapters
are reused.

1. Interview the user briefly: goal, stakeholders, sources (type, location,
   authority, precedence), what is out of scope, the checklist every
   information item must answer (`item_checklist`), optional section
   hints.
2. Create `problems/<name>/` with `profile.yaml`, `guidance.md` (tag citable
   product-owner statements `[G-nn]`; give id and value vocabulary),
   `decisions.yaml` (empty), `examples.yaml` (named cases taken from the
   sources) and `gold.yaml` (hand-labelled expectations; ask the user to
   write or confirm it – never generate it from pipeline output).
   `problems/employee-onboarding/` is the reference. Never change `pipeline/`
   for a new problem; if you think you must, the change belongs in a profile
   or an adapter.
3. Run `python -m pipeline --problem <name> run`.
