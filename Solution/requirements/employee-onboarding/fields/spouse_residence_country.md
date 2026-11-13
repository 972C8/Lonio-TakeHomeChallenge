---
id: spouse_residence_country
kind: field
step: family
order: 5
type: country
format: "ISO 3166-1 alpha-2 (Switzerland = \"CH\")"
ask_when: "civil_status == \"married\" and address_country == \"CH\" and nationality != \"CH\" and permit_type != \"C\" and (spouse_nationality == \"CH\" or spouse_permit_type == \"C\")"
required_when: "true"
depends_on: [address_country, civil_status, nationality, permit_type, spouse_nationality, spouse_permit_type]
consumers: [source_tax]
status: inferred
sources: [F-TR-031, F-TR-036, F-TR-044, F-TR-045]
---

# Spouse's country of residence

> **Question to the employee:** In which country does your spouse live?

**Status: inferred** – parts of this field rest on inferred facts; see Evidence.

## What? (data and form)
| | |
|---|---|
| Type | `country` |
| Format | ISO 3166-1 alpha-2 (Switzerland = "CH") |
| Step | [Civil status and spouse](../flow.md#family) (step 5, position 5) |

**Validation**
- must be a valid ISO 3166-1 alpha-2 code

## When do we ask?
`civil_status == "married" and address_country == "CH" and nationality != "CH" and permit_type != "C" and (spouse_nationality == "CH" or spouse_permit_type == "C")`

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
- `address_country` ([field](./address_country.md))
- `civil_status` ([field](./civil_status.md))
- `nationality` ([field](./nationality.md))
- `permit_type` ([field](./permit_type.md))
- `spouse_nationality` ([field](./spouse_nationality.md))
- `spouse_permit_type` ([field](./spouse_permit_type.md))

Used by: `subject_to_source_tax`
## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Source tax tariff determination (Canton of Zurich calculator) | Spouse exemption applies only if the spouse lives in CH | spouse lives in Switzerland (liability check) |

## Notes
Only relevant when the spouse is Swiss or holds a C permit. 'Lives here' is interpreted as CH (F-TR-045).

## Evidence
- **F-TR-031** (hr_transcript): An employee married to a Swiss national or to a C permit holder who lives in Switzerland is not subject to source tax (e.g. Tomás: Brazilian, B permit, Swiss wife, living in Winterthur).
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." — T-044, Anna
- **F-TR-036** (hr_transcript): For married employees (source tax determination), whether the spouse lives in Switzerland is needed.
  - "and that they live here." — T-046, Anna
- **F-TR-044** (hr_transcript, inferred): Spouse nationality, permit and residence only need to be asked when the employee is married and the spouse exemption could apply (i.e. employee is non-Swiss without C permit and lives in CH).
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "And there it doesn't matter what passport you have, by the way." — T-048, Anna
- **F-TR-045** (hr_transcript, inferred): 'Lives here' in Anna's statements means living in Switzerland.
  - "and they live in Winterthur." — T-044, Anna
  - "they work here and they don't live here." — T-048, Anna

_Trace judge: partial – Facts support asking spouse residence for the exemption, but the country-type ISO alpha-2 format/validation and required_when=true are not backed, and the 'ask_when' narrowing is only inferred, since facts only give 'lives here' (in CH), not a country field._
