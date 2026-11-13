---
id: address_house_number
kind: field
step: address
order: 2
type: text
ask_when: "true"
required_when: "true"
depends_on: []
consumers: [employer_hr]
status: confirmed
sources: [F-TR-010]
---

# House number

> **Question to the employee:** What is your house number?

## What? (data and form)
| | |
|---|---|
| Type | `text` |
| Step | [Home address](../flow.md#address) (step 2, position 2) |

**Validation**
- required non-empty after trimming whitespace
- free text (allows e.g. '12a')

## When do we ask?
always

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
Nothing – asked independently of other answers.

## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Muster AG HR (correspondence, payroll admin, first-day logistics) | Postal address for mailed documents | Number |

## Evidence
- **F-TR-010** (hr_transcript): The address must be complete with street, house number, postcode, town and country, because HR posts many documents to employees.
  - "Street, number, postcode, town, country. We post a lot of documents to people, so it has to be complete." — T-014, Anna

_Trace judge: partial – Required house number for HR is backed, but the free-text allowing '12a' is not stated in the cited facts._
