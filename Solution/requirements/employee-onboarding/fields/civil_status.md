---
id: civil_status
kind: field
step: family
order: 1
type: enum
options: ["single", "married", "divorced", "widowed"]
ask_when: "true"
required_when: "true"
depends_on: []
consumers: [pension_fund, source_tax]
status: inferred
sources: [F-TR-020, F-TR-022, F-SC-009, F-SC-010, F-SC-015, F-TR-031, F-TR-030, F-TR-023, F-SC-019, G-07, G-10]
---

# Civil status

> **Question to the employee:** What is your civil status?

**Status: inferred** – parts of this field rest on inferred facts; see Evidence.

## What? (data and form)
| | |
|---|---|
| Type | `enum` |
| Step | [Civil status and spouse](../flow.md#family) (step 5, position 1) |

**Options** (store the value, show the label):

| Value | Label |
|---|---|
| `single` | Single |
| `married` | Married |
| `divorced` | Divorced |
| `widowed` | Widowed |

**Validation**
- must be one of the option values

## When do we ask?
always

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
Nothing – asked independently of other answers.

Used by: `spouse_date_of_birth`, `spouse_nationality`, `spouse_permit_type`, `spouse_residence_country`, `spouse_employed`, `subject_to_source_tax`
## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Pensionskasse Muster (BVG registration via employer portal) | BVG registration (required dropdown) | Civil status |
| Source tax tariff determination (Canton of Zurich calculator) | Married employees may be exempt via their spouse; it also changes the calculator's questions | civil status |

## Notes
The options are exactly the portal's four (G-07). Registered partnership is not supported by the portal (OQ-04).

## Evidence
- **F-TR-020** (hr_transcript): The pension fund asks for the employee's civil status.
  - "Yes, the civil status. They ask for that." — T-032, Anna
- **F-TR-022** (hr_transcript): Civil status options are, per Anna's uncertain recollection, single, married, divorced, and 'I think' widowed; she defers to the pension fund screenshots for the actual list.
  - "I'd have to look. You'll see it in the screenshots. Single, married, divorced, I think widowed." — T-034, Anna
- **F-SC-009** (pension_portal): The pension fund registration form has a required 'Civil status' dropdown.
  - "Civil status" — 01-empty.png (S01-E19)
  - "Please select" — 01-empty.png (S01-E20)
- **F-SC-010** (pension_portal): The Civil status dropdown offers exactly four options: Single, Married, Divorced, Widowed.
  - "Civil status" — 03-civil-status-list.png (S03-E19)
  - "Single" — 03-civil-status-list.png (S03-E21)
  - "Married" — 03-civil-status-list.png (S03-E22)
  - "Divorced" — 03-civil-status-list.png (S03-E23)
  - "Widowed" — 03-civil-status-list.png (S03-E24)
- **F-SC-015** (pension_portal): Each missing required field shows an error of the form '<Field label> is required.': 'First name is required.', 'Last name is required.', 'Date of birth is required.', 'Canton is required.', 'Insurance start date is required.', 'Civil status is required.'
  - "First name is required." — 06-required-errors.png (S06-E09)
  - "Last name is required." — 06-required-errors.png (S06-E12)
  - "Date of birth is required." — 06-required-errors.png (S06-E16)
  - "Canton is required." — 06-required-errors.png (S06-E19)
  - "Insurance start date is required." — 06-required-errors.png (S06-E24)
  - "Civil status is required." — 06-required-errors.png (S06-E27)
- **F-TR-031** (hr_transcript): An employee married to a Swiss national or to a C permit holder who lives in Switzerland is not subject to source tax (e.g. Tomás: Brazilian, B permit, Swiss wife, living in Winterthur).
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." — T-044, Anna
- **F-TR-030** (hr_transcript): For married employees subject to source tax, the Zurich calculator asks whether the spouse works.
  - "It changes the questions in the calculator, yes. Whether the husband or wife works." — T-044, Anna
- **F-TR-023** (hr_transcript): At least one current employee (Daniel in finance) is in a registered partnership, so this civil status occurs in practice.
  - "we do have one colleague in a registered partnership. Daniel, in finance." — T-034, Anna
- **F-SC-019** (pension_portal, inferred): The Civil status list has no option for registered partnership, separated, or other statuses; it is open how employees with such statuses are registered and whether a partner's date of birth is then needed.
  - "Single" — 03-civil-status-list.png (S03-E21)
  - "Widowed" — 03-civil-status-list.png (S03-E24)
- **G-07** (product owner guidance): The pension fund screenshots show dropdowns with **all** their options.
- **G-10** (product owner guidance): Option values (stored values) for enums: permit types use the official letter as value ("B", "C", ...; a value "other" if needed); civil status uses lower-case snake_case of the label ("single", "married", "divorced", "widowed", ...). Labels are free.

_Trace judge: supported – The fund's required dropdown with exactly four options (F-SC-009/010, G-07), the source-tax use (F-TR-031/030), and the values (G-10) are all backed._
