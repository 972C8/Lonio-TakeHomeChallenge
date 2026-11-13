---
id: nationality
kind: field
step: citizenship
order: 1
type: country
format: "ISO 3166-1 alpha-2 (Switzerland = \"CH\")"
ask_when: "address_country == \"CH\""
required_when: "true"
depends_on: [address_country]
consumers: [source_tax]
status: inferred
sources: [F-TR-040, F-TR-041, F-TR-037, G-01]
---

# Nationality

> **Question to the employee:** What is your nationality?
>
> _Help text:_ If you have more than one nationality and one of them is Swiss, choose Switzerland.

**Status: inferred** – parts of this field rest on inferred facts; see Evidence.

## What? (data and form)
| | |
|---|---|
| Type | `country` |
| Format | ISO 3166-1 alpha-2 (Switzerland = "CH") |
| Step | [Nationality and permit](../flow.md#citizenship) (step 3, position 1) |

**Validation**
- must be a valid ISO 3166-1 alpha-2 code

## When do we ask?
`address_country == "CH"` (and the step condition `address_country == "CH"`)

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
- `address_country` ([field](./address_country.md))

Used by: `permit_type`, `spouse_nationality`, `spouse_permit_type`, `spouse_residence_country`, `subject_to_source_tax`
## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Source tax tariff determination (Canton of Zurich calculator) | Liability check: Swiss nationals living in CH are not subject to source tax | nationality (liability check) |

## Notes
Not asked of residents abroad, because they are subject regardless of nationality (F-TR-037). Whether the calculator itself needs nationality is open (OQ-01). The dual-nationality help text rests on 'If you don't have a Swiss passport'.

## Evidence
- **F-TR-040** (hr_transcript, inferred): Consolidated final rule (Anna hedged completeness with 'I think'): an employee is subject to source tax if residence_country is not CH (regardless of nationality). If living in CH: not subject if nationality is CH; not subject if permit_type is C; not subject if married to a spouse who is Swiss or holds a C permit and lives in CH; otherwise subject.
  - "If you don't have a Swiss passport, you do source tax." — T-010, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — T-038, Anna
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Those people do source tax because they work here and they don't live here. And there it doesn't matter what passport you have, by the way." — T-048, Anna
  - "I think that's it." — T-048, Anna
- **F-TR-041** (hr_transcript, inferred): The employee's nationality is needed to determine source tax liability.
  - "If you don't have a Swiss passport, you do source tax." — T-010, Anna
- **F-TR-037** (hr_transcript): Employees who live abroad and work in Switzerland are always subject to source tax, regardless of nationality (e.g. Stefan, Swiss, lives in Konstanz; a warehouse employee lives in Liechtenstein).
  - "Those people do source tax because they work here and they don't live here. And there it doesn't matter what passport you have, by the way." — T-048, Anna
  - "Stefan is actually Swiss, and he still has it." — T-048, Anna
  - "So someone living abroad and working here always does it?" — T-049, Leo
  - "Yes." — T-050, Anna
- **G-01** (product owner guidance): Lonio collects onboarding data from a new employee **once** and reuses it for every receiving party. Asking too little blocks a registration; asking too much collects personal data we must not have (data minimisation). A question must only be asked when at least one receiving party needs the answer for this person.

_Trace judge: supported – Source-tax liability needs nationality for people living in CH (F-TR-040/041), residents abroad are always subject (F-TR-037), and G-01 backs asking only when needed._
