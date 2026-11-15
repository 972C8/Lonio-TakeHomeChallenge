---
id: employee-onboarding
title: "Employee onboarding questionnaire"
stakeholders: [employee, hr, pension_fund, source_tax]
sections: [SEC-01-questionnaire-flow, SEC-02-personal-details-address, SEC-03-employment-start, SEC-04-civil-status-spouse, SEC-05-source-tax-liability, SEC-08-cross-border-residence, SEC-06-source-tax-tariff-basics, SEC-07-source-tax-children]
stories: [US-01.1, US-01.2, US-01.3, US-01.4, US-01.5, US-01.6, US-01.7, US-01.8, US-02.1, US-02.2, US-02.3, US-02.4, US-03.1, US-03.2, US-03.3, US-04.1, US-04.2, US-04.3, US-04.4, US-05.1, US-05.2, US-05.3, US-05.4, US-08.1, US-08.2, US-08.3, US-08.4, US-08.5, US-06.2, US-06.3, US-06.7, US-06.4, US-06.5, US-06.6, US-07.1, US-07.2, US-07.3, US-07.4, US-07.5, US-07.6]
---

# Employee onboarding questionnaire

Each user story is its own file in [stories/](stories/); this file holds the
feature, its sections and the information and rules they share.

**Goal:** A new employee of Muster AG answers one English onboarding questionnaire in Lonio. It asks each piece of information once and only when a receiving party needs it for that person. From the answers, Lonio registers the employee with Pensionskasse Muster, decides whether source tax applies and computes the full Zurich source tax tariff code, so that HR has everything it needs.

## Context
Today HR at Muster AG collects onboarding data itself and enters it for each receiving party. For the pension fund (Pensionskasse Muster), the insurance start date is 'the number one thing'. It depends on the first working day, and that date often changes. The fund also needs the name, date of birth, canton, civil status and, for married employees, the spouse's date of birth. To find the source tax tariff, HR works out who is subject to source tax using its own rule: anyone living abroad, and people living in Switzerland who are not Swiss, have no C permit and are not married to a Swiss national or C-permit holder living in Switzerland. HR then clicks through the Zurich tariff calculator, including the cross-border questions for Germany and Liechtenstein and the detailed questions per child. HR also wants a complete postal address and asks non-Swiss employees to bring their permit. Asking too little blocks a registration, and asking too much collects personal data no party needs (G-01). Lonio replaces this work. The employee answers once in eight fixed steps (D-047), and Lonio works out the insurance start date, the civil status and canton for the fund, whether source tax applies and the full tariff code (D-001). The sources are fictional and are treated as the truth (G-06). AHV data, IT equipment, the badge photo, how data is sent to each party and all HR screens are out of scope (G-03, G-04, D-034).

**Stakeholders:** new employee, HR, pension fund, source tax office

<a id="flow"></a>

## Questionnaire flow

The questionnaire has eight steps, always in this order. Only the questions that apply to this employee are shown, and a step with no applicable question is skipped (for example step 3 for employees living abroad, steps 5 to 7 for employees who are not subject to source tax). Earlier answers decide which later questions apply, so basic facts come first, then residence, nationality, civil status, cross-border commuting, source tax details and children. Each answer is asked once and reused for every receiving party. Answers are saved as the employee goes and can be resumed until submission.

| Step | What is asked | Shown to | Stories |
|---|---|---|---|
| 1. About you | First name, last name, date of birth and first working day. | Everyone | [US-02.1](stories/US-02.1-collect-the-employee-s-name-and-date-of-birth.md), [US-03.1](stories/US-03.1-employee-confirms-the-first-working-day.md), [US-03.2](stories/US-03.2-derive-the-pension-insurance-start-date-from-the-first.md), [US-03.3](stories/US-03.3-re-derive-the-insurance-start-date-when-the-first-working.md) |
| 2. Home address | Street, house number, postcode, town and country of residence as on the first working day; the canton only if the country is Switzerland. | Everyone | [US-02.2](stories/US-02.2-collect-a-complete-postal-home-address.md), [US-02.3](stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md), [US-02.4](stories/US-02.4-ask-swiss-residents-for-their-canton.md), [US-05.4](stories/US-05.4-derive-the-calculator-s-residence-from-the-home-address.md) |
| 3. Nationality and C permit | Nationality; whether the employee holds a C permit only if not Swiss. | Employees living in Switzerland | [US-05.1](stories/US-05.1-ask-nationality-and-c-permit-only-of-employees-living-in.md), [US-05.3](stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md) |
| 4. Civil status and spouse | Civil status; the spouse's or partner's date of birth if married, in a registered partnership or separated; if the employee lives in Switzerland, is not Swiss, has no C permit and is married or in a registered partnership: the spouse's nationality, whether the spouse holds a C permit (if not Swiss) and whether the spouse lives in Switzerland. | Everyone (spouse questions only where the conditions apply) | [US-04.1](stories/US-04.1-ask-every-employee-for-their-civil-status.md), [US-04.2](stories/US-04.2-ask-for-the-spouse-s-or-registered-partner-s-date-of-birth.md), [US-04.3](stories/US-04.3-answer-the-calculator-s-civil-status-question-from-the.md), [US-04.4](stories/US-04.4-enter-the-civil-status-on-the-pension-fund-s-list.md), [US-05.2](stories/US-05.2-ask-the-spouse-s-nationality-c-permit-and-residence-only.md), [US-05.3](stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md) |
| 5. Cross-border commuting | Liechtenstein: daily return, and if not daily, whether more than 45 non-return days are expected. Germany: daily return; if daily, whether a certificate of residence exists ('not yet' counts as no); if not daily, whether daily return is reasonable and, if so, whether more than 60 non-return days are expected. | Employees living in Liechtenstein or Germany who are subject to source tax | [US-08.1](stories/US-08.1-derive-the-calculator-s-residence-answers-from-the-home.md), [US-08.2](stories/US-08.2-germany-daily-return-and-certificate-of-residence.md), [US-08.3](stories/US-08.3-germany-no-daily-return-reasonableness-and-more-than-60-non.md), [US-08.4](stories/US-08.4-liechtenstein-daily-return-and-more-than-45-non-return-days.md), [US-08.5](stories/US-08.5-liechtenstein-record-the-double-taxation-agreement-note-next.md) |
| 6. Source tax details | Denomination; whether the spouse or partner is gainfully employed (only if married or in a registered partnership); whether the employee has children. | Employees subject to source tax, except Liechtenstein residents who are in principle not liable | [US-06.2](stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md), [US-06.3](stories/US-06.3-ask-married-employees-and-registered-partners-subject-to.md), [US-06.7](stories/US-06.7-ask-employees-subject-to-source-tax-whether-they-have.md) |
| 7. Children | One block per child: whether the child is a minor or an adult in first education, whether the child lives in the household, and the follow-up questions on custody, parental care, common household with the other parent, alternating custody, main financial contributor and more than 50% maintenance, as far as they apply to that child. | Employees subject to source tax who have children | [US-07.1](stories/US-07.1-ask-about-children-only-of-employees-who-need-a-source-tax.md), [US-07.2](stories/US-07.2-one-block-per-child-age-status-and-household.md), [US-07.3](stories/US-07.3-minor-child-living-in-the-employee-s-household.md), [US-07.4](stories/US-07.4-minor-child-not-living-in-the-employee-s-household.md), [US-07.5](stories/US-07.5-adult-child-in-first-education.md) |
| 8. Permit reminder, summary and submission | Nothing new is asked. The employee sees the permit reminder if it applies, reviews a summary of the answers and submits with one confirmation. | Everyone (the permit reminder only to non-Swiss employees living in Switzerland and to employees living abroad) | [US-01.4](stories/US-01.4-remind-non-swiss-employees-and-employees-living-abroad-to.md) |

Never asked, always derived from the answers: Questionnaire flow overview ([US-01.1](stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md), [US-01.2](stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md), [US-01.3](stories/US-01.3-ask-each-piece-of-information-once-and-reuse-it-for-every.md), [US-01.7](stories/US-01.7-save-answers-as-i-go-and-resume-until-i-submit.md), [US-01.8](stories/US-01.8-review-a-summary-and-submit-with-one-confirmation.md)), Civil status for the pension fund ([US-04.4](stories/US-04.4-enter-the-civil-status-on-the-pension-fund-s-list.md)), Canton for the pension fund ([US-02.4](stories/US-02.4-ask-swiss-residents-for-their-canton.md)), Subject to source tax ([US-05.1](stories/US-05.1-ask-nationality-and-c-permit-only-of-employees-living-in.md), [US-05.2](stories/US-05.2-ask-the-spouse-s-nationality-c-permit-and-residence-only.md), [US-05.3](stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md)), Double taxation agreement note (Liechtenstein) ([US-08.5](stories/US-08.5-liechtenstein-record-the-double-taxation-agreement-note-next.md)), Civil status group for source tax ([US-04.3](stories/US-04.3-answer-the-calculator-s-civil-status-question-from-the.md)), Residence for the tariff calculation ([US-05.4](stories/US-05.4-derive-the-calculator-s-residence-from-the-home-address.md), [US-08.1](stories/US-08.1-derive-the-calculator-s-residence-answers-from-the-home.md)), Church-tax suffix ([US-06.2](stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md)), Per-child result ([US-07.2](stories/US-07.2-one-block-per-child-age-status-and-household.md), [US-07.3](stories/US-07.3-minor-child-living-in-the-employee-s-household.md), [US-07.4](stories/US-07.4-minor-child-not-living-in-the-employee-s-household.md), [US-07.5](stories/US-07.5-adult-child-in-first-education.md), [US-07.6](stories/US-07.6-child-digit-of-the-tariff-code-and-go-live-check-of-the.md)), Number of counted children (child digit) ([US-07.6](stories/US-07.6-child-digit-of-the-tariff-code-and-go-live-check-of-the.md)), Base tariff letter ([US-06.4](stories/US-06.4-derive-the-base-source-tax-tariff-letter.md)), Cross-border (Grenzgänger) tariff applies ([US-08.2](stories/US-08.2-germany-daily-return-and-certificate-of-residence.md), [US-08.3](stories/US-08.3-germany-no-daily-return-reasonableness-and-more-than-60-non.md)), Tariff letter ([US-06.5](stories/US-06.5-replace-the-base-letter-with-the-cross-border-letter-where.md)), Full source tax tariff code ([US-06.6](stories/US-06.6-compute-and-record-the-full-source-tax-tariff-code.md)), Discard answers that no longer apply ([US-01.5](stories/US-01.5-discard-answers-that-no-longer-apply-on-submission.md)), Read-only after submission ([US-01.6](stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md)).

