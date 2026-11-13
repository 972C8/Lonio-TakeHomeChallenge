---
id: address_street
kind: field
step: address
order: 1
type: text
ask_when: "true"
required_when: "true"
depends_on: []
consumers: [employer_hr]
status: confirmed
sources: [F-TR-009, F-TR-010, F-TR-011]
---

# Street

> **Question to the employee:** What street do you live on?

## What? (data and form)
| | |
|---|---|
| Type | `text` |
| Step | [Home address](../flow.md#address) (step 2, position 1) |

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
| Muster AG HR (correspondence, payroll admin, first-day logistics) | Postal address for mailed documents | Street |

## Evidence
- **F-TR-009** (hr_transcript): HR needs the employee's full postal address.
  - "Yes, I need the address, obviously. The full address." — T-014, Anna
- **F-TR-010** (hr_transcript): The address must be complete with street, house number, postcode, town and country, because HR posts many documents to employees.
  - "Street, number, postcode, town, country. We post a lot of documents to people, so it has to be complete." — T-014, Anna
- **F-TR-011** (hr_transcript): Nothing beyond a normal postal address (as written on an envelope) is needed for the address.
  - "No, no. Just a normal address, the way you would write it on an envelope." — T-016, Anna

_Trace judge: supported – HR needs full postal address including street, and nothing extra, so the required text field is backed._
