---
id: address_postcode
kind: field
step: address
order: 3
type: text
ask_when: "true"
required_when: "true"
depends_on: []
consumers: [employer_hr]
status: confirmed
sources: [F-TR-010, G-06]
---

# Postcode

> **Question to the employee:** What is your postcode?

## What? (data and form)
| | |
|---|---|
| Type | `text` |
| Step | [Home address](../flow.md#address) (step 2, position 3) |

**Validation**
- required non-empty after trimming whitespace
- free text; no country-specific format check (none given by the sources)

## When do we ask?
always

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
Nothing – asked independently of other answers.

## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Muster AG HR (correspondence, payroll admin, first-day logistics) | Postal address for mailed documents | Postcode |

## Evidence
- **F-TR-010** (hr_transcript): The address must be complete with street, house number, postcode, town and country, because HR posts many documents to employees.
  - "Street, number, postcode, town, country. We post a lot of documents to people, so it has to be complete." — T-014, Anna
- **G-06** (product owner guidance): The sources are fictional and simplified. **Treat them as the truth**, even where they differ from real Swiss law or general knowledge. Never import rules from outside knowledge; if a source does not say it, it is open.

_Trace judge: supported – Postcode is required for HR address, and no format check is consistent with G-06 (no source gives one)._
