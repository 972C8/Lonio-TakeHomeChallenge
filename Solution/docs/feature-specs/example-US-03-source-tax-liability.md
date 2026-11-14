---
id: US-03
title: Show source tax questions only to employees who are subject to source tax
feature: employee-onboarding
persona: hr_manager
priority: 1
milestone: Liability check
labels: [source-tax]
status: needs-decision
blocked_by: [OQ-02]
depends_on: [US-02, US-05]          # home address; civil status
information: [nationality, permit_type, spouse_nationality, spouse_permit_type, spouse_residence_country]
rules: [subject_to_source_tax]
receiving_parties: [source_tax, employer_hr]
sources: [F-TR-004, F-TR-005, F-TR-006, F-TR-025, F-TR-026, F-TR-031, F-TR-037, F-TR-040, F-TR-042, G-10]
linear: { issue: null }
---

# Show source tax questions only to employees who are subject to source tax

**As an** HR manager, **I want** the questionnaire to work out who is subject to source tax, **so that** only those employees answer the source tax questions and Swiss employees aren't asked them.

## Why

Today HR sends the full questionnaire to everybody because it can't tell up front who has to answer the source tax part. Swiss employees are annoyed and call HR. Source tax is HR's biggest pain point.

> "So I send the whole questionnaire to everybody, and the Swiss people get annoyed, and they call me." (T-008, Anna)

## Information collected

| Information | What, and in what form | Asked when | Required when | Depends on | Needed by |
|---|---|---|---|---|---|
| **Nationality** `nationality` | One country | Lives in Switzerland | Always when asked | Home country (US-02) | Source tax (liability check) |
| **Residence permit** `permit_type` | One of: B permit · C permit · Other permit / no permit yet | Lives in Switzerland **and** is not Swiss | Always when asked | Nationality | Source tax (liability check); HR (first-day permit reminder, US-07) |
| **Spouse's nationality** `spouse_nationality` | One country | Married **and** lives in Switzerland **and** is not Swiss **and** has no C permit | Always when asked | Civil status (US-05), permit | Source tax (liability check) |
| **Spouse's residence permit** `spouse_permit_type` | One of: B permit · C permit · Other permit / no permit yet | As above **and** spouse is not Swiss | Always when asked | Spouse's nationality | Source tax (liability check) |
| **Spouse's country of residence** `spouse_residence_country` | One country | As for spouse's nationality **and** spouse is Swiss or has a C permit | Always when asked | Spouse's nationality, spouse's permit | Source tax (liability check) |

Question wording shown to the employee:
- `permit_type`: "Which Swiss residence permit do you have?" (help text: "Choose the permit type shown on your permit card. A C permit means a settlement permit.")

## Rules

Decision table for **subject to source tax** (derived, never asked). First matching row wins; the rows cover every case.

| | Lives in CH | Nationality | Permit | Married to a Swiss or C-permit spouse who lives in CH | Subject to source tax | Source |
|---|---|---|---|---|---|---|
| **R1** | no | any | – | – | **yes** | F-TR-037 |
| **R2** | yes | Swiss | – | – | no | F-TR-006 |
| **R3** | yes | not Swiss | C | – | no | F-TR-025 |
| **R4** | yes | not Swiss | B / other | yes | no | F-TR-031 |
| **R5** | yes | not Swiss | B / other | no | **yes** | F-TR-040 |

- **R6** Only employees who are subject to source tax see the source tax step. (F-TR-005)

## Acceptance criteria

**AC-1** (R1, R6 · Stefan, F-TR-037)
- **Given** an employee whose home address is in Germany and who is Swiss
- **When** they finish the home address step
- **Then** they are not asked their nationality or permit
- **And** they are subject to source tax and see the source tax step

**AC-2** (R2 · *illustrative*)
- **Given** an employee who lives in Switzerland and is Swiss
- **When** they answer their nationality
- **Then** they are not asked about a permit or their spouse's nationality
- **And** they are not subject to source tax and don't see the source tax step

**AC-3** (R3 · Maria, F-TR-026; civil status *illustrative*)
- **Given** an employee who lives in Switzerland, is Portuguese and is single
- **When** they answer "C permit"
- **Then** they are not subject to source tax and don't see the source tax step

**AC-4** (R4 · Tomás, F-TR-031)
- **Given** an employee who lives in Switzerland, is Brazilian, has a B permit and is married
- **When** they say their spouse is Swiss and lives in Switzerland
- **Then** they are not asked their spouse's permit
- **And** they are not subject to source tax and don't see the source tax step

**AC-5** (R5 · *illustrative*)
- **Given** an employee who lives in Switzerland, is Italian, has a B permit and is single
- **When** they finish the nationality and permit step
- **Then** they are subject to source tax and see the source tax step

**AC-6** (data minimisation · decision)
- **Given** an employee who answered "B permit" and the spouse questions
- **When** they change their permit to "C permit"
- **Then** the spouse questions disappear and their answers are discarded

## Open questions

- [OQ-02](../open-questions.md#oq-02) Is the liability rule complete? Anna ended with "I think that's it" (T-048). **Until decided:** build the five rows above.
- [OQ-06](../open-questions.md#oq-06) Which permit types exist besides B and C? **Until decided:** offer B, C and "Other permit / no permit yet".

## Not in this story

- The tariff questions inside the source tax step (spouse works, children, …): [US-04](US-04-source-tax-tariff.md), blocked by OQ-01.
- Civil status itself: [US-05](US-05-civil-status.md).
- Reminding the employee to bring their permit: [US-07](US-07-permit-reminder.md).

## Evidence

| Item | Fact | Quote | Source |
|---|---|---|---|
| Why, R6 | F-TR-004 | "So I send the whole questionnaire to everybody, and the Swiss people get annoyed, and they call me." | T-008, Anna |
| R1, AC-1 | F-TR-037 | "Those people do source tax because they work here and they don't live here. And there it doesn't matter what passport you have, by the way." | T-048, Anna |
| R2 | F-TR-006 | "If you don't have a Swiss passport, you do source tax." | T-010, Anna |
| R3, AC-3 | F-TR-025 | "So, not the people with a C permit. They're treated like Swiss people for this." | T-038, Anna |
| AC-3 | F-TR-026 | "I'm thinking of Maria in sales, she's Portuguese, and she doesn't do source tax at all. She has a C permit." | T-038, Anna |
| R4, AC-4 | F-TR-031 | "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." | T-044, Anna |
| R5 | F-TR-040 | "I think that's it." | T-048, Anna |
| Options | G-10 | Product owner guidance: permit types use the official letter | guidance.md |
