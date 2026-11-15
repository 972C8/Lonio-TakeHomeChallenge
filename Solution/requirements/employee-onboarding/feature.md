---
id: employee-onboarding
title: "Employee onboarding questionnaire"
stakeholders: [employee, hr, pension_fund, source_tax]
sections: [SEC-01-questionnaire-flow, SEC-02-personal-details-address, SEC-03-employment-start, SEC-04-civil-status-spouse, SEC-05-source-tax-liability, SEC-06-source-tax-tariff-basics, SEC-07-source-tax-children, SEC-08-cross-border-residence]
stories: [US-01.1, US-01.2, US-01.3, US-01.4, US-01.5, US-01.6, US-02.1, US-02.2, US-02.3, US-02.4, US-03.1, US-03.2, US-03.3, US-04.1, US-04.2, US-04.3, US-05.1, US-05.2, US-05.3, US-06.2, US-06.3, US-06.4, US-06.5, US-06.6, US-07.1, US-07.2, US-07.3, US-07.4, US-07.5, US-07.6, US-08.1, US-08.2, US-08.3, US-08.4]
---

# Employee onboarding questionnaire

Each user story is its own file in [stories/](stories/); this file holds the
feature, its sections and the information and rules they share.

**Goal:** A new employee at Muster AG answers one short English questionnaire in Lonio that asks each piece of information once, and only when a receiving party needs it for that person. From those answers Lonio records everything HR, Pensionskasse Muster and the Zurich source tax office need, including the derived insurance start date and the computed source tax tariff code.

## Context
Today Muster AG's HR collects onboarding data for several receiving parties: the pension fund registration (Pensionskasse Muster portal), the source tax tariff (the Canton of Zurich calculator, which HR clicks through by hand) and HR's own needs, such as a complete postal address for posting documents. Pain points stated by the sources:
- The first working day is HR's 'number one' item, and it often moves (for example when an earlier exit is negotiated with the old employer). The pension fund insurance start date depends on it (F-hr_transcript-872bd7, F-hr_transcript-1d5c07, F-hr_transcript-e18e66).
- Incomplete addresses block posted documents (F-hr_transcript-c0fe95).
- The pension fund's required fields (Canton, Civil status, Spouse's date of birth) do not fit every case: employees abroad, registered partnerships, separated employees (F-pension_portal-b359c3, F-pension_portal-3d1ae4).
- HR's rule for who is subject to source tax took several corrections to state (F-hr_transcript-5af8d0, F-hr_transcript-550840).
- Determining the tariff code is a manual, multi-branch calculator walk-through: civil status, spouse employment, children, confession and the cross-border cases for Germany and Liechtenstein.

Lonio replaces this. It asks each item once and only when a party needs it (data minimisation, G-01). It derives values instead of asking for them (G-08). It computes the full tariff code itself (D-001).

Scope: the employee side of the questionnaire only (G-04, D-034).

Out of scope:
- transmission of the data to the parties
- HR screens and HR changes after submission
- AHV data and IT equipment (G-03)
- the photo for employee badges
- document uploads (D-035)
- income type and replacement income (D-006)
- special tariffs (D-009)

Decisions to follow:
- D-005: only 'C permit yes/no' is asked, never the permit type.
- D-003: registered partnership and separated are mapped provisionally for the fund.
- D-007: Liechtenstein residents may get 'in principle no source tax liability'.
- D-036, D-037: on submission, answers that no longer apply are discarded and the questionnaire becomes read-only. Derived results are always computed from the latest answers.

**Stakeholders:** new employee, HR, pension fund, source tax office

<a id="flow"></a>

## Questionnaire flow

The questionnaire has 7 steps, in English. Only applicable questions are shown, and a step with no applicable question is skipped (e.g. steps 5 and 6 for employees not subject to source tax). Each piece of information is asked once and reused for every receiving party. The order follows dependencies: the home country and civil status come first, because they decide who is asked about nationality, C permit, spouse, source tax details and cross-border questions. Answers that no longer apply after a change are discarded on submission (D-036).

| Step | What is asked | Shown to | Stories |
|---|---|---|---|
| 1. Personal details | First name, last name and date of birth. | Everyone | [US-02.1](stories/US-02.1-collect-the-employee-s-name-and-date-of-birth.md) |
| 2. Home address | Street, house number, postcode, town and country of residence; the canton only if the country is Switzerland. | Everyone | [US-01.1](stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md), [US-01.2](stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md), [US-01.3](stories/US-01.3-ask-each-piece-of-information-once-and-reuse-it-for-every.md), [US-01.4](stories/US-01.4-remind-non-swiss-employees-and-employees-living-abroad-to.md), [US-01.5](stories/US-01.5-discard-answers-that-no-longer-apply-on-submission.md), [US-01.6](stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md), [US-02.2](stories/US-02.2-collect-a-complete-postal-home-address.md), [US-02.3](stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md), [US-02.4](stories/US-02.4-ask-swiss-residents-for-their-canton.md), [US-08.1](stories/US-08.1-derive-the-calculator-s-residence-answers-from-the-home.md) |
| 3. Start | The first working day. | Everyone | [US-03.1](stories/US-03.1-employee-confirms-the-first-working-day.md), [US-03.2](stories/US-03.2-derive-the-pension-insurance-start-date-from-the-first.md), [US-03.3](stories/US-03.3-re-derive-the-insurance-start-date-when-the-first-working.md) |
| 4. Civil status | Civil status (Single, Married, Divorced, Widowed, Registered partnership, Separated); the spouse's or partner's date of birth only if married, in a registered partnership or separated. | Everyone | [US-01.1](stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md), [US-01.2](stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md), [US-01.3](stories/US-01.3-ask-each-piece-of-information-once-and-reuse-it-for-every.md), [US-01.5](stories/US-01.5-discard-answers-that-no-longer-apply-on-submission.md), [US-01.6](stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md), [US-04.1](stories/US-04.1-ask-the-employee-s-civil-status-using-the-pension-fund-s.md), [US-04.2](stories/US-04.2-ask-the-spouse-s-date-of-birth-when-the-employee-is-married.md), [US-04.3](stories/US-04.3-answer-the-calculator-s-civil-status-question-from-the.md) |
| 5. Source tax status | Nationality; whether the employee holds a C permit, only if not Swiss. If not Swiss, without a C permit, and married or in a registered partnership: the spouse's or partner's nationality, whether they hold a C permit (only if not Swiss), and their country of residence (only if Swiss or C permit holder). | Employees living in Switzerland | [US-01.1](stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md), [US-01.2](stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md), [US-01.3](stories/US-01.3-ask-each-piece-of-information-once-and-reuse-it-for-every.md), [US-01.4](stories/US-01.4-remind-non-swiss-employees-and-employees-living-abroad-to.md), [US-01.5](stories/US-01.5-discard-answers-that-no-longer-apply-on-submission.md), [US-01.6](stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md), [US-05.1](stories/US-05.1-ask-nationality-and-c-permit-only-of-employees-living-in.md), [US-05.2](stories/US-05.2-ask-the-spouse-s-nationality-c-permit-and-residence-only.md), [US-05.3](stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md) |
| 6. Source tax details | Religious denomination; whether the spouse or partner works or receives replacement income (only if married or in a registered partnership); whether the employee has children, then for each child the age status, household, custody, care, maintenance and contribution questions that apply to that child; then cross-border questions: for residents of Germany, daily return, certificate of residence (if returning daily; 'not yet' is valid), whether daily return is reasonable and more than 60 non-return days expected (if not returning daily); for residents of Liechtenstein, daily return and more than 45 non-return days expected (if not returning daily). | Employees subject to source tax (residents of Liechtenstein are included) | [US-06.2](stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md), [US-06.3](stories/US-06.3-ask-married-employees-and-registered-partners-subject-to.md), [US-07.1](stories/US-07.1-ask-about-children-only-of-employees-who-need-a-source-tax.md), [US-07.2](stories/US-07.2-one-block-per-child-age-status-and-household.md), [US-07.3](stories/US-07.3-minor-child-living-in-the-employee-s-household.md), [US-07.4](stories/US-07.4-minor-child-not-living-in-the-employee-s-household.md), [US-07.5](stories/US-07.5-adult-child-in-first-education.md), [US-07.6](stories/US-07.6-child-digit-of-the-tariff-code-and-go-live-check-of-the.md), [US-08.2](stories/US-08.2-germany-daily-return-and-certificate-of-residence.md), [US-08.3](stories/US-08.3-germany-no-daily-return-reasonableness-and-more-than-60-non.md), [US-08.4](stories/US-08.4-liechtenstein-daily-return-and-more-than-45-non-return-days.md) |
| 7. End | Nothing is asked; the employee is reminded to bring their permit on the first working day. | Non-Swiss employees and everyone living abroad (the reminder is worded so that a Swiss citizen living abroad sees it does not apply) | [US-01.4](stories/US-01.4-remind-non-swiss-employees-and-employees-living-abroad-to.md) |

Never asked, always derived from the answers: Insurance start date ([US-03.2](stories/US-03.2-derive-the-pension-insurance-start-date-from-the-first.md), [US-03.3](stories/US-03.3-re-derive-the-insurance-start-date-when-the-first-working.md)), Civil status entered at the pension fund ([US-04.1](stories/US-04.1-ask-the-employee-s-civil-status-using-the-pension-fund-s.md)), Civil status group for source tax ([US-04.3](stories/US-04.3-answer-the-calculator-s-civil-status-question-from-the.md)), Residence for source tax ([US-08.1](stories/US-08.1-derive-the-calculator-s-residence-answers-from-the-home.md)), Church-tax suffix ([US-06.2](stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md)), Per-child result ([US-07.2](stories/US-07.2-one-block-per-child-age-status-and-household.md), [US-07.3](stories/US-07.3-minor-child-living-in-the-employee-s-household.md), [US-07.4](stories/US-07.4-minor-child-not-living-in-the-employee-s-household.md), [US-07.5](stories/US-07.5-adult-child-in-first-education.md), [US-07.6](stories/US-07.6-child-digit-of-the-tariff-code-and-go-live-check-of-the.md)), Child digit of the tariff code ([US-07.1](stories/US-07.1-ask-about-children-only-of-employees-who-need-a-source-tax.md), [US-07.6](stories/US-07.6-child-digit-of-the-tariff-code-and-go-live-check-of-the.md)), Base tariff letter ([US-06.4](stories/US-06.4-derive-the-base-source-tax-tariff-letter.md)), Cross-border (Grenzgänger) tariff applies ([US-08.2](stories/US-08.2-germany-daily-return-and-certificate-of-residence.md), [US-08.3](stories/US-08.3-germany-no-daily-return-reasonableness-and-more-than-60-non.md)), Final tariff letter ([US-06.5](stories/US-06.5-replace-the-base-letter-with-the-cross-border-letter-where.md)), Liechtenstein: in principle no source tax liability ([US-08.4](stories/US-08.4-liechtenstein-daily-return-and-more-than-45-non-return-days.md)), Source tax tariff code ([US-06.6](stories/US-06.6-compute-and-record-the-full-source-tax-tariff-code.md)), Discard answers that no longer apply ([US-01.5](stories/US-01.5-discard-answers-that-no-longer-apply-on-submission.md)), Read-only after submission ([US-01.6](stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md)).

On submission, answers that no longer apply are discarded and the questionnaire becomes read-only for the employee. The answers are recorded for HR. The insurance start date, civil status for the fund and for source tax, subject to source tax and the tariff code (or the Liechtenstein 'in principle no source tax liability' result, flagged for HR) are derived from the latest answers. Later changes are made by HR.

## Contents

