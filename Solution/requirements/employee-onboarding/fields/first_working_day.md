---
id: first_working_day
kind: field
step: employment
order: 1
type: date
format: "stored YYYY-MM-DD; displayed DD.MM.YYYY"
ask_when: "true"
required_when: "true"
depends_on: []
consumers: [pension_fund, employer_hr]
status: confirmed
sources: [F-TR-015, F-TR-016, F-TR-019, G-08]
---

# First working day

> **Question to the employee:** What is your first working day at Muster AG?
>
> _Help text:_ Please check this date carefully. If it changes, for example because you agree an earlier exit with your current employer, update it here straight away. The pension fund insurance start depends on it.

## What? (data and form)
| | |
|---|---|
| Type | `date` |
| Format | stored YYYY-MM-DD; displayed DD.MM.YYYY |
| Step | [Start of employment](../flow.md#employment) (step 4, position 1) |

**Validation**
- must be a valid calendar date

## When do we ask?
always

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
Nothing – asked independently of other answers.

Used by: `insurance_start_date`
## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Pensionskasse Muster (BVG registration via employer portal) | Basis for the derived insurance start date | Insurance start date (via rule insurance_start_date) |
| Muster AG HR (correspondence, payroll admin, first-day logistics) | Payroll administration and first-day logistics | First working day |

## Evidence
- **F-TR-015** (hr_transcript): The employee's first working day is needed (for the pension fund) and is the most important item; the employee should confirm it.
  - "I need their first working day. That's the number one thing, and I ask them to confirm it" — T-024, Anna
- **F-TR-016** (hr_transcript): The first working day changes often, e.g. when people negotiate an earlier exit with their old employer; a missed update (Julia) caused a wrong date at the fund and weeks of fixing.
  - "because it moves more often than you'd think." — T-024, Anna
  - "She moved her first working day to the 15th of March, and I didn't update it." — T-026, Anna
  - "It took weeks to fix." — T-028, Anna
- **F-TR-019** (hr_transcript, inferred): Consolidated: insurance_start_date is derived from first_working_day: if first_working_day is the 1st of a month, insurance starts that day; otherwise it starts on the 1st of the following month. It should be derived, not asked.
  - "because insurance starts on the first of the following month." — T-026, Anna
  - "Unless somebody starts exactly on the first, of course, then it's just that day." — T-028, Anna
- **G-08** (product owner guidance): Prefer asking for primary facts and **deriving** values (e.g. ask the first working day, derive the insurance start date) instead of asking the employee for values they cannot know.

_Trace judge: supported – The first working day is needed for the fund, is confirmed by the employee, changes often, and the insurance start is derived from it (F-TR-015/016/019, G-08)._
