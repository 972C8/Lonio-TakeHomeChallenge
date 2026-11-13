---
id: spouse_permit_type
kind: field
step: family
order: 4
type: enum
options: ["B", "C", "other"]
ask_when: "civil_status == \"married\" and address_country == \"CH\" and nationality != \"CH\" and permit_type != \"C\" and spouse_nationality != \"CH\""
required_when: "true"
depends_on: [address_country, civil_status, nationality, permit_type, spouse_nationality]
consumers: [source_tax]
status: inferred
sources: [F-TR-031, F-TR-034, F-TR-035, F-TR-044, G-10]
---

# Spouse's residence permit

> **Question to the employee:** Which Swiss residence permit does your spouse have?
>
> _Help text:_ Choose 'Other permit / no permit' if your spouse has no Swiss permit, for example because they live abroad.

**Status: inferred** – parts of this field rest on inferred facts; see Evidence.

## What? (data and form)
| | |
|---|---|
| Type | `enum` |
| Step | [Civil status and spouse](../flow.md#family) (step 5, position 4) |

**Options** (store the value, show the label):

| Value | Label |
|---|---|
| `B` | B permit |
| `C` | C permit |
| `other` | Other permit / no permit |

**Validation**
- must be one of the option values

## When do we ask?
`civil_status == "married" and address_country == "CH" and nationality != "CH" and permit_type != "C" and spouse_nationality != "CH"`

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
- `address_country` ([field](./address_country.md))
- `civil_status` ([field](./civil_status.md))
- `nationality` ([field](./nationality.md))
- `permit_type` ([field](./permit_type.md))
- `spouse_nationality` ([field](./spouse_nationality.md))

Used by: `spouse_residence_country`, `subject_to_source_tax`
## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Source tax tariff determination (Canton of Zurich calculator) | Spouse exemption: married to a C permit holder who lives in CH means no source tax | spouse permit type (liability check) |

## Notes
Uses the same option set as permit_type (OQ-06).

## Evidence
- **F-TR-031** (hr_transcript): An employee married to a Swiss national or to a C permit holder who lives in Switzerland is not subject to source tax (e.g. Tomás: Brazilian, B permit, Swiss wife, living in Winterthur).
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." — T-044, Anna
- **F-TR-034** (hr_transcript): For married employees (source tax determination), the spouse's permit type is needed if the spouse has one.
  - "their permit if they have one" — T-046, Anna
- **F-TR-035** (hr_transcript, inferred): The spouse's permit is only relevant when the spouse is not Swiss (Swiss nationals have no permit).
  - "their permit if they have one" — T-046, Anna
- **F-TR-044** (hr_transcript, inferred): Spouse nationality, permit and residence only need to be asked when the employee is married and the spouse exemption could apply (i.e. employee is non-Swiss without C permit and lives in CH).
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "And there it doesn't matter what passport you have, by the way." — T-048, Anna
- **G-10** (product owner guidance): Option values (stored values) for enums: permit types use the official letter as value ("B", "C", ...; a value "other" if needed); civil status uses lower-case snake_case of the label ("single", "married", "divorced", "widowed", ...). Labels are free.

_Trace judge: supported – The spouse's permit matters only for non-Swiss spouses (F-TR-034/035) and only when the exemption could apply (F-TR-044), with option values per G-10._
