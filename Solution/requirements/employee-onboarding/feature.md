---
id: employee-onboarding
title: "Employee onboarding questionnaire"
stakeholders: [employee, hr, pension_fund, source_tax]
sections: [SEC-01-questionnaire-flow, SEC-02-personal-details-address, SEC-03-employment-start, SEC-04-civil-status-spouse, SEC-05-source-tax-liability, SEC-06-source-tax-tariff-basics, SEC-07-source-tax-children, SEC-08-cross-border-residence]
stories: [US-01.1, US-01.2, US-01.3, US-02.1, US-02.2, US-02.3, US-02.4, US-03.1, US-03.2, US-03.3, US-04.1, US-04.2, US-04.3, US-05.1, US-05.2, US-05.3, US-06.1, US-06.2, US-06.3, US-06.4, US-07.1, US-07.2, US-07.3, US-07.4, US-07.5, US-08.1, US-08.2, US-08.3, US-08.4]
---

# Employee onboarding questionnaire

Each user story is its own file in [stories/](stories/); this file holds the
feature, its sections and the information and rules they share.

**Goal:** A new employee of Muster AG answers one English questionnaire that asks each piece of information once, and only when Pensionskasse Muster, the Zurich source tax calculator or HR needs it for this person. The answers are enough to complete the pension registration, find the source tax tariff and run HR onboarding without follow-up emails.

## Context
Today Muster AG's HR runs onboarding by hand and collects the same data for several receiving parties: the pension fund (Pensionskasse Muster), source tax (Zurich tariff calculator) and HR itself [G-01, G-02]. The sources name these pain points:
- **The first working day is HR's "number one" item and often moves.** The pension insurance start date depends on it and must always be the 1st of a month. When the start day changes, the pension fund's date must be corrected [F-hr_transcript-872bd7, F-hr_transcript-1d5c07, F-hr_transcript-e18e66, F-pension_portal-509cbe].
- **HR cannot tell up front who must answer the source tax questions.** Whether someone is subject to source tax depends on residence, nationality, permit and the spouse's situation. HR collects the spouse details through manual email follow-ups [F-hr_transcript-5af8d0, F-hr_transcript-b84498, F-hr_transcript-b90bd9, F-hr_transcript-a45422].
- **Missing required fields block the pension registration.** For example, the spouse's date of birth is required when the employee is married [F-pension_portal-44a27b, F-pension_portal-c5ee15].
- **Data minimisation forbids asking more than needed.** Sensitive data such as religious denomination must only be asked of employees who are subject to source tax [G-01].
- **The Zurich calculator has a deep tree of questions.** These cover income type, denomination, the spouse, children and cross-border situations for Germany and Liechtenstein, and only a subset applies to each person [F-zh_source_tax_calculator-e06ffd, F-zh_source_tax_calculator-103b19, F-zh_source_tax_calculator-69edd5].

**Scope:** which information is asked, in which order, under which conditions and whether it is required, plus the business rules derived from the answers [G-04].

**Out of scope** [G-03, G-04, F-hr_transcript-7668e6, F-hr_transcript-f23d48]:
- how the data is sent to each party
- AHV data
- IT equipment
- employee badge photos

