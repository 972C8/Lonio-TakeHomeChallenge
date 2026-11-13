You are an AI software engineer about to build an onboarding questionnaire.
You have **only** the requirements folder below - no other context, no way to
ask anyone. Read it carefully (use Read / Glob / Grep on the folder).

List every question you would have to ask the product owner before you could
build this correctly and completely: ambiguities, missing values, undefined
behaviour, contradictions between files, conditions that reference unknown
things, fields whose validation or options are unclear, unclear edge cases.

Rules:
- Only list questions whose answer would change what you build. No style
  nitpicks.
- If the requirements already mark something as an open question, list it
  under `already_flagged` instead (it is known, not a defect).
- For each question give the file it concerns and a severity: `blocker`
  (cannot build correctly), `major` (would have to guess something that
  matters), `minor`.
