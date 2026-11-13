---
id: residence_canton
kind: field
step: address
order: 6
type: enum
options: ["AG", "AR", "AI", "BL", "BS", "BE", "FR", "GE", "GL", "GR", "JU", "LU", "NE", "NW", "OW", "SH", "SZ", "SO", "SG", "TG", "TI", "UR", "VS", "VD", "ZG", "ZH"]
ask_when: "address_country == \"CH\""
required_when: "true"
depends_on: [address_country]
consumers: [pension_fund]
status: inferred
sources: [F-SC-005, F-SC-006, F-SC-015, F-SC-018]
---

# Canton

> **Question to the employee:** In which canton do you live?

**Status: inferred** – parts of this field rest on inferred facts; see Evidence.

## What? (data and form)
| | |
|---|---|
| Type | `enum` |
| Step | [Home address](../flow.md#address) (step 2, position 6) |

**Options** (store the value, show the label):

| Value | Label |
|---|---|
| `AG` | Aargau |
| `AR` | Appenzell Ausserrhoden |
| `AI` | Appenzell Innerrhoden |
| `BL` | Basel-Landschaft |
| `BS` | Basel-Stadt |
| `BE` | Bern |
| `FR` | Fribourg |
| `GE` | Geneva |
| `GL` | Glarus |
| `GR` | Graubünden |
| `JU` | Jura |
| `LU` | Lucerne |
| `NE` | Neuchâtel |
| `NW` | Nidwalden |
| `OW` | Obwalden |
| `SH` | Schaffhausen |
| `SZ` | Schwyz |
| `SO` | Solothurn |
| `SG` | St. Gallen |
| `TG` | Thurgau |
| `TI` | Ticino |
| `UR` | Uri |
| `VS` | Valais |
| `VD` | Vaud |
| `ZG` | Zug |
| `ZH` | Zurich |

**Validation**
- must be one of the 26 option values

## When do we ask?
`address_country == "CH"`

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
- `address_country` ([field](./address_country.md))

## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Pensionskasse Muster (BVG registration via employer portal) | BVG registration (required 'Canton' dropdown) | Canton |

## Notes
Option values are the official two-letter canton abbreviations; labels match the portal exactly. Only asked of Swiss residents because the portal lists only Swiss cantons. What the fund needs for residents abroad, and whether 'Canton' means residence canton or work canton, is unresolved (OQ-03).

## Evidence
- **F-SC-005** (pension_portal): The pension fund registration form has a required 'Canton' dropdown.
  - "Canton" — 01-empty.png (S01-E14)
  - "Please select" — 01-empty.png (S01-E15)
- **F-SC-006** (pension_portal): The Canton dropdown offers exactly 26 Swiss cantons: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for living outside Switzerland.
  - "Canton" — 02-canton-list.png (S02-E14)
  - "Aargau" — 02-canton-list.png (S02-E16)
  - "Appenzell Ausserrhoden" — 02-canton-list.png (S02-E17)
  - "Appenzell Innerrhoden" — 02-canton-list.png (S02-E18)
  - "Basel-Landschaft" — 02-canton-list.png (S02-E19)
  - "Basel-Stadt" — 02-canton-list.png (S02-E20)
  - "Bern" — 02-canton-list.png (S02-E21)
  - "Fribourg" — 02-canton-list.png (S02-E22)
  - "Geneva" — 02-canton-list.png (S02-E23)
  - "Glarus" — 02-canton-list.png (S02-E24)
  - "Graubünden" — 02-canton-list.png (S02-E25)
  - "Jura" — 02-canton-list.png (S02-E26)
  - "Lucerne" — 02-canton-list.png (S02-E27)
  - "Neuchâtel" — 02-canton-list.png (S02-E28)
  - "Nidwalden" — 02-canton-list.png (S02-E29)
  - "Obwalden" — 02-canton-list.png (S02-E30)
  - "Schaffhausen" — 02-canton-list.png (S02-E31)
  - "Schwyz" — 02-canton-list.png (S02-E32)
  - "Solothurn" — 02-canton-list.png (S02-E33)
  - "St. Gallen" — 02-canton-list.png (S02-E34)
  - "Thurgau" — 02-canton-list.png (S02-E35)
  - "Ticino" — 02-canton-list.png (S02-E36)
  - "Uri" — 02-canton-list.png (S02-E37)
  - "Valais" — 02-canton-list.png (S02-E38)
  - "Vaud" — 02-canton-list.png (S02-E39)
  - "Zug" — 02-canton-list.png (S02-E40)
  - "Zurich" — 02-canton-list.png (S02-E41)
- **F-SC-015** (pension_portal): Each missing required field shows an error of the form '<Field label> is required.': 'First name is required.', 'Last name is required.', 'Date of birth is required.', 'Canton is required.', 'Insurance start date is required.', 'Civil status is required.'
  - "First name is required." — 06-required-errors.png (S06-E09)
  - "Last name is required." — 06-required-errors.png (S06-E12)
  - "Date of birth is required." — 06-required-errors.png (S06-E16)
  - "Canton is required." — 06-required-errors.png (S06-E19)
  - "Insurance start date is required." — 06-required-errors.png (S06-E24)
  - "Civil status is required." — 06-required-errors.png (S06-E27)
- **F-SC-018** (pension_portal, inferred): The Canton dropdown lists only Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. cross-border commuter), and whether 'Canton' means residence canton or work canton.
  - "Canton" — 02-canton-list.png (S02-E14)
  - "Zurich" — 02-canton-list.png (S02-E41)

_Trace judge: partial – The 26 labels and required status are backed, but the two-letter option values and the ask_when address_country=="CH" restriction are not backed by the cited facts (F-SC-018 leaves residents abroad and residence-vs-work canton unresolved)._