| Section | Stories |
|---|---|
| [1. Questionnaire flow overview](#SEC-01-questionnaire-flow) | [US-01.1](stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md), [US-01.2](stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md), [US-01.3](stories/US-01.3-ask-each-piece-of-information-once-and-reuse-it-for-every.md), [US-01.4](stories/US-01.4-remind-non-swiss-employees-and-employees-living-abroad-to.md), [US-01.5](stories/US-01.5-discard-answers-that-no-longer-apply-on-submission.md), [US-01.6](stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md) |
| [2. Personal details and home address](#SEC-02-personal-details-address) | [US-02.1](stories/US-02.1-collect-the-employee-s-name-and-date-of-birth.md), [US-02.2](stories/US-02.2-collect-a-complete-postal-home-address.md), [US-02.3](stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md), [US-02.4](stories/US-02.4-ask-swiss-residents-for-their-canton.md) |
| [3. First working day and insurance start date](#SEC-03-employment-start) | [US-03.1](stories/US-03.1-employee-confirms-the-first-working-day.md), [US-03.2](stories/US-03.2-derive-the-pension-insurance-start-date-from-the-first.md), [US-03.3](stories/US-03.3-re-derive-the-insurance-start-date-when-the-first-working.md) |
| [4. Civil status and spouse data](#SEC-04-civil-status-spouse) | [US-04.1](stories/US-04.1-ask-the-employee-s-civil-status-using-the-pension-fund-s.md), [US-04.2](stories/US-04.2-ask-the-spouse-s-date-of-birth-when-the-employee-is-married.md), [US-04.3](stories/US-04.3-answer-the-calculator-s-civil-status-question-from-the.md) |
| [5. Who is subject to source tax](#SEC-05-source-tax-liability) | [US-05.1](stories/US-05.1-ask-nationality-and-c-permit-only-of-employees-living-in.md), [US-05.2](stories/US-05.2-ask-the-spouse-s-nationality-c-permit-and-residence-only.md), [US-05.3](stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md) |
| [6. Source tax tariff: denomination, spouse employment and tariff code](#SEC-06-source-tax-tariff-basics) | [US-06.2](stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md), [US-06.3](stories/US-06.3-ask-married-employees-and-registered-partners-subject-to.md), [US-06.4](stories/US-06.4-derive-the-base-source-tax-tariff-letter.md), [US-06.5](stories/US-06.5-replace-the-base-letter-with-the-cross-border-letter-where.md), [US-06.6](stories/US-06.6-compute-and-record-the-full-source-tax-tariff-code.md) |
| [7. Source tax tariff: children](#SEC-07-source-tax-children) | [US-07.1](stories/US-07.1-ask-about-children-only-of-employees-who-need-a-source-tax.md), [US-07.2](stories/US-07.2-one-block-per-child-age-status-and-household.md), [US-07.3](stories/US-07.3-minor-child-living-in-the-employee-s-household.md), [US-07.4](stories/US-07.4-minor-child-not-living-in-the-employee-s-household.md), [US-07.5](stories/US-07.5-adult-child-in-first-education.md), [US-07.6](stories/US-07.6-child-digit-of-the-tariff-code-and-go-live-check-of-the.md) |
| [8. Source tax: residence abroad and cross-border questions](#SEC-08-cross-border-residence) | [US-08.1](stories/US-08.1-derive-the-calculator-s-residence-answers-from-the-home.md), [US-08.2](stories/US-08.2-germany-daily-return-and-certificate-of-residence.md), [US-08.3](stories/US-08.3-germany-no-daily-return-reasonableness-and-more-than-60-non.md), [US-08.4](stories/US-08.4-liechtenstein-daily-return-and-more-than-45-non-return-days.md) |

<a id="SEC-01-questionnaire-flow"></a>

## 1. Questionnaire flow overview

Give the employee one English questionnaire with fixed steps, where each question appears only under its condition. At the end come the permit reminder and a submission that discards answers that no longer apply and makes the questionnaire read-only.

| Story | Priority | Status |
|---|---|---|
| [US-01.1 – Show the source tax step only to employees who are subject to source tax](stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md) | P1 | decision |
| [US-01.2 – Ask the steps in an order that avoids unneeded questions](stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md) | P1 | decision |
| [US-01.3 – Ask each piece of information once and reuse it for every receiving party](stories/US-01.3-ask-each-piece-of-information-once-and-reuse-it-for-every.md) | P1 | decision |
| [US-01.4 – Remind non-Swiss employees and employees living abroad to bring their permit](stories/US-01.4-remind-non-swiss-employees-and-employees-living-abroad-to.md) | P2 | decision |
| [US-01.5 – Discard answers that no longer apply on submission](stories/US-01.5-discard-answers-that-no-longer-apply-on-submission.md) | P1 | decision |
| [US-01.6 – Make the questionnaire read-only after submission and derive results from the latest answers](stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md) | P1 | decision |

### Business rules in this section

#### Questionnaire flow overview
The questionnaire is in English and asks each piece of information once. Steps in order: (1) Personal details - first name, last name, date of birth. (2) Home address - street, house number, postcode, town, country; canton only if living in Switzerland. (3) Start - first working day. (4) Civil status - civil status; spouse's/partner's date of birth if married, in a registered partnership or separated. (5) Source tax status - only for employees living in Switzerland: nationality; C permit if not Swiss; for non-Swiss without C permit who are married or in a registered partnership: spouse's nationality, spouse's C permit if not Swiss, spouse's country of residence if Swiss or C permit. (6) Source tax details - only if subject to source tax: confession; spouse works (married/registered partnership); children and the per-child questions (repeated per child); then cross-border questions for residents of Germany or Liechtenstein. (7) End - permit reminder for non-Swiss employees and everyone living abroad. On submission answers that no longer apply are discarded and the questionnaire becomes read-only for the employee; derived results are computed from the latest answers.

| # | Step | → Result | Sources |
|---|---|---|---|
| 1 | 1. Personal details | Everyone: first name, last name, date of birth. | F-pension_portal-db702a, F-pension_portal-c688e4, F-pension_portal-88b436 |
| 2 | 2. Home address | Everyone: street, house number, postcode, town, country. Canton only if the country is Switzerland. | F-hr_transcript-c0fe95, D-002 |
| 3 | 3. Start | Everyone: first working day (insurance start date is derived, not asked). | F-hr_transcript-872bd7, F-hr_transcript-1d5c07, G-08, D-033 |
| 4 | 4. Civil status | Everyone: civil status. Spouse's/partner's date of birth if Married, Registered partnership or Separated. | F-pension_portal-8664f4, D-003, D-004 |
| 5 | 5. Source tax status | Only employees living in Switzerland: nationality; C permit (non-Swiss); spouse nationality, spouse C permit, spouse country of residence (non-Swiss without C permit, married or registered partnership). Employees abroad skip this step. | F-hr_transcript-5af8d0, F-hr_transcript-54d011, D-005, D-008, D-038 |
| 6 | 6. Source tax details | Only if subject to source tax: confession; spouse works (married/registered partnership); has children and per-child questions; residence-dependent questions for Germany (daily return, certificate of residence, reasonable return, more than 60 non-return days) or Liechtenstein (daily return, more than 45 non-return days). | F-hr_transcript-b84498, F-zh_source_tax_calculator-b05b44, F-zh_source_tax_calculator-a33b65, F-zh_source_tax_calculator-0f1a72, D-001, D-006, D-007 |
| 7 | 7. End | Permit reminder for non-Swiss employees and all employees living abroad; submission. | D-010, D-038, D-036, D-037 |

_Status: decision · Sources: G-01, G-04, G-09, F-hr_transcript-b84498, F-zh_source_tax_calculator-d5a6fe, D-001, D-002, D-003, D-004, D-005, D-006, D-007, D-008, D-010, D-033, D-036, D-037, D-038_

#### Permit reminder
At the end of the questionnaire every non-Swiss employee and every employee living abroad (whatever their nationality, as it is not asked of them) is reminded to bring their permit on the first working day. HR words the reminder so that a Swiss citizen living abroad can see it does not apply to them. It collects no data.

| # | Country of residence | Swiss citizen | → Result | Sources |
|---|---|---|---|---|
| 1 | Switzerland | yes | No reminder | D-010 |
| 2 | Switzerland | no | Reminder | F-hr_transcript-c53552, D-010 |
| 3 | not Switzerland | - | Reminder | D-010, D-038 |

_Status: decision · Sources: F-hr_transcript-c53552, D-010, D-038_

#### Discard answers that no longer apply
If the employee changes an earlier answer so that a later question no longer applies, its answer may be kept while the employee goes back and forth, but is discarded on submission. No personal data that no party needs is kept.

_Status: decision · Sources: G-01, D-036_

#### Read-only after submission
After submission the questionnaire is read-only for the employee. Later changes (move, marriage, new child, certificate of residence handed in later, corrected nationality, moved first working day) are made by HR (later HR-side spec). Every derived result - insurance start date, civil status for the fund and for source tax, subject to source tax, tariff code - is always derived again from the latest answers; for the first working day only the latest date counts and no history is kept.

_Status: decision · Sources: F-hr_transcript-e18e66, D-033, D-034, D-037_

<a id="SEC-02-personal-details-address"></a>

## 2. Personal details and home address

Collect the employee's name, date of birth and complete home address once. HR uses them to post documents and the pension fund to register the employee. The country of the address decides which later questions apply, and the canton is asked only of employees living in Switzerland.

> ⚠ Open questions affecting this section: [OQ-canton-abroad](open-questions.md#oq-canton-abroad)
| Story | Priority | Status |
|---|---|---|
| [US-02.1 – Collect the employee's name and date of birth](stories/US-02.1-collect-the-employee-s-name-and-date-of-birth.md) | P1 | inferred |
| [US-02.2 – Collect a complete postal home address](stories/US-02.2-collect-a-complete-postal-home-address.md) | P1 | confirmed |
| [US-02.3 – Use the home address country as the country of residence](stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md) | P1 | confirmed |
| [US-02.4 – Ask Swiss residents for their canton](stories/US-02.4-ask-swiss-residents-for-their-canton.md) | P1 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### First name
| | |
|---|---|
| **What?** | The employee's first name, as it is to appear in the pension fund registration and on documents HR posts to the employee. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'First name' of the pension fund registration.<br>HR: Identify the employee and address posted documents. |
| **Status · sources** | inferred · F-pension_portal-db702a, F-pension_portal-44a27b, F-hr_transcript-3edf89, G-01 |
| **Notes** | HR's own need for the name is inferred (Anna answered 'Yes' to 'Name, address' but only elaborated on the address); the pension fund need is explicit. |

#### Last name
| | |
|---|---|
| **What?** | The employee's last name. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'Last name' of the pension fund registration.<br>HR: Identify the employee and address posted documents. |
| **Status · sources** | inferred · F-pension_portal-c688e4, F-pension_portal-44a27b, F-hr_transcript-3edf89 |
| **Notes** | HR's need is inferred, the pension fund's need is explicit. |

#### Date of birth
| | |
|---|---|
| **What?** | The employee's date of birth. – Form: Date in the format DD.MM.YYYY |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'Date of birth' of the pension fund registration. |
| **Status · sources** | confirmed · F-pension_portal-88b436, F-pension_portal-967bc9, F-pension_portal-44a27b |

#### Street
| | |
|---|---|
| **What?** | Street of the employee's home address (part of a complete postal address, as written on an envelope). – Form: Part of a complete postal address: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee; the address must be complete. |
| **Status · sources** | confirmed · F-hr_transcript-3beee8, F-hr_transcript-c0fe95, F-hr_transcript-66fe15 |

#### House number
| | |
|---|---|
| **What?** | House number of the employee's home address. – Form: Part of a complete postal address: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee; the address must be complete. |
| **Status · sources** | confirmed · F-hr_transcript-3beee8, F-hr_transcript-c0fe95, F-hr_transcript-66fe15 |
| **Notes** | HR lists the number as part of the complete address. Whether every address has a house number is not stated by any source. |

#### Postcode
| | |
|---|---|
| **What?** | Postcode of the employee's home address. – Form: Part of a complete postal address: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee; the address must be complete. |
| **Status · sources** | confirmed · F-hr_transcript-3beee8, F-hr_transcript-c0fe95, F-hr_transcript-66fe15 |

#### Town
| | |
|---|---|
| **What?** | Town of the employee's home address. – Form: Part of a complete postal address: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee; the address must be complete. |
| **Status · sources** | confirmed · F-hr_transcript-3beee8, F-hr_transcript-c0fe95, F-hr_transcript-66fe15 |

#### Country of residence (country of the home address)
| | |
|---|---|
| **What?** | Country of the employee's home address. This is the employee's country of residence: it decides whether the employee lives in Switzerland or abroad (source tax liability, which questions follow, cross-border questions for Germany and Liechtenstein) and whether the canton is asked. Countries are named in English (e.g. Switzerland, Germany, Liechtenstein). – Form: Part of a complete postal address: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee; the address must be complete.<br>source tax office: Employees living abroad are always subject to source tax; the country of residence (Switzerland, Germany, Liechtenstein, other country) drives the calculator's residence questions and the cross-border tariff.<br>pension fund: Decides whether the canton is asked (only for employees living in Switzerland). |
| **Status · sources** | confirmed · F-hr_transcript-c0fe95, F-hr_transcript-ab3cba, F-hr_transcript-3f2c2a, F-hr_transcript-5af8d0, F-zh_source_tax_calculator-aedb40, F-zh_source_tax_calculator-4c65ae, F-zh_source_tax_calculator-d62dd4, G-09, G-10, D-001, D-002 |

#### Canton
| | |
|---|---|
| **What?** | The Swiss canton for the pension fund's 'Canton' field. Asked only of employees living in Switzerland (provisional, D-002). Whether the fund means the canton of residence or of work, and what to enter for employees living abroad, is open (OQ-canton-abroad). |
| **Allowed values** | Aargau · Appenzell Ausserrhoden · Appenzell Innerrhoden · Basel-Landschaft · Basel-Stadt · Bern · Fribourg · Geneva · Glarus · Graubünden · Jura · Lucerne · Neuchâtel · Nidwalden · Obwalden · Schaffhausen · Schwyz · Solothurn · St. Gallen · Thurgau · Ticino · Uri · Valais · Vaud · Zug · Zurich |
| **When do we ask?** | Only if the employee lives in Switzerland |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (country of the home address) |
| **Who needs it?** | pension fund: Required field 'Canton' of the pension fund registration. |
| **Status · sources** | decision · F-pension_portal-6c621f, F-pension_portal-3432a9, F-pension_portal-44a27b, F-pension_portal-b359c3, D-002 |

<a id="SEC-03-employment-start"></a>

## 3. First working day and insurance start date

Have the employee confirm their first working day, and derive the pension fund insurance start date from it instead of asking for it. The derived date always follows the latest first working day.

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
| **What?** | The employee's first working day at Muster AG, entered by the employee, who confirms it because it often moves (e.g. an earlier exit negotiated with the old employer). The insurance start date is derived from it. After submission only HR can change it; the latest date always counts and no history of earlier dates is kept. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Basis for the derived insurance start date (HR's 'number one' item).<br>HR: Knows when the employee starts; reminder to bring the permit refers to it. |
| **Status · sources** | confirmed · F-hr_transcript-872bd7, F-hr_transcript-e3721e, F-hr_transcript-1d5c07, F-hr_transcript-e18e66, G-08, D-033, D-037 |

### Business rules in this section

#### Insurance start date
The pension fund insurance start date is derived from the first working day: if the first working day is the 1st of a month, insurance starts that day; otherwise on the 1st of the following month (e.g. 15.03 gives 01.04). It is always derived again from the latest first working day, so a moved start date updates it.

| # | First working day | → Result | Sources |
|---|---|---|---|
| 1 | is the 1st of a month | Insurance start date = first working day | F-hr_transcript-1d5c07 |
| 2 | is not the 1st of a month | Insurance start date = 1st of the following month | F-hr_transcript-1d5c07, F-pension_portal-dd8126 |

_Status: confirmed · Sources: F-hr_transcript-1d5c07, F-hr_transcript-e18e66, F-pension_portal-509cbe, F-pension_portal-dd8126, G-08, D-033, D-037_

<a id="SEC-04-civil-status-spouse"></a>

## 4. Civil status and spouse data

Ask the civil status once and map it both to the pension fund's list and to the calculator's civil status group. The spouse's or partner's date of birth is asked only where the fund needs it.

> ⚠ Open questions affecting this section: [OQ-civil-status-partnership](open-questions.md#oq-civil-status-partnership), [OQ-spouse-dob-other-status](open-questions.md#oq-spouse-dob-other-status)
| Story | Priority | Status |
|---|---|---|
| [US-04.1 – Ask the employee's civil status using the pension fund's list](stories/US-04.1-ask-the-employee-s-civil-status-using-the-pension-fund-s.md) | P1 | decision |
| [US-04.2 – Ask the spouse's date of birth when the employee is married](stories/US-04.2-ask-the-spouse-s-date-of-birth-when-the-employee-is-married.md) | P1 | decision |
| [US-04.3 – Answer the calculator's civil status question from the employee's civil status](stories/US-04.3-answer-the-calculator-s-civil-status-question-from-the.md) | P1 | confirmed |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Civil status
| | |
|---|---|
| **What?** | The employee's civil status. Asked of everyone, because the pension fund requires it. Feeds the civil status entered at the fund (pension_fund_civil_status) and, for employees subject to source tax, the calculator's civil status group (calculator_civil_status). |
| **Allowed values** | Single · Married · Divorced · Widowed · Registered partnership · Separated |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'Civil status' of the registration; decides whether the spouse's date of birth is needed.<br>source tax office: Civil status group of the calculator (married/registered partnership vs. single, divorced, separated, widowed); decides the spouse exemption and the tariff letter. |
| **Status · sources** | decision · F-hr_transcript-ce8ca4, F-hr_transcript-bd8c8e, F-hr_transcript-3907fe, F-hr_transcript-f197d6, F-pension_portal-8664f4, F-pension_portal-3d1ae4, F-zh_source_tax_calculator-9007c3, F-zh_source_tax_calculator-051bb9, G-10, D-003 |
| **Notes** | The fund's list has only Single, Married, Divorced, Widowed; 'Registered partnership' and 'Separated' are added by D-003 because the calculator distinguishes them and the case occurs (Daniel). Fund mapping is provisional (OQ-civil-status-partnership). |

#### Spouse's / registered partner's date of birth
| | |
|---|---|
| **What?** | Date of birth of the employee's spouse or registered partner (for separated employees: of the spouse they are separated from). – Form: Date in the format DD.MM.YYYY |
| **When do we ask?** | Only if the employee is married, in a registered partnership or separated |
| **When is it required?** | Whenever asked |
| **Depends on** | Civil status |
| **Who needs it?** | pension fund: 'Spouse's date of birth' is required by the fund when the civil status entered there is Married (which includes registered partnership and separated, D-003). |
| **Status · sources** | decision · F-hr_transcript-2334d8, F-pension_portal-a0065b, F-pension_portal-ef28c3, F-pension_portal-39bab1, F-pension_portal-c5ee15, F-pension_portal-6d3630, D-003, D-004 |
| **Notes** | Not asked of divorced or widowed employees (OQ-spouse-dob-other-status). |

### Business rules in this section

#### Civil status entered at the pension fund
The fund only offers Single, Married, Divorced, Widowed. Provisionally, Registered partnership and Separated are entered as Married (with the partner's/spouse's date of birth); the other values are entered as given.

| # | Civil status | → Result | Sources |
|---|---|---|---|
| 1 | Single | Single | F-pension_portal-3d1ae4 |
| 2 | Married | Married | F-pension_portal-3d1ae4 |
| 3 | Divorced | Divorced | F-pension_portal-3d1ae4 |
| 4 | Widowed | Widowed | F-pension_portal-3d1ae4 |
| 5 | Registered partnership | Married (provisional) | D-003 |
| 6 | Separated | Married (provisional) | D-003 |

_Status: decision · Sources: F-pension_portal-3d1ae4, F-hr_transcript-f197d6, D-003, D-037_

#### Civil status group for source tax
For source tax, Married and Registered partnership count as 'married or registered partnership'; Single, Divorced, Widowed and Separated count as 'single, divorced, separated or widowed'.

| # | Civil status | → Result | Sources |
|---|---|---|---|
| 1 | Married or Registered partnership | Married or registered partnership | F-zh_source_tax_calculator-051bb9, D-003 |
| 2 | Single, Divorced, Widowed or Separated | Single, divorced, separated or widowed | F-zh_source_tax_calculator-051bb9, D-003 |

_Status: confirmed · Sources: F-zh_source_tax_calculator-051bb9, F-zh_source_tax_calculator-9007c3, D-003_

<a id="SEC-05-source-tax-liability"></a>

## 5. Who is subject to source tax

Decide from as few questions as possible whether the employee is subject to source tax: country of residence, Swiss citizenship, C permit (yes/no), and the spouse's citizenship, C permit and residence. Only employees subject to source tax are asked the tariff questions.

> ⚠ Open questions affecting this section: [OQ-source-tax-rule-confirmation](open-questions.md#oq-source-tax-rule-confirmation)
| Story | Priority | Status |
|---|---|---|
| [US-05.1 – Ask nationality and C permit only of employees living in Switzerland](stories/US-05.1-ask-nationality-and-c-permit-only-of-employees-living-in.md) | P1 | decision |
| [US-05.2 – Ask the spouse's nationality, C permit and residence only when they can exempt the employee](stories/US-05.2-ask-the-spouse-s-nationality-c-permit-and-residence-only.md) | P1 | inferred |
| [US-05.3 – Decide whether the employee is subject to source tax](stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md) | P1 | confirmed |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Nationality
| | |
|---|---|
| **What?** | The employee's nationality, named in English. Anyone holding Swiss citizenship answers 'Switzerland', even if they hold another nationality as well. Only asked of employees living in Switzerland: for employees living abroad nationality does not matter for source tax. |
| **When do we ask?** | Only if the employee lives in Switzerland |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (country of the home address) |
| **Who needs it?** | source tax office: Decide whether an employee living in Switzerland is subject to source tax (Swiss citizens are not).<br>HR: Decide whether the permit reminder is shown. |
| **Status · sources** | decision · F-hr_transcript-35fae3, F-hr_transcript-5af8d0, F-hr_transcript-3f2c2a, G-01, G-10, D-008, D-038 |

#### Holds a C permit (permanent residence)
| | |
|---|---|
| **What?** | Whether a non-Swiss employee living in Switzerland holds a C permit (permanent residence). The permit type itself is not asked; only 'C permit or not' drives a rule. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Switzerland and is not a Swiss citizen |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (country of the home address), Nationality |
| **Who needs it?** | source tax office: C-permit holders are treated like Swiss citizens and are not subject to source tax. |
| **Status · sources** | decision · F-hr_transcript-845204, F-hr_transcript-c9d9b9, F-hr_transcript-5af8d0, G-01, D-005 |
| **Notes** | Replaces the listed concept 'permit_type' (D-005). |

#### Spouse's / registered partner's nationality
| | |
|---|---|
| **What?** | Nationality of the spouse or registered partner, named in English ('Switzerland' for anyone holding Swiss citizenship). Only asked when it can change the source tax outcome: the employee lives in Switzerland, is not Swiss, has no C permit and is married or in a registered partnership. |
| **When do we ask?** | Only if the employee lives in Switzerland, is not Swiss, has no C permit and is married or in a registered partnership |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (country of the home address), Civil status, Holds a C permit (permanent residence) |
| **Who needs it?** | source tax office: Spouse exemption: an employee married to a Swiss citizen living in Switzerland is not subject to source tax. |
| **Status · sources** | inferred · F-hr_transcript-f3ce84, F-hr_transcript-b90bd9, F-hr_transcript-5af8d0, F-hr_transcript-54d011, F-hr_transcript-a45422, G-01, D-003, D-008 |
| **Notes** | Restriction to employees who would otherwise be subject is inferred (F-hr_transcript-54d011) and follows data minimisation. Registered partners included per D-003. |

#### Spouse / registered partner holds a C permit
| | |
|---|---|
| **What?** | Whether a non-Swiss spouse or registered partner holds a C permit (permanent residence). The spouse's permit type itself is not asked. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the spouse nationality is asked and the spouse is not Swiss |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (country of the home address), Civil status, Holds a C permit (permanent residence), Spouse's / registered partner's nationality |
| **Who needs it?** | source tax office: Spouse exemption: an employee married to a C-permit holder living in Switzerland is not subject to source tax. |
| **Status · sources** | decision · F-hr_transcript-76eacc, F-hr_transcript-b90bd9, F-hr_transcript-5af8d0, F-hr_transcript-54d011, D-003, D-005 |
| **Notes** | Replaces the listed concept 'spouse_permit_type' (D-005). |

#### Spouse's / registered partner's country of residence
| | |
|---|---|
| **What?** | The country where the spouse or registered partner lives (English name). Only needed to check whether a Swiss or C-permit spouse lives in Switzerland ('lives here'). |
| **When do we ask?** | Only if the spouse is Swiss or holds a C permit (and the spouse questions are asked) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (country of the home address), Civil status, Holds a C permit (permanent residence), Spouse / registered partner holds a C permit, Spouse's / registered partner's nationality |
| **Who needs it?** | source tax office: The spouse exemption only applies if the Swiss or C-permit spouse lives in Switzerland. |
| **Status · sources** | inferred · F-hr_transcript-e5337d, F-hr_transcript-b90bd9, F-hr_transcript-5af8d0, F-hr_transcript-54d011, G-01, G-10 |
| **Notes** | 'Here' is read as Switzerland (F-hr_transcript-5af8d0); see OQ-source-tax-rule-confirmation. |

### Business rules in this section

#### Subject to source tax
An employee living abroad is subject to source tax regardless of nationality. An employee living in Switzerland is subject only if not a Swiss citizen (anyone with Swiss citizenship counts as Swiss), without a C permit, and not married to / in a registered partnership with a Swiss citizen or C-permit holder who lives in Switzerland. Only employees subject to source tax are asked the source tax questions. Liechtenstein residents count as subject (they are asked the questions); their result may still be 'in principle no source tax liability'.

| # | Country of residence | Swiss citizen | C permit | Civil status | Spouse Swiss or C permit | Spouse lives in Switzerland | → Result | Sources |
|---|---|---|---|---|---|---|---|---|
| 1 | not Switzerland | - | - | any | - | - | Subject to source tax | F-hr_transcript-3f2c2a, F-hr_transcript-5af8d0, D-007 |
| 2 | Switzerland | yes | - | any | - | - | Not subject | F-hr_transcript-b0527c, F-hr_transcript-5af8d0, D-008 |
| 3 | Switzerland | no | yes | any | - | - | Not subject | F-hr_transcript-845204, F-hr_transcript-5af8d0 |
| 4 | Switzerland | no | no | Single, Divorced, Widowed or Separated | - | - | Subject to source tax | F-hr_transcript-5af8d0, D-003 |
| 5 | Switzerland | no | no | Married or Registered partnership | no | - | Subject to source tax | F-hr_transcript-5af8d0, D-003 |
| 6 | Switzerland | no | no | Married or Registered partnership | yes | no | Subject to source tax | F-hr_transcript-b90bd9, F-hr_transcript-5af8d0 |
| 7 | Switzerland | no | no | Married or Registered partnership | yes | yes | Not subject | F-hr_transcript-b90bd9, F-hr_transcript-5af8d0, D-003 |

_Status: confirmed · Sources: F-hr_transcript-5af8d0, F-hr_transcript-3f2c2a, F-hr_transcript-b90bd9, F-hr_transcript-845204, F-hr_transcript-b84498, D-003, D-005, D-007, D-008, D-037_

<a id="SEC-06-source-tax-tariff-basics"></a>

## 6. Source tax tariff: denomination, spouse employment and tariff code

Ask employees subject to source tax for their denomination and, if married or in a registered partnership, whether the spouse or partner works. Combine these with the child digit and the cross-border result into the computed Zurich tariff code that Lonio records for HR.

| Story | Priority | Status |
|---|---|---|
| [US-06.2 – Ask the religious denomination only where source tax needs it and derive the church-tax suffix](stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md) | P1 | inferred |
| [US-06.3 – Ask married employees and registered partners subject to source tax whether their spouse or partner works](stories/US-06.3-ask-married-employees-and-registered-partners-subject-to.md) | P1 | confirmed |
| [US-06.4 – Derive the base source tax tariff letter](stories/US-06.4-derive-the-base-source-tax-tariff-letter.md) | P1 | inferred |
| [US-06.5 – Replace the base letter with the cross-border letter where the cross-border tariff applies](stories/US-06.5-replace-the-base-letter-with-the-cross-border-letter-where.md) | P1 | confirmed |
| [US-06.6 – Compute and record the full source tax tariff code](stories/US-06.6-compute-and-record-the-full-source-tax-tariff-code.md) | P1 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Religious denomination (confession)
| | |
|---|---|
| **What?** | Whether the employee belongs to the Roman Catholic, Christian Catholic or Evangelical Reformed church, or to none or another denomination. Sets the church-tax suffix of the tariff code. |
| **Allowed values** | Roman Catholic, Christian Catholic or Evangelical Reformed · None or other |
| **When do we ask?** | Only if the employee is subject to source tax |
| **When is it required?** | Whenever asked |
| **Depends on** | Subject to source tax |
| **Who needs it?** | source tax office: Church-tax suffix (Y/N) of the tariff code. |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-208104, F-zh_source_tax_calculator-b7fea8, F-zh_source_tax_calculator-b05b44, F-zh_source_tax_calculator-2eab9a, F-hr_transcript-b84498, G-09, D-001, D-006 |
| **Notes** | Values are English renderings of the calculator's 'röm.-kath., christ.-kath., evang.-ref.' and 'Keine oder andere'. |

#### Spouse / registered partner works or receives replacement income
| | |
|---|---|
| **What?** | Whether the spouse or registered partner is gainfully employed or receives replacement income. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee is subject to source tax and is married or in a registered partnership |
| **When is it required?** | Whenever asked |
| **Depends on** | Civil status, Subject to source tax |
| **Who needs it?** | source tax office: Tariff letter C (spouse works) or B (spouse does not). |
| **Status · sources** | confirmed · F-hr_transcript-6a0a40, F-zh_source_tax_calculator-7b637b, F-zh_source_tax_calculator-e740d1, F-zh_source_tax_calculator-0137bf, F-zh_source_tax_calculator-97139a, D-001, D-003 |

### Business rules in this section

#### Church-tax suffix
The tariff code ends in Y for Roman Catholic, Christian Catholic or Evangelical Reformed, and N for none or other.

| # | Confession | → Result | Sources |
|---|---|---|---|
| 1 | Roman Catholic, Christian Catholic or Evangelical Reformed | Y | F-zh_source_tax_calculator-2eab9a |
| 2 | None or other | N | F-zh_source_tax_calculator-2eab9a |

_Status: inferred · Sources: F-zh_source_tax_calculator-2eab9a, F-zh_source_tax_calculator-b7fea8, D-001_

#### Base tariff letter
Married or registered partnership: C if the spouse/partner works or receives replacement income, otherwise B. Single, divorced, separated or widowed: H if any child counts with H, otherwise A. Tariffs G and Q (replacement income) and special tariffs such as D do not occur in onboarding.

| # | Civil status group | Spouse works | Any child counts with H | → Result | Sources |
|---|---|---|---|---|---|
| 1 | Married or registered partnership | yes | - | C | F-zh_source_tax_calculator-97139a |
| 2 | Married or registered partnership | no | - | B | F-zh_source_tax_calculator-97139a |
| 3 | Single, divorced, separated or widowed | - | yes | H | F-zh_source_tax_calculator-300c72 |
| 4 | Single, divorced, separated or widowed | - | no | A | F-zh_source_tax_calculator-037b1c |

_Status: confirmed · Sources: F-zh_source_tax_calculator-97139a, F-zh_source_tax_calculator-037b1c, F-zh_source_tax_calculator-300c72, D-001, D-006, D-009_

#### Final tariff letter
If the cross-border tariff applies, the base letter is replaced: A by L, B by M, C by N, H by P. Otherwise the base letter is used.

| # | Cross-border tariff | Base tariff letter | → Result | Sources |
|---|---|---|---|---|
| 1 | no | any | Base tariff letter | F-zh_source_tax_calculator-993db3 |
| 2 | yes | A | L | F-zh_source_tax_calculator-993db3 |
| 3 | yes | B | M | F-zh_source_tax_calculator-993db3 |
| 4 | yes | C | N | F-zh_source_tax_calculator-993db3 |
| 5 | yes | H | P | F-zh_source_tax_calculator-993db3 |

_Status: confirmed · Sources: F-zh_source_tax_calculator-993db3, F-zh_source_tax_calculator-66732c, D-001, D-009_

#### Source tax tariff code
For every employee subject to source tax Lonio computes the Zurich tariff code from the answers: final tariff letter + child digit + church-tax suffix (e.g. A0N, C1Y, L0Y, N1Y). For Liechtenstein residents with daily return or at most 45 non-return days the result is 'in principle no source tax liability, subject to the double taxation agreement' instead, flagged for HR. Employees not subject to source tax get no tariff code. The result is always derived again from the latest answers and is recorded for HR.

| # | Subject to source tax | Liechtenstein no-liability case | → Result | Sources |
|---|---|---|---|---|
| 1 | no | - | No tariff code | F-hr_transcript-5af8d0 |
| 2 | yes | yes | 'In principle no source tax liability, subject to the double taxation agreement', flagged for HR | F-zh_source_tax_calculator-fb87f1, D-007 |
| 3 | yes | no | Tariff letter + child digit + church-tax suffix | F-zh_source_tax_calculator-4c53e3, F-zh_source_tax_calculator-2eab9a, F-zh_source_tax_calculator-993db3, D-001 |

_Status: decision · Sources: F-hr_transcript-34494f, F-hr_transcript-3cd6fa, F-zh_source_tax_calculator-86d588, F-zh_source_tax_calculator-4c53e3, D-001, D-007, D-009, D-034, D-037_

<a id="SEC-07-source-tax-children"></a>

## 7. Source tax tariff: children

Ask employees subject to source tax whether they have children, then ask the calculator's questions once per child. Each child's answers decide whether that child counts toward the child digit, and whether it makes the tariff letter H for single employees. Before go-live, a domain expert checks the paths that were not observed in the calculator.

> ⚠ Open questions affecting this section: [OQ-calculator-coverage](open-questions.md#oq-calculator-coverage)
| Story | Priority | Status |
|---|---|---|
| [US-07.1 – Ask about children only of employees who need a source tax tariff](stories/US-07.1-ask-about-children-only-of-employees-who-need-a-source-tax.md) | P1 | confirmed |
| [US-07.2 – One block per child: age status and household](stories/US-07.2-one-block-per-child-age-status-and-household.md) | P1 | confirmed |
| [US-07.3 – Minor child living in the employee's household](stories/US-07.3-minor-child-living-in-the-employee-s-household.md) | P1 | inferred |
| [US-07.4 – Minor child not living in the employee's household](stories/US-07.4-minor-child-not-living-in-the-employee-s-household.md) | P1 | inferred |
| [US-07.5 – Adult child in first education](stories/US-07.5-adult-child-in-first-education.md) | P1 | inferred |
| [US-07.6 – Child digit of the tariff code and go-live check of the child paths](stories/US-07.6-child-digit-of-the-tariff-code-and-go-live-check-of-the.md) | P1 | inferred |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Has children
| | |
|---|---|
| **What?** | Whether the employee has biological or adopted children. For married employees and registered partners the question covers children of the employee or of the spouse / partner. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee is subject to source tax |
| **When is it required?** | Whenever asked |
| **Depends on** | Subject to source tax |
| **Who needs it?** | source tax office: Opens the per-child questions that determine the child digit and possibly tariff H. |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-103b19, F-zh_source_tax_calculator-a166c7, F-zh_source_tax_calculator-a33b65, F-zh_source_tax_calculator-ab8a06, F-zh_source_tax_calculator-b62b85, F-zh_source_tax_calculator-75cd87, D-001 |

#### Child: minor or adult in first education
| | |
|---|---|
| **What?** | Per child (the child questions repeat for each child): whether the child is a minor, an adult in first education, or neither. 'Neither' ends the questions for that child; the child does not count. – Form: Asked once per child |
| **Allowed values** | Minor · Adult in first education · Neither |
| **When do we ask?** | For each child, if the employee is subject to source tax and has children |
| **When is it required?** | Whenever asked |
| **Depends on** | Has children, Subject to source tax |
| **Who needs it?** | source tax office: Decides whether and how the child counts for the tariff code. |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-640429, F-zh_source_tax_calculator-09b06d, F-zh_source_tax_calculator-6bed1f, F-zh_source_tax_calculator-fd9a15, F-zh_source_tax_calculator-abe889, D-001 |

#### Child lives in the same household
| | |
|---|---|
| **What?** | Per child: whether the child lives in the employee's household. – Form: Asked once per child |
| **Allowed values** | yes · no |
| **When do we ask?** | For each child who is a minor or an adult in first education |
| **When is it required?** | Whenever asked |
| **Depends on** | Child: minor or adult in first education, Subject to source tax |
| **Who needs it?** | source tax office: Child counting for the tariff code. |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-5725a8, F-zh_source_tax_calculator-3a75cc, F-zh_source_tax_calculator-7c667f, D-001 |

#### Child: parental custody (shared or sole)
| | |
|---|---|
| **What?** | Per child: whether the employee has shared or sole parental custody of a minor child living in the household. – Form: Asked once per child |
| **Allowed values** | Shared custody · Sole custody |
| **When do we ask?** | For each minor child living in the same household |
| **When is it required?** | Whenever asked |
| **Depends on** | Child: minor or adult in first education, Child lives in the same household, Subject to source tax |
| **Who needs it?** | source tax office: Child counting; sole custody counts the child (with H for single employees). |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-4b7063, F-zh_source_tax_calculator-c09dc1, F-zh_source_tax_calculator-83de1d, D-001 |

#### Common household with the child's other parent
| | |
|---|---|
| **What?** | Per child: whether the employee lives in a common household with the child's other parent. – Form: Asked once per child |
| **Allowed values** | yes · no |
| **When do we ask?** | For each minor child in the household with shared custody, and for each adult child in first education in the household |
| **When is it required?** | Whenever asked |
| **Depends on** | Child: minor or adult in first education, Child: parental custody (shared or sole), Child lives in the same household, Subject to source tax |
| **Who needs it?** | source tax office: Child counting for the tariff code. |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-d79949, F-zh_source_tax_calculator-e72e42, F-zh_source_tax_calculator-6dcf5c, D-001 |

#### Child not in household: shared custody
| | |
|---|---|
| **What?** | Per child, for married employees / registered partners: whether custody of a minor child not living in the household is shared. – Form: Asked once per child |
| **Allowed values** | yes · no |
| **When do we ask?** | For each minor child not in the household, if the employee is married or in a registered partnership |
| **When is it required?** | Whenever asked |
| **Depends on** | Civil status group for source tax, Child: minor or adult in first education, Child lives in the same household, Subject to source tax |
| **Who needs it?** | source tax office: Child counting for the tariff code. |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-fe0305, F-zh_source_tax_calculator-d2e516, F-zh_source_tax_calculator-7dcce6, D-001, D-003 |

#### Child not in household: parental care
| | |
|---|---|
| **What?** | Per child, for single, divorced, separated or widowed employees: whether they have parental care (custody) of a minor child not living in the household. – Form: Asked once per child |
| **Allowed values** | yes · no |
| **When do we ask?** | For each minor child not in the household, if the employee is single, divorced, separated or widowed |
| **When is it required?** | Whenever asked |
| **Depends on** | Civil status group for source tax, Child: minor or adult in first education, Child lives in the same household, Subject to source tax |
| **Who needs it?** | source tax office: Child counting for the tariff code. |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-956f07, F-zh_source_tax_calculator-32fec9, F-zh_source_tax_calculator-fb4a56, D-001, D-003 |

#### Child: alternating custody
| | |
|---|---|
| **What?** | Per child: whether there is alternating custody of a minor child. – Form: Asked once per child |
| **Allowed values** | yes · no |
| **When do we ask?** | For a minor child: in the household with shared custody and no common household with the other parent; or not in the household with shared custody (married) or parental care (not married) |
| **When is it required?** | Whenever asked |
| **Depends on** | Child: minor or adult in first education, Common household with the child's other parent, Child: parental custody (shared or sole), Child not in household: parental care, Child lives in the same household, Child not in household: shared custody, Subject to source tax |
| **Who needs it?** | source tax office: Child counting for the tariff code. |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-da19df, F-zh_source_tax_calculator-ebd7b3, F-zh_source_tax_calculator-64ac33, D-001 |

#### Child: who contributes most to maintenance
| | |
|---|---|
| **What?** | Per child: who makes the larger financial contribution to the child's maintenance - the employee or the other parent. – Form: Asked once per child |
| **Allowed values** | Employee · Other parent |
| **When do we ask?** | For a child with alternating custody; or, for single, divorced, separated or widowed employees, a child in the household while living in a common household with the other parent |
| **When is it required?** | Whenever asked |
| **Depends on** | Civil status group for source tax, Child: alternating custody, Common household with the child's other parent, Child lives in the same household, Subject to source tax |
| **Who needs it?** | source tax office: Child counting; main contributor counts the child (with H for single employees). |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-cdd0b6, F-zh_source_tax_calculator-939b3b, F-zh_source_tax_calculator-ad867a, D-001 |
| **Notes** | Values are English renderings of 'Quellensteuerpflichtige Person' and 'Anderer Elternteil'. |

#### Adult child: employee pays more than 50% of maintenance
| | |
|---|---|
| **What?** | Per adult child in first education: whether the employee mainly (more than 50%) pays for the child's maintenance. – Form: Asked once per child |
| **Allowed values** | yes · no |
| **When do we ask?** | For an adult child in first education who does not live in the household, or lives in it without a common household with the other parent |
| **When is it required?** | Whenever asked |
| **Depends on** | Child: minor or adult in first education, Common household with the child's other parent, Child lives in the same household, Subject to source tax |
| **Who needs it?** | source tax office: Child counting for the tariff code. |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-b008fe, F-zh_source_tax_calculator-cb54d9, F-zh_source_tax_calculator-cd1015, D-001 |

### Business rules in this section

#### Per-child result
Each child is evaluated on its own: it counts, counts with H (single group only), or does not count. Rows marked as inferred were not observed in the calculator and must be checked before go-live (OQ-calculator-coverage).

| # | Civil status group | Age status | Same household | Custody | Common household with other parent | Shared custody (not in household) | Parental care (not in household) | Alternating custody | Main contributor | More than 50% maintenance | → Result | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | any | Neither | - | - | - | - | - | - | - | - | does not count | F-zh_source_tax_calculator-abe889 |
| 2 | Married | Minor | yes | Sole custody | - | - | - | - | - | - | counts | F-zh_source_tax_calculator-d75286 |
| 3 | Single | Minor | yes | Sole custody | - | - | - | - | - | - | counts with H | F-zh_source_tax_calculator-d75286, F-zh_source_tax_calculator-300c72 |
| 4 | Married | Minor | yes | Shared custody | yes | - | - | - | - | - | counts | F-zh_source_tax_calculator-5d8fb0 |
| 5 | Single | Minor | yes | Shared custody | yes | - | - | - | Employee | - | counts with H | F-zh_source_tax_calculator-300c72 |
| 6 | Single | Minor | yes | Shared custody | yes | - | - | - | Other parent | - | does not count | F-zh_source_tax_calculator-5686d7 |
| 7 | Married | Minor | yes | Shared custody | no | - | - | no | - | - | does not count | F-zh_source_tax_calculator-a4d358 |
| 8 | Single | Minor | yes | Shared custody | no | - | - | no | - | - | counts with H | F-zh_source_tax_calculator-dc0ae9 |
| 9 | Married | Minor | yes | Shared custody | no | - | - | yes | Employee | - | counts (inferred) | F-zh_source_tax_calculator-dc6ace, D-009 |
| 10 | Married | Minor | yes | Shared custody | no | - | - | yes | Other parent | - | does not count | F-zh_source_tax_calculator-a4d358 |
| 11 | Single | Minor | yes | Shared custody | no | - | - | yes | Employee | - | counts with H | F-zh_source_tax_calculator-300c72 |
| 12 | Single | Minor | yes | Shared custody | no | - | - | yes | Other parent | - | does not count (inferred) | F-zh_source_tax_calculator-a4d358, D-009 |
| 13 | Married | Minor | no | - | - | no | - | - | - | - | does not count | F-zh_source_tax_calculator-dc6ace |
| 14 | Married | Minor | no | - | - | yes | - | no | - | - | does not count (inferred) | F-zh_source_tax_calculator-a4d358, D-009 |
| 15 | Married | Minor | no | - | - | yes | - | yes | Employee | - | counts | F-zh_source_tax_calculator-dc6ace |
| 16 | Married | Minor | no | - | - | yes | - | yes | Other parent | - | does not count (inferred) | F-zh_source_tax_calculator-a4d358, D-009 |
| 17 | Single | Minor | no | - | - | - | no | - | - | - | does not count | F-zh_source_tax_calculator-dc6ace |
| 18 | Single | Minor | no | - | - | - | yes | no | - | - | does not count (inferred) | D-009 |
| 19 | Single | Minor | no | - | - | - | yes | yes | Employee | - | counts with H | F-zh_source_tax_calculator-dc6ace |
| 20 | Single | Minor | no | - | - | - | yes | yes | Other parent | - | does not count (inferred) | D-009 |
| 21 | Married | Adult in first education | yes | - | yes | - | - | - | - | - | counts | F-zh_source_tax_calculator-3eb561 |
| 22 | Single | Adult in first education | yes | - | yes | - | - | - | Employee | - | counts with H (inferred) | F-zh_source_tax_calculator-300c72, D-009 |
| 23 | Single | Adult in first education | yes | - | yes | - | - | - | Other parent | - | does not count (inferred) | F-zh_source_tax_calculator-5686d7, D-009 |
| 24 | Married | Adult in first education | yes | - | no | - | - | - | - | yes | counts (inferred) | D-009 |
| 25 | Married | Adult in first education | yes | - | no | - | - | - | - | no | does not count (inferred) | D-009 |
| 26 | Single | Adult in first education | yes | - | no | - | - | - | - | yes | counts with H | F-zh_source_tax_calculator-3eb561 |
| 27 | Single | Adult in first education | yes | - | no | - | - | - | - | no | does not count (inferred) | D-009 |
| 28 | Married | Adult in first education | no | - | - | - | - | - | - | yes | counts (inferred) | F-zh_source_tax_calculator-3eb561, D-009 |
| 29 | Married | Adult in first education | no | - | - | - | - | - | - | no | does not count | F-zh_source_tax_calculator-3eb561 |
| 30 | Single | Adult in first education | no | - | - | - | - | - | - | yes | counts | F-zh_source_tax_calculator-3eb561 |
| 31 | Single | Adult in first education | no | - | - | - | - | - | - | no | does not count (inferred) | D-009 |

_Status: inferred · Sources: F-zh_source_tax_calculator-abe889, F-zh_source_tax_calculator-300c72, F-zh_source_tax_calculator-d75286, F-zh_source_tax_calculator-5d8fb0, F-zh_source_tax_calculator-a4d358, F-zh_source_tax_calculator-dc0ae9, F-zh_source_tax_calculator-5686d7, F-zh_source_tax_calculator-dc6ace, F-zh_source_tax_calculator-3eb561, F-zh_source_tax_calculator-332e2a, D-001, D-009_

#### Child digit of the tariff code
The digit of the tariff code is the number of children whose per-child result is 'counts' or 'counts with H'; 0 if the employee has no children. (The expression shows the contribution of one child; for several children the contributions are added up.)

| # | Has children | Per-child results | → Result | Sources |
|---|---|---|---|---|
| 1 | no | - | 0 | F-zh_source_tax_calculator-037b1c |
| 2 | yes | any | Number of children that count (with or without H) | F-zh_source_tax_calculator-4c53e3 |

_Status: confirmed · Sources: F-zh_source_tax_calculator-4c53e3, F-zh_source_tax_calculator-300c72, F-zh_source_tax_calculator-4957f6, D-001, D-009_

<a id="SEC-08-cross-border-residence"></a>

## 8. Source tax: residence abroad and cross-border questions

Derive the calculator's residence answer from the home address. Germany residents are asked the cross-border questions (daily return, certificate of residence, reasonable return, more than 60 non-return days), which decide the cross-border tariff. Liechtenstein residents are asked about daily return and more than 45 non-return days, which can lead to 'in principle no source tax liability' flagged for HR.

| Story | Priority | Status |
|---|---|---|
| [US-08.1 – Derive the calculator's residence answers from the home address](stories/US-08.1-derive-the-calculator-s-residence-answers-from-the-home.md) | P1 | confirmed |
| [US-08.2 – Germany: daily return and certificate of residence](stories/US-08.2-germany-daily-return-and-certificate-of-residence.md) | P1 | decision |
| [US-08.3 – Germany: no daily return - reasonableness and more than 60 non-return days](stories/US-08.3-germany-no-daily-return-reasonableness-and-more-than-60-non.md) | P1 | decision |
| [US-08.4 – Liechtenstein: daily return and more than 45 non-return days](stories/US-08.4-liechtenstein-daily-return-and-more-than-45-non-return-days.md) | P1 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Returns daily to the home in Germany
| | |
|---|---|
| **What?** | For employees living in Germany: whether they return daily to their main residence in Germany. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Germany |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (country of the home address), Subject to source tax |
| **Who needs it?** | source tax office: Cross-border (Grenzgänger) tariff decision. |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-69edd5, F-zh_source_tax_calculator-64ac42, F-zh_source_tax_calculator-31d762, F-hr_transcript-8595fb, D-001, D-006 |

#### Certificate of residence handed in
| | |
|---|---|
| **What?** | For employees living in Germany who return daily: whether they have provided a certificate of residence (Ansässigkeitsbescheinigung). 'Not yet' is a valid answer and counts as 'no' for the tariff code. The document itself goes to HR outside Lonio. |
| **Allowed values** | yes · no · not yet |
| **When do we ask?** | Only if the employee lives in Germany and returns daily |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (country of the home address), Returns daily to the home in Germany, Subject to source tax |
| **Who needs it?** | source tax office: With daily return and a certificate the cross-border tariff applies. |
| **Status · sources** | decision · F-zh_source_tax_calculator-687e8b, F-zh_source_tax_calculator-823151, F-zh_source_tax_calculator-5f6820, F-zh_source_tax_calculator-993db3, D-001, D-035, D-037 |

#### Daily return reasonable (less than 100 km)
| | |
|---|---|
| **What?** | For employees living in Germany who do not return daily: whether a daily return would basically be reasonable (less than 100 km driving distance). |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Germany and does not return daily |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (country of the home address), Returns daily to the home in Germany, Subject to source tax |
| **Who needs it?** | source tax office: Cross-border tariff decision. |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-d2b3cf, F-zh_source_tax_calculator-087ae5, F-zh_source_tax_calculator-aaece6, D-001 |

#### More than 60 work-related non-return days expected (Germany)
| | |
|---|---|
| **What?** | For employees living in Germany for whom daily return is reasonable: whether they expect more than 60 work-related non-return days in the calendar year. The employee states the expectation; no proof is collected in Lonio. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Germany, does not return daily and daily return is reasonable |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (country of the home address), Daily return reasonable (less than 100 km), Subject to source tax |
| **Who needs it?** | source tax office: More than 60 non-return days gives the normal tariff; otherwise the cross-border tariff. |
| **Status · sources** | decision · F-zh_source_tax_calculator-e8ffac, F-zh_source_tax_calculator-ea3cd8, F-zh_source_tax_calculator-33ef31, F-zh_source_tax_calculator-c8aa5e, D-001, D-035 |

#### Returns daily to the home in Liechtenstein
| | |
|---|---|
| **What?** | For employees living in Liechtenstein: whether they return daily to their main residence in Liechtenstein. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Liechtenstein |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (country of the home address), Subject to source tax |
| **Who needs it?** | source tax office: Decides between 'in principle no source tax liability' and the normal tariff. |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-981b6b, F-zh_source_tax_calculator-a2041b, F-zh_source_tax_calculator-e22d17, F-zh_source_tax_calculator-fb87f1, D-001, D-007 |

#### More than 45 work-related non-return days expected (Liechtenstein)
| | |
|---|---|
| **What?** | For employees living in Liechtenstein who do not return daily: whether they expect more than 45 work-related non-return days in the calendar year. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Liechtenstein and does not return daily |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (country of the home address), Returns daily to the home in Liechtenstein, Subject to source tax |
| **Who needs it?** | source tax office: More than 45 days gives the normal tariff code; otherwise in principle no source tax liability. |
| **Status · sources** | decision · F-zh_source_tax_calculator-e96210, F-zh_source_tax_calculator-0ff846, F-zh_source_tax_calculator-f4ece9, F-zh_source_tax_calculator-cc19c7, D-001, D-007, D-035 |

### Business rules in this section

#### Residence for source tax
The calculator's residence answer is derived from the country of the home address: Switzerland, Germany, Liechtenstein, or any other country. Switzerland and other countries lead straight to the base tariff; Germany and Liechtenstein have their own follow-up questions.

| # | Country of residence | → Result | Sources |
|---|---|---|---|
| 1 | Switzerland | Switzerland (base tariff) | F-zh_source_tax_calculator-aedb40, F-zh_source_tax_calculator-f86c6b |
| 2 | Germany | Germany | F-zh_source_tax_calculator-d62dd4 |
| 3 | Liechtenstein | Liechtenstein | F-zh_source_tax_calculator-d62dd4 |
| 4 | any other country | Other country (base tariff) | F-zh_source_tax_calculator-d62dd4, F-zh_source_tax_calculator-f86c6b |

_Status: confirmed · Sources: F-zh_source_tax_calculator-aedb40, F-zh_source_tax_calculator-4c65ae, F-zh_source_tax_calculator-d62dd4, F-zh_source_tax_calculator-f86c6b, G-08, D-001_

#### Cross-border (Grenzgänger) tariff applies
For employees living in Germany the cross-border tariff applies if they return daily and have handed in a certificate of residence ('not yet' counts as no), or if they do not return daily, a daily return would be reasonable, and they do not expect more than 60 non-return days. In all other cases (and for all other countries) the normal tariff applies.

| # | Country of residence | Daily return to Germany | Certificate of residence | Daily return reasonable | More than 60 non-return days | → Result | Sources |
|---|---|---|---|---|---|---|---|
| 1 | not Germany | - | - | - | - | Normal tariff | F-zh_source_tax_calculator-f86c6b, F-zh_source_tax_calculator-fb87f1 |
| 2 | Germany | yes | yes | - | - | Cross-border tariff | F-zh_source_tax_calculator-993db3 |
| 3 | Germany | yes | no or not yet | - | - | Normal tariff | F-zh_source_tax_calculator-993db3, D-035 |
| 4 | Germany | no | - | no | - | Normal tariff | F-zh_source_tax_calculator-c8aa5e |
| 5 | Germany | no | - | yes | yes | Normal tariff | F-zh_source_tax_calculator-c8aa5e |
| 6 | Germany | no | - | yes | no | Cross-border tariff | F-zh_source_tax_calculator-c8aa5e |

_Status: confirmed · Sources: F-zh_source_tax_calculator-993db3, F-zh_source_tax_calculator-c8aa5e, F-zh_source_tax_calculator-66732c, D-001, D-035_

#### Liechtenstein: in principle no source tax liability
An employee living in Liechtenstein who returns daily, or does not return daily but expects at most 45 work-related non-return days, gets 'in principle no source tax liability, subject to the double taxation agreement' instead of a tariff code, flagged for HR. With more than 45 non-return days the normal tariff code applies.

| # | Country of residence | Daily return to Liechtenstein | More than 45 non-return days | → Result | Sources |
|---|---|---|---|---|---|
| 1 | not Liechtenstein | - | - | Not applicable (tariff code) | F-zh_source_tax_calculator-f86c6b |
| 2 | Liechtenstein | yes | - | In principle no source tax liability, subject to the double taxation agreement (flag for HR) | F-zh_source_tax_calculator-fb87f1, D-007 |
| 3 | Liechtenstein | no | no | In principle no source tax liability, subject to the double taxation agreement (flag for HR) | F-zh_source_tax_calculator-fb87f1, D-007 |
| 4 | Liechtenstein | no | yes | Normal tariff code | F-zh_source_tax_calculator-cc19c7, D-007 |

_Status: decision · Sources: F-zh_source_tax_calculator-fb87f1, F-zh_source_tax_calculator-cc19c7, D-007, D-034_

## Evidence
- **D-001** (product decision (Product owner)): Lonio computes the full Zurich source tax tariff code (tariff letter including the cross-border letters, child digit and church-tax suffix, e.g. "C1Y", "L0Y") for every employee subject to source tax, from the answers it collects, following the calculator's logic. HR no longer clicks through the calculator.
- **D-002** (product decision (Product owner)): Ask for the canton (pension fund 'Canton' field) only from employees living in Switzerland. Provisional - keep OQ-canton-abroad open as non-blocking, to be verified by a domain expert and Pensionskasse Muster (what to enter for employees living abroad, and whether 'Canton' means residence or work).
- **D-003** (product decision (Product owner)): Civil status offers Single, Married, Divorced, Widowed, Registered partnership and Separated. For source tax, registered partnership counts as married (including the spouse exemption) and separated counts as single, as in the calculator. For the pension fund, provisionally, registered partnership is entered as Married with the partner's date of birth, and separated as Married. Keep OQ-civil-status-partnership open as non-blocking, to be verified by a domain expert.
- **D-004** (product decision (Product owner)): The spouse's (or registered partner's) date of birth is asked from married employees, registered partners and separated employees (all entered at the fund as Married, see D-003), not from divorced or widowed employees. Keep OQ-spouse-dob-other-status open as non-blocking, to be verified by a domain expert (screenshot of the fund's screen). This closes OQ-separated-spouse-dob; the separated case is verified together with OQ-civil-status-partnership.
- **D-005** (product decision (Product owner)): Do not ask for the permit type. Ask non-Swiss employees only whether they hold a C permit (permanent residence), yes or no, and the same for a non-Swiss spouse. No party needs any other permit type. This closes OQ-permit-list. To be verified by a domain expert.
- **D-006** (product decision (Product owner)): A new employee always has earned income. Do not ask the income type, and drop the replacement-income questions and the tariff G / Q cases. This closes OQ-income-type. To be verified by a domain expert.
- **D-007** (product decision (Product owner)): Liechtenstein residents are asked the source tax questions (HR's rule decides who is asked). The result follows the calculator - with daily return or at most 45 non-return days, Lonio shows 'in principle no source tax liability, subject to the double taxation agreement' instead of a tariff code, flagged for HR; with more than 45 non-return days, the normal tariff code. This closes OQ-liechtenstein-conflict. To be verified by a domain expert.
- **D-008** (product decision (Product owner)): Anyone with Swiss citizenship counts as Swiss for source tax, even with another nationality. This closes OQ-dual-nationality. To be verified by a domain expert.
- **D-009** (product decision (Product owner)): Before go-live a domain expert compares Lonio's computed tariff code with the calculator for the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N). Special tariffs such as D (second job) are out of scope for onboarding. Keep OQ-calculator-coverage open as a non-blocking go-live condition.
- **D-010** (product decision (Product owner)): At the end of the questionnaire, remind every non-Swiss employee and every employee living abroad to bring their permit on the first working day. HR words the reminder; the spec states only its purpose. This closes OQ-permit-reminder.
- **D-033** (product decision (Product owner)): The employee enters the first working day. After submission only HR can change it; the latest date always counts and no history of earlier dates is kept.
- **D-034** (product decision (Product owner)): Only the employee side is in scope. Who starts the onboarding and any HR screen are specified later; the spec says answers are recorded for HR, not 'available to HR'. HR-side needs from D-007 (flag) and D-033 (HR changes the date) are noted for that later spec.
- **D-035** (product decision (Product owner)): For the cross-border questions the employee states what they expect for the year (non-return days). For the certificate of residence 'not yet' is a valid answer and counts as 'no' for the tariff code. Documents go to HR outside Lonio; no upload.
- **D-036** (product decision (Product owner)): Answers to questions that no longer apply after the employee changes an earlier answer are discarded on submission; until then they may be kept so going back and forth loses no input.
- **D-037** (product decision (Product owner)): After submission the questionnaire is read-only for the employee. Any later change (a move, a marriage, a new child, a certificate of residence handed in later, a corrected nationality) is made by HR and belongs to the later HR-side spec (D-034). Every derived result (insurance start date, civil status for the fund and for source tax, subject to source tax, tariff code) is always derived again from the latest answers, as for the first working day (D-033).
- **D-038** (product decision (Product owner)): Employees living abroad get the permit reminder whatever their nationality, because nationality is not asked of them (data minimisation, G-01). HR words the reminder so that a Swiss citizen living abroad, such as Stefan, can see that it does not apply to them. Asking everyone 'Swiss citizen yes/no' only for the reminder is not worth the extra question.
- **F-hr_transcript-1d5c07** (hr_transcript): Consolidated rule: the insurance start date is derived from the first working day. If the first working day is the 1st of a month, insurance starts that day. Otherwise it starts on the 1st of the following month.
  - "because insurance starts on the first of the following month." — hr_transcript/T-026, Anna
  - "Unless somebody starts exactly on the first, of course, then it's just that day." — hr_transcript/T-028, Anna
- **F-hr_transcript-2334d8** (hr_transcript): If the employee is married, the pension fund wants the spouse's date of birth.
  - "And if someone is married, they want the date of birth of the husband or wife." — hr_transcript/T-032, Anna
- **F-hr_transcript-34494f** (hr_transcript): The source tax questionnaire is the canton of Zurich's online tariff calculator, which outputs the tariff code. HR uses the Zurich calculator for everybody and acknowledges that this is not exactly how it works. Leo agreed to keep it that way for now.
  - "I use the Zurich calculator on the canton's website. The one that gives you the tariff code." — hr_transcript/T-012, Anna
  - "For everybody I use Zurich, by the way. I know it's not exactly how it works, but that's what we do for now." — hr_transcript/T-012, Anna
  - "Understood. We'll keep that for now." — hr_transcript/T-013, Leo
- **F-hr_transcript-35fae3** (hr_transcript): The employee's nationality is needed to decide whether they are subject to source tax.
  - "If you don't have a Swiss passport, you do source tax." — hr_transcript/T-010, Anna
- **F-hr_transcript-3907fe** (hr_transcript): At least one current employee (Daniel, finance) is in a registered partnership, so this case occurs.
  - "we do have one colleague in a registered partnership. Daniel, in finance." — hr_transcript/T-034, Anna
- **F-hr_transcript-3beee8** (hr_transcript): HR needs the employee's home address because HR posts many documents to employees.
  - "Yes, I need the address, obviously." — hr_transcript/T-014, Anna
  - "We post a lot of documents to people, so it has to be complete." — hr_transcript/T-014, Anna
- **F-hr_transcript-3cd6fa** (hr_transcript): Today HR clicks through the Zurich calculator manually using the employee's answers.
  - "I sit with the answers and click through it." — hr_transcript/T-012, Anna
- **F-hr_transcript-3edf89** (hr_transcript, inferred): HR needs the employee's name. Leo asked about 'Name, address' and Anna answered 'Yes', but she only elaborated on the address.
  - "What about the basics? Name, address, that kind of thing?" — hr_transcript/T-013, Leo
  - "Yes, I need the address, obviously." — hr_transcript/T-014, Anna
- **F-hr_transcript-3f2c2a** (hr_transcript): Employees who work here but live abroad (examples: Konstanz in Germany, Liechtenstein) are always subject to source tax, regardless of nationality. Even a Swiss citizen living abroad (Stefan) is subject.
  - "Those people do source tax because they work here and they don't live here." — hr_transcript/T-048, Anna
  - "And there it doesn't matter what passport you have, by the way. Stefan is actually Swiss, and he still has it." — hr_transcript/T-048, Anna
  - "So someone living abroad and working here always does it?" — hr_transcript/T-049, Leo
  - "Yes." — hr_transcript/T-050, Anna
- **F-hr_transcript-54d011** (hr_transcript, inferred): The spouse's nationality, permit and residence only matter for source tax when the employee is married. They are presumably only needed when the employee would otherwise be subject to source tax (non-Swiss, no C permit, living in Switzerland).
  - "it also changes who has to do it at all." — hr_transcript/T-044, Anna
  - "then you don't do source tax either." — hr_transcript/T-044, Anna
- **F-hr_transcript-550840** (hr_transcript): Leo summarised the rule as 'non-Swiss, but not with a C permit'. Anna only answered 'I think so' (hedged), and later added more conditions.
  - "Okay, so non-Swiss, but not with a C permit. Is that everything?" — hr_transcript/T-039, Leo
  - "I think so." — hr_transcript/T-040, Anna
- **F-hr_transcript-5af8d0** (hr_transcript): Consolidated final rule. An employee who lives abroad (outside Switzerland) is subject to source tax regardless of nationality. An employee who lives in Switzerland is subject only if they are non-Swiss without a C permit and are not married to a Swiss national or C-permit holder who lives in Switzerland. Note: Anna said 'here', which is read as Switzerland. Her 'I think' hedges remain.
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
- **F-hr_transcript-ab3cba** (hr_transcript): The employee's country of residence (the country of the home address) is needed to decide source tax liability for cross-border employees.
  - "Those people do source tax because they work here and they don't live here." — hr_transcript/T-048, Anna
- **F-hr_transcript-b0527c** (hr_transcript): First version: all non-Swiss employees (anyone without a Swiss passport) are subject to source tax.
  - "All the non-Swiss employees. Simple as that. If you don't have a Swiss passport, you do source tax." — hr_transcript/T-010, Anna
- **F-hr_transcript-b84498** (hr_transcript): Source tax questions should only be asked of employees who are subject to source tax, not of everybody.
  - "Because I never know up front who has to answer those questions." — hr_transcript/T-008, Anna
  - "So who actually needs to answer them?" — hr_transcript/T-009, Leo
- **F-hr_transcript-b90bd9** (hr_transcript): An employee married to a Swiss person, or to someone with a C permit, is not subject to source tax if that spouse lives 'here'. Example: Tomás, Brazilian with a B permit, has a Swiss wife and they live in Winterthur, so he has no source tax.
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — hr_transcript/T-044, Anna
  - "Tomás in logistics, for example. Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." — hr_transcript/T-044, Anna
- **F-hr_transcript-bd8c8e** (hr_transcript): Anna is unsure of the civil status options. From memory she named Single, Married, Divorced and ('I think') Widowed, and said the screenshots will show the actual list.
  - "I'd have to look. You'll see it in the screenshots. Single, married, divorced, I think widowed." — hr_transcript/T-034, Anna
- **F-hr_transcript-c0fe95** (hr_transcript): The address must be complete: street, house number, postcode, town and country.
  - "The full address. Street, number, postcode, town, country." — hr_transcript/T-014, Anna
- **F-hr_transcript-c53552** (hr_transcript): HR would love the form to remind employees to bring their permit on the first day, because half of them forget. Leo deferred the wording, so this is not decided.
  - "What I would love is if the form could remind people to bring their permit. Half of them forget." — hr_transcript/T-042, Anna
  - "We can look at the wording later." — hr_transcript/T-043, Leo
- **F-hr_transcript-c9d9b9** (hr_transcript): The permit type of non-Swiss employees is needed to decide source tax liability (a C permit exempts them). The permit type is only relevant for non-Swiss employees.
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
- **F-hr_transcript-f197d6** (hr_transcript): Anna does not know how the pension fund's screen handles a registered partnership, or whether the fund wants the partner's details (for example, date of birth).
  - "I honestly don't know what the fund's screen does in that case, or if they want the partner's details too." — hr_transcript/T-036, Anna
- **F-hr_transcript-f3ce84** (hr_transcript): For source tax, HR needs the spouse's nationality.
  - "So you need to know about the spouse as well." — hr_transcript/T-045, Leo
  - "Yes. Their nationality, their permit if they have one, and that they live here." — hr_transcript/T-046, Anna
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
- **F-pension_portal-6d3630** (pension_portal, inferred): No screenshot shows the form with Civil status 'Divorced' or 'Widowed'; it is unknown whether Spouse's date of birth (or any other field) appears for those values.
  - "Divorced" — 03-civil-status-list.png (pension_portal/S03-E23)
  - "Widowed" — 03-civil-status-list.png (pension_portal/S03-E24)
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
- **F-zh_source_tax_calculator-037b1c** (zh_source_tax_calculator): A single/divorced/separated/widowed person without counted children with earned income and residence in Switzerland gets tariff A (A0Y/A0N).
  - ""Q06": "Nein", "Q16": "Ja"} -> result Tarif: A0Y" — zh_source_tax_calculator/C-V01
- **F-zh_source_tax_calculator-051bb9** (zh_source_tax_calculator): Civil status options are exactly two groups: 'Verheiratet oder eingetragene Partnerschaft' (married or registered partnership) and 'Ledig, Geschieden, Getrennt, Verwitwet' (single, divorced, separated, widowed).
  - "Options: Verheiratet oder eingetragene Partnerschaft | Ledig, Geschieden, Getrennt, Verwitwet" — zh_source_tax_calculator/C-Q02
- **F-zh_source_tax_calculator-087ae5** (zh_source_tax_calculator): Daily return reasonable options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q20
- **F-zh_source_tax_calculator-09b06d** (zh_source_tax_calculator): Child age status options are exactly: Minderjährig, Volljährig und in Erstausbildung, weder noch.
  - "Options: Minderjährig | Volljährig und in Erstausbildung | weder noch" — zh_source_tax_calculator/C-Q07
- **F-zh_source_tax_calculator-0ff846** (zh_source_tax_calculator): More than 45 non-return days options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q23
- **F-zh_source_tax_calculator-103b19** (zh_source_tax_calculator): For married persons, the calculator asks whether the person or the spouses/partners have biological or adopted children.
  - "Leibliche oder adoptierte Kinder der Person oder der Ehegatten bzw. Partner?" — zh_source_tax_calculator/C-Q05
- **F-zh_source_tax_calculator-208104** (zh_source_tax_calculator): For earned income, the calculator asks for the confession (religious denomination) of the person.
  - "Konfession" — zh_source_tax_calculator/C-Q03
- **F-zh_source_tax_calculator-2eab9a** (zh_source_tax_calculator, inferred): Confession sets the church-tax suffix of the tariff: Y for röm.-kath./christ.-kath./evang.-ref., N for none or other (e.g. A0Y vs A0N).
  - "Sets the church-tax suffix: Y = röm.-kath., christ.-kath., evang.-ref.; N = Keine oder andere" — zh_source_tax_calculator/C-Q03
  - "result Tarif: A0Y" — zh_source_tax_calculator/C-V01
  - "result Tarif: A0N" — zh_source_tax_calculator/C-V02
- **F-zh_source_tax_calculator-300c72** (zh_source_tax_calculator): For a single/divorced/separated/widowed person, any child counted with H gives an H tariff; a child counts with H when it lives in the household and the person has sole custody or is the main financial contributor.
  - "For a single person, any child counted with H gives an H tariff (e.g. A1 + H1 -> H2N). A child is counted with H when it lives in the household and the person has sole custody or is the main financial contributor." — zh_source_tax_calculator/C-N04
  - "result Tarif: H1Y (Kind Ergebnis: H1)" — zh_source_tax_calculator/C-V17
- **F-zh_source_tax_calculator-31d762** (zh_source_tax_calculator): Q18 is shown only when income type is Erwerbseinkommen and country of residence is Deutschland.
  - "Tägliche Rückkehr an den Hauptwohnsitz in Deutschland?" — zh_source_tax_calculator/C-Q18
- **F-zh_source_tax_calculator-32fec9** (zh_source_tax_calculator): Parental care (Q14) options are Ja / Nein.
  - "Elterliche Sorge Options: Ja | Nein" — zh_source_tax_calculator/C-Q14
- **F-zh_source_tax_calculator-332e2a** (zh_source_tax_calculator): The full cross-product of child paths × residence paths × confession × civil status was not enumerated.
  - "The full cross-product of child paths × residence paths × confession × civil status was not enumerated (combinatorial)." — zh_source_tax_calculator/C-N06
- **F-zh_source_tax_calculator-33ef31** (zh_source_tax_calculator): Q21 is shown only when daily return is reasonable (Q20 = Ja).
  - "Nachweis von mehr als 60 beruflich bedingten Nichtrückkehrtagen im Kalenderjahr beigebracht?" — zh_source_tax_calculator/C-Q21
- **F-zh_source_tax_calculator-3a75cc** (zh_source_tax_calculator): Same-household options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q08
- **F-zh_source_tax_calculator-3eb561** (zh_source_tax_calculator): Adult child in first education: in household with common household (married) counts (B1N); not in household counts only if more than 50% of maintenance is provided (single A1N; married with Nein -> B0N); single, in household without common household and >50% maintenance gives H1N.
  - ""Q10": "Ja", "Q16": "Ja"} -> result Tarif: B1N" — zh_source_tax_calculator/C-V14
  - ""Q15": "Nein", "Q16": "Ja"} -> result Tarif: B0N" — zh_source_tax_calculator/C-V15
  - "result Tarif: A1N (Kind Ergebnis: A1)" — zh_source_tax_calculator/C-V22
  - ""Q15": "Ja", "Q16": "Ja"} -> result Tarif: H1N" — zh_source_tax_calculator/C-V23
- **F-zh_source_tax_calculator-4957f6** (zh_source_tax_calculator): Not tested: more than 3 children (upper limit unknown), whether 'Kind löschen' recomputes correctly, and tariff D or other special tariffs.
  - "Not tested: more than 3 children (the upper limit of 'Ein weiteres Kind erfassen' is unknown); whether 'Kind löschen' recomputes correctly; tariff D or other special tariffs (none appeared in any path)." — zh_source_tax_calculator/C-N07
- **F-zh_source_tax_calculator-4b7063** (zh_source_tax_calculator): For a minor child in the same household, the calculator asks about parental custody (shared or sole).
  - "Elterliche Sorge Options: Geteiltes Sorgerecht | Alleiniges Sorgerecht" — zh_source_tax_calculator/C-Q09
- **F-zh_source_tax_calculator-4c53e3** (zh_source_tax_calculator): The tariff digit equals the number of children whose per-child result digit is 1 (e.g. three counted children -> C3Y).
  - "The final tariff's digit equals the number of children whose 'Kind Ergebnis' digit is 1." — zh_source_tax_calculator/C-N04
  - "result Tarif: C3Y" — zh_source_tax_calculator/C-V28
- **F-zh_source_tax_calculator-4c65ae** (zh_source_tax_calculator): If the main residence is not in Switzerland, the calculator asks for the country of residence.
  - "Wohnsitzstaat" — zh_source_tax_calculator/C-Q17
- **F-zh_source_tax_calculator-5686d7** (zh_source_tax_calculator): Single, minor child in household, shared custody, common household with the other parent and other parent as main contributor gives A0N.
  - ""Q12": "Anderer Elternteil", "Q16": "Ja"} -> result Tarif: A0N (Kind Ergebnis: A0)" — zh_source_tax_calculator/C-V18
- **F-zh_source_tax_calculator-5725a8** (zh_source_tax_calculator): For each minor or adult-in-first-education child, the calculator asks whether the child lives in the same household.
  - "Wohnsitz des Kindes im selben Haushalt?" — zh_source_tax_calculator/C-Q08
- **F-zh_source_tax_calculator-5d8fb0** (zh_source_tax_calculator): Married, minor child in household, shared custody and common household with the other parent: the child counts (C1Y).
  - ""Q10": "Ja", "Q16": "Ja"} -> result Tarif: C1Y" — zh_source_tax_calculator/C-V09
- **F-zh_source_tax_calculator-5f6820** (zh_source_tax_calculator): The residence certificate question is shown only when the person (Germany resident) returns daily (Q18 = Ja for earned income, Q24 = Ja for replacement income).
  - "Ansässigkeitsbescheinigung beigebracht?" — zh_source_tax_calculator/C-Q19
- **F-zh_source_tax_calculator-640429** (zh_source_tax_calculator): For each child, the calculator asks whether the child is minor, or adult and in first education.
  - "Kind minderjährig oder volljährig und in Erstausbildung?" — zh_source_tax_calculator/C-Q07
- **F-zh_source_tax_calculator-64ac33** (zh_source_tax_calculator): Alternating custody is asked only for a minor child when: (in household, shared custody, no common household with other parent) or (married, not in household, shared custody Q13 = Ja) or (non-married, not in household, parental care Q14 = Ja).
  - "Alternierende Obhut?" — zh_source_tax_calculator/C-Q11
- **F-zh_source_tax_calculator-64ac42** (zh_source_tax_calculator): Daily return to Germany options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q18
- **F-zh_source_tax_calculator-66732c** (zh_source_tax_calculator): The residence/cross-border block was explored exhaustively only for married + Y + 1 child and for Ersatzeinkünfte; for tariffs A/B/H it was only spot-checked.
  - "For A/B/H it was spot-checked only via DE daily return + certificate (L0Y, L1N, M0N, M0Y, P1Y, P3N) and LI more than 45 days / Anderes Land (A0N)." — zh_source_tax_calculator/C-N05
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
- **F-zh_source_tax_calculator-823151** (zh_source_tax_calculator): Residence certificate options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q19
- **F-zh_source_tax_calculator-83de1d** (zh_source_tax_calculator): The custody question (Q09) is shown only when the child is Minderjährig and lives in the same household, for both civil status groups.
  - "Elterliche Sorge" — zh_source_tax_calculator/C-Q09
- **F-zh_source_tax_calculator-86d588** (zh_source_tax_calculator): The calculator determines the source tax tariff from employee data; the tariffs shown are not legally binding.
  - "Der Tarifrechner dient der Ermittlung des Quellensteuertarifs." — zh_source_tax_calculator/C-N02
  - "Die ausgewiesenen Tarife sind nicht rechtsverbindlich." — zh_source_tax_calculator/C-N02
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
- **F-zh_source_tax_calculator-993db3** (zh_source_tax_calculator): Germany resident with daily return and a residence certificate gets the cross-border (Grenzgänger) tariff: A->L, B->M, C->N, H->P, G->Q; without a certificate the normal tariff applies.
  - "Ja -> cross-border (Grenzgänger) tariff: A->L, B->M, C->N, H->P, G->Q; Nein -> normal tariff" — zh_source_tax_calculator/C-Q19
  - ""Q18": "Ja", "Q19": "Ja"} -> result Tarif: N1Y" — zh_source_tax_calculator/C-V34
  - ""Q18": "Ja", "Q19": "Nein"} -> result Tarif: C1Y" — zh_source_tax_calculator/C-V35
  - ""Q24": "Ja", "Q19": "Ja"} -> result Tarif: Q" — zh_source_tax_calculator/C-V44
- **F-zh_source_tax_calculator-a166c7** (zh_source_tax_calculator): Children question (married) options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q05
- **F-zh_source_tax_calculator-a2041b** (zh_source_tax_calculator): Daily return to Liechtenstein options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q22
- **F-zh_source_tax_calculator-a33b65** (zh_source_tax_calculator): The married children question is shown only when civil status is 'Verheiratet oder eingetragene Partnerschaft' and the spouse employment question is answered.
  - "Leibliche oder adoptierte Kinder der Person oder der Ehegatten bzw. Partner?" — zh_source_tax_calculator/C-Q05
- **F-zh_source_tax_calculator-a4d358** (zh_source_tax_calculator, inferred): Married, minor child in household, shared custody, no common household: alternating custody with the other parent as main contributor, or no alternating custody, gives C0Y (child not counted).
  - ""Q12": "Anderer Elternteil", "Q16": "Ja"} -> result Tarif: C0Y" — zh_source_tax_calculator/C-V10
  - ""Q11": "Nein", "Q16": "Ja"} -> result Tarif: C0Y" — zh_source_tax_calculator/C-V11
- **F-zh_source_tax_calculator-aaece6** (zh_source_tax_calculator): Q20 is shown only when income type is Erwerbseinkommen, country is Deutschland and daily return = Nein.
  - "Tägliche Rückkehr grundsätzlich zumutbar (weniger als 100km Fahrdistanz)?" — zh_source_tax_calculator/C-Q20
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
- **F-zh_source_tax_calculator-b62b85** (zh_source_tax_calculator): Children question (non-married) options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q06
- **F-zh_source_tax_calculator-b7fea8** (zh_source_tax_calculator): Confession options are exactly: 'röm.-kath., christ.-kath., evang.-ref.' and 'Keine oder andere' (none or other).
  - "Options: röm.-kath., christ.-kath., evang.-ref. | Keine oder andere" — zh_source_tax_calculator/C-Q03
- **F-zh_source_tax_calculator-c09dc1** (zh_source_tax_calculator): Parental custody options (child in household) are exactly: Geteiltes Sorgerecht (shared) and Alleiniges Sorgerecht (sole).
  - "Options: Geteiltes Sorgerecht | Alleiniges Sorgerecht" — zh_source_tax_calculator/C-Q09
- **F-zh_source_tax_calculator-c8aa5e** (zh_source_tax_calculator): Germany resident without daily return: if return is not reasonable -> normal tariff; if reasonable and >60 non-return days proven -> normal tariff; if reasonable and no proof -> cross-border tariff (L/M/N/P, Q).
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
- **F-zh_source_tax_calculator-d2b3cf** (zh_source_tax_calculator): For earned income, Germany residents without daily return are asked whether daily return is basically reasonable (less than 100 km driving distance).
  - "Tägliche Rückkehr grundsätzlich zumutbar (weniger als 100km Fahrdistanz)?" — zh_source_tax_calculator/C-Q20
- **F-zh_source_tax_calculator-d2e516** (zh_source_tax_calculator): Shared custody (Q13) options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q13
- **F-zh_source_tax_calculator-d5a6fe** (zh_source_tax_calculator): The income type question is always shown and is the first question.
  - "Für welche Einkünfte möchten Sie den Quellensteuertarif ermitteln?" — zh_source_tax_calculator/C-Q01
- **F-zh_source_tax_calculator-d62dd4** (zh_source_tax_calculator): Country of residence options are exactly: Deutschland, Liechtenstein, Anderes Land (other country).
  - "Options: Deutschland | Liechtenstein | Anderes Land" — zh_source_tax_calculator/C-Q17
- **F-zh_source_tax_calculator-d75286** (zh_source_tax_calculator): A minor child in the same household with sole custody counts as a child (married: C1/B1; single: H1).
  - "result Tarif: C1Y (Kind Ergebnis: C1)" — zh_source_tax_calculator/C-V07
  - "result Tarif: B1N (Kind Ergebnis: B1)" — zh_source_tax_calculator/C-V08
- **F-zh_source_tax_calculator-d79949** (zh_source_tax_calculator): The calculator asks whether the person lives in a common household with the other parent.
  - "Gemeinsamer Haushalt mit dem anderen Elternteil?" — zh_source_tax_calculator/C-Q10
- **F-zh_source_tax_calculator-da19df** (zh_source_tax_calculator): The calculator asks whether there is alternating custody (alternierende Obhut).
  - "Alternierende Obhut?" — zh_source_tax_calculator/C-Q11
- **F-zh_source_tax_calculator-dc0ae9** (zh_source_tax_calculator, inferred): Single, minor child in household, shared custody, no common household and no alternating custody gives H1N (child counted with H).
  - ""Q11": "Nein", "Q16": "Ja"} -> result Tarif: H1N" — zh_source_tax_calculator/C-V19
- **F-zh_source_tax_calculator-dc6ace** (zh_source_tax_calculator): Minor child not in the household: with shared custody/parental care, alternating custody and the person as main contributor, the child counts (married B1N, single H1N); without shared custody/parental care it does not count (B0N, A0N).
  - "result Tarif: B1N (Kind Ergebnis: B1)" — zh_source_tax_calculator/C-V12
  - ""Q13": "Nein", "Q16": "Ja"} -> result Tarif: B0N" — zh_source_tax_calculator/C-V13
  - "result Tarif: H1N (Kind Ergebnis: H1)" — zh_source_tax_calculator/C-V20
  - ""Q14": "Nein", "Q16": "Ja"} -> result Tarif: A0N" — zh_source_tax_calculator/C-V21
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
- **F-zh_source_tax_calculator-f86c6b** (zh_source_tax_calculator): Residence in Switzerland or in 'Anderes Land' gives the base tariff without further residence questions.
  - "CH or 'Anderes Land' -> base tariff." — zh_source_tax_calculator/C-N05
  - ""Q17": "Anderes Land"} -> result Tarif: A0N" — zh_source_tax_calculator/C-V42
  - ""Q17": "Anderes Land"} -> result Tarif: G" — zh_source_tax_calculator/C-V52
- **F-zh_source_tax_calculator-fb4a56** (zh_source_tax_calculator): Q14 is shown only when civil status is 'Ledig, Geschieden, Getrennt, Verwitwet', the child is minor and not in the same household.
  - "Elterliche Sorge Options: Ja | Nein" — zh_source_tax_calculator/C-Q14
- **F-zh_source_tax_calculator-fb87f1** (zh_source_tax_calculator): Liechtenstein residents with daily return, or without daily return and not more than 45 non-return days, get 'Grundsätzlich keine Quellensteuerpflicht' (in principle no source tax liability), subject to the double taxation agreement.
  - "Ja -> 'Grundsätzlich keine Quellensteuerpflicht'" — zh_source_tax_calculator/C-Q22
  - ""Q22": "Ja"} -> result Grundsätzlich keine Quellensteuerpflicht / Unter Vorbehalt des Doppelbesteuerungsabkommens" — zh_source_tax_calculator/C-V39
  - ""Q23": "Nein"} -> result Grundsätzlich keine Quellensteuerpflicht" — zh_source_tax_calculator/C-V41
  - ""Q27": "Ja"} -> result Grundsätzlich keine Quellensteuerpflicht" — zh_source_tax_calculator/C-V49
- **F-zh_source_tax_calculator-fd9a15** (zh_source_tax_calculator): Child questions repeat per child; 'Ein weiteres Kind erfassen' adds another child block and 'Kind löschen' removes one. Each completed block shows a per-child result ('Kind Ergebnis').
  - "A link button 'Ein weiteres Kind erfassen' adds another child block, and each block has a 'Kind löschen' button." — zh_source_tax_calculator/C-Q07
  - "Child questions repeat for each child (input names child-1__…, child-2__…)." — zh_source_tax_calculator/C-N04
- **F-zh_source_tax_calculator-fe0305** (zh_source_tax_calculator): For married persons with a minor child not in the household, the calculator asks whether custody is shared (Geteiltes Sorgerecht).
  - "Geteiltes Sorgerecht Options: Ja | Nein" — zh_source_tax_calculator/C-Q13
- **G-01** (product owner guidance): Lonio collects onboarding data from a new employee **once** and reuses it for every receiving party. Asking too little blocks a registration; asking too much collects personal data we must not have (data minimisation). A question must only be asked when at least one receiving party needs the answer for this person.
- **G-04** (product owner guidance): Scope of these feature specs: what Lonio asks the new employee (which information, in which order, under which conditions, required or not) and the business rules derived from the answers. How collected data is transmitted to each receiving party (exports, portal entry, change notifications) is a separate topic; each information item documents which stakeholder needs it and why.
- **G-08** (product owner guidance): Prefer asking for primary facts and **deriving** values (e.g. ask the first working day, derive the insurance start date) instead of asking the employee for values they cannot know.
- **G-09** (product owner guidance): Questionnaire language: English.
- **G-10** (product owner guidance): Business wording for values (used in allowed values and examples): countries by English name ("Switzerland", "Germany", "Liechtenstein"), permits as "B permit", "C permit", civil status exactly as the pension fund's list shows it ("Single", "Married", ...), dates as DD.MM.YYYY, yes/no as "yes"/"no".
