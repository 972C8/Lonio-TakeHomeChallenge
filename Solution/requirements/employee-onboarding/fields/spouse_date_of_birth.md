---
id: spouse_date_of_birth
kind: field
step: family
order: 2
type: date
format: "stored YYYY-MM-DD; displayed DD.MM.YYYY"
ask_when: "civil_status == \"married\""
required_when: "true"
depends_on: [civil_status]
consumers: [pension_fund]
status: confirmed
sources: [F-TR-021, F-SC-011, F-SC-012, F-SC-013, F-SC-016, F-SC-020]
---

# Spouse's date of birth

> **Question to the employee:** What is your spouse's date of birth?
>
> _Help text:_ Format DD.MM.YYYY.

## What? (data and form)
| | |
|---|---|
| Type | `date` |
| Format | stored YYYY-MM-DD; displayed DD.MM.YYYY |
| Step | [Civil status and spouse](../flow.md#family) (step 5, position 2) |

**Validation**
- must be a valid calendar date
- must not be in the future

## When do we ask?
`civil_status == "married"`

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
- `civil_status` ([field](./civil_status.md))

## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Pensionskasse Muster (BVG registration via employer portal) | BVG registration (required when civil status is Married) | Spouse's date of birth |

## Evidence
- **F-TR-021** (hr_transcript): If the employee is married, the pension fund wants the spouse's date of birth.
  - "And if someone is married, they want the date of birth of the husband or wife." — T-032, Anna
- **F-SC-011** (pension_portal): The pension fund registration form has a 'Spouse's date of birth' field, marked required when shown.
  - "Spouse's date of birth" — 05-married.png (S05-E21)
- **F-SC-012** (pension_portal): Spouse's date of birth is entered in the format DD.MM.YYYY.
  - "DD.MM.YYYY" — 05-married.png (S05-E23)
- **F-SC-013** (pension_portal): 'Spouse's date of birth' appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in 01, 02, 03, 06 (civil status not selected).
  - "Married" — 05-married.png (S05-E20)
  - "Spouse's date of birth" — 05-married.png (S05-E21)
  - "Married" — 07-married-missing-spouse.png (S07-E20)
  - "Spouse's date of birth" — 07-married-missing-spouse.png (S07-E21)
  - "Single" — 04-single.png (S04-E20)
- **F-SC-016** (pension_portal): When Civil status is Married and Spouse's date of birth is empty, registration is rejected with 'Spouse's date of birth is required.'
  - "Married" — 07-married-missing-spouse.png (S07-E20)
  - "Spouse's date of birth is required." — 07-married-missing-spouse.png (S07-E24)
- **F-SC-020** (pension_portal, inferred): No screenshot shows the form with Civil status 'Divorced' or 'Widowed'; whether Spouse's date of birth is hidden for those values is assumed but not proven.
  - "Divorced" — 03-civil-status-list.png (S03-E23)
  - "Widowed" — 03-civil-status-list.png (S03-E24)

_Trace judge: partial – Asking when married, required, and the DD.MM.YYYY format are backed, but the 'must not be in the future' validation is not backed by any cited fact._