**Simplifications** [G-05]: Switzerland has exactly one source tax system (Zurich's) and exactly one pension fund (Pensionskasse Muster).

**Stakeholders:** new employee, HR, pension fund, source tax office

<a id="flow"></a>

## Questionnaire flow

The questionnaire has 6 steps. Only the questions that apply to the employee are shown, and a step where no question applies is skipped (in practice only steps 4 and 6 can be skipped). The order follows dependencies: the address comes before nationality because employees living abroad need no nationality question, and civil status comes before the spouse questions. The source tax step comes last because it depends on the answers from all earlier steps. Each piece of information is asked once and reused for every receiving party.

| Step | What is asked | Shown to | Stories |
|---|---|---|---|
| 1. Personal details | First name, last name and date of birth. | Everyone | [US-02.1](stories/US-02.1-collect-the-employee-s-name-and-date-of-birth.md) |
| 2. Home address | Street, house number, postcode, town and country of the home address; the canton only if the country is Switzerland. The country of the home address is also used as the country of residence. | Everyone | [US-02.2](stories/US-02.2-collect-a-complete-postal-home-address.md), [US-02.3](stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md), [US-02.4](stories/US-02.4-ask-swiss-residents-for-their-canton.md) |
| 3. Employment start | The first working day (confirmed if HR already knows it). The pension insurance start date is derived from it and not asked. | Everyone | [US-03.1](stories/US-03.1-employee-confirms-the-first-working-day.md), [US-03.2](stories/US-03.2-derive-the-pension-insurance-start-date-from-the-first.md), [US-03.3](stories/US-03.3-re-derive-the-insurance-start-date-when-the-first-working.md) |
| 4. Nationality and permit | Nationality; the permit type only if the employee is not Swiss. | Employees living in Switzerland | [US-05.1](stories/US-05.1-ask-nationality-and-permit-only-of-employees-living-in.md) |
| 5. Family | Civil status. If married: the spouse's date of birth. The spouse's nationality only if the employee is married, lives in Switzerland, is not Swiss and has no C permit; the spouse's permit only if the spouse is not Swiss; the spouse's country of residence only if the spouse is Swiss or holds a C permit. | Everyone (spouse questions only to married employees, as conditioned) | [US-04.1](stories/US-04.1-ask-the-employee-s-civil-status-using-the-pension-fund-s.md), [US-04.2](stories/US-04.2-ask-the-spouse-s-date-of-birth-when-the-employee-is-married.md), [US-04.3](stories/US-04.3-answer-the-calculator-s-civil-status-question-from-the.md), [US-05.2](stories/US-05.2-ask-the-spouse-s-nationality-permit-and-residence-only-when.md), [US-05.3](stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md) |
| 6. Source tax | Type of income; if earned income: religious denomination; if married: whether the spouse works or receives replacement income; whether the employee has children, and for each child a block: age status, same household, and the follow-up custody, household, contributor and maintenance questions depending on the answers. Then the cross-border questions: if living in Germany, daily return, residence certificate (if daily return), reasonableness of daily return and proof of more than 60 non-return days (if no daily return); if living in Liechtenstein, daily return and more than 45 non-return days (if no daily return). | Only employees subject to source tax | [US-06.1](stories/US-06.1-ask-the-type-of-income-only-of-employees-subject-to-source.md), [US-06.2](stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md), [US-06.3](stories/US-06.3-ask-married-employees-subject-to-source-tax-whether-their.md), [US-07.1](stories/US-07.1-ask-about-children-only-of-employees-who-need-a-source-tax.md), [US-07.2](stories/US-07.2-one-block-per-child-age-status-and-household.md), [US-07.3](stories/US-07.3-minor-child-living-in-the-employee-s-household.md), [US-07.4](stories/US-07.4-minor-child-not-living-in-the-employee-s-household.md), [US-07.5](stories/US-07.5-adult-child-in-first-education.md), [US-08.2](stories/US-08.2-germany-daily-return-and-certificate-of-residence.md), [US-08.3](stories/US-08.3-germany-no-daily-return-reasonableness-and-proof-of-more.md), [US-08.4](stories/US-08.4-liechtenstein-daily-return-and-more-than-45-non-return-days.md) |

Never asked, always derived from the answers: Residence answers for the source tax calculator ([US-08.1](stories/US-08.1-derive-the-calculator-s-residence-answers-from-the-home.md)), Church-tax suffix of the tariff ([US-06.2](stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md)), Base tariff letter (source tax) ([US-06.4](stories/US-06.4-derive-the-base-source-tax-tariff-letter.md)), Questionnaire flow overview ([US-01.1](stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md), [US-01.2](stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md), [US-01.3](stories/US-01.3-ask-each-piece-of-information-once-and-reuse-it-for-every.md)).

## Contents

| Section | Stories |
|---|---|
| [1. Questionnaire flow overview](#SEC-01-questionnaire-flow) | [US-01.1](stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md), [US-01.2](stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md), [US-01.3](stories/US-01.3-ask-each-piece-of-information-once-and-reuse-it-for-every.md) |
| [2. Personal details and home address](#SEC-02-personal-details-address) | [US-02.1](stories/US-02.1-collect-the-employee-s-name-and-date-of-birth.md), [US-02.2](stories/US-02.2-collect-a-complete-postal-home-address.md), [US-02.3](stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md), [US-02.4](stories/US-02.4-ask-swiss-residents-for-their-canton.md) |
| [3. First working day and insurance start date](#SEC-03-employment-start) | [US-03.1](stories/US-03.1-employee-confirms-the-first-working-day.md), [US-03.2](stories/US-03.2-derive-the-pension-insurance-start-date-from-the-first.md), [US-03.3](stories/US-03.3-re-derive-the-insurance-start-date-when-the-first-working.md) |
| [4. Civil status and spouse data for the pension fund](#SEC-04-civil-status-spouse) | [US-04.1](stories/US-04.1-ask-the-employee-s-civil-status-using-the-pension-fund-s.md), [US-04.2](stories/US-04.2-ask-the-spouse-s-date-of-birth-when-the-employee-is-married.md), [US-04.3](stories/US-04.3-answer-the-calculator-s-civil-status-question-from-the.md) |
| [5. Who is subject to source tax](#SEC-05-source-tax-liability) | [US-05.1](stories/US-05.1-ask-nationality-and-permit-only-of-employees-living-in.md), [US-05.2](stories/US-05.2-ask-the-spouse-s-nationality-permit-and-residence-only-when.md), [US-05.3](stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md) |
| [6. Source tax tariff: income, denomination and spouse employment](#SEC-06-source-tax-tariff-basics) | [US-06.1](stories/US-06.1-ask-the-type-of-income-only-of-employees-subject-to-source.md), [US-06.2](stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md), [US-06.3](stories/US-06.3-ask-married-employees-subject-to-source-tax-whether-their.md), [US-06.4](stories/US-06.4-derive-the-base-source-tax-tariff-letter.md) |
| [7. Source tax tariff: children](#SEC-07-source-tax-children) | [US-07.1](stories/US-07.1-ask-about-children-only-of-employees-who-need-a-source-tax.md), [US-07.2](stories/US-07.2-one-block-per-child-age-status-and-household.md), [US-07.3](stories/US-07.3-minor-child-living-in-the-employee-s-household.md), [US-07.4](stories/US-07.4-minor-child-not-living-in-the-employee-s-household.md), [US-07.5](stories/US-07.5-adult-child-in-first-education.md) |
| [8. Source tax: residence abroad and cross-border questions](#SEC-08-cross-border-residence) | [US-08.1](stories/US-08.1-derive-the-calculator-s-residence-answers-from-the-home.md), [US-08.2](stories/US-08.2-germany-daily-return-and-certificate-of-residence.md), [US-08.3](stories/US-08.3-germany-no-daily-return-reasonableness-and-proof-of-more.md), [US-08.4](stories/US-08.4-liechtenstein-daily-return-and-more-than-45-non-return-days.md) |

<a id="SEC-01-questionnaire-flow"></a>

## 1. Questionnaire flow overview

Set the steps of the questionnaire, their order and the conditions for showing each step, so every employee sees only the questions that apply to them and answers each one once.

| Story | Priority | Status |
|---|---|---|
| [US-01.1 – Show the source tax step only to employees who are subject to source tax](stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md) | P1 | inferred |
| [US-01.2 – Ask the steps in an order that avoids unneeded questions](stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md) | P2 | inferred |
| [US-01.3 – Ask each piece of information once and reuse it for every receiving party](stories/US-01.3-ask-each-piece-of-information-once-and-reuse-it-for-every.md) | P1 | inferred |

### Business rules in this section

#### Questionnaire flow overview
The questionnaire runs in this order, each step only with the questions that apply: 1 Personal details (first name, last name, date of birth). 2 Home address (street, house number, postcode, town, country, and the canton if the employee lives in Switzerland). 3 Employment start (confirm the first working day, from which the insurance start date is derived). 4 Nationality and permit (only if the employee lives in Switzerland: nationality, and the permit if not Swiss). 5 Family (civil status. Spouse's date of birth if married. Spouse's nationality, permit and residence only if married and otherwise subject to source tax). 6 Source tax (only if subject to source tax: type of income, denomination, spouse works, children and one block per child, then the Germany or Liechtenstein cross-border questions). Address comes before nationality because employees living abroad need no nationality question. Civil status comes before the spouse questions.

| # | Subject to source tax | → Result | Sources |
|---|---|---|---|
| 1 | no | Steps 1-5 | F-hr_transcript-b84498, F-hr_transcript-51c17d, G-01 |
| 2 | yes | Steps 1-6 | F-hr_transcript-b84498, F-hr_transcript-34494f, G-01 |

_Status: inferred · Sources: G-01, G-04, G-08, F-hr_transcript-b84498, F-hr_transcript-51c17d, F-hr_transcript-5af8d0_

<a id="SEC-02-personal-details-address"></a>

## 2. Personal details and home address

Collect the employee's identity and complete postal address. The pension registration needs these, HR posts documents to the address, and the country of the address decides which later questions apply.

> ⚠ Open questions affecting this section: [OQ-canton](open-questions.md#oq-canton)
| Story | Priority | Status |
|---|---|---|
| [US-02.1 – Collect the employee's name and date of birth](stories/US-02.1-collect-the-employee-s-name-and-date-of-birth.md) | P1 | inferred |
| [US-02.2 – Collect a complete postal home address](stories/US-02.2-collect-a-complete-postal-home-address.md) | P1 | confirmed |
| [US-02.3 – Use the home address country as the country of residence](stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md) | P1 | inferred |
| [US-02.4 – Ask Swiss residents for their canton](stories/US-02.4-ask-swiss-residents-for-their-canton.md) | P1 | inferred |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### First name
| | |
|---|---|
| **What?** | The new employee's first name. Questionnaire step 1 (Personal details). |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'First name' for the occupational pension registration<br>HR: Identify the employee and address documents (HR asked for the 'basics', name and address) |
| **Status · sources** | confirmed · F-pension_portal-db702a, F-pension_portal-44a27b, F-hr_transcript-3edf89 |
| **Notes** | HR's own need for the name is only implied in the transcript. The pension fund's required flag is explicit. |

#### Last name
| | |
|---|---|
| **What?** | The new employee's last name. Step 1 (Personal details). |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'Last name' for the registration<br>HR: Identify the employee and address documents |
| **Status · sources** | confirmed · F-pension_portal-c688e4, F-pension_portal-44a27b, F-hr_transcript-3edf89 |

#### Date of birth
| | |
|---|---|
| **What?** | The new employee's date of birth. Step 1 (Personal details). – Form: Date in the format DD.MM.YYYY |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'Date of birth' for the registration |
| **Status · sources** | confirmed · F-pension_portal-88b436, F-pension_portal-967bc9, F-pension_portal-44a27b |

#### Street
| | |
|---|---|
| **What?** | The street of the employee's home address. Step 2 (Home address). – Form: Part of a complete postal address, written as on an envelope: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always (the address must be complete) |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee |
| **Status · sources** | confirmed · F-hr_transcript-3beee8, F-hr_transcript-c0fe95, F-hr_transcript-66fe15 |

#### House number
| | |
|---|---|
| **What?** | The house number of the employee's home address. Step 2 (Home address). – Form: Part of a complete postal address: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always (the address must be complete) |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee |
| **Status · sources** | confirmed · F-hr_transcript-3beee8, F-hr_transcript-c0fe95, F-hr_transcript-66fe15 |

#### Postcode
| | |
|---|---|
| **What?** | The postcode of the employee's home address. Step 2 (Home address). – Form: Part of a complete postal address: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always (the address must be complete) |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee |
| **Status · sources** | confirmed · F-hr_transcript-3beee8, F-hr_transcript-c0fe95, F-hr_transcript-66fe15 |

#### Town
| | |
|---|---|
| **What?** | The town of the employee's home address. Step 2 (Home address). – Form: Part of a complete postal address: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always (the address must be complete) |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee |
| **Status · sources** | confirmed · F-hr_transcript-3beee8, F-hr_transcript-c0fe95, F-hr_transcript-66fe15 |

#### Country (of the home address)
| | |
|---|---|
| **What?** | The country of the employee's home address. It is also the employee's country of residence, used to decide whether the employee is subject to source tax and which residence questions of the source tax calculator apply. Step 2 (Home address). – Form: Part of a complete postal address: street, house number, postcode, town and country. Country written by its English name (e.g. "Switzerland", "Germany", "Liechtenstein") |
| **When do we ask?** | Always |
| **When is it required?** | Always (the address must be complete) |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee<br>source tax office: Employees living abroad are always subject to source tax. Also answers the calculator's 'main residence in Switzerland' and 'country of residence' questions |
| **Status · sources** | inferred · F-hr_transcript-c0fe95, F-hr_transcript-ab3cba, F-hr_transcript-3f2c2a, F-hr_transcript-5af8d0, F-zh_source_tax_calculator-aedb40, F-zh_source_tax_calculator-4c65ae, G-08, G-09, G-10 |
| **Notes** | Using the address country for the calculator's residence questions follows G-08/G-09 and is not stated by the calculator itself. |

#### Canton of residence
| | |
|---|---|
| **What?** | The Swiss canton the employee lives in. Step 2 (Home address), right after the country. |
| **Allowed values** | Aargau · Appenzell Ausserrhoden · Appenzell Innerrhoden · Basel-Landschaft · Basel-Stadt · Bern · Fribourg · Geneva · Glarus · Graubünden · Jura · Lucerne · Neuchâtel · Nidwalden · Obwalden · Schaffhausen · Schwyz · Solothurn · St. Gallen · Thurgau · Ticino · Uri · Valais · Vaud · Zug · Zurich |
| **When do we ask?** | Only if the employee lives in Switzerland |
| **When is it required?** | Always when asked |
| **Depends on** | Country (of the home address) |
| **Who needs it?** | pension fund: Required field 'Canton' for the registration |
| **Status · sources** | inferred · F-pension_portal-6c621f, F-pension_portal-3432a9, F-pension_portal-44a27b, F-pension_portal-b359c3, G-07 |
| **Notes** | The portal does not say whether 'Canton' means canton of residence or of work, and it has no option for people living abroad. See OQ-canton. |

<a id="SEC-03-employment-start"></a>

## 3. First working day and insurance start date

Have the employee confirm the first working day and derive the pension insurance start date from it, so a moved start date never leaves a wrong date at the pension fund.

| Story | Priority | Status |
|---|---|---|
| [US-03.1 – Employee confirms the first working day](stories/US-03.1-employee-confirms-the-first-working-day.md) | P1 | confirmed |
| [US-03.2 – Derive the pension insurance start date from the first working day](stories/US-03.2-derive-the-pension-insurance-start-date-from-the-first.md) | P1 | confirmed |
| [US-03.3 – Re-derive the insurance start date when the first working day moves](stories/US-03.3-re-derive-the-insurance-start-date-when-the-first-working.md) | P1 | inferred |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### First working day
| | |
|---|---|
| **What?** | The date of the employee's first working day at Muster AG, confirmed by the employee because it often moves. The pension insurance start date is derived from it. Step 3 (Employment start). |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Basis for deriving the insurance start date (HR calls it the 'number one' item)<br>HR: Confirm the agreed start, which often changes |
| **Status · sources** | confirmed · F-hr_transcript-872bd7, F-hr_transcript-e3721e, F-hr_transcript-1d5c07, G-08 |
| **Notes** | If HR already knows the date, the employee is asked to confirm it. If it changes, insurance_start_date must be derived again. |

### Business rules in this section

#### Pension insurance start date
The insurance start date is derived from the first working day, not asked. If the first working day is the 1st of a month, insurance starts that day. Otherwise it starts on the 1st of the following month. If the first working day changes, the insurance start date must be derived again and the pension fund's date corrected. The result is always the 1st of a month, as the pension fund requires.

| # | First working day | → Result | Sources |
|---|---|---|---|
| 1 | is the 1st of a month | Insurance starts on the first working day | F-hr_transcript-fdf50a, F-hr_transcript-1d5c07 |
| 2 | is not the 1st of a month | Insurance starts on the 1st of the following month (e.g. 15.03 gives 01.04) | F-hr_transcript-30d25c, F-hr_transcript-1d5c07 |

_Status: confirmed · Sources: F-hr_transcript-1d5c07, F-hr_transcript-30d25c, F-hr_transcript-fdf50a, F-hr_transcript-e18e66, F-pension_portal-509cbe, F-pension_portal-dd8126, F-pension_portal-3a97ab, G-08_

<a id="SEC-04-civil-status-spouse"></a>

## 4. Civil status and spouse data for the pension fund

Ask the civil status once, using the pension fund's list, and the spouse's date of birth when the employee is married. The source tax calculator's civil status question is answered from the same answer, not asked again.

> ⚠ Open questions affecting this section: [OQ-registered-partnership](open-questions.md#oq-registered-partnership), [OQ-separated](open-questions.md#oq-separated), [OQ-divorced-widowed](open-questions.md#oq-divorced-widowed)
| Story | Priority | Status |
|---|---|---|
| [US-04.1 – Ask the employee's civil status using the pension fund's list](stories/US-04.1-ask-the-employee-s-civil-status-using-the-pension-fund-s.md) | P1 | confirmed |
| [US-04.2 – Ask the spouse's date of birth when the employee is married](stories/US-04.2-ask-the-spouse-s-date-of-birth-when-the-employee-is-married.md) | P1 | inferred |
| [US-04.3 – Answer the calculator's civil status question from the employee's civil status](stories/US-04.3-answer-the-calculator-s-civil-status-question-from-the.md) | P1 | inferred |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Civil status
| | |
|---|---|
| **What?** | The employee's civil status, as listed by the pension fund. It also answers the source tax calculator's civil status question (see rule calculator_civil_status). Step 5 (Family). |
| **Allowed values** | Single · Married · Divorced · Widowed |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'Civil status' for the registration<br>source tax office: Decides the spouse exemption and the base tariff (married/registered partnership vs. single/divorced/separated/widowed) |
| **Status · sources** | confirmed · F-hr_transcript-ce8ca4, F-pension_portal-8664f4, F-pension_portal-3d1ae4, F-pension_portal-44a27b, F-hr_transcript-bd8c8e, F-zh_source_tax_calculator-9007c3, F-zh_source_tax_calculator-051bb9, G-07, G-10 |
| **Notes** | The pension list has no registered partnership and no 'separated'. See OQ-registered-partnership and OQ-separated. |

#### Spouse's date of birth
| | |
|---|---|
| **What?** | The date of birth of the employee's husband or wife. Step 5 (Family). – Form: Date in the format DD.MM.YYYY |
| **When do we ask?** | Only if the employee is married |
| **When is it required?** | Always when asked (the pension fund blocks the registration without it) |
| **Depends on** | Civil status |
| **Who needs it?** | pension fund: Required field 'Spouse's date of birth' when civil status is Married |
| **Status · sources** | confirmed · F-hr_transcript-2334d8, F-pension_portal-a0065b, F-pension_portal-ef28c3, F-pension_portal-39bab1, F-pension_portal-c5ee15 |
| **Notes** | Unknown for Divorced/Widowed (OQ-divorced-widowed) and for registered partners (OQ-registered-partnership). |

### Business rules in this section

#### Civil status answer for the source tax calculator
The source tax calculator's civil status question is answered from the employee's civil status, not asked again: Married maps to 'married or registered partnership' (Verheiratet oder eingetragene Partnerschaft). Single, Divorced and Widowed map to 'single, divorced, separated, widowed' (Ledig, Geschieden, Getrennt, Verwitwet).

| # | Civil status | → Result | Sources |
|---|---|---|---|
| 1 | Married | Married or registered partnership | F-zh_source_tax_calculator-051bb9, F-pension_portal-3d1ae4 |
| 2 | Single, Divorced or Widowed | Single, divorced, separated, widowed | F-zh_source_tax_calculator-051bb9, F-pension_portal-3d1ae4 |

_Status: inferred · Sources: F-zh_source_tax_calculator-9007c3, F-zh_source_tax_calculator-051bb9, F-pension_portal-3d1ae4, G-01, G-08_

<a id="SEC-05-source-tax-liability"></a>

## 5. Who is subject to source tax

Ask only the nationality, permit and spouse questions needed to decide whether the employee is subject to source tax. This tells HR up front who must answer the source tax questions and replaces the manual email follow-up about the spouse.

> ⚠ Open questions affecting this section: [OQ-source-tax-rule](open-questions.md#oq-source-tax-rule), [OQ-permit-list](open-questions.md#oq-permit-list), [OQ-dual-nationality](open-questions.md#oq-dual-nationality), [OQ-spouse-residence-form](open-questions.md#oq-spouse-residence-form), [OQ-permit-reminder](open-questions.md#oq-permit-reminder)
| Story | Priority | Status |
|---|---|---|
| [US-05.1 – Ask nationality and permit only of employees living in Switzerland](stories/US-05.1-ask-nationality-and-permit-only-of-employees-living-in.md) | P1 | inferred |
| [US-05.2 – Ask the spouse's nationality, permit and residence only when they can exempt the employee](stories/US-05.2-ask-the-spouse-s-nationality-permit-and-residence-only-when.md) | P1 | inferred |
| [US-05.3 – Decide whether the employee is subject to source tax](stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md) | P1 | inferred |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Nationality
| | |
|---|---|
| **What?** | The employee's nationality (whether they hold a Swiss passport). Used only to decide whether the employee is subject to source tax. Step 4 (Nationality and permit). – Form: Country by English name (e.g. "Switzerland") |
| **When do we ask?** | Only if the employee lives in Switzerland (employees living abroad are subject to source tax whatever their nationality) |
| **When is it required?** | Always when asked |
| **Depends on** | Country (of the home address) |
| **Who needs it?** | source tax office: Swiss nationals living in Switzerland are not subject to source tax<br>HR: Know up front who must answer the source tax questions |
| **Status · sources** | inferred · F-hr_transcript-35fae3, F-hr_transcript-5af8d0, F-hr_transcript-3f2c2a, F-hr_transcript-b84498, G-01 |

#### Permit type
| | |
|---|---|
| **What?** | The Swiss residence permit the non-Swiss employee holds (e.g. B permit, C permit). A C permit exempts the employee from source tax. Step 4. – Form: Permits written as "B permit", "C permit" |
| **When do we ask?** | Only if the employee lives in Switzerland and is not Swiss |
| **When is it required?** | Always when asked |
| **Depends on** | Country (of the home address), Nationality |
| **Who needs it?** | source tax office: Non-Swiss employees with a C permit are not subject to source tax |
| **Status · sources** | inferred · F-hr_transcript-c9d9b9, F-hr_transcript-845204, F-hr_transcript-5af8d0, G-01, G-10 |
| **Notes** | No source gives the full list of permit types. See OQ-permit-list. |

#### Spouse's nationality
| | |
|---|---|
| **What?** | The nationality of the employee's spouse. Used to check the spouse exemption from source tax (spouse is Swiss). Step 5 (Family). – Form: Country by English name |
| **When do we ask?** | Only if the employee is married, lives in Switzerland, is not Swiss and has no C permit (i.e. would otherwise be subject to source tax) |
| **When is it required?** | Always when asked |
| **Depends on** | Country (of the home address), Civil status, Nationality, Permit type |
| **Who needs it?** | source tax office: An employee married to a Swiss national living in Switzerland is not subject to source tax<br>HR: Replaces today's manual email follow-up about the spouse |
| **Status · sources** | inferred · F-hr_transcript-f3ce84, F-hr_transcript-b90bd9, F-hr_transcript-54d011, F-hr_transcript-5af8d0, F-hr_transcript-a45422, G-01 |

#### Spouse's permit type
| | |
|---|---|
| **What?** | The Swiss permit of the employee's non-Swiss spouse, if the spouse has one. A C permit held by a spouse who lives in Switzerland exempts the employee from source tax. Step 5. – Form: Permits written as "B permit", "C permit" |
| **When do we ask?** | Only if the spouse's nationality is asked and the spouse is not Swiss |
| **When is it required?** | When asked, if the spouse has a permit (HR: 'their permit if they have one') |
| **Depends on** | Country (of the home address), Civil status, Nationality, Permit type, Spouse's nationality |
| **Who needs it?** | source tax office: An employee married to a C-permit holder living in Switzerland is not subject to source tax |
| **Status · sources** | inferred · F-hr_transcript-76eacc, F-hr_transcript-b90bd9, F-hr_transcript-54d011, F-hr_transcript-5af8d0, G-01 |
| **Notes** | A spouse without a permit needs a way to answer 'no permit'. The list of permits is open (OQ-permit-list). |

#### Spouse's country of residence
| | |
|---|---|
| **What?** | The country the employee's spouse lives in. The spouse exemption applies only if the spouse lives in Switzerland. Step 5. – Form: Country by English name |
| **When do we ask?** | Only if the spouse question was asked and the spouse is Swiss or holds a C permit |
| **When is it required?** | Always when asked |
| **Depends on** | Country (of the home address), Civil status, Nationality, Permit type, Spouse's nationality, Spouse's permit type |
| **Who needs it?** | source tax office: The spouse exemption applies only if the Swiss or C-permit spouse lives 'here' (Switzerland) |
| **Status · sources** | inferred · F-hr_transcript-e5337d, F-hr_transcript-b90bd9, F-hr_transcript-5af8d0, G-01 |
| **Notes** | HR said 'here', which is read as Switzerland (OQ-source-tax-rule). |

### Business rules in this section

#### Employee is subject to source tax
An employee who lives outside Switzerland is subject to source tax regardless of nationality. An employee who lives in Switzerland is subject only if they are not Swiss, do not hold a C permit, and are not married to a Swiss national or C-permit holder who lives in Switzerland. Only employees who are subject answer the source tax questions.

| # | Country of residence | Nationality | Permit type | Civil status | Spouse is Swiss or holds a C permit | Spouse lives in Switzerland | → Result | Sources |
|---|---|---|---|---|---|---|---|---|
| 1 | not Switzerland | - | - | any | - | - | Subject to source tax | F-hr_transcript-3f2c2a, F-hr_transcript-5af8d0 |
| 2 | Switzerland | Switzerland | - | any | - | - | Not subject | F-hr_transcript-b0527c, F-hr_transcript-5af8d0 |
| 3 | Switzerland | not Switzerland | C permit | any | - | - | Not subject | F-hr_transcript-845204, F-hr_transcript-5af8d0 |
| 4 | Switzerland | not Switzerland | not C permit | not Married | - | - | Subject to source tax | F-hr_transcript-845204, F-hr_transcript-5af8d0 |
| 5 | Switzerland | not Switzerland | not C permit | Married | no | - | Subject to source tax | F-hr_transcript-b90bd9, F-hr_transcript-5af8d0 |
| 6 | Switzerland | not Switzerland | not C permit | Married | yes | Switzerland | Not subject | F-hr_transcript-b90bd9, F-hr_transcript-5af8d0 |
| 7 | Switzerland | not Switzerland | not C permit | Married | yes | not Switzerland | Subject to source tax | F-hr_transcript-b90bd9, F-hr_transcript-5af8d0 |

_Status: inferred · Sources: F-hr_transcript-5af8d0, F-hr_transcript-845204, F-hr_transcript-b90bd9, F-hr_transcript-3f2c2a, F-hr_transcript-b0527c, F-hr_transcript-550840, F-hr_transcript-b84498_

<a id="SEC-06-source-tax-tariff-basics"></a>

## 6. Source tax tariff: income, denomination and spouse employment

For employees subject to source tax only, ask the calculator's income type, denomination and spouse employment questions that set the base tariff letter and the church-tax suffix.

> ⚠ Open questions affecting this section: [OQ-income-type](open-questions.md#oq-income-type)
| Story | Priority | Status |
|---|---|---|
| [US-06.1 – Ask the type of income only of employees subject to source tax](stories/US-06.1-ask-the-type-of-income-only-of-employees-subject-to-source.md) | P2 | inferred |
| [US-06.2 – Ask the religious denomination only where source tax needs it and derive the church-tax suffix](stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md) | P1 | inferred |
| [US-06.3 – Ask married employees subject to source tax whether their spouse works](stories/US-06.3-ask-married-employees-subject-to-source-tax-whether-their.md) | P1 | inferred |
| [US-06.4 – Derive the base source tax tariff letter](stories/US-06.4-derive-the-base-source-tax-tariff-letter.md) | P1 | inferred |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Type of income (source tax)
| | |
|---|---|
| **What?** | Which income the source tax tariff is determined for: earned income or replacement income. First question of the source tax calculator. Step 6 (Source tax). |
| **Allowed values** | Earned income · Replacement income |
| **When do we ask?** | Only if the employee is subject to source tax |
| **When is it required?** | Always when asked |
| **Depends on** | Employee is subject to source tax |
| **Who needs it?** | source tax office: Selects the tariff path. Replacement income gives tariff G/Q and skips the personal and child questions |
| **Status · sources** | inferred · F-zh_source_tax_calculator-e06ffd, F-zh_source_tax_calculator-feb9df, F-zh_source_tax_calculator-d5a6fe, F-zh_source_tax_calculator-351289, F-hr_transcript-34494f, F-hr_transcript-b84498 |
| **Notes** | Calculator labels: Erwerbseinkommen / Ersatzeinkünfte. For a new hire this is presumably always earned income (OQ-income-type). |

#### Religious denomination (church tax)
| | |
|---|---|
| **What?** | Whether the employee belongs to a Roman Catholic, Christian Catholic or Evangelical Reformed church, or to none/another. It sets the church-tax suffix of the tariff. Step 6. |
| **Allowed values** | Roman Catholic, Christian Catholic or Evangelical Reformed · None or other |
| **When do we ask?** | Only if the employee is subject to source tax and has earned income |
| **When is it required?** | Always when asked |
| **Depends on** | Type of income (source tax), Employee is subject to source tax |
| **Who needs it?** | source tax office: Church-tax suffix of the tariff (Y/N) |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-208104, F-zh_source_tax_calculator-b7fea8, F-zh_source_tax_calculator-b05b44, F-zh_source_tax_calculator-2eab9a, G-09 |
| **Notes** | Calculator labels: 'röm.-kath., christ.-kath., evang.-ref.' / 'Keine oder andere'. Sensitive personal data: ask only of employees subject to source tax. |

#### Spouse works or receives replacement income
| | |
|---|---|
| **What?** | Whether the spouse is gainfully employed or receives replacement income. Step 6. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee is subject to source tax, has earned income and is married |
| **When is it required?** | Always when asked |
| **Depends on** | Civil status, Type of income (source tax), Employee is subject to source tax |
| **Who needs it?** | source tax office: Spouse working leads to tariff C, otherwise tariff B |
| **Status · sources** | confirmed · F-hr_transcript-6a0a40, F-zh_source_tax_calculator-7b637b, F-zh_source_tax_calculator-e740d1, F-zh_source_tax_calculator-0137bf, F-zh_source_tax_calculator-97139a |

### Business rules in this section

#### Church-tax suffix of the tariff
For earned income, the employee's denomination sets the church-tax suffix of the source tax tariff: Y for Roman Catholic, Christian Catholic or Evangelical Reformed, N for none or other (e.g. A0Y vs A0N). Replacement income tariffs (G/Q) have no suffix.

| # | Type of income | Religious denomination | → Result | Sources |
|---|---|---|---|---|
| 1 | Earned income | Roman Catholic, Christian Catholic or Evangelical Reformed | Y | F-zh_source_tax_calculator-2eab9a |
| 2 | Earned income | None or other | N | F-zh_source_tax_calculator-2eab9a |
| 3 | Replacement income | - | No suffix | F-zh_source_tax_calculator-2d4dda |

_Status: inferred · Sources: F-zh_source_tax_calculator-2eab9a, F-zh_source_tax_calculator-2d4dda_

#### Base tariff letter (source tax)
The calculator's base tariff letter: replacement income gives G. Married with a working spouse gives C, married with a non-working spouse gives B. Not married gives A, or H if at least one child is counted with H (child in household, and sole custody or the employee is the main contributor). For employees in Germany the cross-border tariff replaces A→L, B→M, C→N, H→P, G→Q when it applies. The tariff digit is the number of counted children. HR keeps the calculator as the authority for the final tariff.

| # | Type of income | Civil status | Spouse works | Child counted with H | → Result | Sources |
|---|---|---|---|---|---|---|
| 1 | Replacement income | - | - | - | G | F-zh_source_tax_calculator-2d4dda |
| 2 | Earned income | Married | yes | - | C | F-zh_source_tax_calculator-97139a |
| 3 | Earned income | Married | no | - | B | F-zh_source_tax_calculator-97139a |
| 4 | Earned income | Single, Divorced or Widowed | - | no | A | F-zh_source_tax_calculator-037b1c |
| 5 | Earned income | Single, Divorced or Widowed | - | yes | H | F-zh_source_tax_calculator-300c72 |

_Status: inferred · Sources: F-zh_source_tax_calculator-97139a, F-zh_source_tax_calculator-037b1c, F-zh_source_tax_calculator-300c72, F-zh_source_tax_calculator-2d4dda, F-zh_source_tax_calculator-993db3, F-zh_source_tax_calculator-4c53e3, F-hr_transcript-34494f_

<a id="SEC-07-source-tax-children"></a>

## 7. Source tax tariff: children

For employees subject to source tax only, ask whether there are children, then one block of questions per child. Each block asks only what is needed to decide whether that child counts towards the tariff digit or leads to tariff H.

> ⚠ Open questions affecting this section: [OQ-calculator-coverage](open-questions.md#oq-calculator-coverage)
| Story | Priority | Status |
|---|---|---|
| [US-07.1 – Ask about children only of employees who need a source tax tariff](stories/US-07.1-ask-about-children-only-of-employees-who-need-a-source-tax.md) | P1 | inferred |
| [US-07.2 – One block per child: age status and household](stories/US-07.2-one-block-per-child-age-status-and-household.md) | P1 | confirmed |
| [US-07.3 – Minor child living in the employee's household](stories/US-07.3-minor-child-living-in-the-employee-s-household.md) | P2 | confirmed |
| [US-07.4 – Minor child not living in the employee's household](stories/US-07.4-minor-child-not-living-in-the-employee-s-household.md) | P2 | confirmed |
| [US-07.5 – Adult child in first education](stories/US-07.5-adult-child-in-first-education.md) | P2 | confirmed |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Has biological or adopted children
| | |
|---|---|
| **What?** | Whether the employee (for married employees: the employee or the spouse) has biological or adopted children. Step 6. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee is subject to source tax and has earned income: for married employees after the spouse-employment question, otherwise after the denomination question |
| **When is it required?** | Always when asked |
| **Depends on** | Civil status, Religious denomination (church tax), Type of income (source tax), Spouse works or receives replacement income, Employee is subject to source tax |
| **Who needs it?** | source tax office: Opens the per-child questions that set the tariff digit |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-103b19, F-zh_source_tax_calculator-a166c7, F-zh_source_tax_calculator-a33b65, F-zh_source_tax_calculator-ab8a06, F-zh_source_tax_calculator-b62b85, F-zh_source_tax_calculator-75cd87 |

#### Child: minor or adult in first education
| | |
|---|---|
| **What?** | For each child: whether the child is a minor, an adult in first education, or neither. Repeated per child (Child 1, Child 2, ...). – Form: Asked once per child |
| **Allowed values** | Minor · Adult in first education · Neither |
| **When do we ask?** | For each child, only if the employee has children |
| **When is it required?** | Always when asked |
| **Depends on** | Has biological or adopted children |
| **Who needs it?** | source tax office: Children who are neither do not count towards the tariff |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-640429, F-zh_source_tax_calculator-09b06d, F-zh_source_tax_calculator-6bed1f, F-zh_source_tax_calculator-fd9a15, F-zh_source_tax_calculator-abe889 |
| **Notes** | Calculator labels: Minderjährig / Volljährig und in Erstausbildung / weder noch. |

#### Child lives in the same household
| | |
|---|---|
| **What?** | For each counted child: whether the child lives in the employee's household. – Form: Asked once per child |
| **Allowed values** | yes · no |
| **When do we ask?** | For each child who is a minor or an adult in first education |
| **When is it required?** | Always when asked |
| **Depends on** | Child: minor or adult in first education |
| **Who needs it?** | source tax office: Decides whether the child counts towards the tariff |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-5725a8, F-zh_source_tax_calculator-3a75cc, F-zh_source_tax_calculator-7c667f |

#### Parental custody (child in household)
| | |
|---|---|
| **What?** | For a minor child in the household: shared or sole parental custody. – Form: Asked once per child |
| **Allowed values** | Shared custody · Sole custody |
| **When do we ask?** | For each minor child living in the same household |
| **When is it required?** | Always when asked |
| **Depends on** | Child: minor or adult in first education, Child lives in the same household |
| **Who needs it?** | source tax office: Decides whether and how the child counts (sole custody counts. For single employees it gives tariff H) |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-4b7063, F-zh_source_tax_calculator-c09dc1, F-zh_source_tax_calculator-83de1d, F-zh_source_tax_calculator-d75286, F-zh_source_tax_calculator-300c72 |
| **Notes** | Calculator labels: Geteiltes Sorgerecht / Alleiniges Sorgerecht. |

#### Common household with the other parent
| | |
|---|---|
| **What?** | For a child in the household: whether the employee lives in a common household with the child's other parent. – Form: Asked once per child |
| **Allowed values** | yes · no |
| **When do we ask?** | For a minor child in the household with shared custody, or an adult child in first education in the household |
| **When is it required?** | Always when asked |
| **Depends on** | Child: minor or adult in first education, Parental custody (child in household), Child lives in the same household |
| **Who needs it?** | source tax office: Decides whether the child counts and which follow-up questions apply |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-d79949, F-zh_source_tax_calculator-e72e42, F-zh_source_tax_calculator-6dcf5c, F-zh_source_tax_calculator-5d8fb0 |

#### Shared custody (child not in household, married)
| | |
|---|---|
| **What?** | For married employees with a minor child not in the household: whether custody is shared. – Form: Asked once per child |
| **Allowed values** | yes · no |
| **When do we ask?** | For a minor child not in the household, if the employee is married |
| **When is it required?** | Always when asked |
| **Depends on** | Child: minor or adult in first education, Child lives in the same household, Civil status |
| **Who needs it?** | source tax office: Without shared custody the child does not count |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-fe0305, F-zh_source_tax_calculator-d2e516, F-zh_source_tax_calculator-7dcce6, F-zh_source_tax_calculator-dc6ace |

#### Parental care (child not in household, not married)
| | |
|---|---|
| **What?** | For employees who are not married with a minor child not in the household: whether they have parental care. – Form: Asked once per child |
| **Allowed values** | yes · no |
| **When do we ask?** | For a minor child not in the household, if the employee is not married |
| **When is it required?** | Always when asked |
| **Depends on** | Child: minor or adult in first education, Child lives in the same household, Civil status |
| **Who needs it?** | source tax office: Without parental care the child does not count |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-956f07, F-zh_source_tax_calculator-32fec9, F-zh_source_tax_calculator-fb4a56, F-zh_source_tax_calculator-dc6ace |

#### Alternating custody
| | |
|---|---|
| **What?** | For a minor child: whether there is alternating custody (alternierende Obhut). – Form: Asked once per child |
| **Allowed values** | yes · no |
| **When do we ask?** | For a minor child: in the household with shared custody and no common household with the other parent; or not in the household with shared custody (married) or parental care (not married) |
| **When is it required?** | Always when asked |
| **Depends on** | Child: minor or adult in first education, Common household with the other parent, Parental custody (child in household), Parental care (child not in household, not married), Child lives in the same household, Shared custody (child not in household, married) |
| **Who needs it?** | source tax office: Decides whether the child counts |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-da19df, F-zh_source_tax_calculator-ebd7b3, F-zh_source_tax_calculator-64ac33, F-zh_source_tax_calculator-a4d358, F-zh_source_tax_calculator-dc0ae9 |

#### Main financial contributor to the child's maintenance
| | |
|---|---|
| **What?** | Who pays the larger share of the child's maintenance: the employee or the other parent. – Form: Asked once per child |
| **Allowed values** | The employee · The other parent |
| **When do we ask?** | If there is alternating custody, or (employee not married) the child lives in the household and the employee shares a household with the other parent |
| **When is it required?** | Always when asked |
| **Depends on** | Alternating custody, Common household with the other parent, Child lives in the same household, Civil status |
| **Who needs it?** | source tax office: Decides whether the child counts (for single employees, possibly with tariff H) |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-cdd0b6, F-zh_source_tax_calculator-939b3b, F-zh_source_tax_calculator-ad867a, F-zh_source_tax_calculator-5686d7, F-zh_source_tax_calculator-300c72 |
| **Notes** | Calculator labels: Quellensteuerpflichtige Person / Anderer Elternteil. |

#### Pays more than 50% of the child's maintenance
| | |
|---|---|
| **What?** | For an adult child in first education: whether the employee mainly (more than 50%) pays for the child's maintenance. – Form: Asked once per child |
| **Allowed values** | yes · no |
| **When do we ask?** | For an adult child in first education who does not live in the household, or lives in it without a common household with the other parent |
| **When is it required?** | Always when asked |
| **Depends on** | Child: minor or adult in first education, Common household with the other parent, Child lives in the same household |
| **Who needs it?** | source tax office: The child counts only if more than 50% of maintenance is provided |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-b008fe, F-zh_source_tax_calculator-cb54d9, F-zh_source_tax_calculator-cd1015, F-zh_source_tax_calculator-3eb561 |

<a id="SEC-08-cross-border-residence"></a>

## 8. Source tax: residence abroad and cross-border questions

Answer the calculator's residence questions from the home address. Ask employees living in Germany or Liechtenstein only the daily-return and non-return-day questions that decide between the cross-border tariff and the normal tariff.

> ⚠ Open questions affecting this section: [OQ-liechtenstein](open-questions.md#oq-liechtenstein), [OQ-proof-documents](open-questions.md#oq-proof-documents)
| Story | Priority | Status |
|---|---|---|
| [US-08.1 – Derive the calculator's residence answers from the home address](stories/US-08.1-derive-the-calculator-s-residence-answers-from-the-home.md) | P1 | inferred |
| [US-08.2 – Germany: daily return and certificate of residence](stories/US-08.2-germany-daily-return-and-certificate-of-residence.md) | P1 | confirmed |
| [US-08.3 – Germany: no daily return - reasonableness and proof of more than 60 non-return days](stories/US-08.3-germany-no-daily-return-reasonableness-and-proof-of-more.md) | P1 | confirmed |
| [US-08.4 – Liechtenstein: daily return and more than 45 non-return days](stories/US-08.4-liechtenstein-daily-return-and-more-than-45-non-return-days.md) | P1 | confirmed |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Returns daily to the home in Germany
| | |
|---|---|
| **What?** | For employees living in Germany: whether they return daily to their main residence in Germany. For replacement income, the question is whether they did so during or before receiving it. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee is subject to source tax and lives in Germany |
| **When is it required?** | Always when asked |
| **Depends on** | Country (of the home address), Type of income (source tax), Employee is subject to source tax |
| **Who needs it?** | source tax office: Decides between the cross-border (Grenzgänger) tariff and the normal tariff |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-69edd5, F-zh_source_tax_calculator-64ac42, F-zh_source_tax_calculator-31d762, F-zh_source_tax_calculator-099cf0, F-zh_source_tax_calculator-532d5f, F-zh_source_tax_calculator-5c099a, F-hr_transcript-8595fb |

#### Certificate of residence provided
| | |
|---|---|
| **What?** | For employees living in Germany who return daily: whether a certificate of residence (Ansässigkeitsbescheinigung) has been provided. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Germany and returns daily |
| **When is it required?** | Always when asked |
| **Depends on** | Country (of the home address), Returns daily to the home in Germany, Employee is subject to source tax |
| **Who needs it?** | source tax office: With a certificate the cross-border tariff applies, without it the normal tariff |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-687e8b, F-zh_source_tax_calculator-823151, F-zh_source_tax_calculator-5f6820, F-zh_source_tax_calculator-993db3, F-zh_source_tax_calculator-2754e8 |
| **Notes** | Probably the 'German forms' HR could not name. See OQ-proof-documents. |

#### Daily return reasonable (under 100 km)
| | |
|---|---|
| **What?** | For employees living in Germany who do not return daily: whether daily return is basically reasonable (driving distance under 100 km). For replacement income: during or before receiving it. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Germany and does not return daily |
| **When is it required?** | Always when asked |
| **Depends on** | Country (of the home address), Returns daily to the home in Germany, Employee is subject to source tax |
| **Who needs it?** | source tax office: Not reasonable leads to the normal tariff |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-d2b3cf, F-zh_source_tax_calculator-087ae5, F-zh_source_tax_calculator-aaece6, F-zh_source_tax_calculator-580ad4, F-zh_source_tax_calculator-a18842, F-zh_source_tax_calculator-5373ec, F-zh_source_tax_calculator-c8aa5e |

#### Proof of more than 60 work-related non-return days
| | |
|---|---|
| **What?** | For employees living in Germany for whom daily return is reasonable: whether proof of more than 60 work-related non-return days in the calendar year has been provided. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if daily return to Germany is reasonable |
| **When is it required?** | Always when asked |
| **Depends on** | Country (of the home address), Daily return reasonable (under 100 km), Employee is subject to source tax |
| **Who needs it?** | source tax office: With proof the normal tariff applies, without it the cross-border tariff |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-e8ffac, F-zh_source_tax_calculator-ea3cd8, F-zh_source_tax_calculator-33ef31, F-zh_source_tax_calculator-ab4fae, F-zh_source_tax_calculator-bab153, F-zh_source_tax_calculator-6746d6, F-zh_source_tax_calculator-c8aa5e |

#### Returns daily to the home in Liechtenstein
| | |
|---|---|
| **What?** | For employees living in Liechtenstein: whether they return daily to their main residence there. For replacement income: during or before receiving it. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee is subject to source tax and lives in Liechtenstein |
| **When is it required?** | Always when asked |
| **Depends on** | Country (of the home address), Type of income (source tax), Employee is subject to source tax |
| **Who needs it?** | source tax office: Daily return means that in principle there is no source tax liability (subject to the double taxation agreement) |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-981b6b, F-zh_source_tax_calculator-a2041b, F-zh_source_tax_calculator-e22d17, F-zh_source_tax_calculator-cf291a, F-zh_source_tax_calculator-589042, F-zh_source_tax_calculator-634043, F-zh_source_tax_calculator-fb87f1 |

#### More than 45 work-related non-return days
| | |
|---|---|
| **What?** | For employees living in Liechtenstein who do not return daily: whether they have more than 45 work-related non-return days in the calendar year. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Liechtenstein and does not return daily |
| **When is it required?** | Always when asked |
| **Depends on** | Country (of the home address), Returns daily to the home in Liechtenstein, Employee is subject to source tax |
| **Who needs it?** | source tax office: More than 45 days: normal tariff (subject to the double taxation agreement). Otherwise in principle no liability |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-e96210, F-zh_source_tax_calculator-0ff846, F-zh_source_tax_calculator-f4ece9, F-zh_source_tax_calculator-b207ef, F-zh_source_tax_calculator-dd0a17, F-zh_source_tax_calculator-a24a52, F-zh_source_tax_calculator-cc19c7, F-zh_source_tax_calculator-fb87f1 |

### Business rules in this section

#### Residence answers for the source tax calculator
The calculator's 'main residence in Switzerland?' and 'country of residence' questions are answered from the country of the home address, not asked again: Switzerland gives main residence in Switzerland. Germany and Liechtenstein give that country. Any other country gives 'other country' (Anderes Land). Switzerland and other countries give the base tariff without more residence questions.

| # | Country of residence | → Result | Sources |
|---|---|---|---|
| 1 | Switzerland | Main residence in Switzerland: yes | F-zh_source_tax_calculator-aedb40, F-zh_source_tax_calculator-f86c6b |
| 2 | Germany | Main residence in Switzerland: no. Country of residence: Germany (Germany questions follow) | F-zh_source_tax_calculator-4c65ae, F-zh_source_tax_calculator-d62dd4, F-zh_source_tax_calculator-31d762 |
| 3 | Liechtenstein | Main residence in Switzerland: no. Country of residence: Liechtenstein (Liechtenstein questions follow) | F-zh_source_tax_calculator-4c65ae, F-zh_source_tax_calculator-d62dd4, F-zh_source_tax_calculator-e22d17 |
| 4 | any other country | Main residence in Switzerland: no. Country of residence: other country (base tariff) | F-zh_source_tax_calculator-d62dd4, F-zh_source_tax_calculator-f86c6b |

_Status: inferred · Sources: F-zh_source_tax_calculator-aedb40, F-zh_source_tax_calculator-4c65ae, F-zh_source_tax_calculator-d62dd4, F-zh_source_tax_calculator-80bf97, F-zh_source_tax_calculator-f86c6b, G-08, G-09_

## Evidence
- **F-hr_transcript-1d5c07** (hr_transcript, inferred): Consolidated rule: the insurance start date is derived from the first working day. If the first working day is the 1st of a month, insurance starts that day. Otherwise it starts on the 1st of the following month.
  - "because insurance starts on the first of the following month." — hr_transcript/T-026, Anna
  - "Unless somebody starts exactly on the first, of course, then it's just that day." — hr_transcript/T-028, Anna
- **F-hr_transcript-2334d8** (hr_transcript): If the employee is married, the pension fund wants the spouse's date of birth.
  - "And if someone is married, they want the date of birth of the husband or wife." — hr_transcript/T-032, Anna
- **F-hr_transcript-30d25c** (hr_transcript): First version: pension fund insurance starts on the first day of the month after the first working day (for example, first working day 15.03 gives insurance start 01.04).
  - "because insurance starts on the first of the following month. So for her that was the first of April" — hr_transcript/T-026, Anna
- **F-hr_transcript-34494f** (hr_transcript): The source tax questionnaire is the canton of Zurich's online tariff calculator, which outputs the tariff code. HR uses the Zurich calculator for everybody and acknowledges that this is not exactly how it works. Leo agreed to keep it that way for now.
  - "I use the Zurich calculator on the canton's website. The one that gives you the tariff code." — hr_transcript/T-012, Anna
  - "For everybody I use Zurich, by the way. I know it's not exactly how it works, but that's what we do for now." — hr_transcript/T-012, Anna
  - "Understood. We'll keep that for now." — hr_transcript/T-013, Leo
- **F-hr_transcript-35fae3** (hr_transcript, inferred): The employee's nationality is needed to decide whether they are subject to source tax.
  - "If you don't have a Swiss passport, you do source tax." — hr_transcript/T-010, Anna
- **F-hr_transcript-3beee8** (hr_transcript): HR needs the employee's home address because HR posts many documents to employees.
  - "Yes, I need the address, obviously." — hr_transcript/T-014, Anna
  - "We post a lot of documents to people, so it has to be complete." — hr_transcript/T-014, Anna
- **F-hr_transcript-3edf89** (hr_transcript, inferred): HR needs the employee's name. Leo asked about 'Name, address' and Anna answered 'Yes', but she only elaborated on the address.
  - "What about the basics? Name, address, that kind of thing?" — hr_transcript/T-013, Leo
  - "Yes, I need the address, obviously." — hr_transcript/T-014, Anna
- **F-hr_transcript-3f2c2a** (hr_transcript): Employees who work here but live abroad (examples: Konstanz in Germany, Liechtenstein) are always subject to source tax, regardless of nationality. Even a Swiss citizen living abroad (Stefan) is subject.
  - "Those people do source tax because they work here and they don't live here." — hr_transcript/T-048, Anna
  - "And there it doesn't matter what passport you have, by the way. Stefan is actually Swiss, and he still has it." — hr_transcript/T-048, Anna
  - "So someone living abroad and working here always does it?" — hr_transcript/T-049, Leo
  - "Yes." — hr_transcript/T-050, Anna
- **F-hr_transcript-51c17d** (hr_transcript): Source tax is HR's biggest time sink. Because HR does not know up front who must answer the source tax questions, it sends the whole questionnaire to everybody, which annoys Swiss employees.
  - "Source tax, without any doubt." — hr_transcript/T-008, Anna
  - "So I send the whole questionnaire to everybody, and the Swiss people get annoyed, and they call me." — hr_transcript/T-008, Anna
- **F-hr_transcript-54d011** (hr_transcript, inferred): The spouse's nationality, permit and residence only matter for source tax when the employee is married. They are presumably only needed when the employee would otherwise be subject to source tax (non-Swiss, no C permit, living in Switzerland).
  - "it also changes who has to do it at all." — hr_transcript/T-044, Anna
  - "then you don't do source tax either." — hr_transcript/T-044, Anna
- **F-hr_transcript-550840** (hr_transcript): Leo summarised the rule as 'non-Swiss, but not with a C permit'. Anna only answered 'I think so' (hedged), and later added more conditions.
  - "Okay, so non-Swiss, but not with a C permit. Is that everything?" — hr_transcript/T-039, Leo
  - "I think so." — hr_transcript/T-040, Anna
- **F-hr_transcript-5af8d0** (hr_transcript, inferred): Consolidated final rule. An employee who lives abroad (outside Switzerland) is subject to source tax regardless of nationality. An employee who lives in Switzerland is subject only if they are non-Swiss without a C permit and are not married to a Swiss national or C-permit holder who lives in Switzerland. Note: Anna said 'here', which is read as Switzerland. Her 'I think' hedges remain.
  - "If you don't have a Swiss passport, you do source tax." — hr_transcript/T-010, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — hr_transcript/T-038, Anna
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — hr_transcript/T-044, Anna
  - "Those people do source tax because they work here and they don't live here." — hr_transcript/T-048, Anna
  - "Yes." — hr_transcript/T-050, Anna
- **F-hr_transcript-66fe15** (hr_transcript): Nothing beyond a normal postal address is needed, the way you would write it on an envelope.
  - "No, no. Just a normal address, the way you would write it on an envelope." — hr_transcript/T-016, Anna
- **F-hr_transcript-6a0a40** (hr_transcript): For married employees, the source tax calculator asks whether the spouse works.
  - "It changes the questions in the calculator, yes. Whether the husband or wife works." — hr_transcript/T-044, Anna
- **F-hr_transcript-76eacc** (hr_transcript): For source tax, HR needs the spouse's permit, if the spouse has one.
  - "their permit if they have one" — hr_transcript/T-046, Anna
- **F-hr_transcript-845204** (hr_transcript): Correction: non-Swiss employees with a C permit are not subject to source tax. They are treated like Swiss people (example: Maria, Portuguese, C permit).
  - "No, that's actually not right." — hr_transcript/T-038, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — hr_transcript/T-038, Anna
- **F-hr_transcript-8595fb** (hr_transcript): For employees living abroad, the calculator asks more questions, and Germany has its own forms. Anna cannot remember what they are called. Leo deferred to the calculator, so the exact questions are unresolved in this transcript.
  - "And with them the calculator gets much more complicated, there are more questions. Germany has its own forms, I can never remember what they're called." — hr_transcript/T-050, Anna
  - "Okay, that's fine, the calculator will tell us." — hr_transcript/T-051, Leo
- **F-hr_transcript-872bd7** (hr_transcript): The pension fund needs the employee's first working day. Anna calls it the number one item.
  - "I need their first working day. That's the number one thing" — hr_transcript/T-024, Anna
- **F-hr_transcript-a45422** (hr_transcript): Today HR checks the spouse exemption by hand and asks for the spouse details by email, which takes forever.
  - "I always have to check that one by hand." — hr_transcript/T-044, Anna
  - "I ask them by email, and it takes forever." — hr_transcript/T-046, Anna
- **F-hr_transcript-ab3cba** (hr_transcript, inferred): The employee's country of residence (the country of the home address) is needed to decide source tax liability for cross-border employees.
  - "Those people do source tax because they work here and they don't live here." — hr_transcript/T-048, Anna
- **F-hr_transcript-b0527c** (hr_transcript): First version: all non-Swiss employees (anyone without a Swiss passport) are subject to source tax.
  - "All the non-Swiss employees. Simple as that. If you don't have a Swiss passport, you do source tax." — hr_transcript/T-010, Anna
- **F-hr_transcript-b84498** (hr_transcript, inferred): Source tax questions should only be asked of employees who are subject to source tax, not of everybody.
  - "Because I never know up front who has to answer those questions." — hr_transcript/T-008, Anna
  - "So who actually needs to answer them?" — hr_transcript/T-009, Leo
- **F-hr_transcript-b90bd9** (hr_transcript): An employee married to a Swiss person, or to someone with a C permit, is not subject to source tax if that spouse lives 'here'. Example: Tomás, Brazilian with a B permit, has a Swiss wife and they live in Winterthur, so he has no source tax.
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — hr_transcript/T-044, Anna
  - "Tomás in logistics, for example. Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." — hr_transcript/T-044, Anna
- **F-hr_transcript-bd8c8e** (hr_transcript): Anna is unsure of the civil status options. From memory she named Single, Married, Divorced and ('I think') Widowed, and said the screenshots will show the actual list.
  - "I'd have to look. You'll see it in the screenshots. Single, married, divorced, I think widowed." — hr_transcript/T-034, Anna
- **F-hr_transcript-c0fe95** (hr_transcript): The address must be complete: street, house number, postcode, town and country.
  - "The full address. Street, number, postcode, town, country." — hr_transcript/T-014, Anna
- **F-hr_transcript-c9d9b9** (hr_transcript, inferred): The permit type of non-Swiss employees is needed to decide source tax liability (a C permit exempts them). The permit type is only relevant for non-Swiss employees.
  - "So, not the people with a C permit." — hr_transcript/T-038, Anna
- **F-hr_transcript-ce8ca4** (hr_transcript): The pension fund asks for the employee's civil status.
  - "Yes, the civil status. They ask for that." — hr_transcript/T-032, Anna
- **F-hr_transcript-e18e66** (hr_transcript, inferred): When the first working day changes, the insurance start date given to the pension fund must be re-derived and updated. A missed update (Julia) caused a wrong date at the fund, an unfriendly letter and weeks of fixing.
  - "She moved her first working day to the 15th of March, and I didn't update it." — hr_transcript/T-026, Anna
  - "I got a very unfriendly letter." — hr_transcript/T-026, Anna
  - "It took weeks to fix." — hr_transcript/T-028, Anna
- **F-hr_transcript-e3721e** (hr_transcript): The employee should confirm the first working day, because it changes often (for example, when people negotiate an earlier exit with their old employer).
  - "I ask them to confirm it, because it moves more often than you'd think." — hr_transcript/T-024, Anna
  - "People negotiate with their old employer, they get out a week earlier." — hr_transcript/T-026, Anna
- **F-hr_transcript-e5337d** (hr_transcript): For source tax, HR needs to know whether the spouse lives 'here'.
  - "and that they live here." — hr_transcript/T-046, Anna
- **F-hr_transcript-f3ce84** (hr_transcript): For source tax, HR needs the spouse's nationality.
  - "So you need to know about the spouse as well." — hr_transcript/T-045, Leo
  - "Yes. Their nationality, their permit if they have one, and that they live here." — hr_transcript/T-046, Anna
- **F-hr_transcript-fdf50a** (hr_transcript): Exception: if the first working day is the first day of a month, insurance starts on that same day.
  - "Unless somebody starts exactly on the first, of course, then it's just that day." — hr_transcript/T-028, Anna
- **F-pension_portal-3432a9** (pension_portal): The Canton dropdown offers exactly these 26 options: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for a residence outside Switzerland.
  - "Canton" — 02-canton-list.png (pension_portal/S02-E10)
  - "Aargau" — 02-canton-list.png (pension_portal/S02-E12)
  - "Appenzell Ausserrhoden" — 02-canton-list.png (pension_portal/S02-E13)
  - "Appenzell Innerrhoden" — 02-canton-list.png (pension_portal/S02-E14)
  - "Basel-Landschaft" — 02-canton-list.png (pension_portal/S02-E15)
  - "Basel-Stadt" — 02-canton-list.png (pension_portal/S02-E16)
  - "Bern" — 02-canton-list.png (pension_portal/S02-E17)
  - "Fribourg" — 02-canton-list.png (pension_portal/S02-E18)
  - "Geneva" — 02-canton-list.png (pension_portal/S02-E19)
  - "Glarus" — 02-canton-list.png (pension_portal/S02-E20)
  - "Graubünden" — 02-canton-list.png (pension_portal/S02-E21)
  - "Jura" — 02-canton-list.png (pension_portal/S02-E22)
  - "Lucerne" — 02-canton-list.png (pension_portal/S02-E23)
  - "Neuchâtel" — 02-canton-list.png (pension_portal/S02-E24)
  - "Nidwalden" — 02-canton-list.png (pension_portal/S02-E25)
  - "Obwalden" — 02-canton-list.png (pension_portal/S02-E26)
  - "Schaffhausen" — 02-canton-list.png (pension_portal/S02-E27)
  - "Schwyz" — 02-canton-list.png (pension_portal/S02-E28)
  - "Solothurn" — 02-canton-list.png (pension_portal/S02-E29)
  - "St. Gallen" — 02-canton-list.png (pension_portal/S02-E30)
  - "Thurgau" — 02-canton-list.png (pension_portal/S02-E31)
  - "Ticino" — 02-canton-list.png (pension_portal/S02-E32)
  - "Uri" — 02-canton-list.png (pension_portal/S02-E33)
  - "Valais" — 02-canton-list.png (pension_portal/S02-E34)
  - "Vaud" — 02-canton-list.png (pension_portal/S02-E35)
  - "Zug" — 02-canton-list.png (pension_portal/S02-E36)
  - "Zurich" — 02-canton-list.png (pension_portal/S02-E37)
- **F-pension_portal-39bab1** (pension_portal): The 'Spouse's date of birth' field appears only when Civil status is 'Married' (shown in screenshots 05 and 07, both with Married); it is absent in screenshot 04 (Civil status 'Single') and in screenshots 01, 02, 03 and 06 (Civil status not selected).
  - "Married" — 05-married.png (pension_portal/S05-E20)
  - "Spouse's date of birth" — 05-married.png (pension_portal/S05-E21)
  - "Married" — 07-married-missing-spouse.png (pension_portal/S07-E20)
  - "Spouse's date of birth" — 07-married-missing-spouse.png (pension_portal/S07-E21)
  - "Single" — 04-single.png (pension_portal/S04-E20)
- **F-pension_portal-3a97ab** (pension_portal, inferred): The portal requires an insurance start date on the 1st of a month but does not show how it relates to the employee's first working day (e.g. which 1st of a month to choose when work starts mid-month); the derivation rule is unknown.
  - "DD.MM.YYYY. Must be the 1st of a month." — 01-empty.png (pension_portal/S01-E14)
- **F-pension_portal-3d1ae4** (pension_portal): The Civil status dropdown offers exactly these options: Single, Married, Divorced, Widowed.
  - "Civil status" — 03-civil-status-list.png (pension_portal/S03-E19)
  - "Single" — 03-civil-status-list.png (pension_portal/S03-E21)
  - "Married" — 03-civil-status-list.png (pension_portal/S03-E22)
  - "Divorced" — 03-civil-status-list.png (pension_portal/S03-E23)
  - "Widowed" — 03-civil-status-list.png (pension_portal/S03-E24)
- **F-pension_portal-44a27b** (pension_portal): Submitting the form with empty required fields shows the banner 'Please correct the highlighted fields.' and a per-field error of the form '<Field> is required.' for First name, Last name, Date of birth, Canton, Insurance start date and Civil status.
  - "Please correct the highlighted fields." — 06-required-errors.png (pension_portal/S06-E05)
  - "First name is required." — 06-required-errors.png (pension_portal/S06-E08)
  - "Last name is required." — 06-required-errors.png (pension_portal/S06-E10)
  - "Date of birth is required." — 06-required-errors.png (pension_portal/S06-E13)
  - "Canton is required." — 06-required-errors.png (pension_portal/S06-E16)
  - "Insurance start date is required." — 06-required-errors.png (pension_portal/S06-E20)
  - "Civil status is required." — 06-required-errors.png (pension_portal/S06-E23)
- **F-pension_portal-509cbe** (pension_portal): The pension fund registration form has a text field 'Insurance start date' in the Insurance section, marked required.
  - "Insurance start date" — 01-empty.png (pension_portal/S01-E13)
  - "Insurance" — 01-empty.png (pension_portal/S01-E12)
- **F-pension_portal-6c621f** (pension_portal): The pension fund registration form has a dropdown 'Canton' in the Employee section, marked required, with placeholder 'Please select'.
  - "Canton" — 01-empty.png (pension_portal/S01-E10)
  - "Please select" — 01-empty.png (pension_portal/S01-E11)
- **F-pension_portal-8664f4** (pension_portal): The pension fund registration form has a dropdown 'Civil status' in the Insurance section, marked required, with placeholder 'Please select'.
  - "Civil status" — 01-empty.png (pension_portal/S01-E15)
  - "Please select" — 01-empty.png (pension_portal/S01-E16)
- **F-pension_portal-88b436** (pension_portal): The pension fund registration form has a text field 'Date of birth' (employee), marked required.
  - "Date of birth" — 01-empty.png (pension_portal/S01-E08)
- **F-pension_portal-967bc9** (pension_portal): Date of birth must be entered in the format DD.MM.YYYY.
  - "DD.MM.YYYY" — 01-empty.png (pension_portal/S01-E09)
- **F-pension_portal-a0065b** (pension_portal): The pension fund registration form has a text field 'Spouse's date of birth', marked required when shown.
  - "Spouse's date of birth" — 05-married.png (pension_portal/S05-E21)
- **F-pension_portal-b359c3** (pension_portal, inferred): The portal does not say whether 'Canton' means canton of residence or of work, and the list offers no option for employees living outside Switzerland; how to register such employees is unknown.
  - "Canton" — 01-empty.png (pension_portal/S01-E10)
  - "Zurich" — 02-canton-list.png (pension_portal/S02-E37)
- **F-pension_portal-c5ee15** (pension_portal): When Civil status is 'Married', registration is blocked if Spouse's date of birth is empty, with the error 'Spouse's date of birth is required.'
  - "Married" — 07-married-missing-spouse.png (pension_portal/S07-E20)
  - "Spouse's date of birth is required." — 07-married-missing-spouse.png (pension_portal/S07-E24)
- **F-pension_portal-c688e4** (pension_portal): The pension fund registration form has a text field 'Last name', marked required.
  - "Last name" — 01-empty.png (pension_portal/S01-E07)
- **F-pension_portal-db702a** (pension_portal): The pension fund registration form has a text field 'First name', marked required.
  - "First name" — 01-empty.png (pension_portal/S01-E06)
  - "Fields marked * are required." — 01-empty.png (pension_portal/S01-E19)
- **F-pension_portal-dd8126** (pension_portal): Insurance start date must be in the format DD.MM.YYYY and must be the 1st of a month.
  - "DD.MM.YYYY. Must be the 1st of a month." — 01-empty.png (pension_portal/S01-E14)
- **F-pension_portal-ef28c3** (pension_portal): Spouse's date of birth must be entered in the format DD.MM.YYYY.
  - "DD.MM.YYYY" — 05-married.png (pension_portal/S05-E23)
- **F-zh_source_tax_calculator-0137bf** (zh_source_tax_calculator): The spouse employment question is shown only when civil status is 'Verheiratet oder eingetragene Partnerschaft'.
  - "Ist der Ehegatte / eingetragene Partner erwerbstätig oder bezieht er/sie Ersatzeinkünfte?" — zh_source_tax_calculator/C-Q04
- **F-zh_source_tax_calculator-037b1c** (zh_source_tax_calculator, inferred): A single/divorced/separated/widowed person without counted children with earned income and residence in Switzerland gets tariff A (A0Y/A0N).
  - ""Q06": "Nein", "Q16": "Ja"} -> result Tarif: A0Y" — zh_source_tax_calculator/C-V01
- **F-zh_source_tax_calculator-051bb9** (zh_source_tax_calculator): Civil status options are exactly two groups: 'Verheiratet oder eingetragene Partnerschaft' (married or registered partnership) and 'Ledig, Geschieden, Getrennt, Verwitwet' (single, divorced, separated, widowed).
  - "Options: Verheiratet oder eingetragene Partnerschaft | Ledig, Geschieden, Getrennt, Verwitwet" — zh_source_tax_calculator/C-Q02
- **F-zh_source_tax_calculator-087ae5** (zh_source_tax_calculator): Daily return reasonable options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q20
- **F-zh_source_tax_calculator-099cf0** (zh_source_tax_calculator): For replacement income with residence in Germany, the calculator asks whether the person returned daily to the main residence in Germany during or before receiving the replacement income.
  - "Tägliche Rückkehr an den Hauptwohnsitz in Deutschland während oder vor Bezug der Ersatzeinkünfte?" — zh_source_tax_calculator/C-Q24
- **F-zh_source_tax_calculator-09b06d** (zh_source_tax_calculator): Child age status options are exactly: Minderjährig, Volljährig und in Erstausbildung, weder noch.
  - "Options: Minderjährig | Volljährig und in Erstausbildung | weder noch" — zh_source_tax_calculator/C-Q07
- **F-zh_source_tax_calculator-0ff846** (zh_source_tax_calculator): More than 45 non-return days options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q23
- **F-zh_source_tax_calculator-103b19** (zh_source_tax_calculator): For married persons, the calculator asks whether the person or the spouses/partners have biological or adopted children.
  - "Leibliche oder adoptierte Kinder der Person oder der Ehegatten bzw. Partner?" — zh_source_tax_calculator/C-Q05
- **F-zh_source_tax_calculator-208104** (zh_source_tax_calculator): For earned income, the calculator asks for the confession (religious denomination) of the person.
  - "Konfession" — zh_source_tax_calculator/C-Q03
- **F-zh_source_tax_calculator-2754e8** (zh_source_tax_calculator, inferred): Replacement income, Germany: daily return with certificate -> Q; daily return without certificate -> G; no daily return, reasonable, no >60-day proof -> Q; with proof -> G; not reasonable -> G.
  - ""Q24": "Ja", "Q19": "Nein"} -> result Tarif: G" — zh_source_tax_calculator/C-V45
  - ""Q25": "Ja", "Q26": "Nein"} -> result Tarif: Q" — zh_source_tax_calculator/C-V46
  - ""Q25": "Ja", "Q26": "Ja"} -> result Tarif: G" — zh_source_tax_calculator/C-V47
  - ""Q25": "Nein"} -> result Tarif: G" — zh_source_tax_calculator/C-V48
- **F-zh_source_tax_calculator-2d4dda** (zh_source_tax_calculator, inferred): Replacement income (Ersatzeinkünfte) yields tariff G (cross-border variant Q), without child digit or confession suffix.
  - "Answers {"Q01": "Ersatzeinkünfte", "Q16": "Ja"} -> result Tarif: G" — zh_source_tax_calculator/C-V43
- **F-zh_source_tax_calculator-2eab9a** (zh_source_tax_calculator, inferred): Confession sets the church-tax suffix of the tariff: Y for röm.-kath./christ.-kath./evang.-ref., N for none or other (e.g. A0Y vs A0N).
  - "Sets the church-tax suffix: Y = röm.-kath., christ.-kath., evang.-ref.; N = Keine oder andere" — zh_source_tax_calculator/C-Q03
  - "result Tarif: A0Y" — zh_source_tax_calculator/C-V01
  - "result Tarif: A0N" — zh_source_tax_calculator/C-V02
- **F-zh_source_tax_calculator-300c72** (zh_source_tax_calculator, inferred): For a single/divorced/separated/widowed person, any child counted with H gives an H tariff; a child counts with H when it lives in the household and the person has sole custody or is the main financial contributor.
  - "For a single person, any child counted with H gives an H tariff (e.g. A1 + H1 -> H2N). A child is counted with H when it lives in the household and the person has sole custody or is the main financial contributor." — zh_source_tax_calculator/C-N04
  - "result Tarif: H1Y (Kind Ergebnis: H1)" — zh_source_tax_calculator/C-V17
- **F-zh_source_tax_calculator-31d762** (zh_source_tax_calculator): Q18 is shown only when income type is Erwerbseinkommen and country of residence is Deutschland.
  - "Tägliche Rückkehr an den Hauptwohnsitz in Deutschland?" — zh_source_tax_calculator/C-Q18
- **F-zh_source_tax_calculator-32fec9** (zh_source_tax_calculator): Parental care (Q14) options are Ja / Nein.
  - "Elterliche Sorge Options: Ja | Nein" — zh_source_tax_calculator/C-Q14
- **F-zh_source_tax_calculator-33ef31** (zh_source_tax_calculator): Q21 is shown only when daily return is reasonable (Q20 = Ja).
  - "Nachweis von mehr als 60 beruflich bedingten Nichtrückkehrtagen im Kalenderjahr beigebracht?" — zh_source_tax_calculator/C-Q21
- **F-zh_source_tax_calculator-351289** (zh_source_tax_calculator): If the income type is Ersatzeinkünfte, all personal and child questions are skipped and the calculator goes straight to the main-residence question (Q16).
  - "Ersatzeinkünfte skips all personal/child questions and goes straight to Q16." — zh_source_tax_calculator/C-Q01
- **F-zh_source_tax_calculator-3a75cc** (zh_source_tax_calculator): Same-household options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q08
- **F-zh_source_tax_calculator-3eb561** (zh_source_tax_calculator, inferred): Adult child in first education: in household with common household (married) counts (B1N); not in household counts only if more than 50% of maintenance is provided (single A1N; married with Nein -> B0N); single, in household without common household and >50% maintenance gives H1N.
  - ""Q10": "Ja", "Q16": "Ja"} -> result Tarif: B1N" — zh_source_tax_calculator/C-V14
  - ""Q15": "Nein", "Q16": "Ja"} -> result Tarif: B0N" — zh_source_tax_calculator/C-V15
  - "result Tarif: A1N (Kind Ergebnis: A1)" — zh_source_tax_calculator/C-V22
  - ""Q15": "Ja", "Q16": "Ja"} -> result Tarif: H1N" — zh_source_tax_calculator/C-V23
- **F-zh_source_tax_calculator-4b7063** (zh_source_tax_calculator): For a minor child in the same household, the calculator asks about parental custody (shared or sole).
  - "Elterliche Sorge Options: Geteiltes Sorgerecht | Alleiniges Sorgerecht" — zh_source_tax_calculator/C-Q09
- **F-zh_source_tax_calculator-4c53e3** (zh_source_tax_calculator, inferred): The tariff digit equals the number of children whose per-child result digit is 1 (e.g. three counted children -> C3Y).
  - "The final tariff's digit equals the number of children whose 'Kind Ergebnis' digit is 1." — zh_source_tax_calculator/C-N04
  - "result Tarif: C3Y" — zh_source_tax_calculator/C-V28
- **F-zh_source_tax_calculator-4c65ae** (zh_source_tax_calculator): If the main residence is not in Switzerland, the calculator asks for the country of residence.
  - "Wohnsitzstaat" — zh_source_tax_calculator/C-Q17
- **F-zh_source_tax_calculator-532d5f** (zh_source_tax_calculator): Q24 options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q24
- **F-zh_source_tax_calculator-5373ec** (zh_source_tax_calculator): Q25 is shown only when income type is Ersatzeinkünfte, country is Deutschland and Q24 = Nein.
  - "Tägliche Rückkehr grundsätzlich zumutbar während oder vor Bezug der Ersatzeinkünfte" — zh_source_tax_calculator/C-Q25
- **F-zh_source_tax_calculator-5686d7** (zh_source_tax_calculator, inferred): Single, minor child in household, shared custody, common household with the other parent and other parent as main contributor gives A0N.
  - ""Q12": "Anderer Elternteil", "Q16": "Ja"} -> result Tarif: A0N (Kind Ergebnis: A0)" — zh_source_tax_calculator/C-V18
- **F-zh_source_tax_calculator-5725a8** (zh_source_tax_calculator): For each minor or adult-in-first-education child, the calculator asks whether the child lives in the same household.
  - "Wohnsitz des Kindes im selben Haushalt?" — zh_source_tax_calculator/C-Q08
- **F-zh_source_tax_calculator-580ad4** (zh_source_tax_calculator): For replacement income, Germany residents without daily return are asked whether daily return was basically reasonable (less than 100 km) during or before receipt of the replacement income.
  - "Tägliche Rückkehr grundsätzlich zumutbar während oder vor Bezug der Ersatzeinkünfte (weniger als 100km Fahrdistanz)?" — zh_source_tax_calculator/C-Q25
- **F-zh_source_tax_calculator-589042** (zh_source_tax_calculator): Q27 options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q27
- **F-zh_source_tax_calculator-5c099a** (zh_source_tax_calculator): Q24 is shown only when income type is Ersatzeinkünfte and country is Deutschland.
  - "während oder vor Bezug der Ersatzeinkünfte?" — zh_source_tax_calculator/C-Q24
- **F-zh_source_tax_calculator-5d8fb0** (zh_source_tax_calculator, inferred): Married, minor child in household, shared custody and common household with the other parent: the child counts (C1Y).
  - ""Q10": "Ja", "Q16": "Ja"} -> result Tarif: C1Y" — zh_source_tax_calculator/C-V09
- **F-zh_source_tax_calculator-5f6820** (zh_source_tax_calculator): The residence certificate question is shown only when the person (Germany resident) returns daily (Q18 = Ja for earned income, Q24 = Ja for replacement income).
  - "Ansässigkeitsbescheinigung beigebracht?" — zh_source_tax_calculator/C-Q19
- **F-zh_source_tax_calculator-634043** (zh_source_tax_calculator): Q27 is shown only when income type is Ersatzeinkünfte and country is Liechtenstein.
  - "Tägliche Rückkehr an den Hauptwohnsitz in Liechtenstein während oder vor Bezug der Ersatzeinkünfte?" — zh_source_tax_calculator/C-Q27
- **F-zh_source_tax_calculator-640429** (zh_source_tax_calculator): For each child, the calculator asks whether the child is minor, or adult and in first education.
  - "Kind minderjährig oder volljährig und in Erstausbildung?" — zh_source_tax_calculator/C-Q07
- **F-zh_source_tax_calculator-64ac33** (zh_source_tax_calculator): Alternating custody is asked only for a minor child when: (in household, shared custody, no common household with other parent) or (married, not in household, shared custody Q13 = Ja) or (non-married, not in household, parental care Q14 = Ja).
  - "Alternierende Obhut?" — zh_source_tax_calculator/C-Q11
- **F-zh_source_tax_calculator-64ac42** (zh_source_tax_calculator): Daily return to Germany options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q18
- **F-zh_source_tax_calculator-6746d6** (zh_source_tax_calculator): Q26 is shown only when Q25 = Ja.
  - "beigebracht während oder vor Bezug der Ersatzeinkünfte?" — zh_source_tax_calculator/C-Q26
- **F-zh_source_tax_calculator-687e8b** (zh_source_tax_calculator): The calculator asks whether a certificate of residence (Ansässigkeitsbescheinigung) has been provided.
  - "Ansässigkeitsbescheinigung beigebracht?" — zh_source_tax_calculator/C-Q19
- **F-zh_source_tax_calculator-69edd5** (zh_source_tax_calculator): For earned income with residence in Germany, the calculator asks whether the person returns daily to the main residence in Germany.
  - "Tägliche Rückkehr an den Hauptwohnsitz in Deutschland?" — zh_source_tax_calculator/C-Q18
- **F-zh_source_tax_calculator-6bed1f** (zh_source_tax_calculator): The child questions are shown only when the person answered Ja to having children (Q05 or Q06), with one block per child ('Kind 1', 'Kind 2', …).
  - "Section heading: 'Angaben zu den Kindern'" — zh_source_tax_calculator/C-Q07
- **F-zh_source_tax_calculator-6dcf5c** (zh_source_tax_calculator): The common-household question is shown only when (child minor, in same household, shared custody) or (child adult in first education and in same household).
  - "Gemeinsamer Haushalt mit dem anderen Elternteil?" — zh_source_tax_calculator/C-Q10
- **F-zh_source_tax_calculator-75cd87** (zh_source_tax_calculator): The non-married children question is shown only when civil status is 'Ledig, Geschieden, Getrennt, Verwitwet' and confession is answered.
  - "Leibliche oder adoptierte Kinder der Person?" — zh_source_tax_calculator/C-Q06
- **F-zh_source_tax_calculator-7b637b** (zh_source_tax_calculator): For married persons / registered partners, the calculator asks whether the spouse/registered partner is gainfully employed or receives replacement income.
  - "Ist der Ehegatte / eingetragene Partner erwerbstätig oder bezieht er/sie Ersatzeinkünfte?" — zh_source_tax_calculator/C-Q04
- **F-zh_source_tax_calculator-7c667f** (zh_source_tax_calculator): The same-household question is shown only when the child is Minderjährig or Volljährig und in Erstausbildung.
  - "Wohnsitz des Kindes im selben Haushalt?" — zh_source_tax_calculator/C-Q08
- **F-zh_source_tax_calculator-7dcce6** (zh_source_tax_calculator): Q13 is shown only when civil status is married/registered partnership, the child is minor and not in the same household.
  - "Geteiltes Sorgerecht" — zh_source_tax_calculator/C-Q13
- **F-zh_source_tax_calculator-80bf97** (zh_source_tax_calculator): The country of residence question is shown only when main residence in Switzerland = Nein.
  - "Wohnsitzstaat" — zh_source_tax_calculator/C-Q17
- **F-zh_source_tax_calculator-823151** (zh_source_tax_calculator): Residence certificate options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q19
- **F-zh_source_tax_calculator-83de1d** (zh_source_tax_calculator): The custody question (Q09) is shown only when the child is Minderjährig and lives in the same household, for both civil status groups.
  - "Elterliche Sorge" — zh_source_tax_calculator/C-Q09
- **F-zh_source_tax_calculator-9007c3** (zh_source_tax_calculator): For earned income, the calculator asks for the civil status of the person subject to source tax.
  - "Zivilstand" — zh_source_tax_calculator/C-Q02
  - "Section heading: 'Angaben zur quellensteuerpflichtigen Person'" — zh_source_tax_calculator/C-Q02
- **F-zh_source_tax_calculator-939b3b** (zh_source_tax_calculator): Main contributor options are exactly: Quellensteuerpflichtige Person (the person subject to source tax) and Anderer Elternteil (other parent).
  - "Options: Quellensteuerpflichtige Person | Anderer Elternteil" — zh_source_tax_calculator/C-Q12
- **F-zh_source_tax_calculator-956f07** (zh_source_tax_calculator): For non-married persons with a minor child not in the household, the calculator asks whether they have parental care (Elterliche Sorge, yes/no).
  - "Same title as Q09, but with Ja/Nein options (internal name child-n__parentalCare)" — zh_source_tax_calculator/C-Q14
- **F-zh_source_tax_calculator-97139a** (zh_source_tax_calculator, inferred): For married/registered partners, a spouse who is employed or receives replacement income leads to tariff C; otherwise tariff B.
  - "Ja -> C tariff; Nein -> B tariff" — zh_source_tax_calculator/C-Q04
  - "result Tarif: B0Y" — zh_source_tax_calculator/C-V03
  - "result Tarif: C0Y" — zh_source_tax_calculator/C-V05
- **F-zh_source_tax_calculator-981b6b** (zh_source_tax_calculator): For earned income with residence in Liechtenstein, the calculator asks whether the person returns daily to the main residence in Liechtenstein.
  - "Tägliche Rückkehr an den Hauptwohnsitz in Liechtenstein?" — zh_source_tax_calculator/C-Q22
- **F-zh_source_tax_calculator-993db3** (zh_source_tax_calculator, inferred): Germany resident with daily return and a residence certificate gets the cross-border (Grenzgänger) tariff: A->L, B->M, C->N, H->P, G->Q; without a certificate the normal tariff applies.
  - "Ja -> cross-border (Grenzgänger) tariff: A->L, B->M, C->N, H->P, G->Q; Nein -> normal tariff" — zh_source_tax_calculator/C-Q19
  - ""Q18": "Ja", "Q19": "Ja"} -> result Tarif: N1Y" — zh_source_tax_calculator/C-V34
  - ""Q18": "Ja", "Q19": "Nein"} -> result Tarif: C1Y" — zh_source_tax_calculator/C-V35
  - ""Q24": "Ja", "Q19": "Ja"} -> result Tarif: Q" — zh_source_tax_calculator/C-V44
- **F-zh_source_tax_calculator-a166c7** (zh_source_tax_calculator): Children question (married) options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q05
- **F-zh_source_tax_calculator-a18842** (zh_source_tax_calculator): Q25 options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q25
- **F-zh_source_tax_calculator-a2041b** (zh_source_tax_calculator): Daily return to Liechtenstein options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q22
- **F-zh_source_tax_calculator-a24a52** (zh_source_tax_calculator): Q28 is shown only when Q27 = Nein.
  - "Mehr als 45 beruflich bedingte Nichtrückkehrtage im Kalenderjahr während oder vor Bezug der Ersatzeinkünfte?" — zh_source_tax_calculator/C-Q28
- **F-zh_source_tax_calculator-a33b65** (zh_source_tax_calculator): The married children question is shown only when civil status is 'Verheiratet oder eingetragene Partnerschaft' and the spouse employment question is answered.
  - "Leibliche oder adoptierte Kinder der Person oder der Ehegatten bzw. Partner?" — zh_source_tax_calculator/C-Q05
- **F-zh_source_tax_calculator-a4d358** (zh_source_tax_calculator, inferred): Married, minor child in household, shared custody, no common household: alternating custody with the other parent as main contributor, or no alternating custody, gives C0Y (child not counted).
  - ""Q12": "Anderer Elternteil", "Q16": "Ja"} -> result Tarif: C0Y" — zh_source_tax_calculator/C-V10
  - ""Q11": "Nein", "Q16": "Ja"} -> result Tarif: C0Y" — zh_source_tax_calculator/C-V11
- **F-zh_source_tax_calculator-aaece6** (zh_source_tax_calculator): Q20 is shown only when income type is Erwerbseinkommen, country is Deutschland and daily return = Nein.
  - "Tägliche Rückkehr grundsätzlich zumutbar (weniger als 100km Fahrdistanz)?" — zh_source_tax_calculator/C-Q20
- **F-zh_source_tax_calculator-ab4fae** (zh_source_tax_calculator): For replacement income, the calculator asks whether proof of more than 60 work-related non-return days in the calendar year was provided during or before receipt of the replacement income.
  - "Nachweis von mehr als 60 beruflich bedingten Nichtrückkehrtagen im Kalenderjahr beigebracht während oder vor Bezug der Ersatzeinkünfte?" — zh_source_tax_calculator/C-Q26
- **F-zh_source_tax_calculator-ab8a06** (zh_source_tax_calculator): For non-married persons, the calculator asks whether the person has biological or adopted children.
  - "Leibliche oder adoptierte Kinder der Person?" — zh_source_tax_calculator/C-Q06
- **F-zh_source_tax_calculator-abe889** (zh_source_tax_calculator): A child answered 'weder noch' (neither minor nor adult in first education) ends the child block and does not count towards the tariff.
  - "'weder noch' ends the child block right away (child does not count)." — zh_source_tax_calculator/C-Q07
  - ""Q07": "weder noch", "Q16": "Ja"} -> result Tarif: B0N" — zh_source_tax_calculator/C-V16
- **F-zh_source_tax_calculator-ad867a** (zh_source_tax_calculator): The main-contributor question is shown when alternating custody = Ja, or for non-married persons when the child is in the household and there is a common household with the other parent; for married persons a common household with the other parent ends the child block without it.
  - "Wer leistet den grösseren finanziellen Beitrag an den Unterhalt des Kindes?" — zh_source_tax_calculator/C-Q12
- **F-zh_source_tax_calculator-aedb40** (zh_source_tax_calculator): The calculator asks whether the main residence is in Switzerland.
  - "Hauptwohnsitz in der Schweiz?" — zh_source_tax_calculator/C-Q16
- **F-zh_source_tax_calculator-b008fe** (zh_source_tax_calculator): For adult children in first education, the calculator asks whether more than 50% of the child's maintenance is mainly provided.
  - "Wird zur Hauptsache (mehr als 50%) für den Kindsunterhalt aufgekommen?" — zh_source_tax_calculator/C-Q15
- **F-zh_source_tax_calculator-b05b44** (zh_source_tax_calculator): Confession is asked only when the income type is Erwerbseinkommen and civil status has been answered.
  - "Konfession" — zh_source_tax_calculator/C-Q03
- **F-zh_source_tax_calculator-b207ef** (zh_source_tax_calculator): For replacement income, Liechtenstein residents without daily return are asked whether they had more than 45 work-related non-return days in the calendar year during or before receipt of the replacement income.
  - "Mehr als 45 beruflich bedingte Nichtrückkehrtage im Kalenderjahr während oder vor Bezug der Ersatzeinkünfte?" — zh_source_tax_calculator/C-Q28
- **F-zh_source_tax_calculator-b62b85** (zh_source_tax_calculator): Children question (non-married) options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q06
- **F-zh_source_tax_calculator-b7fea8** (zh_source_tax_calculator): Confession options are exactly: 'röm.-kath., christ.-kath., evang.-ref.' and 'Keine oder andere' (none or other).
  - "Options: röm.-kath., christ.-kath., evang.-ref. | Keine oder andere" — zh_source_tax_calculator/C-Q03
- **F-zh_source_tax_calculator-bab153** (zh_source_tax_calculator): Q26 options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q26
- **F-zh_source_tax_calculator-c09dc1** (zh_source_tax_calculator): Parental custody options (child in household) are exactly: Geteiltes Sorgerecht (shared) and Alleiniges Sorgerecht (sole).
  - "Options: Geteiltes Sorgerecht | Alleiniges Sorgerecht" — zh_source_tax_calculator/C-Q09
- **F-zh_source_tax_calculator-c8aa5e** (zh_source_tax_calculator, inferred): Germany resident without daily return: if return is not reasonable -> normal tariff; if reasonable and >60 non-return days proven -> normal tariff; if reasonable and no proof -> cross-border tariff (L/M/N/P, Q).
  - "Nein -> normal tariff" — zh_source_tax_calculator/C-Q20
  - "Ja -> normal tariff; Nein -> cross-border tariff (L/M/N/P)" — zh_source_tax_calculator/C-Q21
  - ""Q20": "Ja", "Q21": "Nein"} -> result Tarif: N1Y" — zh_source_tax_calculator/C-V36
  - ""Q20": "Ja", "Q21": "Ja"} -> result Tarif: C1Y" — zh_source_tax_calculator/C-V37
  - ""Q20": "Nein"} -> result Tarif: C1Y" — zh_source_tax_calculator/C-V38
- **F-zh_source_tax_calculator-cb54d9** (zh_source_tax_calculator): Maintenance >50% options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q15
- **F-zh_source_tax_calculator-cc19c7** (zh_source_tax_calculator, inferred): Liechtenstein residents without daily return and more than 45 non-return days get the normal tariff plus 'Unter Vorbehalt des Doppelbesteuerungsabkommens'.
  - "Ja -> normal tariff + 'Unter Vorbehalt des Doppelbesteuerungsabkommens'" — zh_source_tax_calculator/C-Q23
  - "result Tarif: C1Y / Unter Vorbehalt des Doppelbesteuerungsabkommens" — zh_source_tax_calculator/C-V40
  - "result Tarif: G / Unter Vorbehalt des Doppelbesteuerungsabkommens" — zh_source_tax_calculator/C-V50
- **F-zh_source_tax_calculator-cd1015** (zh_source_tax_calculator): Q15 is shown only when the child is adult in first education and either not in the same household, or in the household without a common household with the other parent.
  - "Wird zur Hauptsache (mehr als 50%) für den Kindsunterhalt aufgekommen?" — zh_source_tax_calculator/C-Q15
- **F-zh_source_tax_calculator-cdd0b6** (zh_source_tax_calculator): The calculator asks who makes the larger financial contribution to the child's maintenance.
  - "Wer leistet den grösseren finanziellen Beitrag an den Unterhalt des Kindes?" — zh_source_tax_calculator/C-Q12
- **F-zh_source_tax_calculator-cf291a** (zh_source_tax_calculator): For replacement income with residence in Liechtenstein, the calculator asks whether the person returned daily to the main residence in Liechtenstein during or before receipt of the replacement income.
  - "Tägliche Rückkehr an den Hauptwohnsitz in Liechtenstein während oder vor Bezug der Ersatzeinkünfte?" — zh_source_tax_calculator/C-Q27
- **F-zh_source_tax_calculator-d2b3cf** (zh_source_tax_calculator): For earned income, Germany residents without daily return are asked whether daily return is basically reasonable (less than 100 km driving distance).
  - "Tägliche Rückkehr grundsätzlich zumutbar (weniger als 100km Fahrdistanz)?" — zh_source_tax_calculator/C-Q20
- **F-zh_source_tax_calculator-d2e516** (zh_source_tax_calculator): Shared custody (Q13) options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q13
- **F-zh_source_tax_calculator-d5a6fe** (zh_source_tax_calculator): The income type question is always shown and is the first question.
  - "Für welche Einkünfte möchten Sie den Quellensteuertarif ermitteln?" — zh_source_tax_calculator/C-Q01
- **F-zh_source_tax_calculator-d62dd4** (zh_source_tax_calculator): Country of residence options are exactly: Deutschland, Liechtenstein, Anderes Land (other country).
  - "Options: Deutschland | Liechtenstein | Anderes Land" — zh_source_tax_calculator/C-Q17
- **F-zh_source_tax_calculator-d75286** (zh_source_tax_calculator, inferred): A minor child in the same household with sole custody counts as a child (married: C1/B1; single: H1).
  - "result Tarif: C1Y (Kind Ergebnis: C1)" — zh_source_tax_calculator/C-V07
  - "result Tarif: B1N (Kind Ergebnis: B1)" — zh_source_tax_calculator/C-V08
- **F-zh_source_tax_calculator-d79949** (zh_source_tax_calculator): The calculator asks whether the person lives in a common household with the other parent.
  - "Gemeinsamer Haushalt mit dem anderen Elternteil?" — zh_source_tax_calculator/C-Q10
- **F-zh_source_tax_calculator-da19df** (zh_source_tax_calculator): The calculator asks whether there is alternating custody (alternierende Obhut).
  - "Alternierende Obhut?" — zh_source_tax_calculator/C-Q11
- **F-zh_source_tax_calculator-dc0ae9** (zh_source_tax_calculator, inferred): Single, minor child in household, shared custody, no common household and no alternating custody gives H1N (child counted with H).
  - ""Q11": "Nein", "Q16": "Ja"} -> result Tarif: H1N" — zh_source_tax_calculator/C-V19
- **F-zh_source_tax_calculator-dc6ace** (zh_source_tax_calculator, inferred): Minor child not in the household: with shared custody/parental care, alternating custody and the person as main contributor, the child counts (married B1N, single H1N); without shared custody/parental care it does not count (B0N, A0N).
  - "result Tarif: B1N (Kind Ergebnis: B1)" — zh_source_tax_calculator/C-V12
  - ""Q13": "Nein", "Q16": "Ja"} -> result Tarif: B0N" — zh_source_tax_calculator/C-V13
  - "result Tarif: H1N (Kind Ergebnis: H1)" — zh_source_tax_calculator/C-V20
  - ""Q14": "Nein", "Q16": "Ja"} -> result Tarif: A0N" — zh_source_tax_calculator/C-V21
- **F-zh_source_tax_calculator-dd0a17** (zh_source_tax_calculator): Q28 options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q28
- **F-zh_source_tax_calculator-e06ffd** (zh_source_tax_calculator): The calculator asks which income the source tax tariff is to be determined for.
  - "Für welche Einkünfte möchten Sie den Quellensteuertarif ermitteln?" — zh_source_tax_calculator/C-Q01
- **F-zh_source_tax_calculator-e22d17** (zh_source_tax_calculator): Q22 is shown only when income type is Erwerbseinkommen and country is Liechtenstein.
  - "Tägliche Rückkehr an den Hauptwohnsitz in Liechtenstein?" — zh_source_tax_calculator/C-Q22
- **F-zh_source_tax_calculator-e72e42** (zh_source_tax_calculator): Common-household-with-other-parent options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q10
- **F-zh_source_tax_calculator-e740d1** (zh_source_tax_calculator): Spouse employment options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q04
- **F-zh_source_tax_calculator-e8ffac** (zh_source_tax_calculator): The calculator asks whether proof of more than 60 work-related non-return days in the calendar year has been provided.
  - "Nachweis von mehr als 60 beruflich bedingten Nichtrückkehrtagen im Kalenderjahr beigebracht?" — zh_source_tax_calculator/C-Q21
- **F-zh_source_tax_calculator-e96210** (zh_source_tax_calculator): Liechtenstein residents without daily return are asked whether they have more than 45 work-related non-return days in the calendar year.
  - "Mehr als 45 beruflich bedingte Nichtrückkehrtage im Kalenderjahr?" — zh_source_tax_calculator/C-Q23
- **F-zh_source_tax_calculator-ea3cd8** (zh_source_tax_calculator): Proof of >60 non-return days options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q21
- **F-zh_source_tax_calculator-ebd7b3** (zh_source_tax_calculator): Alternating custody options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q11
- **F-zh_source_tax_calculator-f4ece9** (zh_source_tax_calculator): Q23 is shown only when daily return to Liechtenstein = Nein.
  - "Mehr als 45 beruflich bedingte Nichtrückkehrtage im Kalenderjahr?" — zh_source_tax_calculator/C-Q23
- **F-zh_source_tax_calculator-f86c6b** (zh_source_tax_calculator, inferred): Residence in Switzerland or in 'Anderes Land' gives the base tariff without further residence questions.
  - "CH or 'Anderes Land' -> base tariff." — zh_source_tax_calculator/C-N05
  - ""Q17": "Anderes Land"} -> result Tarif: A0N" — zh_source_tax_calculator/C-V42
  - ""Q17": "Anderes Land"} -> result Tarif: G" — zh_source_tax_calculator/C-V52
- **F-zh_source_tax_calculator-fb4a56** (zh_source_tax_calculator): Q14 is shown only when civil status is 'Ledig, Geschieden, Getrennt, Verwitwet', the child is minor and not in the same household.
  - "Elterliche Sorge Options: Ja | Nein" — zh_source_tax_calculator/C-Q14
- **F-zh_source_tax_calculator-fb87f1** (zh_source_tax_calculator, inferred): Liechtenstein residents with daily return, or without daily return and not more than 45 non-return days, get 'Grundsätzlich keine Quellensteuerpflicht' (in principle no source tax liability), subject to the double taxation agreement.
  - "Ja -> 'Grundsätzlich keine Quellensteuerpflicht'" — zh_source_tax_calculator/C-Q22
  - ""Q22": "Ja"} -> result Grundsätzlich keine Quellensteuerpflicht / Unter Vorbehalt des Doppelbesteuerungsabkommens" — zh_source_tax_calculator/C-V39
  - ""Q23": "Nein"} -> result Grundsätzlich keine Quellensteuerpflicht" — zh_source_tax_calculator/C-V41
  - ""Q27": "Ja"} -> result Grundsätzlich keine Quellensteuerpflicht" — zh_source_tax_calculator/C-V49
- **F-zh_source_tax_calculator-fd9a15** (zh_source_tax_calculator): Child questions repeat per child; 'Ein weiteres Kind erfassen' adds another child block and 'Kind löschen' removes one. Each completed block shows a per-child result ('Kind Ergebnis').
  - "A link button 'Ein weiteres Kind erfassen' adds another child block, and each block has a 'Kind löschen' button." — zh_source_tax_calculator/C-Q07
  - "Child questions repeat for each child (input names child-1__…, child-2__…)." — zh_source_tax_calculator/C-N04
- **F-zh_source_tax_calculator-fe0305** (zh_source_tax_calculator): For married persons with a minor child not in the household, the calculator asks whether custody is shared (Geteiltes Sorgerecht).
  - "Geteiltes Sorgerecht Options: Ja | Nein" — zh_source_tax_calculator/C-Q13
- **F-zh_source_tax_calculator-feb9df** (zh_source_tax_calculator): Income type options are exactly: Erwerbseinkommen (earned income) and Ersatzeinkünfte (replacement income).
  - "Options: Erwerbseinkommen | Ersatzeinkünfte" — zh_source_tax_calculator/C-Q01
- **G-01** (product owner guidance): Lonio collects onboarding data from a new employee **once** and reuses it for every receiving party. Asking too little blocks a registration; asking too much collects personal data we must not have (data minimisation). A question must only be asked when at least one receiving party needs the answer for this person.
- **G-04** (product owner guidance): Scope of these feature specs: what Lonio asks the new employee (which information, in which order, under which conditions, required or not) and the business rules derived from the answers. How collected data is transmitted to each receiving party (exports, portal entry, change notifications) is a separate topic; each information item documents which stakeholder needs it and why.
- **G-07** (product owner guidance): The pension fund screenshots show dropdowns with **all** their options.
- **G-08** (product owner guidance): Prefer asking for primary facts and **deriving** values (e.g. ask the first working day, derive the insurance start date) instead of asking the employee for values they cannot know.
- **G-09** (product owner guidance): Questionnaire language: English.
- **G-10** (product owner guidance): Business wording for values (used in allowed values and examples): countries by English name ("Switzerland", "Germany", "Liechtenstein"), permits as "B permit", "C permit", civil status exactly as the pension fund's list shows it ("Single", "Married", ...), dates as DD.MM.YYYY, yes/no as "yes"/"no".
