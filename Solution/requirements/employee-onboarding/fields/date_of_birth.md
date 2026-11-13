---
id: date_of_birth
kind: field
step: personal
order: 3
type: date
format: "stored YYYY-MM-DD; displayed DD.MM.YYYY"
ask_when: "true"
required_when: "true"
depends_on: []
consumers: [pension_fund]
status: confirmed
sources: [F-SC-003, F-SC-004, F-SC-015, G-09]
---

# Date of birth

> **Question to the employee:** What is your date of birth?
>
> _Help text:_ Format DD.MM.YYYY.

## What? (data and form)
| | |
|---|---|
| Type | `date` |
| Format | stored YYYY-MM-DD; displayed DD.MM.YYYY |
| Step | [Personal details](../flow.md#personal) (step 1, position 3) |

**Validation**
- must be a valid calendar date
- must not be in the future

## When do we ask?
always

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
Nothing – asked independently of other answers.

## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Pensionskasse Muster (BVG registration via employer portal) | BVG registration (required field, DD.MM.YYYY) | Date of birth |

## Evidence
- **F-SC-003** (pension_portal): The pension fund registration form has a required 'Date of birth' field (text input).
  - "Date of birth" — 01-empty.png (S01-E12)
- **F-SC-004** (pension_portal): Date of birth is entered in the format DD.MM.YYYY.
  - "DD.MM.YYYY" — 01-empty.png (S01-E13)
- **F-SC-015** (pension_portal): Each missing required field shows an error of the form '<Field label> is required.': 'First name is required.', 'Last name is required.', 'Date of birth is required.', 'Canton is required.', 'Insurance start date is required.', 'Civil status is required.'
  - "First name is required." — 06-required-errors.png (S06-E09)
  - "Last name is required." — 06-required-errors.png (S06-E12)
  - "Date of birth is required." — 06-required-errors.png (S06-E16)
  - "Canton is required." — 06-required-errors.png (S06-E19)
  - "Insurance start date is required." — 06-required-errors.png (S06-E24)
  - "Civil status is required." — 06-required-errors.png (S06-E27)
- **G-09** (product owner guidance): Countries as ISO 3166-1 alpha-2 codes; Switzerland = "CH". Dates as ISO YYYY-MM-DD internally; display DD.MM.YYYY. Questionnaire language: English.

_Trace judge: partial – Required field, DD.MM.YYYY display and ISO storage are backed, but the validation rules (valid calendar date, not in the future) are not supported by any cited fact._