After submission the questionnaire is read-only for the employee and is never reopened. Answers that no longer apply are discarded on submission. Later changes are made by HR.

## Contents

| Section | Stories |
|---|---|
| [1. Questionnaire flow overview](#SEC-01-questionnaire-flow) | [US-01.1](stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md), [US-01.2](stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md), [US-01.3](stories/US-01.3-ask-each-piece-of-information-once-and-reuse-it-for-every.md), [US-01.4](stories/US-01.4-remind-non-swiss-employees-and-employees-living-abroad-to.md), [US-01.5](stories/US-01.5-discard-answers-that-no-longer-apply-on-submission.md), [US-01.6](stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md), [US-01.7](stories/US-01.7-save-answers-as-i-go-and-resume-until-i-submit.md), [US-01.8](stories/US-01.8-review-a-summary-and-submit-with-one-confirmation.md) |
| [2. Personal details and home address](#SEC-02-personal-details-address) | [US-02.1](stories/US-02.1-collect-the-employee-s-name-and-date-of-birth.md), [US-02.2](stories/US-02.2-collect-a-complete-postal-home-address.md), [US-02.3](stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md), [US-02.4](stories/US-02.4-ask-swiss-residents-for-their-canton.md) |
| [3. First working day and insurance start date](#SEC-03-employment-start) | [US-03.1](stories/US-03.1-employee-confirms-the-first-working-day.md), [US-03.2](stories/US-03.2-derive-the-pension-insurance-start-date-from-the-first.md), [US-03.3](stories/US-03.3-re-derive-the-insurance-start-date-when-the-first-working.md) |
| [4. Civil status and spouse data](#SEC-04-civil-status-spouse) | [US-04.1](stories/US-04.1-ask-every-employee-for-their-civil-status.md), [US-04.2](stories/US-04.2-ask-for-the-spouse-s-or-registered-partner-s-date-of-birth.md), [US-04.3](stories/US-04.3-answer-the-calculator-s-civil-status-question-from-the.md), [US-04.4](stories/US-04.4-enter-the-civil-status-on-the-pension-fund-s-list.md) |
| [5. Who is subject to source tax](#SEC-05-source-tax-liability) | [US-05.1](stories/US-05.1-ask-nationality-and-c-permit-only-of-employees-living-in.md), [US-05.2](stories/US-05.2-ask-the-spouse-s-nationality-c-permit-and-residence-only.md), [US-05.3](stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md), [US-05.4](stories/US-05.4-derive-the-calculator-s-residence-from-the-home-address.md) |
| [6. Source tax: residence abroad and cross-border questions](#SEC-08-cross-border-residence) | [US-08.1](stories/US-08.1-derive-the-calculator-s-residence-answers-from-the-home.md), [US-08.2](stories/US-08.2-germany-daily-return-and-certificate-of-residence.md), [US-08.3](stories/US-08.3-germany-no-daily-return-reasonableness-and-more-than-60-non.md), [US-08.4](stories/US-08.4-liechtenstein-daily-return-and-more-than-45-non-return-days.md), [US-08.5](stories/US-08.5-liechtenstein-record-the-double-taxation-agreement-note-next.md) |
| [7. Source tax tariff: denomination, spouse employment and tariff code](#SEC-06-source-tax-tariff-basics) | [US-06.2](stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md), [US-06.3](stories/US-06.3-ask-married-employees-and-registered-partners-subject-to.md), [US-06.7](stories/US-06.7-ask-employees-subject-to-source-tax-whether-they-have.md), [US-06.4](stories/US-06.4-derive-the-base-source-tax-tariff-letter.md), [US-06.5](stories/US-06.5-replace-the-base-letter-with-the-cross-border-letter-where.md), [US-06.6](stories/US-06.6-compute-and-record-the-full-source-tax-tariff-code.md) |
| [8. Source tax tariff: children](#SEC-07-source-tax-children) | [US-07.1](stories/US-07.1-ask-about-children-only-of-employees-who-need-a-source-tax.md), [US-07.2](stories/US-07.2-one-block-per-child-age-status-and-household.md), [US-07.3](stories/US-07.3-minor-child-living-in-the-employee-s-household.md), [US-07.4](stories/US-07.4-minor-child-not-living-in-the-employee-s-household.md), [US-07.5](stories/US-07.5-adult-child-in-first-education.md), [US-07.6](stories/US-07.6-child-digit-of-the-tariff-code-and-go-live-check-of-the.md) |

<a id="SEC-01-questionnaire-flow"></a>

## 1. Questionnaire flow overview

Set the eight steps, their order and when each applies, how the employee saves, resumes, reviews and submits, and what happens to answers that no longer apply or need changing after submission.

| Story | Priority | Status |
|---|---|---|
| [US-01.1 – Show the source tax step only to employees who are subject to source tax](stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md) | P1 | decision |
| [US-01.2 – Ask the steps in an order that avoids unneeded questions](stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md) | P1 | decision |
| [US-01.3 – Ask each piece of information once and reuse it for every receiving party](stories/US-01.3-ask-each-piece-of-information-once-and-reuse-it-for-every.md) | P1 | decision |
| [US-01.4 – Remind non-Swiss employees and employees living abroad to bring their permit](stories/US-01.4-remind-non-swiss-employees-and-employees-living-abroad-to.md) | P2 | decision |
| [US-01.5 – Discard answers that no longer apply on submission](stories/US-01.5-discard-answers-that-no-longer-apply-on-submission.md) | P2 | decision |
| [US-01.6 – Make the questionnaire read-only after submission and derive results from the latest answers](stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md) | P1 | decision |
| [US-01.7 – Save answers as I go and resume until I submit](stories/US-01.7-save-answers-as-i-go-and-resume-until-i-submit.md) | P2 | decision |
| [US-01.8 – Review a summary and submit with one confirmation](stories/US-01.8-review-a-summary-and-submit-with-one-confirmation.md) | P2 | decision |

### Business rules in this section

#### Questionnaire flow overview
The questionnaire has exactly eight steps in this order. Each question is asked once and its answer is reused for every receiving party; a question is only asked when at least one party needs the answer for this person. Answers are saved as the employee goes and they can resume until they submit; submitting needs one confirmation on a summary page.

| # | Step | → Result | Sources |
|---|---|---|---|
| 1 | 1 About you | Always: first name, last name, date of birth, first working day | D-047, F-pension_portal-db702a, F-hr_transcript-872bd7 |
| 2 | 2 Home address | Always: street, house number (or 'no house number'), postcode, town and country as on the first working day; canton only if the country is Switzerland | D-047, D-041, D-042, D-049, D-002 |
| 3 | 3 Nationality and C permit | Only employees living in Switzerland: nationality; C permit (yes/no) only if not Swiss | D-047, D-005, D-008 |
| 4 | 4 Civil status and spouse | Civil status from everyone; spouse's date of birth if married, registered partnership or separated; spouse's nationality, C permit and whether the spouse lives in Switzerland only for non-Swiss employees without C permit living in Switzerland who are married or in a registered partnership | D-047, D-003, D-004, F-hr_transcript-5af8d0 |
| 5 | 5 Cross-border commuting | Only employees living in Liechtenstein or Germany (always subject to source tax): daily return and non-return days; certificate of residence for Germany | D-047, D-007, D-035, D-040 |
| 6 | 6 Source tax details | Only employees subject to source tax, except Liechtenstein residents in principle not liable: denomination, spouse gainfully employed (married or registered partnership), has children | D-047, D-040, F-hr_transcript-b84498 |
| 7 | 7 Children | Only if source tax details are asked and the employee has children: one block per child, no maximum | D-047, D-044 |
| 8 | 8 Permit reminder, summary and submission | Always: summary and one confirmation; permit reminder for non-Swiss employees and employees living abroad | D-047, D-010, D-038, D-050 |

_Status: decision · Sources: D-047, D-050, G-01, D-036, D-037_

#### Discard answers that no longer apply
Answers to questions that no longer apply after an earlier answer changes are kept while the employee goes back and forth, and discarded on submission. The same applies after an HR change.

| # | Moment | → Result | Sources |
|---|---|---|---|
| 1 | before submission | answers kept | D-036, D-050 |
| 2 | on submission or after an HR change | answers to questions that no longer apply are discarded | D-036, D-048 |

_Status: decision · Sources: G-01, D-036, D-048, D-050_

#### Read-only after submission
After submission the questionnaire is read-only for the employee and never reopened. Later changes (move, marriage, new child, late certificate of residence, corrected nationality, first working day) are made by HR; every derived result is derived again from the latest answers, and results depending on questions never asked show 'incomplete - HR must complete' until HR enters the answers.

| # | Moment | → Result | Sources |
|---|---|---|---|
| 1 | before submission | employee can edit and resume | D-050 |
| 2 | after submission | read-only for the employee; changes by HR only | D-037, D-053, D-033 |

_Status: decision · Sources: D-033, D-034, D-037, D-048, D-053_

#### Permit reminder
At the end of the questionnaire, every non-Swiss employee living in Switzerland and every employee living abroad (whatever their nationality, which is not asked) is reminded to bring their permit on the first working day. HR provides the wording before go-live, so that a Swiss citizen living abroad can see it does not apply to them. It collects no data.

| # | Country of residence | Nationality | → Result | Sources |
|---|---|---|---|---|
| 1 | Switzerland | Switzerland | no reminder | D-010 |
| 2 | Switzerland | other than Switzerland | reminder shown | D-010, F-hr_transcript-c53552 |
| 3 | any country other than Switzerland | - | reminder shown | D-010, D-038 |

_Status: decision · Sources: F-hr_transcript-c53552, D-010, D-038, D-050_

<a id="SEC-02-personal-details-address"></a>

## 2. Personal details and home address

Collect the employee's identity and the complete home address that applies on the first working day, plus the canton the pension fund needs.

| Story | Priority | Status |
|---|---|---|
| [US-02.1 – Collect the employee's name and date of birth](stories/US-02.1-collect-the-employee-s-name-and-date-of-birth.md) | P1 | decision |
| [US-02.2 – Collect a complete postal home address](stories/US-02.2-collect-a-complete-postal-home-address.md) | P2 | decision |
| [US-02.3 – Use the home address country as the country of residence](stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md) | P1 | decision |
| [US-02.4 – Ask Swiss residents for their canton](stories/US-02.4-ask-swiss-residents-for-their-canton.md) | P1 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### First name
| | |
|---|---|
| **What?** | The employee's first name, as needed to register the employee with the pension fund and for HR's records. |
| **When do we ask?** | Always (step 1 About you) |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'First name' of the registration form<br>HR: Identify the employee (HR asked for 'the basics, name, address') |
| **Status · sources** | confirmed · F-pension_portal-db702a, F-pension_portal-44a27b, F-hr_transcript-3edf89, D-047 |

#### Last name
| | |
|---|---|
| **What?** | The employee's last name. |
| **When do we ask?** | Always (step 1 About you) |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'Last name' of the registration form<br>HR: Identify the employee |
| **Status · sources** | confirmed · F-pension_portal-c688e4, F-pension_portal-44a27b, F-hr_transcript-3edf89, D-047 |

#### Date of birth
| | |
|---|---|
| **What?** | The employee's date of birth. – Form: Date in the format DD.MM.YYYY; the employee must be at least 14 and at most 100 years old on the first working day |
| **When do we ask?** | Always (step 1 About you) |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'Date of birth' of the registration form |
| **Status · sources** | confirmed · F-pension_portal-88b436, F-pension_portal-967bc9, F-pension_portal-44a27b, D-050, D-047 |

#### Street
| | |
|---|---|
| **What?** | Street of the employee's home address that applies on the first working day. – Form: Part of a normal postal address as written on an envelope |
| **When do we ask?** | Always (step 2 Home address) |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee; the address must be complete |
| **Status · sources** | confirmed · F-hr_transcript-3beee8, F-hr_transcript-c0fe95, F-hr_transcript-66fe15, D-041, D-049, D-047 |

#### House number
| | |
|---|---|
| **What?** | House number of the home address on the first working day. An explicit 'no house number' option covers addresses without one. – Form: Part of a normal postal address; the option 'no house number' may be chosen instead |
| **When do we ask?** | Always (step 2 Home address) |
| **When is it required?** | Always (a number or 'no house number') |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee; HR wants the address complete including the number |
| **Status · sources** | decision · F-hr_transcript-c0fe95, F-hr_transcript-3beee8, D-042, D-049 |

#### Postcode
| | |
|---|---|
| **What?** | Postcode of the home address on the first working day. – Form: Part of a normal postal address |
| **When do we ask?** | Always (step 2 Home address) |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee |
| **Status · sources** | confirmed · F-hr_transcript-c0fe95, F-hr_transcript-3beee8, D-041, D-049 |

#### Town
| | |
|---|---|
| **What?** | Town of the home address on the first working day. – Form: Part of a normal postal address |
| **When do we ask?** | Always (step 2 Home address) |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Post documents to the employee |
| **Status · sources** | confirmed · F-hr_transcript-c0fe95, F-hr_transcript-3beee8, D-041, D-049 |

#### Country of residence (home address country)
| | |
|---|---|
| **What?** | Country of the employee's home address on the first working day. It is the employee's country of residence and decides whether the employee lives in Switzerland or abroad (source tax liability, cross-border questions, canton, permit reminder). The calculator's questions 'main residence in Switzerland?' and 'country of residence' are derived from it, not asked again. – Form: Chosen from the ISO 3166 country list (English names, e.g. Switzerland, Germany, Liechtenstein) |
| **When do we ask?** | Always (step 2 Home address) |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Complete postal address<br>source tax office: Employees living abroad are always subject to source tax; residence block of the tariff calculator<br>pension fund: Decides whether the canton is the canton of residence or of the place of work |
| **Status · sources** | confirmed · F-hr_transcript-c0fe95, F-hr_transcript-ab3cba, F-hr_transcript-5af8d0, F-zh_source_tax_calculator-aedb40, F-zh_source_tax_calculator-4c65ae, G-08, G-09, D-041, D-049, D-050 |

#### Canton of residence
| | |
|---|---|
| **What?** | The Swiss canton the employee lives in on the first working day, for the pension fund's 'Canton' field. Not asked of employees living abroad; for them the canton of the place of work (Zurich) is used (assumption D-002). |
| **Allowed values** | Aargau · Appenzell Ausserrhoden · Appenzell Innerrhoden · Basel-Landschaft · Basel-Stadt · Bern · Fribourg · Geneva · Glarus · Graubünden · Jura · Lucerne · Neuchâtel · Nidwalden · Obwalden · Schaffhausen · Schwyz · Solothurn · St. Gallen · Thurgau · Ticino · Uri · Valais · Vaud · Zug · Zurich |
| **When do we ask?** | Only if the employee lives in Switzerland (step 2 Home address) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country) |
| **Who needs it?** | pension fund: Required field 'Canton' of the registration form |
| **Status · sources** | decision · F-pension_portal-6c621f, F-pension_portal-3432a9, F-pension_portal-b359c3, F-pension_portal-44a27b, D-002, D-047 |

### Business rules in this section

#### Canton for the pension fund
Employees living in Switzerland: the canton they chose. Employees living abroad: the canton of the place of work, Zurich for Muster AG, not asked (assumption D-002).

| # | Country of residence | Canton of residence | → Result | Sources |
|---|---|---|---|---|
| 1 | Switzerland | any canton | the chosen canton | D-002, F-pension_portal-3432a9 |
| 2 | any country other than Switzerland | - | Zurich | D-002 |

_Status: decision · Sources: F-pension_portal-6c621f, F-pension_portal-b359c3, D-002_

<a id="SEC-03-employment-start"></a>

## 3. First working day and insurance start date

Ask the employee for the contractual first working day and derive the pension fund insurance start date from it.

| Story | Priority | Status |
|---|---|---|
| [US-03.1 – Employee confirms the first working day](stories/US-03.1-employee-confirms-the-first-working-day.md) | P1 | decision |
| [US-03.2 – Derive the pension insurance start date from the first working day](stories/US-03.2-derive-the-pension-insurance-start-date-from-the-first.md) | P1 | confirmed |
| [US-03.3 – Re-derive the insurance start date when the first working day moves](stories/US-03.3-re-derive-the-insurance-start-date-when-the-first-working.md) | P1 | inferred |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### First working day
| | |
|---|---|
| **What?** | The contractual start date of employment, entered and confirmed by the employee, even if it falls on a weekend or public holiday. After submission only HR can change it; the latest date always counts and no history is kept. It is the reference date for the insurance start, the home address and the children's age. – Form: Date in the format DD.MM.YYYY; must lie within one year after the questionnaire is sent |
| **When do we ask?** | Always (step 1 About you) |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Derive the insurance start date (HR: 'the number one thing')<br>HR: Start of employment; HR makes later changes |
| **Status · sources** | decision · F-hr_transcript-872bd7, F-hr_transcript-e3721e, F-hr_transcript-e18e66, G-08, G-10, D-033, D-039, D-041, D-044, D-050, D-047 |

### Business rules in this section

#### Insurance start date
The pension fund insurance start date is derived from the first working day only: if the first working day is the 1st of a month, insurance starts that day; otherwise on the 1st of the following month. It is always derived again from the latest first working day.

| # | First working day | → Result | Sources |
|---|---|---|---|
| 1 | is the 1st of a month | the first working day itself | F-hr_transcript-1d5c07, F-hr_transcript-fdf50a |
| 2 | any other day | the 1st of the following month | F-hr_transcript-1d5c07, F-hr_transcript-30d25c |

_Status: confirmed · Sources: F-hr_transcript-1d5c07, F-hr_transcript-e18e66, F-pension_portal-509cbe, F-pension_portal-dd8126, F-pension_portal-3a97ab, G-08, D-033, D-037, D-039_

<a id="SEC-04-civil-status-spouse"></a>

## 4. Civil status and spouse data

Ask the civil status of every employee and the spouse's or partner's date of birth where the fund needs it, and convert the civil status to the pension fund's list and to the calculator's two groups.

| Story | Priority | Status |
|---|---|---|
| [US-04.1 – Ask every employee for their civil status](stories/US-04.1-ask-every-employee-for-their-civil-status.md) | P1 | decision |
| [US-04.2 – Ask for the spouse's or registered partner's date of birth when the fund registers the employee as Married](stories/US-04.2-ask-for-the-spouse-s-or-registered-partner-s-date-of-birth.md) | P1 | decision |
| [US-04.3 – Answer the calculator's civil status question from the employee's civil status](stories/US-04.3-answer-the-calculator-s-civil-status-question-from-the.md) | P1 | decision |
| [US-04.4 – Enter the civil status on the pension fund's list](stories/US-04.4-enter-the-civil-status-on-the-pension-fund-s-list.md) | P1 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Civil status
| | |
|---|---|
| **What?** | The employee's civil status. Asked of everyone, wherever they live. Mapped to the pension fund's list and to the calculator's two groups (assumption D-003). |
| **Allowed values** | Single · Married · Divorced · Widowed · Registered partnership · Separated |
| **When do we ask?** | Always (step 4 Civil status and spouse) |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'Civil status'; Married triggers the spouse's date of birth<br>source tax office: Spouse exemption and calculator civil status group (tariff A/H vs B/C) |
| **Status · sources** | decision · F-hr_transcript-ce8ca4, F-hr_transcript-bd8c8e, F-hr_transcript-3907fe, F-hr_transcript-f197d6, F-pension_portal-8664f4, F-pension_portal-3d1ae4, F-zh_source_tax_calculator-9007c3, F-zh_source_tax_calculator-051bb9, G-10, D-003, D-047 |

#### Spouse's or registered partner's date of birth
| | |
|---|---|
| **What?** | Date of birth of the spouse or registered partner. Asked of married, registered-partner and separated employees, who are all entered at the fund as Married; not asked of divorced or widowed employees (assumption D-004). – Form: Date in the format DD.MM.YYYY |
| **When do we ask?** | Only if the employee is married, in a registered partnership or separated (step 4) |
| **When is it required?** | Whenever asked |
| **Depends on** | Civil status |
| **Who needs it?** | pension fund: 'Spouse's date of birth' is required when Civil status is Married |
| **Status · sources** | decision · F-hr_transcript-2334d8, F-pension_portal-a0065b, F-pension_portal-ef28c3, F-pension_portal-39bab1, F-pension_portal-c5ee15, F-pension_portal-6d3630, F-hr_transcript-f197d6, D-003, D-004 |

### Business rules in this section

#### Civil status for the pension fund
The fund only accepts Single, Married, Divorced and Widowed. Registered partnership and Separated are entered as Married (with the spouse's/partner's date of birth); the other values are entered as they are (assumption D-003).

| # | Civil status | → Result | Sources |
|---|---|---|---|
| 1 | Single | Single | F-pension_portal-3d1ae4 |
| 2 | Married | Married | F-pension_portal-3d1ae4 |
| 3 | Divorced | Divorced | F-pension_portal-3d1ae4 |
| 4 | Widowed | Widowed | F-pension_portal-3d1ae4 |
| 5 | Registered partnership | Married | D-003 |
| 6 | Separated | Married | D-003 |

_Status: decision · Sources: F-pension_portal-3d1ae4, F-hr_transcript-f197d6, D-003, D-004_

#### Civil status group for source tax
For source tax, Married and Registered partnership count as 'married or registered partnership'; Single, Divorced, Widowed and Separated count as 'single, divorced, separated or widowed', as in the calculator.

| # | Civil status | → Result | Sources |
|---|---|---|---|
| 1 | Married or Registered partnership | Married or registered partnership | F-zh_source_tax_calculator-051bb9, D-003 |
| 2 | Single, Divorced, Widowed or Separated | Single, divorced, separated or widowed | F-zh_source_tax_calculator-051bb9, D-003 |

_Status: decision · Sources: F-zh_source_tax_calculator-051bb9, D-003_

<a id="SEC-05-source-tax-liability"></a>

## 5. Who is subject to source tax

Ask only what HR's rule needs (nationality, C permit, and the spouse's nationality, C permit and whether the spouse lives in Switzerland) to decide whether the employee is subject to source tax.

| Story | Priority | Status |
|---|---|---|
| [US-05.1 – Ask nationality and C permit only of employees living in Switzerland](stories/US-05.1-ask-nationality-and-c-permit-only-of-employees-living-in.md) | P1 | decision |
| [US-05.2 – Ask the spouse's nationality, C permit and residence only when they can exempt the employee](stories/US-05.2-ask-the-spouse-s-nationality-c-permit-and-residence-only.md) | P1 | inferred |
| [US-05.3 – Decide whether the employee is subject to source tax](stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md) | P1 | decision |
| [US-05.4 – Derive the calculator's residence from the home address country](stories/US-05.4-derive-the-calculator-s-residence-from-the-home-address.md) | P2 | inferred |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Nationality
| | |
|---|---|
| **What?** | The employee's nationality. Anyone with Swiss citizenship counts as Swiss, even with another nationality, and chooses Switzerland. Only asked of employees living in Switzerland; employees living abroad are subject to source tax whatever their passport. – Form: Chosen from the ISO 3166 country list, plus 'stateless' |
| **When do we ask?** | Only if the employee lives in Switzerland (step 3) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country) |
| **Who needs it?** | source tax office: Swiss citizens living in Switzerland are not subject to source tax<br>HR: Decide whether the permit reminder applies |
| **Status · sources** | decision · F-hr_transcript-35fae3, F-hr_transcript-5af8d0, F-hr_transcript-3f2c2a, G-01, D-008, D-010, D-038, D-047, D-050 |

#### Holds a C permit
| | |
|---|---|
| **What?** | Whether a non-Swiss employee living in Switzerland holds a C permit (permanent residence). No other permit type is asked. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Switzerland and is not Swiss (step 3) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Nationality |
| **Who needs it?** | source tax office: C-permit holders are treated like Swiss people and are not subject to source tax |
| **Status · sources** | decision · F-hr_transcript-845204, F-hr_transcript-c9d9b9, F-hr_transcript-5af8d0, G-01, D-005, D-047 |

#### Spouse's nationality
| | |
|---|---|
| **What?** | Nationality of the spouse or registered partner, to check the spouse exemption from source tax. A spouse with Swiss citizenship counts as Swiss. – Form: Chosen from the ISO 3166 country list, plus 'stateless' |
| **When do we ask?** | Only if the employee lives in Switzerland, is not Swiss, has no C permit and is married or in a registered partnership (step 4) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Civil status, Holds a C permit, Nationality |
| **Who needs it?** | source tax office: Being married to a Swiss national living in Switzerland exempts the employee |
| **Status · sources** | inferred · F-hr_transcript-f3ce84, F-hr_transcript-b90bd9, F-hr_transcript-5af8d0, F-hr_transcript-54d011, F-hr_transcript-a45422, G-01, D-003, D-008, D-050 |

#### Spouse holds a C permit
| | |
|---|---|
| **What?** | Whether a non-Swiss spouse or registered partner holds a C permit. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the spouse's nationality is asked and the spouse is not Swiss (step 4) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Civil status, Holds a C permit, Nationality, Spouse's nationality |
| **Who needs it?** | source tax office: Being married to a C-permit holder living in Switzerland exempts the employee |
| **Status · sources** | inferred · F-hr_transcript-76eacc, F-hr_transcript-b90bd9, F-hr_transcript-5af8d0, F-hr_transcript-54d011, D-005 |

#### Spouse lives in Switzerland
| | |
|---|---|
| **What?** | Whether the spouse or registered partner lives in Switzerland ('here' in HR's wording). Asked as yes/no, not as a country. |
| **Allowed values** | yes · no |
| **When do we ask?** | Same as the spouse's nationality (step 4) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Civil status, Holds a C permit, Nationality |
| **Who needs it?** | source tax office: The spouse exemption applies only if the Swiss or C-permit spouse lives in Switzerland |
| **Status · sources** | inferred · F-hr_transcript-e5337d, F-hr_transcript-b90bd9, F-hr_transcript-5af8d0, F-hr_transcript-54d011, D-043, D-050 |

### Business rules in this section

#### Subject to source tax
An employee living abroad is subject to source tax whatever their nationality. An employee living in Switzerland is subject only if not Swiss, without a C permit, and not married to (or in a registered partnership with) a Swiss national or C-permit holder who lives in Switzerland. Separated counts as single. 'Here' in HR's wording means Switzerland (assumption D-043).

| # | Country of residence | Nationality | Holds a C permit | Civil status | Spouse lives in Switzerland | Spouse Swiss or holds a C permit | → Result | Sources |
|---|---|---|---|---|---|---|---|---|
| 1 | any country other than Switzerland | - | - | any | - | - | subject to source tax | F-hr_transcript-3f2c2a, F-hr_transcript-5af8d0 |
| 2 | Switzerland | Switzerland | - | any | - | - | not subject | F-hr_transcript-b0527c, F-hr_transcript-5af8d0, D-008 |
| 3 | Switzerland | other than Switzerland | yes | any | - | - | not subject | F-hr_transcript-845204, F-hr_transcript-5af8d0 |
| 4 | Switzerland | other than Switzerland | no | Single, Divorced, Widowed or Separated | - | - | subject to source tax | F-hr_transcript-5af8d0, D-003 |
| 5 | Switzerland | other than Switzerland | no | Married or Registered partnership | yes | yes | not subject | F-hr_transcript-b90bd9, F-hr_transcript-5af8d0, D-003 |
| 6 | Switzerland | other than Switzerland | no | Married or Registered partnership | yes | no | subject to source tax | F-hr_transcript-5af8d0 |
| 7 | Switzerland | other than Switzerland | no | Married or Registered partnership | no | any | subject to source tax | F-hr_transcript-5af8d0 |

_Status: decision · Sources: F-hr_transcript-5af8d0, F-hr_transcript-b84498, F-hr_transcript-845204, F-hr_transcript-b90bd9, F-hr_transcript-3f2c2a, D-003, D-008, D-043_

<a id="SEC-08-cross-border-residence"></a>

## 6. Source tax: residence abroad and cross-border questions

For employees living in Germany or Liechtenstein, ask the cross-border questions to decide between the cross-border tariff, the normal tariff and 'in principle no source tax liability' for Liechtenstein, including the separate note on the double taxation agreement.

| Story | Priority | Status |
|---|---|---|
| [US-08.1 – Derive the calculator's residence answers from the home address and ask cross-border questions only of Germany and Liechtenstein residents](stories/US-08.1-derive-the-calculator-s-residence-answers-from-the-home.md) | P1 | inferred |
| [US-08.2 – Germany: daily return and certificate of residence](stories/US-08.2-germany-daily-return-and-certificate-of-residence.md) | P1 | decision |
| [US-08.3 – Germany: no daily return - reasonableness and more than 60 non-return days](stories/US-08.3-germany-no-daily-return-reasonableness-and-more-than-60-non.md) | P1 | decision |
| [US-08.4 – Liechtenstein: daily return and more than 45 non-return days](stories/US-08.4-liechtenstein-daily-return-and-more-than-45-non-return-days.md) | P1 | decision |
| [US-08.5 – Liechtenstein: record the double taxation agreement note next to the plain tariff code](stories/US-08.5-liechtenstein-record-the-double-taxation-agreement-note-next.md) | P2 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Daily return to Liechtenstein
| | |
|---|---|
| **What?** | Whether the employee living in Liechtenstein returns daily to the main residence in Liechtenstein, as expected for the year. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Liechtenstein (step 5, before denomination, spouse and children) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country) |
| **Who needs it?** | source tax office: Daily return means in principle no source tax liability (subject to the DTA) |
| **Status · sources** | decision · F-zh_source_tax_calculator-981b6b, F-zh_source_tax_calculator-a2041b, F-zh_source_tax_calculator-e22d17, F-zh_source_tax_calculator-fb87f1, F-hr_transcript-8595fb, D-001, D-007, D-035, D-040, D-047 |

#### More than 45 non-return days (Liechtenstein)
| | |
|---|---|
| **What?** | Whether the employee living in Liechtenstein without daily return expects more than 45 work-related non-return days in the calendar year. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Liechtenstein and does not return daily (step 5) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Daily return to Liechtenstein |
| **Who needs it?** | source tax office: More than 45 days gives the normal tariff with the DTA reservation; otherwise in principle no liability |
| **Status · sources** | decision · F-zh_source_tax_calculator-e96210, F-zh_source_tax_calculator-0ff846, F-zh_source_tax_calculator-f4ece9, F-zh_source_tax_calculator-cc19c7, D-007, D-035, D-040 |

#### Daily return to Germany
| | |
|---|---|
| **What?** | Whether the employee living in Germany returns daily to the main residence in Germany, as expected for the year. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Germany (step 5) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country) |
| **Who needs it?** | source tax office: Decides between cross-border (L/M/N/P) and normal tariff |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-69edd5, F-zh_source_tax_calculator-64ac42, F-zh_source_tax_calculator-31d762, F-hr_transcript-8595fb, D-001, D-035, D-047 |

#### Certificate of residence
| | |
|---|---|
| **What?** | Whether the employee living in Germany who returns daily has a certificate of residence (Ansässigkeitsbescheinigung) for HR. 'Not yet' is a valid answer and counts as 'no' for the tariff code. The document goes to HR outside Lonio; no upload. |
| **Allowed values** | yes · no · not yet |
| **When do we ask?** | Only if the employee lives in Germany and returns daily (step 5) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Daily return to Germany |
| **Who needs it?** | source tax office: With a certificate the cross-border tariff applies, without it the normal tariff<br>HR: Collect the certificate outside Lonio |
| **Status · sources** | decision · F-zh_source_tax_calculator-687e8b, F-zh_source_tax_calculator-823151, F-zh_source_tax_calculator-5f6820, F-zh_source_tax_calculator-993db3, D-035, D-037 |

#### Daily return reasonable
| | |
|---|---|
| **What?** | For an employee living in Germany without daily return: whether a daily return would in principle be reasonable (less than 100 km driving distance). |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Germany and does not return daily (step 5) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Daily return to Germany |
| **Who needs it?** | source tax office: Not reasonable gives the normal tariff |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-d2b3cf, F-zh_source_tax_calculator-087ae5, F-zh_source_tax_calculator-aaece6, F-zh_source_tax_calculator-c8aa5e |

#### More than 60 non-return days (Germany)
| | |
|---|---|
| **What?** | For an employee living in Germany without daily return although it would be reasonable: whether they expect more than 60 work-related non-return days in the calendar year (a declaration, not proof). |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Germany, does not return daily and daily return is reasonable (step 5) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Daily return to Germany, Daily return reasonable |
| **Who needs it?** | source tax office: More than 60 days gives the normal tariff, otherwise the cross-border tariff |
| **Status · sources** | decision · F-zh_source_tax_calculator-e8ffac, F-zh_source_tax_calculator-ea3cd8, F-zh_source_tax_calculator-33ef31, F-zh_source_tax_calculator-c8aa5e, D-035 |

### Business rules in this section

#### Residence for the tariff calculation
The calculator's residence answers are derived from the home address country instead of being asked again: Switzerland, Germany, Liechtenstein or another country. Switzerland and other countries give the base tariff without further residence questions.

| # | Country of residence | → Result | Sources |
|---|---|---|---|
| 1 | Switzerland | Switzerland (base tariff) | F-zh_source_tax_calculator-f86c6b |
| 2 | Germany | Germany (cross-border questions) | F-zh_source_tax_calculator-d62dd4 |
| 3 | Liechtenstein | Liechtenstein (cross-border questions) | F-zh_source_tax_calculator-d62dd4 |
| 4 | any other country | Other country (base tariff) | F-zh_source_tax_calculator-f86c6b |

_Status: inferred · Sources: F-zh_source_tax_calculator-aedb40, F-zh_source_tax_calculator-4c65ae, F-zh_source_tax_calculator-d62dd4, F-zh_source_tax_calculator-f86c6b, G-01, G-08_

#### Liechtenstein resident in principle not liable
An employee living in Liechtenstein who returns daily, or who does not return daily but expects at most 45 non-return days, is in principle not liable to source tax, subject to the double taxation agreement. Lonio shows this instead of a tariff code, flags it for HR and skips the remaining tariff questions.

| # | Country of residence | Daily return to Liechtenstein | More than 45 non-return days | → Result | Sources |
|---|---|---|---|---|---|
| 1 | Liechtenstein | yes | - | in principle no source tax liability (flagged for HR) | F-zh_source_tax_calculator-fb87f1 |
| 2 | Liechtenstein | no | no | in principle no source tax liability (flagged for HR) | F-zh_source_tax_calculator-fb87f1 |
| 3 | Liechtenstein | no | yes | normal tariff code | F-zh_source_tax_calculator-cc19c7, D-054 |
| 4 | any country other than Liechtenstein | - | - | does not apply | F-zh_source_tax_calculator-e22d17 |

_Status: decision · Sources: F-zh_source_tax_calculator-fb87f1, D-007, D-034, D-040_

#### Double taxation agreement note (Liechtenstein)
For an employee living in Liechtenstein without daily return and with more than 45 non-return days, the plain tariff code is recorded and the note 'subject to the double taxation agreement' is recorded separately next to it and flagged for HR; the note is not part of the code.

| # | Country of residence | Daily return to Liechtenstein | More than 45 non-return days | → Result | Sources |
|---|---|---|---|---|---|
| 1 | Liechtenstein | no | yes | note recorded and flagged for HR | F-zh_source_tax_calculator-cc19c7, D-054 |
| 2 | Liechtenstein | yes | - | no separate note (in principle not liable) | D-007 |
| 3 | Liechtenstein | no | no | no separate note (in principle not liable) | D-007 |
| 4 | any country other than Liechtenstein | - | - | no note | F-zh_source_tax_calculator-cc19c7 |

_Status: decision · Sources: F-zh_source_tax_calculator-cc19c7, D-040, D-054, D-034_

#### Cross-border (Grenzgänger) tariff applies
For an employee living in Germany the cross-border tariff applies if they return daily and have a certificate of residence ('not yet' counts as no), or if they do not return daily, daily return would be reasonable and they do not expect more than 60 non-return days. Otherwise the normal tariff applies.

| # | Country of residence | Daily return to Germany | Certificate of residence | Daily return reasonable | More than 60 non-return days | → Result | Sources |
|---|---|---|---|---|---|---|---|
| 1 | Germany | yes | yes | - | - | cross-border tariff | F-zh_source_tax_calculator-993db3 |
| 2 | Germany | yes | no or not yet | - | - | normal tariff | F-zh_source_tax_calculator-993db3, D-035 |
| 3 | Germany | no | - | no | - | normal tariff | F-zh_source_tax_calculator-c8aa5e |
| 4 | Germany | no | - | yes | yes | normal tariff | F-zh_source_tax_calculator-c8aa5e |
| 5 | Germany | no | - | yes | no | cross-border tariff | F-zh_source_tax_calculator-c8aa5e |
| 6 | any country other than Germany | - | - | - | - | normal tariff | F-zh_source_tax_calculator-f86c6b |

_Status: decision · Sources: F-zh_source_tax_calculator-993db3, F-zh_source_tax_calculator-c8aa5e, D-001, D-035_

<a id="SEC-06-source-tax-tariff-basics"></a>

## 7. Source tax tariff: denomination, spouse employment and tariff code

Ask the denomination, whether the spouse or partner is gainfully employed and whether the employee has children, then compute the full Zurich tariff code (letter, child digit and church-tax suffix) or the result shown when no code applies.

> ⚠ Open questions affecting this section: [OQ-calculator-coverage](open-questions.md#oq-calculator-coverage)
| Story | Priority | Status |
|---|---|---|
| [US-06.2 – Ask the religious denomination only where source tax needs it and derive the church-tax suffix](stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md) | P1 | decision |
| [US-06.3 – Ask married employees and registered partners subject to source tax whether their spouse or partner works](stories/US-06.3-ask-married-employees-and-registered-partners-subject-to.md) | P1 | decision |
| [US-06.7 – Ask employees subject to source tax whether they have children](stories/US-06.7-ask-employees-subject-to-source-tax-whether-they-have.md) | P1 | decision |
| [US-06.4 – Derive the base source tax tariff letter](stories/US-06.4-derive-the-base-source-tax-tariff-letter.md) | P1 | inferred |
| [US-06.5 – Replace the base letter with the cross-border letter where the cross-border tariff applies](stories/US-06.5-replace-the-base-letter-with-the-cross-border-letter-where.md) | P1 | decision |
| [US-06.6 – Compute and record the full source tax tariff code](stories/US-06.6-compute-and-record-the-full-source-tax-tariff-code.md) | P1 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Denomination
| | |
|---|---|
| **What?** | The employee's religious denomination, which sets the church-tax suffix of the tariff code. |
| **Allowed values** | Roman Catholic, Christ Catholic or Evangelical Reformed · None or other |
| **When do we ask?** | Only if the employee is subject to source tax, except Liechtenstein residents who are in principle not liable (step 6) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), More than 45 non-return days (Liechtenstein), Subject to source tax |
| **Who needs it?** | source tax office: Church-tax suffix Y or N |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-208104, F-zh_source_tax_calculator-b7fea8, F-zh_source_tax_calculator-b05b44, F-zh_source_tax_calculator-2eab9a, F-hr_transcript-b84498, D-001, D-040, D-047 |

#### Spouse gainfully employed
| | |
|---|---|
| **What?** | Whether the spouse or registered partner is gainfully employed or receives replacement income. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if source tax details are asked and the employee is married or in a registered partnership (step 6) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Civil status, More than 45 non-return days (Liechtenstein), Subject to source tax |
| **Who needs it?** | source tax office: Yes gives tariff C, no gives tariff B |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-7b637b, F-zh_source_tax_calculator-e740d1, F-zh_source_tax_calculator-0137bf, F-zh_source_tax_calculator-97139a, F-hr_transcript-6a0a40, D-003, D-047 |

#### Has children
| | |
|---|---|
| **What?** | Whether the employee (or, for married/registered partners, either spouse/partner) has biological or adopted children. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if source tax details are asked (step 6) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), More than 45 non-return days (Liechtenstein), Subject to source tax |
| **Who needs it?** | source tax office: Opens the child blocks for the child digit and tariff H |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-103b19, F-zh_source_tax_calculator-a166c7, F-zh_source_tax_calculator-a33b65, F-zh_source_tax_calculator-ab8a06, F-zh_source_tax_calculator-b62b85, F-zh_source_tax_calculator-75cd87, D-047 |

### Business rules in this section

#### Church-tax suffix
Roman Catholic, Christ Catholic or Evangelical Reformed gives the suffix Y; none or other gives N.

| # | Denomination | → Result | Sources |
|---|---|---|---|
| 1 | Roman Catholic, Christ Catholic or Evangelical Reformed | Y | F-zh_source_tax_calculator-2eab9a |
| 2 | None or other | N | F-zh_source_tax_calculator-2eab9a |

_Status: confirmed · Sources: F-zh_source_tax_calculator-2eab9a, D-001_

#### Base tariff letter
Married or registered partnership: C if the spouse/partner is gainfully employed (or receives replacement income), otherwise B. Single, divorced, separated or widowed: H if any child is counted with H, otherwise A. Earned income is always assumed, so G does not occur (D-006).

| # | Civil status group | Spouse gainfully employed | Any child counted with H | → Result | Sources |
|---|---|---|---|---|---|
| 1 | Married or registered partnership | yes | any | C | F-zh_source_tax_calculator-97139a |
| 2 | Married or registered partnership | no | any | B | F-zh_source_tax_calculator-97139a |
| 3 | Single, divorced, separated or widowed | - | yes | H | F-zh_source_tax_calculator-300c72 |
| 4 | Single, divorced, separated or widowed | - | no | A | F-zh_source_tax_calculator-037b1c |

_Status: confirmed · Sources: F-zh_source_tax_calculator-97139a, F-zh_source_tax_calculator-037b1c, F-zh_source_tax_calculator-300c72, D-001, D-006_

#### Tariff letter
When the cross-border tariff applies, the base letter is replaced: A by L, B by M, C by N, H by P (and G by Q, which cannot occur for onboarding). Otherwise the base letter is used.

| # | Base tariff letter | Cross-border tariff applies | → Result | Sources |
|---|---|---|---|---|
| 1 | any | no | the base letter | F-zh_source_tax_calculator-993db3 |
| 2 | A | yes | L | F-zh_source_tax_calculator-993db3 |
| 3 | B | yes | M | F-zh_source_tax_calculator-993db3 |
| 4 | C | yes | N | F-zh_source_tax_calculator-993db3 |
| 5 | H | yes | P | F-zh_source_tax_calculator-993db3 |
| 6 | G | yes | Q | F-zh_source_tax_calculator-993db3, D-051 |

_Status: confirmed · Sources: F-zh_source_tax_calculator-993db3, F-zh_source_tax_calculator-c8aa5e, D-051_

#### Full source tax tariff code
Lonio computes the full Zurich tariff code as one text: tariff letter, number of counted children and church-tax suffix (e.g. 'C1Y', 'L0Y'). Not subject to source tax: 'no tariff code'. Liechtenstein resident in principle not liable: 'in principle no source tax liability, subject to the double taxation agreement', flagged for HR. When answers needed for the code are missing (e.g. after an HR change made new questions apply): 'incomplete - HR must complete'. Always derived again from the latest answers.

| # | Subject to source tax | Liechtenstein in principle not liable | Tariff letter | Number of counted children | Church-tax suffix | → Result | Sources |
|---|---|---|---|---|---|---|---|
| 1 | no | - | - | - | - | no tariff code | D-051, F-hr_transcript-5af8d0 |
| 2 | yes | yes | - | - | - | in principle no source tax liability, subject to the double taxation agreement (flagged for HR) | D-007, F-zh_source_tax_calculator-fb87f1 |
| 3 | yes | no | not determined | any | any | incomplete - HR must complete | D-048, D-053 |
| 4 | yes | no | any | any | not determined | incomplete - HR must complete | D-048, D-053 |
| 5 | yes | no | letter | number | Y or N | letter + number + suffix, e.g. C1Y, N1Y, A0N, H1Y | F-zh_source_tax_calculator-4c53e3, F-zh_source_tax_calculator-993db3, D-051, D-054 |

_Status: decision · Sources: D-001, D-007, D-037, D-048, D-051, D-052, D-053, D-054, F-hr_transcript-34494f, F-zh_source_tax_calculator-2eab9a, F-zh_source_tax_calculator-4c53e3, F-zh_source_tax_calculator-993db3, F-zh_source_tax_calculator-cc19c7, F-zh_source_tax_calculator-fb87f1_

<a id="SEC-07-source-tax-children"></a>

## 8. Source tax tariff: children

Ask one block of questions per child (no maximum, age judged on the first working day) to decide whether each child counts, whether tariff H applies and what the child digit is.

| Story | Priority | Status |
|---|---|---|
| [US-07.1 – Ask about children only of employees who need a source tax tariff](stories/US-07.1-ask-about-children-only-of-employees-who-need-a-source-tax.md) | P1 | decision |
| [US-07.2 – One block per child: age status and household](stories/US-07.2-one-block-per-child-age-status-and-household.md) | P1 | decision |
| [US-07.3 – Minor child living in the employee's household](stories/US-07.3-minor-child-living-in-the-employee-s-household.md) | P1 | inferred |
| [US-07.4 – Minor child not living in the employee's household](stories/US-07.4-minor-child-not-living-in-the-employee-s-household.md) | P1 | inferred |
| [US-07.5 – Adult child in first education](stories/US-07.5-adult-child-in-first-education.md) | P1 | inferred |
| [US-07.6 – Child digit of the tariff code and go-live check of the child paths](stories/US-07.6-child-digit-of-the-tariff-code-and-go-live-check-of-the.md) | P1 | inferred |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Child: minor or adult in first education
| | |
|---|---|
| **What?** | Per child: whether the child is a minor, an adult in first education, or neither, judged on the first working day. There is no maximum number of children; one block per child. – Form: One block per child |
| **Allowed values** | Minor · Adult in first education · Neither |
| **When do we ask?** | For each child, if the employee has children (step 7) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Has children, More than 45 non-return days (Liechtenstein), Subject to source tax |
| **Who needs it?** | source tax office: 'Neither' does not count; decides the following child questions |
| **Status · sources** | decision · F-zh_source_tax_calculator-640429, F-zh_source_tax_calculator-09b06d, F-zh_source_tax_calculator-6bed1f, F-zh_source_tax_calculator-fd9a15, F-zh_source_tax_calculator-abe889, D-044, D-047 |

#### Child lives in the same household
| | |
|---|---|
| **What?** | Per child: whether the child lives in the employee's household. |
| **Allowed values** | yes · no |
| **When do we ask?** | Per child, if the child is a minor or an adult in first education |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Child: minor or adult in first education, Has children, More than 45 non-return days (Liechtenstein), Subject to source tax |
| **Who needs it?** | source tax office: Per-child result |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-5725a8, F-zh_source_tax_calculator-3a75cc, F-zh_source_tax_calculator-7c667f |

#### Child: parental custody (shared or sole)
| | |
|---|---|
| **What?** | Per minor child in the household: whether parental custody is shared or sole. |
| **Allowed values** | Shared custody · Sole custody |
| **When do we ask?** | Per child, if the child is a minor living in the household |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Child: minor or adult in first education, Child lives in the same household, Has children, More than 45 non-return days (Liechtenstein), Subject to source tax |
| **Who needs it?** | source tax office: Sole custody counts the child (H for single persons) |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-4b7063, F-zh_source_tax_calculator-c09dc1, F-zh_source_tax_calculator-83de1d |

#### Common household with the other parent
| | |
|---|---|
| **What?** | Per child: whether the employee lives in a common household with the child's other parent. |
| **Allowed values** | yes · no |
| **When do we ask?** | Per child in the household that is either a minor with shared custody or an adult in first education |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Child: minor or adult in first education, Child: parental custody (shared or sole), Child lives in the same household, Has children, More than 45 non-return days (Liechtenstein), Subject to source tax |
| **Who needs it?** | source tax office: Per-child result |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-d79949, F-zh_source_tax_calculator-e72e42, F-zh_source_tax_calculator-6dcf5c |

#### Child: shared custody (married, child not in household)
| | |
|---|---|
| **What?** | Per minor child not in the household of a married employee or registered partner: whether custody is shared. |
| **Allowed values** | yes · no |
| **When do we ask?** | Per child, if the employee is married or in a registered partnership and the child is a minor not in the household |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Civil status group for source tax, Child: minor or adult in first education, Child lives in the same household, Has children, More than 45 non-return days (Liechtenstein), Subject to source tax |
| **Who needs it?** | source tax office: Without shared custody the child does not count |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-fe0305, F-zh_source_tax_calculator-d2e516, F-zh_source_tax_calculator-7dcce6, D-003 |

#### Child: parental care (non-married, child not in household)
| | |
|---|---|
| **What?** | Per minor child not in the household of a single, divorced, separated or widowed employee: whether the employee has parental care. |
| **Allowed values** | yes · no |
| **When do we ask?** | Per child, if the employee is single, divorced, separated or widowed and the child is a minor not in the household |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Civil status group for source tax, Child: minor or adult in first education, Child lives in the same household, Has children, More than 45 non-return days (Liechtenstein), Subject to source tax |
| **Who needs it?** | source tax office: Without parental care the child does not count |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-956f07, F-zh_source_tax_calculator-32fec9, F-zh_source_tax_calculator-fb4a56, D-003 |

#### Child: alternating custody
| | |
|---|---|
| **What?** | Per minor child: whether there is alternating custody. |
| **Allowed values** | yes · no |
| **When do we ask?** | Per minor child: in the household with shared custody and no common household with the other parent; or not in the household with shared custody (married) or parental care (non-married) |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Civil status group for source tax, Child: minor or adult in first education, Common household with the other parent, Child: parental custody (shared or sole), Child: parental care (non-married, child not in household), Child lives in the same household, Child: shared custody (married, child not in household), Has children, More than 45 non-return days (Liechtenstein), Subject to source tax |
| **Who needs it?** | source tax office: Per-child result |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-da19df, F-zh_source_tax_calculator-ebd7b3, F-zh_source_tax_calculator-64ac33 |

#### Child: main financial contributor
| | |
|---|---|
| **What?** | Per child: who makes the larger financial contribution to the child's maintenance - the employee or the other parent. |
| **Allowed values** | Myself · Other parent |
| **When do we ask?** | Per child, if there is alternating custody, or if a single, divorced, separated or widowed employee lives with the child and the other parent in a common household |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Civil status group for source tax, Child: alternating custody, Common household with the other parent, Child lives in the same household, Has children, More than 45 non-return days (Liechtenstein), Subject to source tax |
| **Who needs it?** | source tax office: Being the main contributor counts the child (H for single persons) |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-cdd0b6, F-zh_source_tax_calculator-939b3b, F-zh_source_tax_calculator-ad867a |

#### Child: more than 50% of maintenance provided
| | |
|---|---|
| **What?** | Per adult child in first education: whether the employee mainly (more than 50%) provides for the child's maintenance. |
| **Allowed values** | yes · no |
| **When do we ask?** | Per adult child in first education that does not live in the household, or lives in it without a common household with the other parent |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of residence (home address country), Child: minor or adult in first education, Common household with the other parent, Child lives in the same household, Has children, More than 45 non-return days (Liechtenstein), Subject to source tax |
| **Who needs it?** | source tax office: Per-child result |
| **Status · sources** | confirmed · F-zh_source_tax_calculator-b008fe, F-zh_source_tax_calculator-cb54d9, F-zh_source_tax_calculator-cd1015 |

### Business rules in this section

#### Per-child result
Each child block yields one result: counted, counted with H (single, divorced, separated or widowed employees only) or not counted. Observed calculator results win over the general rule (D-046); rows marked inferred are checked against the calculator before go-live (D-009).

| # | Civil status group | Child age status | Same household | Custody | Common household with other parent | Shared custody (married, not in household) | Parental care (non-married, not in household) | Alternating custody | Main financial contributor | More than 50% of maintenance | → Result | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | any | Neither | - | - | - | - | - | - | - | - | not counted | F-zh_source_tax_calculator-abe889 |
| 2 | Married or registered partnership | Minor | yes | Sole custody | - | - | - | - | - | - | counted | F-zh_source_tax_calculator-d75286 |
| 3 | Single, divorced, separated or widowed | Minor | yes | Sole custody | - | - | - | - | - | - | counted with H | F-zh_source_tax_calculator-d75286, F-zh_source_tax_calculator-300c72 |
| 4 | Married or registered partnership | Minor | yes | Shared custody | yes | - | - | - | - | - | counted | F-zh_source_tax_calculator-5d8fb0 |
| 5 | Single, divorced, separated or widowed | Minor | yes | Shared custody | yes | - | - | - | Other parent | - | not counted | F-zh_source_tax_calculator-5686d7 |
| 6 | Single, divorced, separated or widowed | Minor | yes | Shared custody | yes | - | - | - | Myself | - | counted with H (inferred) | F-zh_source_tax_calculator-300c72, D-009 |
| 7 | Married or registered partnership | Minor | yes | Shared custody | no | - | - | yes | Other parent | - | not counted | F-zh_source_tax_calculator-a4d358 |
| 8 | Married or registered partnership | Minor | yes | Shared custody | no | - | - | yes | Myself | - | counted (inferred) | F-zh_source_tax_calculator-a4d358, D-009 |
| 9 | Single, divorced, separated or widowed | Minor | yes | Shared custody | no | - | - | yes | Other parent | - | not counted (inferred) | F-zh_source_tax_calculator-300c72, D-009 |
| 10 | Single, divorced, separated or widowed | Minor | yes | Shared custody | no | - | - | yes | Myself | - | counted with H (inferred) | F-zh_source_tax_calculator-300c72, D-009 |
| 11 | Married or registered partnership | Minor | yes | Shared custody | no | - | - | no | - | - | not counted | F-zh_source_tax_calculator-a4d358 |
| 12 | Single, divorced, separated or widowed | Minor | yes | Shared custody | no | - | - | no | - | - | counted with H | F-zh_source_tax_calculator-dc0ae9, D-046 |
| 13 | Married or registered partnership | Minor | no | - | - | no | - | - | - | - | not counted | F-zh_source_tax_calculator-dc6ace |
| 14 | Married or registered partnership | Minor | no | - | - | yes | - | yes | Myself | - | counted | F-zh_source_tax_calculator-dc6ace |
| 15 | Married or registered partnership | Minor | no | - | - | yes | - | yes | Other parent | - | not counted (inferred) | F-zh_source_tax_calculator-a4d358, D-009 |
| 16 | Married or registered partnership | Minor | no | - | - | yes | - | no | - | - | not counted (inferred) | F-zh_source_tax_calculator-a4d358, D-009 |
| 17 | Single, divorced, separated or widowed | Minor | no | - | - | - | no | - | - | - | not counted | F-zh_source_tax_calculator-dc6ace |
| 18 | Single, divorced, separated or widowed | Minor | no | - | - | - | yes | yes | Myself | - | counted with H | F-zh_source_tax_calculator-dc6ace, D-046 |
| 19 | Single, divorced, separated or widowed | Minor | no | - | - | - | yes | yes | Other parent | - | not counted (inferred) | D-009 |
| 20 | Single, divorced, separated or widowed | Minor | no | - | - | - | yes | no | - | - | not counted (inferred) | D-009 |
| 21 | Married or registered partnership | Adult in first education | yes | - | yes | - | - | - | - | - | counted | F-zh_source_tax_calculator-3eb561 |
| 22 | Single, divorced, separated or widowed | Adult in first education | yes | - | yes | - | - | - | Myself | - | counted with H (inferred) | F-zh_source_tax_calculator-300c72, D-009 |
| 23 | Single, divorced, separated or widowed | Adult in first education | yes | - | yes | - | - | - | Other parent | - | not counted (inferred) | F-zh_source_tax_calculator-300c72, D-009 |
| 24 | Married or registered partnership | Adult in first education | yes | - | no | - | - | - | - | yes | counted (inferred) | F-zh_source_tax_calculator-3eb561, D-009 |
| 25 | Married or registered partnership | Adult in first education | yes | - | no | - | - | - | - | no | not counted (inferred) | F-zh_source_tax_calculator-3eb561, D-009 |
| 26 | Single, divorced, separated or widowed | Adult in first education | yes | - | no | - | - | - | - | yes | counted with H | F-zh_source_tax_calculator-3eb561 |
| 27 | Single, divorced, separated or widowed | Adult in first education | yes | - | no | - | - | - | - | no | not counted (inferred) | D-009 |
| 28 | any | Adult in first education | no | - | - | - | - | - | - | yes | counted | F-zh_source_tax_calculator-3eb561 |
| 29 | any | Adult in first education | no | - | - | - | - | - | - | no | not counted | F-zh_source_tax_calculator-3eb561 |

_Status: inferred · Sources: F-zh_source_tax_calculator-abe889, F-zh_source_tax_calculator-300c72, F-zh_source_tax_calculator-d75286, F-zh_source_tax_calculator-5d8fb0, F-zh_source_tax_calculator-a4d358, F-zh_source_tax_calculator-dc0ae9, F-zh_source_tax_calculator-5686d7, F-zh_source_tax_calculator-dc6ace, F-zh_source_tax_calculator-3eb561, D-001, D-009, D-046_

#### Number of counted children (child digit)
The child digit of the tariff code is the number of children whose result is 'counted' or 'counted with H', summed over all child blocks. Without children it is 0. (The internal expression evaluates one child block; it is summed over all blocks.)

| # | Has children | Per-child result | → Result | Sources |
|---|---|---|---|---|
| 1 | no | - | 0 | F-zh_source_tax_calculator-037b1c |
| 2 | yes | counted or counted with H | adds 1 per such child | F-zh_source_tax_calculator-4c53e3 |
| 3 | yes | not counted | adds 0 | F-zh_source_tax_calculator-4c53e3 |

_Status: confirmed · Sources: F-zh_source_tax_calculator-4c53e3, F-zh_source_tax_calculator-fd9a15, D-044_

## Evidence
- **D-001** (product decision (Product owner)): Lonio computes the full Zurich source tax tariff code (tariff letter including the cross-border letters, child digit and church-tax suffix, e.g. "C1Y", "L0Y") for every employee subject to source tax, from the answers it collects, following the calculator's logic. HR no longer clicks through the calculator.
- **D-002** (product decision (Product owner)): Ask for the canton (pension fund 'Canton' field) from every employee. Employees living in Switzerland choose their canton of residence; for employees living abroad the canton of the place of work is entered (Zurich for Muster AG) and not asked. This closes OQ-canton-abroad. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-003** (product decision (Product owner)): Civil status offers Single, Married, Divorced, Widowed, Registered partnership and Separated. For source tax, registered partnership counts as married (including the spouse exemption) and separated counts as single, as in the calculator. For the pension fund, registered partnership is entered as Married with the partner's date of birth, and separated as Married. This closes OQ-civil-status-partnership. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-004** (product decision (Product owner)): The spouse's (or registered partner's) date of birth is asked from married employees, registered partners and separated employees (all entered at the fund as Married, see D-003), not from divorced or widowed employees; no spouse data is sent to the fund for them. This closes OQ-spouse-dob-other-status and OQ-separated-spouse-dob. Assumption - to be verified by a domain expert; state this assumption in the user story.
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
- **D-039** (product decision (Product owner)): The first working day is the contractual start date, even when it falls on a weekend or public holiday. The insurance start date is derived from this date only. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-040** (product decision (Product owner)): For employees living in Liechtenstein, the questions on daily return and on more than 45 days abroad come before denomination, spouse and children. When the answers mean 'in principle no source tax liability', the tariff questions are skipped. When the employee stays abroad more than 45 days, the normal tariff is recorded with the note 'subject to the double taxation agreement' and flagged for HR. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-041** (product decision (Product owner)): The residence country and address asked are those that apply on the first working day. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-042** (product decision (Product owner)): The house number is required, as HR wants the address complete including the house number; an explicit 'no house number' option covers addresses without one. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-043** (product decision (Product owner)): Apply HR's consolidated source tax rule as stated; 'here' in HR's wording means Switzerland. This closes OQ-source-tax-rule-confirmation. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-044** (product decision (Product owner)): There is no maximum number of children. A child's age is judged on the first working day. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-045** (product decision (Product owner)): Business text (stories, acceptance criteria, notices) uses no internal snake_case ids and does not speak of 'expressions'. Any behaviour that has no cited fact or decision is stated in the story as an assumption. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-046** (product decision (Product owner)): For the per-child source tax result, observed calculator table rows win over the derived expression. Inferred rows stay under the D-009 go-live check. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-047** (product decision (Product owner)): The questionnaire has exactly these steps, in this order, and feature.md, the flow rule and the stories use the same list. 1 About you (first name, last name, date of birth, first working day); 2 Home address (as on the first working day, canton only in Switzerland); 3 Nationality and C permit (only employees living in Switzerland); 4 Civil status and spouse (civil status is asked of everyone, wherever they live); 5 Cross-border commuting (Liechtenstein and Germany residents subject to source tax); 6 Source tax details (denomination, spouse gainfully employed, has children); 7 Children (one block per child); 8 Permit reminder, summary and submission. There is no separate step for the first working day. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-048** (product decision (Product owner)): When HR changes an answer after submission so that questions apply that were never asked, the derived results that depend on them (for example the tariff code) show 'incomplete - HR must complete' instead of a value, until HR enters the missing answers. Answers that no longer apply after an HR change are discarded, as on the employee's submission. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-049** (product decision (Product owner)): Every home address field (street, house number, postcode, town, country) is required; the only exception is the explicit 'no house number' option. Examples and acceptance criteria use the term 'required' for these fields, never 'asked'. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-050** (product decision (Product owner)): Build-time values. HR provides the permit reminder wording before go-live. Country of residence and nationality are chosen from the ISO 3166 country list; nationality also offers 'stateless'. The date of birth must make the employee at least 14 and at most 100 years old on the first working day; the first working day must lie within one year after the questionnaire is sent. Answers are saved as the employee goes and they can resume until they submit; submitting needs one confirmation on a summary page. Answers are kept when the employee goes back and changes an earlier answer (until submission), and this is testable. The spouse's residence is asked as 'Does your spouse live in Switzerland? yes/no', not as a country. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-051** (product decision (Product owner)): The full tariff code is one text such as 'N1Y' (letter, child digit, church-tax suffix). When no tariff code is needed the result is the text 'no tariff code'. The cross-border letter mapping follows the calculator fact in full, including G to Q where the calculator shows it. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-052** (product decision (Product owner)): The tariff code is one code made of the tariff letter, the child digit and the church-tax suffix (D-051), for example C1Y. The child digit is the number of children who count; the examples have one child each. When the letter or the church-tax suffix cannot be derived because an answer is missing (for example after an HR change), the result is 'incomplete - HR must complete' (D-048, D-053).
- **D-053** (product decision (Product owner)): After submission the questionnaire stays read-only for the employee and is never reopened. When an HR change makes new questions apply, HR enters the missing answers itself; until then the derived results that depend on them show 'incomplete - HR must complete' (D-048). Examples after an HR change therefore expect 'HR must complete', not 'asked'. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **D-054** (product decision (Product owner)): For Liechtenstein residents with more than 45 non-return days, the recorded tariff code is the plain code (for example C0Y). The note 'subject to the double taxation agreement' is recorded separately next to the code and flagged for HR; it is not part of the code. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **F-hr_transcript-1d5c07** (hr_transcript): Consolidated rule: the insurance start date is derived from the first working day. If the first working day is the 1st of a month, insurance starts that day. Otherwise it starts on the 1st of the following month.
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
- **F-hr_transcript-35fae3** (hr_transcript): The employee's nationality is needed to decide whether they are subject to source tax.
  - "If you don't have a Swiss passport, you do source tax." — hr_transcript/T-010, Anna
- **F-hr_transcript-3907fe** (hr_transcript): At least one current employee (Daniel, finance) is in a registered partnership, so this case occurs.
  - "we do have one colleague in a registered partnership. Daniel, in finance." — hr_transcript/T-034, Anna
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
- **F-hr_transcript-54d011** (hr_transcript, inferred): The spouse's nationality, permit and residence only matter for source tax when the employee is married. They are presumably only needed when the employee would otherwise be subject to source tax (non-Swiss, no C permit, living in Switzerland).
  - "it also changes who has to do it at all." — hr_transcript/T-044, Anna
  - "then you don't do source tax either." — hr_transcript/T-044, Anna
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
- **F-zh_source_tax_calculator-33ef31** (zh_source_tax_calculator): Q21 is shown only when daily return is reasonable (Q20 = Ja).
  - "Nachweis von mehr als 60 beruflich bedingten Nichtrückkehrtagen im Kalenderjahr beigebracht?" — zh_source_tax_calculator/C-Q21
- **F-zh_source_tax_calculator-3a75cc** (zh_source_tax_calculator): Same-household options are Ja / Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q08
- **F-zh_source_tax_calculator-3eb561** (zh_source_tax_calculator): Adult child in first education: in household with common household (married) counts (B1N); not in household counts only if more than 50% of maintenance is provided (single A1N; married with Nein -> B0N); single, in household without common household and >50% maintenance gives H1N.
  - ""Q10": "Ja", "Q16": "Ja"} -> result Tarif: B1N" — zh_source_tax_calculator/C-V14
  - ""Q15": "Nein", "Q16": "Ja"} -> result Tarif: B0N" — zh_source_tax_calculator/C-V15
  - "result Tarif: A1N (Kind Ergebnis: A1)" — zh_source_tax_calculator/C-V22
  - ""Q15": "Ja", "Q16": "Ja"} -> result Tarif: H1N" — zh_source_tax_calculator/C-V23
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
- **G-08** (product owner guidance): Prefer asking for primary facts and **deriving** values (e.g. ask the first working day, derive the insurance start date) instead of asking the employee for values they cannot know.
- **G-09** (product owner guidance): Questionnaire language: English.
- **G-10** (product owner guidance): Business wording for values (used in allowed values and examples): countries by English name ("Switzerland", "Germany", "Liechtenstein"), permits as "B permit", "C permit", civil status exactly as the pension fund's list shows it ("Single", "Married", ...), dates as DD.MM.YYYY, yes/no as "yes"/"no".
