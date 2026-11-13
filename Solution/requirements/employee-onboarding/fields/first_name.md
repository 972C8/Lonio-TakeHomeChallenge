---
id: first_name
kind: field
step: personal
order: 1
type: text
ask_when: "true"
required_when: "true"
depends_on: []
consumers: [pension_fund, employer_hr]
status: inferred
sources: [F-SC-001, F-SC-015, F-TR-010]
---

# First name

> **Question to the employee:** What is your first name?
>
> _Help text:_ As shown on your passport or ID card.

**Status: inferred** – parts of this field rest on inferred facts; see Evidence.

## What? (data and form)
| | |
|---|---|
| Type | `text` |
| Step | [Personal details](../flow.md#personal) (step 1, position 1) |

**Validation**
- required non-empty after trimming whitespace

## When do we ask?
always

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
Nothing – asked independently of other answers.

## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Pensionskasse Muster (BVG registration via employer portal) | BVG registration (required field) | First name |
| Muster AG HR (correspondence, payroll admin, first-day logistics) | Correspondence and payroll administration | First name |

## Notes
Required by the pension portal. HR's need for the name for addressing post is inferred from F-TR-010.

## Evidence
- **F-SC-001** (pension_portal): The pension fund registration form has a required 'First name' text field.
  - "First name" — 01-empty.png (S01-E10)
  - "Fields marked * are required." — 01-empty.png (S01-E23)
- **F-SC-015** (pension_portal): Each missing required field shows an error of the form '<Field label> is required.': 'First name is required.', 'Last name is required.', 'Date of birth is required.', 'Canton is required.', 'Insurance start date is required.', 'Civil status is required.'
  - "First name is required." — 06-required-errors.png (S06-E09)
  - "Last name is required." — 06-required-errors.png (S06-E12)
  - "Date of birth is required." — 06-required-errors.png (S06-E16)
  - "Canton is required." — 06-required-errors.png (S06-E19)
  - "Insurance start date is required." — 06-required-errors.png (S06-E24)
  - "Civil status is required." — 06-required-errors.png (S06-E27)
- **F-TR-010** (hr_transcript): The address must be complete with street, house number, postcode, town and country, because HR posts many documents to employees.
  - "Street, number, postcode, town, country. We post a lot of documents to people, so it has to be complete." — T-014, Anna

_Trace judge: partial – Pension portal required field is backed, but the HR consumer (correspondence and payroll administration) is only weakly inferred from the address quote, and the passport/ID help text and trim validation are not backed by any cited fact._
