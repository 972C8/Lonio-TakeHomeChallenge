---
id: permit_type
kind: field
step: citizenship
order: 2
type: enum
options: ["B", "C", "other"]
ask_when: "address_country == \"CH\" and nationality != \"CH\""
required_when: "true"
depends_on: [address_country, nationality]
consumers: [source_tax, employer_hr]
status: inferred
sources: [F-TR-025, F-TR-026, F-TR-040, F-TR-042, F-TR-029, G-10]
---

# Residence permit

> **Question to the employee:** Which Swiss residence permit do you have?
>
> _Help text:_ Choose the permit type shown on your permit card. A C permit means a settlement permit.

**Status: inferred** – parts of this field rest on inferred facts; see Evidence.

## What? (data and form)
| | |
|---|---|
| Type | `enum` |
| Step | [Nationality and permit](../flow.md#citizenship) (step 3, position 2) |

**Options** (store the value, show the label):

| Value | Label |
|---|---|
| `B` | B permit |
| `C` | C permit |
| `other` | Other permit / no permit yet |

**Validation**
- must be one of the option values

## When do we ask?
`address_country == "CH" and nationality != "CH"` (and the step condition `address_country == "CH"`)

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
- `address_country` ([field](./address_country.md))
- `nationality` ([field](./nationality.md))

Used by: `spouse_nationality`, `spouse_permit_type`, `spouse_residence_country`, `subject_to_source_tax`
## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Source tax tariff determination (Canton of Zurich calculator) | Liability check: C permit holders are not subject to source tax | permit type (liability check) |
| Muster AG HR (correspondence, payroll admin, first-day logistics) | First-day logistics: remind the employee to bring the permit | permit |

## Notes
Only B and C appear in the sources. 'other' covers everything else until the calculator's permit list is known (OQ-06).

## Evidence
- **F-TR-025** (hr_transcript): Correction: non-Swiss employees holding a C permit are not subject to source tax; they are treated like Swiss people for this.
  - "No, that's actually not right." — T-038, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — T-038, Anna
  - "Okay, so non-Swiss, but not with a C permit." — T-039, Leo
- **F-TR-026** (hr_transcript): Example: Maria in sales is Portuguese with a C permit and does not pay source tax.
  - "I'm thinking of Maria in sales, she's Portuguese, and she doesn't do source tax at all. She has a C permit." — T-038, Anna
- **F-TR-040** (hr_transcript, inferred): Consolidated final rule (Anna hedged completeness with 'I think'): an employee is subject to source tax if residence_country is not CH (regardless of nationality). If living in CH: not subject if nationality is CH; not subject if permit_type is C; not subject if married to a spouse who is Swiss or holds a C permit and lives in CH; otherwise subject.
  - "If you don't have a Swiss passport, you do source tax." — T-010, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — T-038, Anna
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Those people do source tax because they work here and they don't live here. And there it doesn't matter what passport you have, by the way." — T-048, Anna
  - "I think that's it." — T-048, Anna
- **F-TR-042** (hr_transcript, inferred): Non-Swiss employees' permit type (at least whether it is a C permit) is needed to determine source tax liability.
  - "So, not the people with a C permit." — T-038, Anna
- **F-TR-029** (hr_transcript): Anna would love the form to remind employees to bring their permit (on the first day), because half of them forget; wording to be looked at later, not decided.
  - "What I would love is if the form could remind people to bring their permit. Half of them forget." — T-042, Anna
  - "We can look at the wording later." — T-043, Leo
- **G-10** (product owner guidance): Option values (stored values) for enums: permit types use the official letter as value ("B", "C", ...; a value "other" if needed); civil status uses lower-case snake_case of the label ("single", "married", "divorced", "widowed", ...). Labels are free.

_Trace judge: supported – The C-permit exemption (F-TR-025/040/042), the first-day permit reminder (F-TR-029), and the option values (G-10) back the field and its ask condition._
