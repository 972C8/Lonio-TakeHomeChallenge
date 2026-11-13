---
name: new-problem
description: Start a new investigation (a new process to extract requirements for) by scaffolding a problem profile. Use when the user has a new problem/process, not just a new source.
---

# /new-problem <name>

Everything problem-specific lives in `problems/<name>/`; engine and adapters
are reused.

1. Interview the user briefly: goal, receiving parties (consumers), sources
   (type, location, authority), what is out of scope, requirement shape
   (today: `data_field`; other shapes need a new schema + templates).
2. Create `problems/<name>/` with `profile.yaml`, `guidance.md`,
   `decisions.yaml` (empty), `personas.yaml` (test cases taken from the
   sources), `gold.yaml` (hand-labelled expectations; ask the user to write or
   confirm it – never generate it from pipeline output).
   Use `problems/employee-onboarding/` as the reference.
3. Run `python -m pipeline --problem <name> run`.
