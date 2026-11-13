---
id: address_town
kind: field
step: address
order: 4
type: text
ask_when: "true"
required_when: "true"
depends_on: []
consumers: [employer_hr]
status: confirmed
sources: [F-TR-010]
---

# Town

> **Question to the employee:** What town do you live in?

## What? (data and form)
| | |
|---|---|
| Type | `text` |
| Step | [Home address](../flow.md#address) (step 2, position 4) |

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
| Muster AG HR (correspondence, payroll admin, first-day logistics) | Postal address for mailed documents | Town |

## Evidence
- **F-TR-010** (hr_transcript): The address must be complete with street, house number, postcode, town and country, because HR posts many documents to employees.
  - "Street, number, postcode, town, country. We post a lot of documents to people, so it has to be complete." — T-014, Anna

_Trace judge: supported – Town is part of the complete address HR requires._
