---
id: subject_to_source_tax
kind: rule
output_type: boolean
expression: "address_country != \"CH\" or (address_country == \"CH\" and nationality != \"CH\" and permit_type != \"C\" and not (civil_status == \"married\" and (spouse_nationality == \"CH\" or spouse_permit_type == \"C\") and spouse_residence_country == \"CH\"))"
depends_on: [address_country, civil_status, nationality, permit_type, spouse_nationality, spouse_permit_type, spouse_residence_country]
status: inferred
sources: [F-TR-040, F-TR-025, F-TR-031, F-TR-037, F-TR-005, F-TR-004, F-TR-006]
---

# Rule: `subject_to_source_tax`

Whether the employee is subject to source tax. Residents abroad are always subject. Residents of CH are not subject if they are Swiss, hold a C permit, or are married to a Swiss national or C permit holder who lives in CH. Everyone else is subject.

**Derived, never asked.** Computed from the answers as:

```
subject_to_source_tax = address_country != "CH" or (address_country == "CH" and nationality != "CH" and permit_type != "C" and not (civil_status == "married" and (spouse_nationality == "CH" or spouse_permit_type == "C") and spouse_residence_country == "CH"))
```

Output type: `boolean`. Inputs: `address_country`, `civil_status`, `nationality`, `permit_type`, `spouse_nationality`, `spouse_permit_type`, `spouse_residence_country`.

Used by: [`spouse_employed`](../fields/spouse_employed.md)
## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Source tax tariff determination (Canton of Zurich calculator) | Decides whether a tariff must be determined at all | liability |
| Muster AG HR (correspondence, payroll admin, first-day logistics) | Payroll: apply source tax deduction | source tax yes/no |

## Evidence
- **F-TR-040** (hr_transcript, inferred): Consolidated final rule (Anna hedged completeness with 'I think'): an employee is subject to source tax if residence_country is not CH (regardless of nationality). If living in CH: not subject if nationality is CH; not subject if permit_type is C; not subject if married to a spouse who is Swiss or holds a C permit and lives in CH; otherwise subject.
  - "If you don't have a Swiss passport, you do source tax." — T-010, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — T-038, Anna
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Those people do source tax because they work here and they don't live here. And there it doesn't matter what passport you have, by the way." — T-048, Anna
  - "I think that's it." — T-048, Anna
- **F-TR-025** (hr_transcript): Correction: non-Swiss employees holding a C permit are not subject to source tax; they are treated like Swiss people for this.
  - "No, that's actually not right." — T-038, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — T-038, Anna
  - "Okay, so non-Swiss, but not with a C permit." — T-039, Leo
- **F-TR-031** (hr_transcript): An employee married to a Swiss national or to a C permit holder who lives in Switzerland is not subject to source tax (e.g. Tomás: Brazilian, B permit, Swiss wife, living in Winterthur).
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." — T-044, Anna
- **F-TR-037** (hr_transcript): Employees who live abroad and work in Switzerland are always subject to source tax, regardless of nationality (e.g. Stefan, Swiss, lives in Konstanz; a warehouse employee lives in Liechtenstein).
  - "Those people do source tax because they work here and they don't live here. And there it doesn't matter what passport you have, by the way." — T-048, Anna
  - "Stefan is actually Swiss, and he still has it." — T-048, Anna
  - "So someone living abroad and working here always does it?" — T-049, Leo
  - "Yes." — T-050, Anna
- **F-TR-005** (hr_transcript, inferred): Source tax questions should be asked only to employees who are subject to source tax, not to everybody.
  - "Because I never know up front who has to answer those questions." — T-008, Anna
  - "the Swiss people get annoyed, and they call me." — T-008, Anna
- **F-TR-004** (hr_transcript): Source tax is HR's biggest pain point: because HR doesn't know in advance who must answer the source tax questions, the whole questionnaire is sent to everybody, which annoys Swiss employees.
  - "Source tax, without any doubt." — T-008, Anna
  - "So I send the whole questionnaire to everybody, and the Swiss people get annoyed, and they call me." — T-008, Anna
- **F-TR-006** (hr_transcript): Initial statement: all non-Swiss employees (anyone without a Swiss passport) are subject to source tax.
  - "All the non-Swiss employees. Simple as that. If you don't have a Swiss passport, you do source tax." — T-010, Anna

_Trace judge: supported – F-TR-040, F-TR-025, F-TR-031 and F-TR-037 back every branch: abroad always subject, and in CH exempt if Swiss, C permit, or married to a Swiss/C-permit spouse living in CH._
