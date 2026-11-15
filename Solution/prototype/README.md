# Employee onboarding questionnaire – prototype

A clickable prototype of the employee side of the feature spec in
[`../requirements/employee-onboarding/`](../requirements/employee-onboarding/feature.md).
It implements the employee side of the 40 user stories and their acceptance criteria, and nothing more.
Vite + vanilla TypeScript, no backend. Answers live in the browser (`localStorage`).

## Run it

Needs Node 18 or newer.

```bash
cd Solution/prototype
npm install
npm run dev      # opens on http://localhost:5173
npm test         # every example table of the spec, read from build/, plus a few validation checks
npm run build    # type check + production build into dist/
```

## How it maps to the spec

| Step (D-047) | Shown when | Stories |
|---|---|---|
| 1. About you (name, date of birth, first working day) | always | US-02.1, US-03.1 |
| 2. Home address (as on the first working day; canton only in Switzerland) | always | US-02.2, US-02.3, US-02.4 |
| 3. Nationality and C permit | only if living in Switzerland | US-05.1 |
| 4. Civil status and spouse | always (spouse questions where they apply) | US-04.1, US-04.2, US-05.2 |
| 5. Cross-border commuting | only if living in Germany or Liechtenstein | US-08.2, US-08.3, US-08.4 |
| 6. Source tax details (denomination, spouse employed, children yes/no) | subject to source tax, except Liechtenstein residents who are in principle not liable | US-06.2, US-06.3, US-07.1 |
| 7. Children (one block per child) | if the employee has children | US-07.2 to US-07.5 |
| 8. Summary and submission (with the permit reminder) | always | US-01.4, US-01.5, US-01.8 |

Derived values (never asked) are computed in `src/rules.ts`: insurance start date
(US-03.2), canton and civil status for the fund (US-02.4, US-04.4), civil status and
residence for the calculator (US-04.3, US-05.4, US-08.1), source tax liability
(US-05.3), child results and child digit (US-07.6), base and cross-border tariff letter
(US-06.4, US-06.5), the tariff code (US-06.6) and the Liechtenstein DTA note (US-08.5).

- `src/rules.ts` – the business rules as pure functions, plus when each question is asked.
- `src/questions.ts` – steps, question wording, validation, and dropping answers that no longer apply.
- `src/record.ts` – what is recorded on submission (applicable answers + derived values).
- `src/main.ts` – the page.
- `tests/spec-examples.test.ts` – runs **every example table of the spec** against the
  prototype. It reads them from `../build/employee-onboarding/spec.json`, maps each
  information item to an answer field and each business rule to a function, so a
  pipeline run that changes the requirements turns these tests red until the
  prototype follows. 268 examples, all passing.
- `tests/validation.test.ts` – rules the spec states only as text (date limits, house
  number, step order).

Answers are saved as the employee goes and can be resumed until submission (US-01.7).
Answers to questions that stop applying are kept in the draft while the employee goes
back and forth, and are dropped on submission (US-01.5). After submission the
questionnaire is read-only (US-01.6).

## Prototype-only parts and choices

- **"Recorded on submission" panel.** After submitting, the page shows what Lonio
  records per party (pension fund, HR) and the full JSON. In the product this goes
  to HR, not to the employee; how it is transmitted is out of scope (G-04, D-034).
- **Reset link** to start a new questionnaire, so the flow can be tried repeatedly.
- **Permit reminder wording** is a placeholder; HR provides the real text before go-live (D-050).
- **"Sent" date** for the one-year window of the first working day is the day the
  prototype was first opened in this browser.
- **Children:** answering "yes" to having children requires adding at least one child.
  The spec's review still lists this as unconfirmed.
- **Missing answers block "Next"** within a step. Whether they should block only the
  submission is an open review finding; the prototype keeps the stricter behaviour.
- **Steps hide** once earlier answers show they cannot apply.

Not built, as out of scope: HR screens and HR changes after submission (including the
"incomplete - HR must complete" result, D-048, D-053), sending data to the fund or the
tax office, auth, uploads, AHV data, photos, IT equipment. Decisions marked as
assumptions in the spec (for example canton Zurich for employees abroad, D-002) are
implemented as decided and need the same domain-expert check.

See [CHANGES.md](CHANGES.md) for what changed against the previous build.
