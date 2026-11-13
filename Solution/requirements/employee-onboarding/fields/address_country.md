---
id: address_country
kind: field
step: address
order: 5
type: country
format: "ISO 3166-1 alpha-2 (Switzerland = \"CH\")"
ask_when: "true"
required_when: "true"
depends_on: []
consumers: [employer_hr, source_tax]
status: inferred
sources: [F-TR-010, F-TR-037, F-TR-040, F-TR-043, F-TR-045, G-09]
---

# Country

> **Question to the employee:** In which country do you live?
>
> _Help text:_ The country of your home address. If you live outside Switzerland (for example, you commute across the border), choose that country.

**Status: inferred** – parts of this field rest on inferred facts; see Evidence.

## What? (data and form)
| | |
|---|---|
| Type | `country` |
| Format | ISO 3166-1 alpha-2 (Switzerland = "CH") |
| Step | [Home address](../flow.md#address) (step 2, position 5) |

**Validation**
- must be a valid ISO 3166-1 alpha-2 code

## When do we ask?
always

## When is it required?
Always required when asked; the employee cannot leave it empty.

## What does it depend on?
Nothing – asked independently of other answers.

Used by: `residence_canton`, `nationality`, `permit_type`, `spouse_nationality`, `spouse_permit_type`, `spouse_residence_country`, `subject_to_source_tax`
## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Muster AG HR (correspondence, payroll admin, first-day logistics) | Postal address for mailed documents | Country |
| Source tax tariff determination (Canton of Zurich calculator) | Country of residence: anyone living outside CH is always subject to source tax | residence country (liability check) |

## Notes
Also serves as the residence country, so the employee is asked once (see OQ-07). The id residence_country is deliberately not used as a separate field.

## Evidence
- **F-TR-010** (hr_transcript): The address must be complete with street, house number, postcode, town and country, because HR posts many documents to employees.
  - "Street, number, postcode, town, country. We post a lot of documents to people, so it has to be complete." — T-014, Anna
- **F-TR-037** (hr_transcript): Employees who live abroad and work in Switzerland are always subject to source tax, regardless of nationality (e.g. Stefan, Swiss, lives in Konstanz; a warehouse employee lives in Liechtenstein).
  - "Those people do source tax because they work here and they don't live here. And there it doesn't matter what passport you have, by the way." — T-048, Anna
  - "Stefan is actually Swiss, and he still has it." — T-048, Anna
  - "So someone living abroad and working here always does it?" — T-049, Leo
  - "Yes." — T-050, Anna
- **F-TR-040** (hr_transcript, inferred): Consolidated final rule (Anna hedged completeness with 'I think'): an employee is subject to source tax if residence_country is not CH (regardless of nationality). If living in CH: not subject if nationality is CH; not subject if permit_type is C; not subject if married to a spouse who is Swiss or holds a C permit and lives in CH; otherwise subject.
  - "If you don't have a Swiss passport, you do source tax." — T-010, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — T-038, Anna
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Those people do source tax because they work here and they don't live here. And there it doesn't matter what passport you have, by the way." — T-048, Anna
  - "I think that's it." — T-048, Anna
- **F-TR-043** (hr_transcript, inferred): The employee's country of residence is needed to determine source tax liability (living abroad means always subject).
  - "Those people do source tax because they work here and they don't live here." — T-048, Anna
- **F-TR-045** (hr_transcript, inferred): 'Lives here' in Anna's statements means living in Switzerland.
  - "and they live in Winterthur." — T-044, Anna
  - "they work here and they don't live here." — T-048, Anna
- **G-09** (product owner guidance): Countries as ISO 3166-1 alpha-2 codes; Switzerland = "CH". Dates as ISO YYYY-MM-DD internally; display DD.MM.YYYY. Questionnaire language: English.

_Trace judge: supported – Country is part of HR's address, ISO alpha-2 is per G-09, and use as residence country for source tax is backed by F-TR-037/040/043/045._
