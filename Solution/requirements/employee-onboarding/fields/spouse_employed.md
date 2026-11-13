---
id: spouse_employed
kind: field
step: source_tax
order: 1
type: boolean
ask_when: "subject_to_source_tax and civil_status == \"married\""
required_when: "true"
depends_on: [civil_status, subject_to_source_tax]
consumers: [source_tax]
status: inferred
sources: [F-TR-030, F-TR-007]
---

# Spouse works

> **Question to the employee:** Does your spouse work (is your spouse gainfully employed)?

**Status: inferred** – parts of this field rest on inferred facts; see Evidence.

## What? (data and form)
| | |
|---|---|
| Type | `boolean` |
| Step | [Source tax details](../flow.md#source_tax) (step 6, position 1) |

**Validation**
- must be answered yes or no

## When do we ask?
`subject_to_source_tax and civil_status == "married"` (and the step condition `subject_to_source_tax`)

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
- `civil_status` ([field](./civil_status.md))
- `subject_to_source_tax` ([rule](../rules/subject_to_source_tax.md))

## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Source tax tariff determination (Canton of Zurich calculator) | Input to the Zurich tariff calculator for married employees | spouse works (calculator question) |

## Notes
Only the transcript supports this; the calculator source has no extracted facts yet (OQ-01). The calculator's exact wording and options are unknown.

## Evidence
- **F-TR-030** (hr_transcript): For married employees subject to source tax, the Zurich calculator asks whether the spouse works.
  - "It changes the questions in the calculator, yes. Whether the husband or wife works." — T-044, Anna
- **F-TR-007** (hr_transcript): The Zurich source tax calculator (canton website, yields the tariff code) is used for every employee regardless of where they actually belong; Anna acknowledges this is not exactly correct but it is what they do for now, and Leo agrees to keep it.
  - "I use the Zurich calculator on the canton's website. The one that gives you the tariff code." — T-012, Anna
  - "For everybody I use Zurich, by the way. I know it's not exactly how it works, but that's what we do for now." — T-012, Anna
  - "Understood. We'll keep that for now." — T-013, Leo

_Trace judge: partial – Calculator asking whether the spouse works for married employees is supported (F-TR-030), but the boolean yes/no format, validation and required_when=true are not backed, and the notes admit the calculator wording is unknown._
