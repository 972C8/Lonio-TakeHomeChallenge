---
name: new-feature
description: Start a new feature (a new process to extract requirements for) by scaffolding its folder under features/. Use when the user has a new process to specify, not just a new source.
---

# /new-feature <name>

Everything feature-specific lives in `features/<name>/`; engine and adapters
are reused.

1. Interview the user briefly: goal, stakeholders, sources (type, location,
   authority, precedence), what is out of scope, the checklist every
   information item must answer (`item_checklist`), optional section
   hints.
2. Create `features/<name>/` with `profile.yaml`, `guidance.md` (tag citable
   product-owner statements `[G-nn]`; give id and value vocabulary),
   `decisions.yaml` (empty), `examples.yaml` (named cases taken from the
   sources; ask the user to confirm them – never generate them from pipeline
   output).
   `features/employee-onboarding/` is the reference. Never change `pipeline/`
   for a new feature; if you think you must, the change belongs in a profile
   or an adapter.
3. Run `python -m pipeline --feature <name> run`.
