---
id: spouse_nationality
kind: field
step: family
order: 3
type: country
format: "ISO 3166-1 alpha-2 (Switzerland = \"CH\")"
ask_when: "civil_status == \"married\" and address_country == \"CH\" and nationality != \"CH\" and permit_type != \"C\""
required_when: "true"
depends_on: [address_country, civil_status, nationality, permit_type]
consumers: [source_tax]
status: inferred
sources: [F-TR-031, F-TR-033, F-TR-040, F-TR-044, F-TR-032]
---

# Spouse's nationality

> **Question to the employee:** What is your spouse's nationality?
>
> _Help text:_ If your spouse has more than one nationality and one of them is Swiss, choose Switzerland.

**Status: inferred** – parts of this field rest on inferred facts; see Evidence.

## What? (data and form)
| | |
|---|---|
| Type | `country` |
| Format | ISO 3166-1 alpha-2 (Switzerland = "CH") |
| Step | [Civil status and spouse](../flow.md#family) (step 5, position 3) |

**Validation**
- must be a valid ISO 3166-1 alpha-2 code

## When do we ask?
`civil_status == "married" and address_country == "CH" and nationality != "CH" and permit_type != "C"`

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
- `address_country` ([field](./address_country.md))
- `civil_status` ([field](./civil_status.md))
- `nationality` ([field](./nationality.md))
- `permit_type` ([field](./permit_type.md))

Used by: `spouse_permit_type`, `spouse_residence_country`, `subject_to_source_tax`
## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Source tax tariff determination (Canton of Zurich calculator) | Spouse exemption: married to a Swiss national who lives in CH means no source tax | spouse nationality (liability check) |

## Notes
Only asked when the spouse exemption could change the outcome (F-TR-044).

## Evidence
- **F-TR-031** (hr_transcript): An employee married to a Swiss national or to a C permit holder who lives in Switzerland is not subject to source tax (e.g. Tomás: Brazilian, B permit, Swiss wife, living in Winterthur).
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." — T-044, Anna
- **F-TR-033** (hr_transcript): For married employees (source tax determination), the spouse's nationality is needed.
  - "So you need to know about the spouse as well." — T-045, Leo
  - "Yes. Their nationality, their permit if they have one, and that they live here." — T-046, Anna
- **F-TR-040** (hr_transcript, inferred): Consolidated final rule (Anna hedged completeness with 'I think'): an employee is subject to source tax if residence_country is not CH (regardless of nationality). If living in CH: not subject if nationality is CH; not subject if permit_type is C; not subject if married to a spouse who is Swiss or holds a C permit and lives in CH; otherwise subject.
  - "If you don't have a Swiss passport, you do source tax." — T-010, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — T-038, Anna
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Those people do source tax because they work here and they don't live here. And there it doesn't matter what passport you have, by the way." — T-048, Anna
  - "I think that's it." — T-048, Anna
- **F-TR-044** (hr_transcript, inferred): Spouse nationality, permit and residence only need to be asked when the employee is married and the spouse exemption could apply (i.e. employee is non-Swiss without C permit and lives in CH).
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "And there it doesn't matter what passport you have, by the way." — T-048, Anna
- **F-TR-032** (hr_transcript): Today HR checks the spouse exemption by hand and asks for spouse data by email, which takes very long.
  - "I always have to check that one by hand." — T-044, Anna
  - "I ask them by email, and it takes forever." — T-046, Anna

_Trace judge: supported – The spouse-exemption rule (F-TR-031/033/040) and the ask condition limited to cases where the exemption could apply (F-TR-044) are backed._
