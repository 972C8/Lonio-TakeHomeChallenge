# Employee onboarding questionnaire – prototype

A clickable prototype of the employee side of the feature spec in
[`../requirements/employee-onboarding/`](../requirements/employee-onboarding/feature.md).
It implements the 28 user stories and their acceptance criteria, and nothing more.
Vite + vanilla TypeScript, no backend. Answers live in the browser (`localStorage`).

## Run it

Needs Node 18 or newer.

```bash
cd Solution/prototype
npm install
npm run dev      # opens on http://localhost:5173
npm test         # the acceptance-criteria example tables as tests
npm run build    # type check + production build into dist/
```

## How it maps to the spec

| Step | Shown when | Stories |
|---|---|---|
| 1. Personal details | always | US-01.1 |
| 2. Home address (canton only if living in Switzerland) | always | US-01.2, US-01.3, US-01.4 |
| 3. Nationality and permit | only if living in Switzerland | US-04.1 |
| 4. Employment (first working day) | always | US-02.1 |
| 5. Family (civil status, spouse details where needed) | always | US-03.1, US-03.2, US-04.2 |
| 6. Source tax (denomination, spouse works, children, Germany / Liechtenstein questions) | only if subject to source tax | US-05.3, US-05.4, US-06.1–06.5, US-07.2, US-07.3 |
| 7. Review and submit (with the permit reminder) | always | US-08.1, US-08.2 |

Derived values (never asked) are computed in `src/rules.ts`: insurance start date
(US-02.2), civil status for the fund and for source tax (US-03.3, US-03.4),
residence and liability (US-01.3, US-04.3, US-07.1), child results, child digit
and H tariff (US-06.6), cross-border and Liechtenstein outcomes (US-07.2, US-07.3),
tariff letter and the full source tax result (US-05.6, US-05.7).

- `src/rules.ts` – the business rules as pure functions, plus when each question is asked.
- `src/questions.ts` – steps, question wording, validation, and dropping answers that no longer apply.
- `src/record.ts` – what is recorded on submission (applicable answers + derived values).
- `src/main.ts` – the page.
- `tests/examples.test.ts` – the example tables from the acceptance criteria, named by AC.

Answers to questions that stop applying are kept in the draft while the employee goes
back and forth, and are dropped on submission (US-08.2). After submission the
questionnaire is read-only (AC-02.1.4).

## Prototype-only parts and choices

- **"Recorded on submission" panel.** After submitting, the page shows what Lonio
  records per party (pension fund, HR) and the full JSON. In the product this goes
  to HR, not to the employee; how it is transmitted is out of scope (G-04, D-034).
- **Reset link** to start a new questionnaire, so the flow can be tried repeatedly.
- **Permit reminder wording** is a placeholder; HR provides the real text (AC-08.1.3).
- **Children:** answering "yes" to having children requires adding at least one child.
  The spec only says each added child needs answers.
- **Steps hide** once earlier answers show they cannot apply (e.g. step 3 for
  employees living abroad, step 6 for employees not subject to source tax).

Not built, as out of scope: HR screens, HR changing the first working day,
sending data to the fund or the tax office, auth, uploads, AHV data, photos, IT equipment.
Open questions in the spec (e.g. canton for employees abroad, registered
partnership at the fund) are implemented as the spec's provisional decisions.
