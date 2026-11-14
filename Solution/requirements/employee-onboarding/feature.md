---
id: employee-onboarding
title: "Employee onboarding questionnaire"
stakeholders: [employee, hr, pension_fund, source_tax]
sections: [SEC-01-identity-and-address, SEC-02-start-date-insurance, SEC-03-civil-status-spouse, SEC-04-source-tax-liability, SEC-05-tariff-basics, SEC-06-children, SEC-07-living-abroad, SEC-08-completion-and-submission]
stories: [US-01.1, US-01.2, US-01.3, US-01.4, US-02.1, US-02.2, US-03.1, US-03.2, US-03.3, US-03.4, US-04.1, US-04.2, US-04.3, US-05.3, US-05.4, US-05.6, US-05.7, US-06.1, US-06.2, US-06.3, US-06.4, US-06.5, US-06.6, US-07.1, US-07.2, US-07.3, US-08.1, US-08.2, US-08.3]
---

# Employee onboarding questionnaire

Each user story is its own file in [stories/](stories/); this file holds the
feature, its sections and the information and rules they share.

**Goal:** A new employee answers one short, conditional English questionnaire once, and Lonio records exactly the data that Pensionskasse Muster, source tax (the Zurich tariff) and Muster AG HR need for that person. From the answers it derives the insurance start date and the full source tax tariff code, and it collects no personal data that no party needs.

## Context
Today Muster AG HR collects onboarding data by hand and enters it at each receiving party. This causes several problems, which the sources describe:
- HR posts many documents to employees, so it needs a complete postal address (F-hr_transcript-5518ad, F-hr_transcript-ec57d3).
- The pension fund needs an insurance start date that is always the 1st of a month and follows the first working day. In one case (Julia), a changed start date did not flow into the insurance start (F-hr_transcript-1d5c07, F-hr_transcript-d7a23b).
- HR decides by hand who is subject to source tax, from residence, nationality, C permit and spouse (F-hr_transcript-b6d9b3, F-hr_transcript-d7431e). It then clicks through the Zurich calculator to get the tariff code (F-hr_transcript-4e180e, F-hr_transcript-563a9f).

Lonio replaces this with a questionnaire that asks each fact once and only when a party needs it (G-01, G-08):
- it computes the tariff code itself (D-001);
- it asks the canton only from residents of Switzerland (D-002);
- it maps civil status for the fund and for source tax (D-003, D-004);
- it asks only 'C permit yes/no' (D-005) and drops income type (D-006);
- it handles Liechtenstein and Germany cross-border cases following the calculator (D-007, D-035);
- it reminds non-Swiss employees and employees living abroad to bring their permit (D-010);
- it discards answers that no longer apply when the questionnaire is submitted (D-036).

Out of scope:
- the HR side and how data is transmitted to the parties (G-04, D-034);
- AHV data and IT equipment (G-03).

Domain-expert checks remain open but do not block (D-002, D-003, D-004, D-009).

**Stakeholders:** new employee, HR, pension fund, source tax office

## Questionnaire flow

The employee answers the questionnaire in seven steps, in this order. Each
step shows only the questions that apply to this employee (see "When do we
ask?" for each piece of information). A step in which no question applies is
skipped. The order follows the dependencies: whether the employee is subject
to source tax is only known after steps 2, 4 and 5, so the source tax
questions come last. The step numbers match the "Flow step" notes on each
piece of information.

| Step | What the employee is asked | Shown to | Stories |
|---|---|---|---|
| 1. Personal details | First name, last name, date of birth | Everyone | [US-01.1](stories/US-01.1-personal-details-for-the-pension-fund-registration.md) |
| 2. Home address | Street, house number, postcode, town, country; the canton only if the country is Switzerland | Everyone | [US-01.2](stories/US-01.2-complete-home-address-for-posting-documents.md), [US-01.3](stories/US-01.3-home-address-country-is-the-country-of-residence-for-later.md), [US-01.4](stories/US-01.4-canton-of-residence-for-employees-living-in-switzerland.md) |
| 3. Employment | First working day | Everyone | [US-02.1](stories/US-02.1-employee-enters-the-first-working-day.md) |
| 4. Residence status | Whether they are a Swiss citizen; whether they hold a C permit (only if not Swiss) | Employees living in Switzerland | [US-04.1](stories/US-04.1-ask-swiss-citizenship-and-c-permit-only-of-employees-living.md) |
| 5. Family | Civil status; the spouse's or partner's date of birth (married, registered partnership, separated); the spouse's or partner's Swiss citizenship, C permit and whether they live in Switzerland, only as far as they can exempt the employee from source tax | Everyone (spouse questions as stated) | [US-03.1](stories/US-03.1-ask-the-civil-status-once-using-the-pension-fund-s-list.md), [US-03.2](stories/US-03.2-ask-the-spouse-s-or-partner-s-date-of-birth-from-married.md), [US-04.2](stories/US-04.2-ask-spouse-details-only-when-the-spouse-could-exempt-the.md) |
| 6. Source tax | Denomination; whether the spouse or partner works (married, registered partnership); children, one block per child; the Germany or Liechtenstein questions (only for employees living there) | Employees subject to source tax ([US-04.3](stories/US-04.3-decide-whether-the-employee-is-subject-to-source-tax.md)) | [US-05.3](stories/US-05.3-state-the-denomination-for-the-church-tax-part-of-the-tariff.md), [US-05.4](stories/US-05.4-state-whether-the-spouse-or-registered-partner-works-for.md), [US-06.1](stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md)–[US-06.5](stories/US-06.5-ask-household-and-maintenance-for-a-child-of-age-in-first.md), [US-07.2](stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md), [US-07.3](stories/US-07.3-determine-the-source-tax-outcome-for-employees-living-in.md) |
| 7. Review and submit | Nothing new: the employee checks the answers and submits; non-Swiss employees and employees living abroad see the permit reminder | Everyone | [US-08.1](stories/US-08.1-remind-employees-to-bring-their-permit-on-the-first-working.md), [US-08.2](stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md), [US-08.3](stories/US-08.3-questionnaire-is-read-only-for-the-employee-after-submission.md) |

Never asked, always derived from the answers: the insurance start date
(US-02.2), the civil status for the fund and for source tax (US-03.3, US-03.4),
whether the employee is subject to source tax (US-04.3), the calculator's
residence answers (US-07.1), and the tariff code or Liechtenstein result
(US-05.6, US-05.7, US-06.6). After submission the questionnaire is read-only
for the employee (US-08.3, D-037).

## Contents

| Section | Stories |
|---|---|
| [1. Personal details and home address](#SEC-01-identity-and-address) | [US-01.1](stories/US-01.1-personal-details-for-the-pension-fund-registration.md), [US-01.2](stories/US-01.2-complete-home-address-for-posting-documents.md), [US-01.3](stories/US-01.3-home-address-country-is-the-country-of-residence-for-later.md), [US-01.4](stories/US-01.4-canton-of-residence-for-employees-living-in-switzerland.md) |
| [2. First working day and insurance start date](#SEC-02-start-date-insurance) | [US-02.1](stories/US-02.1-employee-enters-the-first-working-day.md), [US-02.2](stories/US-02.2-insurance-start-date-derived-from-the-first-working-day.md) |
| [3. Civil status and spouse for the pension fund](#SEC-03-civil-status-spouse) | [US-03.1](stories/US-03.1-ask-the-civil-status-once-using-the-pension-fund-s-list.md), [US-03.2](stories/US-03.2-ask-the-spouse-s-or-partner-s-date-of-birth-from-married.md), [US-03.3](stories/US-03.3-enter-the-civil-status-in-the-pension-fund-s-terms.md), [US-03.4](stories/US-03.4-group-the-civil-status-for-source-tax.md) |
| [4. Source tax liability check](#SEC-04-source-tax-liability) | [US-04.1](stories/US-04.1-ask-swiss-citizenship-and-c-permit-only-of-employees-living.md), [US-04.2](stories/US-04.2-ask-spouse-details-only-when-the-spouse-could-exempt-the.md), [US-04.3](stories/US-04.3-decide-whether-the-employee-is-subject-to-source-tax.md) |
| [5. Source tax tariff basics and computed result](#SEC-05-tariff-basics) | [US-05.3](stories/US-05.3-state-the-denomination-for-the-church-tax-part-of-the-tariff.md), [US-05.4](stories/US-05.4-state-whether-the-spouse-or-registered-partner-works-for.md), [US-05.6](stories/US-05.6-determine-the-tariff-letter-including-the-cross-border.md), [US-05.7](stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md) |
| [6. Children for the source tax tariff](#SEC-06-children) | [US-06.1](stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md), [US-06.2](stories/US-06.2-ask-custody-and-common-household-for-a-minor-child-living.md), [US-06.3](stories/US-06.3-ask-custody-and-alternating-care-for-a-minor-child-not.md), [US-06.4](stories/US-06.4-ask-who-contributes-more-to-the-child-s-maintenance.md), [US-06.5](stories/US-06.5-ask-household-and-maintenance-for-a-child-of-age-in-first.md), [US-06.6](stories/US-06.6-derive-the-child-digit-and-the-single-parent-h-tariff.md) |
| [7. Employees living abroad (Germany, Liechtenstein)](#SEC-07-living-abroad) | [US-07.1](stories/US-07.1-derive-the-calculator-s-residence-answers-from-the-home.md), [US-07.2](stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md), [US-07.3](stories/US-07.3-determine-the-source-tax-outcome-for-employees-living-in.md) |
| [8. Completing and submitting the questionnaire](#SEC-08-completion-and-submission) | [US-08.1](stories/US-08.1-remind-employees-to-bring-their-permit-on-the-first-working.md), [US-08.2](stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md), [US-08.3](stories/US-08.3-questionnaire-is-read-only-for-the-employee-after-submission.md) |

<a id="SEC-01-identity-and-address"></a>

## 1. Personal details and home address

Collect the employee's name, date of birth and complete postal address, which also gives the country of residence, and the canton for Swiss residents, so the fund can register the employee and HR can post documents.

> ⚠ Open questions affecting this section: [OQ-canton-abroad](open-questions.md#oq-canton-abroad)
| Story | Priority | Status |
|---|---|---|
| [US-01.1 – Personal details for the pension fund registration](stories/US-01.1-personal-details-for-the-pension-fund-registration.md) | P1 | confirmed |
| [US-01.2 – Complete home address for posting documents](stories/US-01.2-complete-home-address-for-posting-documents.md) | P1 | confirmed |
| [US-01.3 – Home address country is the country of residence for later questions](stories/US-01.3-home-address-country-is-the-country-of-residence-for-later.md) | P1 | decision |
| [US-01.4 – Canton of residence for employees living in Switzerland](stories/US-01.4-canton-of-residence-for-employees-living-in-switzerland.md) | P1 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### First name
| | |
|---|---|
| **What?** | The employee's first name, as needed to register the employee with the pension fund. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'First name' when registering the new employee as an insured person |
| **Status · sources** | confirmed · F-pension_portal-b5c835, F-pension_portal-44a27b, F-pension_portal-3cfe89 |
| **Notes** | Flow step 1 (personal details). |

#### Last name
| | |
|---|---|
| **What?** | The employee's last name, as needed to register the employee with the pension fund. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'Last name' when registering the new employee |
| **Status · sources** | confirmed · F-pension_portal-c688e4, F-pension_portal-44a27b, F-pension_portal-3cfe89 |
| **Notes** | Flow step 1 (personal details). |

#### Date of birth
| | |
|---|---|
| **What?** | The employee's date of birth. – Form: Date in the format DD.MM.YYYY |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'Date of birth' when registering the new employee |
| **Status · sources** | confirmed · F-pension_portal-88b436, F-pension_portal-967bc9, F-pension_portal-44a27b |
| **Notes** | Flow step 1 (personal details). |

#### Street
| | |
|---|---|
| **What?** | Street of the employee's home address. – Form: Part of a complete postal address as written on an envelope: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Posting documents to the employee; the address must be complete |
| **Status · sources** | confirmed · F-hr_transcript-5518ad, F-hr_transcript-ec57d3, F-hr_transcript-66fe15 |
| **Notes** | Flow step 2 (home address). |

#### House number
| | |
|---|---|
| **What?** | House number of the employee's home address. – Form: Part of a complete postal address: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Posting documents to the employee; the address must be complete |
| **Status · sources** | confirmed · F-hr_transcript-ec57d3, F-hr_transcript-66fe15 |
| **Notes** | Flow step 2. |

#### Postcode
| | |
|---|---|
| **What?** | Postcode of the employee's home address. – Form: Part of a complete postal address: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Posting documents to the employee; the address must be complete |
| **Status · sources** | confirmed · F-hr_transcript-ec57d3, F-hr_transcript-66fe15 |
| **Notes** | Flow step 2. |

#### Town
| | |
|---|---|
| **What?** | Town of the employee's home address. – Form: Part of a complete postal address: street, house number, postcode, town and country |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Posting documents to the employee; the address must be complete |
| **Status · sources** | confirmed · F-hr_transcript-ec57d3, F-hr_transcript-66fe15 |
| **Notes** | Flow step 2. |

#### Country of home address (country of residence)
| | |
|---|---|
| **What?** | Country of the employee's home address. It is also the employee's country of residence: it decides whether the employee lives abroad (always subject to source tax), whether the canton and the citizenship questions are asked, and which cross-border questions apply (Germany, Liechtenstein, other country). – Form: Country by English name (e.g. Switzerland, Germany, Liechtenstein); part of a complete postal address |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Posting documents to the employee; the address must be complete<br>source tax office: Living abroad makes the employee subject to source tax; state of residence (Germany, Liechtenstein, other country) drives the cross-border part of the tariff |
| **Status · sources** | decision · F-hr_transcript-ec57d3, F-hr_transcript-e505f8, F-hr_transcript-b6d9b3, F-zh_source_tax_calculator-f29009, F-zh_source_tax_calculator-d62dd4, G-08, G-10, D-001, D-007 |
| **Notes** | Flow step 2. Replaces the calculator's 'Main residence in Switzerland?' and 'State of residence' questions, which are derived from it (G-08). |

#### Canton
| | |
|---|---|
| **What?** | The Swiss canton the employee lives in, for the pension fund's 'Canton' field. Provisionally interpreted as canton of residence and asked only from employees living in Switzerland. |
| **Allowed values** | Aargau · Appenzell Ausserrhoden · Appenzell Innerrhoden · Basel-Landschaft · Basel-Stadt · Bern · Fribourg · Geneva · Glarus · Graubünden · Jura · Lucerne · Neuchâtel · Nidwalden · Obwalden · Schaffhausen · Schwyz · Solothurn · St. Gallen · Thurgau · Ticino · Uri · Valais · Vaud · Zug · Zurich |
| **When do we ask?** | Only if the employee lives in Switzerland |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence) |
| **Who needs it?** | pension fund: Required field 'Canton' when registering the new employee |
| **Status · sources** | decision · F-pension_portal-587d3f, F-pension_portal-3432a9, F-pension_portal-44a27b, F-pension_portal-b359c3, D-002 |
| **Notes** | Flow step 2, after the country. What to enter for employees living abroad is open (OQ-canton-abroad). |

<a id="SEC-02-start-date-insurance"></a>

## 2. First working day and insurance start date

Ask the employee for the first working day and derive the pension fund insurance start date from it, so that the start date always falls on the 1st of a month and follows the latest first working day.

| Story | Priority | Status |
|---|---|---|
| [US-02.1 – Employee enters the first working day](stories/US-02.1-employee-enters-the-first-working-day.md) | P1 | decision |
| [US-02.2 – Insurance start date derived from the first working day](stories/US-02.2-insurance-start-date-derived-from-the-first-working-day.md) | P1 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### First working day
| | |
|---|---|
| **What?** | The employee's first working day at Muster AG, entered and confirmed by the employee. The insurance start date is derived from it. After submission only HR can change it; the latest date always counts and no history is kept. – Form: Date (DD.MM.YYYY) |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Basis for the insurance start date<br>HR: Start of employment; HR changes it if it moves after submission |
| **Status · sources** | decision · F-hr_transcript-872bd7, F-hr_transcript-e3721e, F-hr_transcript-d7a23b, G-08, G-10, D-033, D-037 |
| **Notes** | Flow step 3 (employment). HR-side change is for the later HR spec (D-034). |

### Business rules in this section

#### Insurance start date
The pension fund insurance starts on the first working day if that is the 1st of a month; otherwise on the 1st of the following month. Always derived from the latest first working day.

| # | First working day | → Result | Sources |
|---|---|---|---|
| 1 | is the 1st of a month | Insurance starts on the first working day | F-hr_transcript-fdf50a, F-hr_transcript-1d5c07 |
| 2 | any other day | Insurance starts on the 1st of the following month (e.g. 15.03. → 01.04.) | F-hr_transcript-30d25c, F-hr_transcript-1d5c07, F-pension_portal-dd8126 |

_Status: decision · Sources: F-hr_transcript-1d5c07, F-hr_transcript-d7a23b, F-pension_portal-509cbe, F-pension_portal-dd8126, G-08, D-033, D-037_

<a id="SEC-03-civil-status-spouse"></a>

## 3. Civil status and spouse for the pension fund

Ask the civil status once. Map it to the fund's list and to married/single for source tax. Ask the spouse's or partner's date of birth only where the fund requires it.

> ⚠ Open questions affecting this section: [OQ-civil-status-partnership](open-questions.md#oq-civil-status-partnership), [OQ-spouse-dob-other-status](open-questions.md#oq-spouse-dob-other-status)
| Story | Priority | Status |
|---|---|---|
| [US-03.1 – Ask the civil status once, using the pension fund's list](stories/US-03.1-ask-the-civil-status-once-using-the-pension-fund-s-list.md) | P1 | decision |
| [US-03.2 – Ask the spouse's or partner's date of birth from married, partnered and separated employees](stories/US-03.2-ask-the-spouse-s-or-partner-s-date-of-birth-from-married.md) | P1 | decision |
| [US-03.3 – Enter the civil status in the pension fund's terms](stories/US-03.3-enter-the-civil-status-in-the-pension-fund-s-terms.md) | P1 | decision |
| [US-03.4 – Group the civil status for source tax](stories/US-03.4-group-the-civil-status-for-source-tax.md) | P1 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Civil status
| | |
|---|---|
| **What?** | The employee's civil status. Mapped to the pension fund's list and to the calculator's two civil-status groups. |
| **Allowed values** | Single · Married · Divorced · Widowed · Registered partnership · Separated |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field 'Civil status'; decides whether the spouse's date of birth is required<br>source tax office: Decides married or single tariff, the spouse exemption and the follow-up questions (only for employees subject to source tax) |
| **Status · sources** | decision · F-hr_transcript-ce8ca4, F-pension_portal-ec4512, F-pension_portal-3d1ae4, F-zh_source_tax_calculator-9007c3, F-zh_source_tax_calculator-051bb9, F-hr_transcript-3907fe, G-10, D-003 |
| **Notes** | Flow step 5 (family). |

#### Spouse's or registered partner's date of birth
| | |
|---|---|
| **What?** | Date of birth of the employee's husband, wife or registered partner (for separated employees: of the spouse they are separated from). – Form: Date in the format DD.MM.YYYY |
| **When do we ask?** | Only if the employee is married, in a registered partnership or separated |
| **When is it required?** | Whenever asked |
| **Depends on** | Civil status |
| **Who needs it?** | pension fund: Required 'Spouse's date of birth' when civil status is entered as Married |
| **Status · sources** | decision · F-hr_transcript-2334d8, F-pension_portal-a0065b, F-pension_portal-ef28c3, F-pension_portal-39bab1, F-pension_portal-0eed50, D-003, D-004 |
| **Notes** | Flow step 5. Divorced/widowed: OQ-spouse-dob-other-status. |

### Business rules in this section

#### Civil status for the pension fund
The civil status is entered at the pension fund from its list. Provisionally, registered partnership and separated are entered as Married.

| # | Civil status | → Result | Sources |
|---|---|---|---|
| 1 | Single | Single | F-pension_portal-3d1ae4 |
| 2 | Married | Married | F-pension_portal-3d1ae4 |
| 3 | Divorced | Divorced | F-pension_portal-3d1ae4 |
| 4 | Widowed | Widowed | F-pension_portal-3d1ae4 |
| 5 | Registered partnership | Married (with the partner's date of birth), provisional | D-003 |
| 6 | Separated | Married (with the spouse's date of birth), provisional | D-003, D-004 |

_Status: decision · Sources: F-pension_portal-3d1ae4, F-pension_portal-9b24c5, F-hr_transcript-f197d6, D-003_

#### Civil status for source tax
For source tax, married and registered partnership count as 'married or registered partnership'; single, divorced, separated and widowed count as 'single'.

| # | Civil status | → Result | Sources |
|---|---|---|---|
| 1 | Married or Registered partnership | Married or registered partnership | F-zh_source_tax_calculator-051bb9, D-003 |
| 2 | Single, Divorced, Widowed or Separated | Single, divorced, separated or widowed | F-zh_source_tax_calculator-051bb9, D-003 |

_Status: decision · Sources: F-zh_source_tax_calculator-051bb9, D-003_

<a id="SEC-04-source-tax-liability"></a>

## 4. Source tax liability check

Decide from residence, Swiss citizenship, C permit and the spouse exemption whether the employee is subject to source tax. Ask these facts only as far as they are needed, so that only employees subject to source tax get the source tax questions.

| Story | Priority | Status |
|---|---|---|
| [US-04.1 – Ask Swiss citizenship and C permit only of employees living in Switzerland](stories/US-04.1-ask-swiss-citizenship-and-c-permit-only-of-employees-living.md) | P1 | decision |
| [US-04.2 – Ask spouse details only when the spouse could exempt the employee](stories/US-04.2-ask-spouse-details-only-when-the-spouse-could-exempt-the.md) | P1 | inferred |
| [US-04.3 – Decide whether the employee is subject to source tax](stories/US-04.3-decide-whether-the-employee-is-subject-to-source-tax.md) | P1 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Swiss citizenship
| | |
|---|---|
| **What?** | Whether the employee holds Swiss citizenship. Anyone with Swiss citizenship counts as Swiss, even with another nationality. Only 'Swiss or not' drives a rule, so the actual nationality is not collected. Not asked of employees living abroad, who are subject to source tax regardless of nationality. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Switzerland |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence) |
| **Who needs it?** | source tax office: Swiss citizens living in Switzerland are not subject to source tax<br>HR: Decides whether the permit reminder is shown |
| **Status · sources** | decision · F-hr_transcript-35fae3, F-hr_transcript-b6d9b3, F-hr_transcript-1a20bb, G-01, D-008, D-038, D-010 |
| **Notes** | Flow step 4 (residence status). |

#### C permit held
| | |
|---|---|
| **What?** | Whether a non-Swiss employee living in Switzerland holds a C permit (permanent residence). No other permit type is needed by any party. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Switzerland and is not a Swiss citizen |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence), Swiss citizenship |
| **Who needs it?** | source tax office: Non-Swiss employees with a C permit are treated like Swiss and are not subject to source tax |
| **Status · sources** | decision · F-hr_transcript-4ad146, F-hr_transcript-845204, F-hr_transcript-b6d9b3, G-01, D-005 |
| **Notes** | Flow step 4. |

#### Spouse lives in Switzerland
| | |
|---|---|
| **What?** | Whether the spouse or registered partner lives in Switzerland. Only needed when the spouse is Swiss or holds a C permit. |
| **Allowed values** | Switzerland · Another country |
| **When do we ask?** | Only if the spouse is a Swiss citizen or holds a C permit |
| **When is it required?** | Whenever asked |
| **Depends on** | Spouse's Swiss citizenship, Spouse holds a C permit |
| **Who needs it?** | source tax office: The spouse exemption applies only if the Swiss / C-permit spouse lives in Switzerland |
| **Status · sources** | inferred · F-hr_transcript-f3ce84, F-hr_transcript-d7431e, F-hr_transcript-b6d9b3, G-01 |
| **Notes** | Flow step 5. Two values instead of a full country, because only 'in Switzerland or not' drives the rule (data minimisation). |

#### Spouse's Swiss citizenship
| | |
|---|---|
| **What?** | Whether the employee's spouse or registered partner holds Swiss citizenship (dual citizens count as Swiss). |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Switzerland, is not Swiss, holds no C permit and is married or in a registered partnership |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence), Civil status, Swiss citizenship, C permit held |
| **Who needs it?** | source tax office: A Swiss spouse living in Switzerland exempts the employee from source tax |
| **Status · sources** | decision · F-hr_transcript-f3ce84, F-hr_transcript-d7431e, F-hr_transcript-b6d9b3, G-01, D-003, D-005, D-008 |
| **Notes** | Flow step 5. Separated employees count as single for source tax, so no spouse exemption applies. |

#### Spouse holds a C permit
| | |
|---|---|
| **What?** | Whether the non-Swiss spouse or registered partner holds a C permit (permanent residence). |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the spouse question was asked and the spouse is not a Swiss citizen |
| **When is it required?** | Whenever asked |
| **Depends on** | Spouse's Swiss citizenship |
| **Who needs it?** | source tax office: A spouse with a C permit living in Switzerland exempts the employee from source tax |
| **Status · sources** | decision · F-hr_transcript-f3ce84, F-hr_transcript-d7431e, F-hr_transcript-b6d9b3, D-005 |
| **Notes** | Flow step 5. |

### Business rules in this section

#### Subject to source tax
An employee living abroad is always subject to source tax, whatever the nationality. An employee living in Switzerland is subject only if not a Swiss citizen, holding no C permit and not exempted by a Swiss / C-permit spouse living in Switzerland. Only employees subject to source tax are asked the source tax questions.

| # | Country of home address | Swiss citizen | Holds C permit | Spouse exemption | → Result | Sources |
|---|---|---|---|---|---|---|
| 1 | not Switzerland | - | - | - | Subject to source tax | F-hr_transcript-1a20bb, F-hr_transcript-b6d9b3, D-007 |
| 2 | Switzerland | yes | - | - | Not subject | F-hr_transcript-b6d9b3, D-008 |
| 3 | Switzerland | no | yes | - | Not subject | F-hr_transcript-845204, D-005 |
| 4 | Switzerland | no | no | Exempt | Not subject | F-hr_transcript-d7431e |
| 5 | Switzerland | no | no | No exemption | Subject to source tax | F-hr_transcript-b6d9b3 |

_Status: decision · Sources: F-hr_transcript-b6d9b3, F-hr_transcript-b84498, F-hr_transcript-1a20bb, F-hr_transcript-845204, F-hr_transcript-d7431e, D-005, D-007, D-008_

#### Spouse exemption from source tax
A married or registered-partner employee is exempt from source tax if the spouse/partner is Swiss or holds a C permit and lives in Switzerland. Separated employees count as single and get no exemption.

| # | Civil status | Spouse Swiss citizen | Spouse holds C permit | Spouse lives in | → Result | Sources |
|---|---|---|---|---|---|---|
| 1 | Single, Divorced, Widowed or Separated | - | - | - | No exemption | D-003 |
| 2 | Married or Registered partnership | yes | - | Switzerland | Exempt | F-hr_transcript-d7431e, F-hr_transcript-b6d9b3 |
| 3 | Married or Registered partnership | no | yes | Switzerland | Exempt | F-hr_transcript-d7431e, F-hr_transcript-b6d9b3 |
| 4 | Married or Registered partnership | yes | - | Another country | No exemption | F-hr_transcript-d7431e |
| 5 | Married or Registered partnership | no | yes | Another country | No exemption | F-hr_transcript-d7431e |
| 6 | Married or Registered partnership | no | no | - | No exemption | F-hr_transcript-b6d9b3 |

_Status: decision · Sources: F-hr_transcript-d7431e, F-hr_transcript-b6d9b3, F-hr_transcript-f3ce84, D-003, D-005, D-008_

<a id="SEC-05-tariff-basics"></a>

## 5. Source tax tariff basics and computed result

Ask the denomination and whether the spouse works. Combine these with the child digit and the cross-border outcome into the full Zurich tariff code (or the Liechtenstein result), which Lonio records for HR instead of HR using the calculator.

> ⚠ Open questions affecting this section: [OQ-calculator-coverage](open-questions.md#oq-calculator-coverage)
| Story | Priority | Status |
|---|---|---|
| [US-05.3 – State the denomination for the church-tax part of the tariff](stories/US-05.3-state-the-denomination-for-the-church-tax-part-of-the-tariff.md) | P1 | decision |
| [US-05.4 – State whether the spouse or registered partner works, for married employees and registered partners](stories/US-05.4-state-whether-the-spouse-or-registered-partner-works-for.md) | P1 | decision |
| [US-05.6 – Determine the tariff letter, including the cross-border letters](stories/US-05.6-determine-the-tariff-letter-including-the-cross-border.md) | P1 | decision |
| [US-05.7 – Compute and record the source tax result for HR](stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md) | P1 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Denomination
| | |
|---|---|
| **What?** | Whether the employee belongs to the Roman Catholic, Christian Catholic or Evangelical Reformed church, or to none or another denomination. Sets the church-tax suffix of the tariff code. |
| **Allowed values** | Roman Catholic, Christian Catholic or Evangelical Reformed · None or other |
| **When do we ask?** | Only if the employee is subject to source tax |
| **When is it required?** | Whenever asked |
| **Depends on** | Subject to source tax |
| **Who needs it?** | source tax office: Church-tax suffix Y / N of the tariff code |
| **Status · sources** | decision · F-zh_source_tax_calculator-208104, F-zh_source_tax_calculator-b7fea8, F-zh_source_tax_calculator-2eab9a, F-hr_transcript-b84498, G-09, D-001 |
| **Notes** | Flow step 6 (source tax details). |

#### Spouse employed or receiving replacement income
| | |
|---|---|
| **What?** | Whether the spouse or registered partner is gainfully employed or receives replacement income. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee is subject to source tax and married or in a registered partnership |
| **When is it required?** | Whenever asked |
| **Depends on** | Civil status, Subject to source tax |
| **Who needs it?** | source tax office: Tariff letter C (yes) or B (no) |
| **Status · sources** | decision · F-zh_source_tax_calculator-7b637b, F-zh_source_tax_calculator-e740d1, F-zh_source_tax_calculator-0137bf, F-zh_source_tax_calculator-97139a, F-hr_transcript-09b3fe, D-001, D-003 |
| **Notes** | Flow step 6. |

### Business rules in this section

#### Church-tax suffix
Y for Roman Catholic, Christian Catholic or Evangelical Reformed; N for none or other.

| # | Denomination | → Result | Sources |
|---|---|---|---|
| 1 | Roman Catholic, Christian Catholic or Evangelical Reformed | Y | F-zh_source_tax_calculator-2eab9a |
| 2 | None or other | N | F-zh_source_tax_calculator-2eab9a |

_Status: decision · Sources: F-zh_source_tax_calculator-2eab9a, D-001_

#### Married tariff letter
For married / registered-partner employees: C if the spouse is employed or receives replacement income, otherwise B.

| # | Spouse employed or receiving replacement income | → Result | Sources |
|---|---|---|---|
| 1 | yes | C | F-zh_source_tax_calculator-97139a |
| 2 | no | B | F-zh_source_tax_calculator-97139a |

_Status: decision · Sources: F-zh_source_tax_calculator-97139a, D-001_

#### Tariff letter
Married/registered partnership: C (spouse employed) or B; single etc.: H (single-parent) or A. With the cross-border tariff the letter becomes A→L, B→M, C→N, H→P.

| # | Civil status for source tax | Spouse employed | Single-parent H tariff | Cross-border tariff applies | → Result | Sources |
|---|---|---|---|---|---|---|
| 1 | Married or registered partnership | yes | - | no | C | F-zh_source_tax_calculator-97139a |
| 2 | Married or registered partnership | yes | - | yes | N | F-zh_source_tax_calculator-4d3ac0 |
| 3 | Married or registered partnership | no | - | no | B | F-zh_source_tax_calculator-97139a |
| 4 | Married or registered partnership | no | - | yes | M | F-zh_source_tax_calculator-4d3ac0, F-zh_source_tax_calculator-b7154e |
| 5 | Single, divorced, separated or widowed | - | no | no | A | F-zh_source_tax_calculator-c78e0c |
| 6 | Single, divorced, separated or widowed | - | no | yes | L | F-zh_source_tax_calculator-b7154e |
| 7 | Single, divorced, separated or widowed | - | yes | no | H | F-zh_source_tax_calculator-96658b |
| 8 | Single, divorced, separated or widowed | - | yes | yes | P | F-zh_source_tax_calculator-b7154e |

_Status: decision · Sources: F-zh_source_tax_calculator-97139a, F-zh_source_tax_calculator-c78e0c, F-zh_source_tax_calculator-96658b, F-zh_source_tax_calculator-4d3ac0, F-zh_source_tax_calculator-b7154e, D-001, D-003, D-006_

#### Source tax result
For every employee subject to source tax Lonio computes the tariff code = tariff letter + child digit + church-tax suffix (e.g. C1Y, L0Y) and records it for HR. Liechtenstein residents with daily return or at most 45 non-return days get 'in principle no source tax liability, subject to the double taxation agreement' instead, flagged for HR. Always recomputed from the latest answers.

| # | Subject to source tax | Liechtenstein: in principle no source tax | Country of home address | → Result | Sources |
|---|---|---|---|---|---|
| 1 | no | - | - | No tariff code (not subject to source tax) | F-hr_transcript-b6d9b3 |
| 2 | yes | yes | Liechtenstein | 'In principle no source tax liability, subject to the double taxation agreement', flagged for HR | F-zh_source_tax_calculator-e80d8f, D-007 |
| 3 | yes | no | Liechtenstein | Tariff code, subject to the double taxation agreement | F-zh_source_tax_calculator-ab4e1e, D-007 |
| 4 | yes | - | not Liechtenstein | Tariff code (letter + child digit + church-tax suffix) | F-zh_source_tax_calculator-ecef37, F-zh_source_tax_calculator-2eab9a, D-001 |

_Status: decision · Sources: F-zh_source_tax_calculator-ecef37, F-zh_source_tax_calculator-e80d8f, F-zh_source_tax_calculator-ab4e1e, F-hr_transcript-4e180e, D-001, D-007, D-034, D-037_

<a id="SEC-06-children"></a>

## 6. Children for the source tax tariff

Ask employees subject to source tax about each child, following the calculator's per-child logic, to decide which children count for the tariff digit and whether a single employee gets the H tariff.

| Story | Priority | Status |
|---|---|---|
| [US-06.1 – Ask each child's age status and household, only where the tariff needs it](stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md) | P1 | decision |
| [US-06.2 – Ask custody and common household for a minor child living with the employee](stories/US-06.2-ask-custody-and-common-household-for-a-minor-child-living.md) | P1 | inferred |
| [US-06.3 – Ask custody and alternating care for a minor child not living with the employee](stories/US-06.3-ask-custody-and-alternating-care-for-a-minor-child-not.md) | P1 | inferred |
| [US-06.4 – Ask who contributes more to the child's maintenance](stories/US-06.4-ask-who-contributes-more-to-the-child-s-maintenance.md) | P1 | decision |
| [US-06.5 – Ask household and maintenance for a child of age in first education](stories/US-06.5-ask-household-and-maintenance-for-a-child-of-age-in-first.md) | P1 | inferred |
| [US-06.6 – Derive the child digit and the single-parent H tariff](stories/US-06.6-derive-the-child-digit-and-the-single-parent-h-tariff.md) | P1 | inferred |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Children
| | |
|---|---|
| **What?** | Whether the employee has biological or adopted children. For married employees and registered partners this includes the children of the spouse / partner. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee is subject to source tax |
| **When is it required?** | Whenever asked |
| **Depends on** | Subject to source tax |
| **Who needs it?** | source tax office: Opens the child questions that determine the child digit and the H tariff |
| **Status · sources** | decision · F-zh_source_tax_calculator-103b19, F-zh_source_tax_calculator-a166c7, F-zh_source_tax_calculator-a33b65, F-zh_source_tax_calculator-ab8a06, F-zh_source_tax_calculator-b62b85, F-zh_source_tax_calculator-75cd87, D-001 |
| **Notes** | Flow step 6. The wording differs for married/partnered vs single employees. |

#### Child: minor or of age in first education
| | |
|---|---|
| **What?** | For each child: whether the child is a minor, of age and in first education, or neither. 'Neither' ends the questions for this child (child does not count). |
| **Allowed values** | Minor · Of age and in first education · Neither |
| **When do we ask?** | For each child, if the employee has children |
| **When is it required?** | Whenever asked |
| **Depends on** | Children |
| **Who needs it?** | source tax office: Decides whether and how the child counts for the tariff |
| **Status · sources** | decision · F-zh_source_tax_calculator-052c98, F-zh_source_tax_calculator-09b06d, F-zh_source_tax_calculator-42d590, F-zh_source_tax_calculator-987091, F-zh_source_tax_calculator-fd9a15, D-001 |
| **Notes** | Flow step 6, child block repeated per child (employee can add further children). Expressions describe one child. |

#### Child lives in the same household
| | |
|---|---|
| **What?** | For each child that is a minor or of age in first education: whether the child lives in the employee's household. |
| **Allowed values** | yes · no |
| **When do we ask?** | For each child that is a minor or of age and in first education |
| **When is it required?** | Whenever asked |
| **Depends on** | Child: minor or of age in first education |
| **Who needs it?** | source tax office: Child counting and H tariff |
| **Status · sources** | decision · F-zh_source_tax_calculator-5725a8, F-zh_source_tax_calculator-3a75cc, F-zh_source_tax_calculator-7c667f, D-001 |
| **Notes** | Per child. |

#### Parental custody (child in household)
| | |
|---|---|
| **What?** | For a minor child in the employee's household: whether custody is shared or sole. |
| **Allowed values** | Shared custody · Sole custody |
| **When do we ask?** | For each minor child living in the same household |
| **When is it required?** | Whenever asked |
| **Depends on** | Child: minor or of age in first education, Child lives in the same household |
| **Who needs it?** | source tax office: Sole custody counts the child (H for single employees) |
| **Status · sources** | decision · F-zh_source_tax_calculator-f7f3ea, F-zh_source_tax_calculator-c09dc1, F-zh_source_tax_calculator-509a7d, D-001 |
| **Notes** | Per child. |

#### Common household with the other parent
| | |
|---|---|
| **What?** | Whether the employee lives in a common household with the child's other parent. |
| **Allowed values** | yes · no |
| **When do we ask?** | For each child in the same household that is either a minor with shared custody or of age and in first education |
| **When is it required?** | Whenever asked |
| **Depends on** | Child: minor or of age in first education, Parental custody (child in household), Child lives in the same household |
| **Who needs it?** | source tax office: Child counting and H tariff |
| **Status · sources** | decision · F-zh_source_tax_calculator-d79949, F-zh_source_tax_calculator-e72e42, F-zh_source_tax_calculator-6dcf5c, D-001 |
| **Notes** | Per child. |

#### Shared custody (child not in household, married)
| | |
|---|---|
| **What?** | For married / partnered employees with a minor child outside the household: whether there is shared custody. |
| **Allowed values** | yes · no |
| **When do we ask?** | For each minor child not in the household, if the employee is married or in a registered partnership |
| **When is it required?** | Whenever asked |
| **Depends on** | Child: minor or of age in first education, Child lives in the same household, Civil status |
| **Who needs it?** | source tax office: Child counting |
| **Status · sources** | decision · F-zh_source_tax_calculator-fe0305, F-zh_source_tax_calculator-d2e516, F-zh_source_tax_calculator-7dcce6, D-001, D-003 |
| **Notes** | Per child. |

#### Parental custody (child not in household, single)
| | |
|---|---|
| **What?** | For single, divorced, widowed or separated employees with a minor child outside the household: whether the employee has parental custody. |
| **Allowed values** | yes · no |
| **When do we ask?** | For each minor child not in the household, if the employee is single, divorced, widowed or separated |
| **When is it required?** | Whenever asked |
| **Depends on** | Child: minor or of age in first education, Child lives in the same household, Civil status |
| **Who needs it?** | source tax office: Child counting and H tariff |
| **Status · sources** | decision · F-zh_source_tax_calculator-956f07, F-zh_source_tax_calculator-32fec9, F-zh_source_tax_calculator-fb4a56, D-001, D-003 |
| **Notes** | Per child. |

#### Alternating care
| | |
|---|---|
| **What?** | Whether the child is in alternating care between the parents. |
| **Allowed values** | yes · no |
| **When do we ask?** | For a minor child in the household with shared custody and no common household with the other parent; or a minor child outside the household with shared custody (married) or parental custody (single) |
| **When is it required?** | Whenever asked |
| **Depends on** | Child: minor or of age in first education, Common household with the other parent, Parental custody (child not in household, single), Parental custody (child in household), Child lives in the same household, Shared custody (child not in household, married) |
| **Who needs it?** | source tax office: Child counting and H tariff |
| **Status · sources** | decision · F-zh_source_tax_calculator-da19df, F-zh_source_tax_calculator-ebd7b3, F-zh_source_tax_calculator-64ac33, D-001 |
| **Notes** | Per child. |

#### Larger financial contributor to the child's maintenance
| | |
|---|---|
| **What?** | Who makes the larger financial contribution to the child's maintenance: the employee or the other parent. |
| **Allowed values** | The employee · The other parent |
| **When do we ask?** | If the child is in alternating care; or, for single, divorced, widowed or separated employees, if the child lives in the household and there is a common household with the other parent |
| **When is it required?** | Whenever asked |
| **Depends on** | Alternating care, Common household with the other parent, Child lives in the same household, Civil status |
| **Who needs it?** | source tax office: Child counting and H tariff |
| **Status · sources** | decision · F-zh_source_tax_calculator-cdd0b6, F-zh_source_tax_calculator-939b3b, F-zh_source_tax_calculator-ad867a, D-001 |
| **Notes** | Per child. |

#### Employee pays more than 50% of the child's maintenance
| | |
|---|---|
| **What?** | For a child of age in first education: whether the employee mainly (more than 50%) pays for the child's maintenance. |
| **Allowed values** | yes · no |
| **When do we ask?** | For a child of age in first education that lives outside the household, or in the household without a common household with the other parent |
| **When is it required?** | Whenever asked |
| **Depends on** | Child: minor or of age in first education, Common household with the other parent, Child lives in the same household |
| **Who needs it?** | source tax office: Child counting and H tariff |
| **Status · sources** | decision · F-zh_source_tax_calculator-b008fe, F-zh_source_tax_calculator-cb54d9, F-zh_source_tax_calculator-cd1015, D-001 |
| **Notes** | Per child. |

### Business rules in this section

#### Child result (per child)
For each child the answers decide whether the child counts for the tariff, and for single (incl. divorced, separated, widowed) employees whether it counts with H. Rows marked inferred were not observed in the calculator and must be checked (OQ-calculator-coverage). Expression describes one child.

| # | Civil status for source tax | Child age status | Same household | Custody (in household) | Common household with other parent | Shared custody (not in household, married) | Parental custody (not in household, single) | Alternating care | Larger financial contributor | More than 50% maintenance | → Result | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | any | Neither | - | - | - | - | - | - | - | - | does not count | F-zh_source_tax_calculator-987091 |
| 2 | Married or registered partnership | Minor | yes | Sole custody | - | - | - | - | - | - | counts | F-zh_source_tax_calculator-c53a22 |
| 3 | Married or registered partnership | Minor | yes | Shared custody | yes | - | - | - | - | - | counts | F-zh_source_tax_calculator-3058a4 |
| 4 | Married or registered partnership | Minor | yes | Shared custody | no | - | - | no | - | - | does not count | F-zh_source_tax_calculator-3058a4 |
| 5 | Married or registered partnership | Minor | yes | Shared custody | no | - | - | yes | The other parent | - | does not count | F-zh_source_tax_calculator-3058a4 |
| 6 | Married or registered partnership | Minor | yes | Shared custody | no | - | - | yes | The employee | - | counts (inferred) | F-zh_source_tax_calculator-56e79b, D-009 |
| 7 | Married or registered partnership | Minor | no | - | - | no | - | - | - | - | does not count | F-zh_source_tax_calculator-56e79b |
| 8 | Married or registered partnership | Minor | no | - | - | yes | - | yes | The employee | - | counts | F-zh_source_tax_calculator-56e79b |
| 9 | Married or registered partnership | Minor | no | - | - | yes | - | yes | The other parent | - | does not count (inferred) | F-zh_source_tax_calculator-3058a4, D-009 |
| 10 | Married or registered partnership | Minor | no | - | - | yes | - | no | - | - | does not count (inferred) | F-zh_source_tax_calculator-3058a4, D-009 |
| 11 | Married or registered partnership | Of age and in first education | yes | - | yes | - | - | - | - | - | counts | F-zh_source_tax_calculator-50f74a |
| 12 | Married or registered partnership | Of age and in first education | yes | - | no | - | - | - | - | yes | counts (inferred) | F-zh_source_tax_calculator-562299, D-009 |
| 13 | Married or registered partnership | Of age and in first education | yes | - | no | - | - | - | - | no | does not count (inferred) | F-zh_source_tax_calculator-50f74a, D-009 |
| 14 | Married or registered partnership | Of age and in first education | no | - | - | - | - | - | - | yes | counts (inferred) | F-zh_source_tax_calculator-562299, D-009 |
| 15 | Married or registered partnership | Of age and in first education | no | - | - | - | - | - | - | no | does not count | F-zh_source_tax_calculator-50f74a |
| 16 | Single, divorced, separated or widowed | Minor | yes | Sole custody | - | - | - | - | - | - | counts with H | F-zh_source_tax_calculator-c53a22, F-zh_source_tax_calculator-96658b |
| 17 | Single, divorced, separated or widowed | Minor | yes | Shared custody | yes | - | - | - | The employee | - | counts with H | F-zh_source_tax_calculator-96658b |
| 18 | Single, divorced, separated or widowed | Minor | yes | Shared custody | yes | - | - | - | The other parent | - | does not count | F-zh_source_tax_calculator-38dd4a |
| 19 | Single, divorced, separated or widowed | Minor | yes | Shared custody | no | - | - | no | - | - | counts with H | F-zh_source_tax_calculator-38dd4a |
| 20 | Single, divorced, separated or widowed | Minor | yes | Shared custody | no | - | - | yes | The employee | - | counts with H | F-zh_source_tax_calculator-96658b |
| 21 | Single, divorced, separated or widowed | Minor | yes | Shared custody | no | - | - | yes | The other parent | - | does not count (inferred) | F-zh_source_tax_calculator-38dd4a, D-009 |
| 22 | Single, divorced, separated or widowed | Minor | no | - | - | - | yes | yes | The employee | - | counts with H | F-zh_source_tax_calculator-c2faa7 |
| 23 | Single, divorced, separated or widowed | Minor | no | - | - | - | yes | yes | The other parent | - | does not count (inferred) | F-zh_source_tax_calculator-c2faa7, D-009 |
| 24 | Single, divorced, separated or widowed | Minor | no | - | - | - | yes | no | - | - | does not count (inferred) | F-zh_source_tax_calculator-c2faa7, D-009 |
| 25 | Single, divorced, separated or widowed | Minor | no | - | - | - | no | - | - | - | does not count | F-zh_source_tax_calculator-c2faa7 |
| 26 | Single, divorced, separated or widowed | Of age and in first education | yes | - | yes | - | - | - | The employee | - | counts with H (inferred) | F-zh_source_tax_calculator-96658b, D-009 |
| 27 | Single, divorced, separated or widowed | Of age and in first education | yes | - | yes | - | - | - | The other parent | - | does not count (inferred) | F-zh_source_tax_calculator-38dd4a, D-009 |
| 28 | Single, divorced, separated or widowed | Of age and in first education | yes | - | no | - | - | - | - | yes | counts with H | F-zh_source_tax_calculator-562299 |
| 29 | Single, divorced, separated or widowed | Of age and in first education | yes | - | no | - | - | - | - | no | does not count (inferred) | F-zh_source_tax_calculator-562299, D-009 |
| 30 | Single, divorced, separated or widowed | Of age and in first education | no | - | - | - | - | - | - | yes | counts | F-zh_source_tax_calculator-562299 |
| 31 | Single, divorced, separated or widowed | Of age and in first education | no | - | - | - | - | - | - | no | does not count (inferred) | F-zh_source_tax_calculator-50f74a, D-009 |

_Status: inferred · Sources: F-zh_source_tax_calculator-987091, F-zh_source_tax_calculator-96658b, F-zh_source_tax_calculator-c53a22, F-zh_source_tax_calculator-3058a4, F-zh_source_tax_calculator-56e79b, F-zh_source_tax_calculator-50f74a, F-zh_source_tax_calculator-38dd4a, F-zh_source_tax_calculator-c2faa7, F-zh_source_tax_calculator-562299, D-001, D-003, D-009_

#### Child digit of the tariff code
The digit equals the number of children that count (with or without H). No children or none counting gives 0.

| # | Number of children that count | → Result | Sources |
|---|---|---|---|
| 1 | 0 | 0 | F-zh_source_tax_calculator-ecef37 |
| 2 | n (1 or more) | n | F-zh_source_tax_calculator-ecef37 |

_Status: decision · Sources: F-zh_source_tax_calculator-ecef37, D-001_

#### Single-parent H tariff
A single, divorced, separated or widowed employee with at least one child counting with H gets the H tariff.

| # | Civil status for source tax | At least one child counts with H | → Result | Sources |
|---|---|---|---|---|
| 1 | Single, divorced, separated or widowed | yes | H tariff | F-zh_source_tax_calculator-96658b |
| 2 | Single, divorced, separated or widowed | no | No H tariff (A) | F-zh_source_tax_calculator-c78e0c |
| 3 | Married or registered partnership | - | No H tariff | F-zh_source_tax_calculator-97139a |

_Status: decision · Sources: F-zh_source_tax_calculator-96658b, D-001, D-003_

<a id="SEC-07-living-abroad"></a>

## 7. Employees living abroad (Germany, Liechtenstein)

Derive the calculator's residence answers from the home address country. Ask employees living in Germany or Liechtenstein the cross-border questions about their expected year, which decide the cross-border tariff or the Liechtenstein result.

| Story | Priority | Status |
|---|---|---|
| [US-07.1 – Derive the calculator's residence answers from the home address](stories/US-07.1-derive-the-calculator-s-residence-answers-from-the-home.md) | P1 | decision |
| [US-07.2 – Decide the cross-border tariff for employees living in Germany](stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md) | P1 | decision |
| [US-07.3 – Determine the source tax outcome for employees living in Liechtenstein](stories/US-07.3-determine-the-source-tax-outcome-for-employees-living-in.md) | P1 | decision |

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Daily return to home in Germany
| | |
|---|---|
| **What?** | For employees living in Germany: whether they expect to return daily to their main residence in Germany. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee is subject to source tax and lives in Germany |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence), Subject to source tax |
| **Who needs it?** | source tax office: Decides whether the cross-border tariff applies |
| **Status · sources** | decision · F-zh_source_tax_calculator-69edd5, F-zh_source_tax_calculator-64ac42, F-zh_source_tax_calculator-31d762, D-001, D-006, D-035 |
| **Notes** | Flow step 6 (cross-border). |

#### Certificate of residence
| | |
|---|---|
| **What?** | Whether the employee has provided a German certificate of residence. 'Not yet' is valid and counts as 'no' for the tariff code. The document goes to HR outside Lonio. |
| **Allowed values** | yes · no · not yet |
| **When do we ask?** | Only if the employee lives in Germany and returns home daily |
| **When is it required?** | Whenever asked |
| **Depends on** | Daily return to home in Germany |
| **Who needs it?** | source tax office: With a certificate the cross-border tariff applies |
| **Status · sources** | decision · F-zh_source_tax_calculator-687e8b, F-zh_source_tax_calculator-823151, F-zh_source_tax_calculator-5f6820, F-zh_source_tax_calculator-4d3ac0, D-035, D-037 |
| **Notes** | A certificate handed in later is updated by HR (D-037). |

#### Daily return reasonable (under 100 km)
| | |
|---|---|
| **What?** | For employees living in Germany who do not return daily: whether a daily return would in principle be reasonable (less than 100 km driving distance). |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Germany and does not return home daily |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence), Daily return to home in Germany |
| **Who needs it?** | source tax office: Decides whether the cross-border tariff applies |
| **Status · sources** | decision · F-zh_source_tax_calculator-d2b3cf, F-zh_source_tax_calculator-087ae5, F-zh_source_tax_calculator-aaece6, F-zh_source_tax_calculator-bc1639, D-001 |

#### More than 60 work-related non-return days expected
| | |
|---|---|
| **What?** | Whether the employee expects more than 60 work-related non-return days in the calendar year (a declaration, no proof uploaded). |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if a daily return to Germany is reasonable but the employee does not return daily |
| **When is it required?** | Whenever asked |
| **Depends on** | Daily return reasonable (under 100 km) |
| **Who needs it?** | source tax office: More than 60 days: normal tariff; otherwise cross-border tariff |
| **Status · sources** | decision · F-zh_source_tax_calculator-e8ffac, F-zh_source_tax_calculator-ea3cd8, F-zh_source_tax_calculator-33ef31, F-zh_source_tax_calculator-b948fd, D-035 |

#### Daily return to home in Liechtenstein
| | |
|---|---|
| **What?** | For employees living in Liechtenstein: whether they expect to return daily to their main residence in Liechtenstein. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee is subject to source tax and lives in Liechtenstein |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence), Subject to source tax |
| **Who needs it?** | source tax office: Daily return: in principle no source tax liability |
| **Status · sources** | decision · F-zh_source_tax_calculator-981b6b, F-zh_source_tax_calculator-a2041b, F-zh_source_tax_calculator-e22d17, F-zh_source_tax_calculator-e80d8f, D-007, D-035 |

#### More than 45 work-related non-return days expected
| | |
|---|---|
| **What?** | For employees living in Liechtenstein who do not return daily: whether they expect more than 45 work-related non-return days in the calendar year. |
| **Allowed values** | yes · no |
| **When do we ask?** | Only if the employee lives in Liechtenstein and does not return home daily |
| **When is it required?** | Whenever asked |
| **Depends on** | Daily return to home in Liechtenstein |
| **Who needs it?** | source tax office: More than 45 days: normal tariff subject to the double taxation agreement; otherwise in principle no source tax liability |
| **Status · sources** | decision · F-zh_source_tax_calculator-e96210, F-zh_source_tax_calculator-0ff846, F-zh_source_tax_calculator-f4ece9, F-zh_source_tax_calculator-ab4e1e, D-007, D-035 |

### Business rules in this section

#### Source tax state of residence
The calculator's residence answers are derived from the home address country: Switzerland, Germany, Liechtenstein, or another country. Switzerland and another country leave the base tariff unchanged.

| # | Country of home address | → Result | Sources |
|---|---|---|---|
| 1 | Switzerland | Main residence in Switzerland | F-zh_source_tax_calculator-52b67a |
| 2 | Germany | Germany (cross-border questions for Germany) | F-zh_source_tax_calculator-d62dd4 |
| 3 | Liechtenstein | Liechtenstein (cross-border questions for Liechtenstein) | F-zh_source_tax_calculator-d62dd4 |
| 4 | any other country | Other country (base tariff) | F-zh_source_tax_calculator-52b67a |

_Status: decision · Sources: F-zh_source_tax_calculator-f29009, F-zh_source_tax_calculator-4c65ae, F-zh_source_tax_calculator-d62dd4, F-zh_source_tax_calculator-52b67a, G-08, D-001_

#### Cross-border tariff applies
For employees living in Germany the cross-border tariff applies with daily return and a certificate of residence ('not yet' counts as no), or without daily return when a return is reasonable and not more than 60 non-return days are expected. All other cases use the normal tariff.

| # | Country of home address | Daily return to Germany | Certificate of residence | Daily return reasonable | More than 60 non-return days | → Result | Sources |
|---|---|---|---|---|---|---|---|
| 1 | Germany | yes | yes | - | - | Cross-border tariff | F-zh_source_tax_calculator-4d3ac0, F-zh_source_tax_calculator-89a9f1 |
| 2 | Germany | yes | no or not yet | - | - | Normal tariff | F-zh_source_tax_calculator-4d3ac0, D-035 |
| 3 | Germany | no | - | yes | no | Cross-border tariff | F-zh_source_tax_calculator-b948fd |
| 4 | Germany | no | - | yes | yes | Normal tariff | F-zh_source_tax_calculator-b948fd |
| 5 | Germany | no | - | no | - | Normal tariff | F-zh_source_tax_calculator-bc1639 |
| 6 | not Germany | - | - | - | - | Normal tariff | F-zh_source_tax_calculator-52b67a, F-zh_source_tax_calculator-89a9f1 |

_Status: decision · Sources: F-zh_source_tax_calculator-89a9f1, F-zh_source_tax_calculator-4d3ac0, F-zh_source_tax_calculator-b948fd, D-001, D-035_

#### Liechtenstein: in principle no source tax
For employees living in Liechtenstein, daily return or not more than 45 non-return days gives 'in principle no source tax liability, subject to the double taxation agreement' instead of a tariff code, flagged for HR. More than 45 non-return days gives the normal tariff code subject to the double taxation agreement.

| # | Country of home address | Daily return to Liechtenstein | More than 45 non-return days | → Result | Sources |
|---|---|---|---|---|---|
| 1 | Liechtenstein | yes | - | In principle no source tax liability (flag for HR) | F-zh_source_tax_calculator-e80d8f, D-007 |
| 2 | Liechtenstein | no | no | In principle no source tax liability (flag for HR) | F-zh_source_tax_calculator-ab4e1e, D-007 |
| 3 | Liechtenstein | no | yes | Normal tariff code, subject to the double taxation agreement | F-zh_source_tax_calculator-ab4e1e, D-007 |
| 4 | not Liechtenstein | - | - | Does not apply | D-007 |

_Status: decision · Sources: F-zh_source_tax_calculator-e80d8f, F-zh_source_tax_calculator-ab4e1e, D-007, D-034_

<a id="SEC-08-completion-and-submission"></a>

## 8. Completing and submitting the questionnaire

Close the questionnaire. Remind non-Swiss employees and employees living abroad to bring their permit, and on submission record only the answers to questions that still apply.

| Story | Priority | Status |
|---|---|---|
| [US-08.1 – Remind employees to bring their permit on the first working day](stories/US-08.1-remind-employees-to-bring-their-permit-on-the-first-working.md) | P2 | decision |
| [US-08.2 – Discard answers that no longer apply on submission](stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md) | P1 | decision |
| [US-08.3 – Questionnaire is read-only for the employee after submission](stories/US-08.3-questionnaire-is-read-only-for-the-employee-after-submission.md) | P2 | decision |

### Business rules in this section

#### Permit reminder
At the end of the questionnaire, every non-Swiss employee and every employee living abroad is reminded to bring their permit on the first working day. HR words it so a Swiss citizen living abroad sees it does not apply to them. It collects no data.

| # | Country of home address | Swiss citizen | → Result | Sources |
|---|---|---|---|---|
| 1 | Switzerland | yes | No reminder | D-010 |
| 2 | Switzerland | no | Show reminder | F-hr_transcript-c53552, D-010 |
| 3 | not Switzerland | - | Show reminder | D-010, D-038 |

_Status: decision · Sources: F-hr_transcript-c53552, D-010, D-038_

#### Discard answers that no longer apply
If the employee changes an earlier answer so that later questions no longer apply, those answers are kept while the employee goes back and forth but discarded on submission. After submission the questionnaire is read-only for the employee; changes are made by HR and all derived results are derived again from the latest answers.

_Status: decision · Sources: G-01, D-036, D-037_

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
- **F-hr_transcript-09b3fe** (hr_transcript): For married employees, the source tax calculator asks additional questions, e.g. whether the husband or wife works.
  - "It changes the questions in the calculator, yes. Whether the husband or wife works." — hr_transcript/T-044, Anna
- **F-hr_transcript-1a20bb** (hr_transcript): Employees who work in Switzerland but live abroad (e.g. Konstanz in Germany, Liechtenstein) are always subject to source tax, regardless of nationality – even Swiss citizens.
  - "Those people do source tax because they work here and they don't live here. And there it doesn't matter what passport you have, by the way." — hr_transcript/T-048, Anna
  - "Stefan is actually Swiss, and he still has it." — hr_transcript/T-048, Anna
  - "So someone living abroad and working here always does it?" — hr_transcript/T-049, Leo
  - "Yes." — hr_transcript/T-050, Anna
- **F-hr_transcript-1d5c07** (hr_transcript): Consolidated: insurance start date is derived from the (latest confirmed) first working day: if it is the 1st of a month, insurance starts that day; otherwise on the 1st of the following month.
  - "because insurance starts on the first of the following month." — hr_transcript/T-026, Anna
  - "Unless somebody starts exactly on the first, of course, then it's just that day." — hr_transcript/T-028, Anna
- **F-hr_transcript-2334d8** (hr_transcript): If the employee is married, the pension fund wants the date of birth of the husband or wife.
  - "And if someone is married, they want the date of birth of the husband or wife." — hr_transcript/T-032, Anna
- **F-hr_transcript-30d25c** (hr_transcript): Pension fund insurance starts on the first of the month following the first working day (e.g. first working day 15 March → insurance start 1 April).
  - "because insurance starts on the first of the following month. So for her that was the first of April" — hr_transcript/T-026, Anna
- **F-hr_transcript-35fae3** (hr_transcript): The employee's nationality is needed to determine source tax liability.
  - "If you don't have a Swiss passport, you do source tax." — hr_transcript/T-010, Anna
- **F-hr_transcript-3907fe** (hr_transcript): Muster AG has at least one employee (Daniel, finance) in a registered partnership.
  - "we do have one colleague in a registered partnership. Daniel, in finance." — hr_transcript/T-034, Anna
- **F-hr_transcript-4ad146** (hr_transcript): For non-Swiss employees, the permit type (e.g. C permit vs B permit) is needed to determine source tax liability.
  - "So, not the people with a C permit." — hr_transcript/T-038, Anna
  - "Brazilian, B permit" — hr_transcript/T-044, Anna
- **F-hr_transcript-4e180e** (hr_transcript): The Zurich source tax calculator (canton website, yields the tariff code) is used for every employee, regardless of where they live; HR acknowledges this is not exactly how it works but it is the approach for now, and Leo agreed to keep it.
  - "For everybody I use Zurich, by the way. I know it's not exactly how it works, but that's what we do for now." — hr_transcript/T-012, Anna
  - "Understood. We'll keep that for now." — hr_transcript/T-013, Leo
- **F-hr_transcript-5518ad** (hr_transcript): HR needs the employee's home address.
  - "Yes, I need the address, obviously." — hr_transcript/T-014, Anna
- **F-hr_transcript-563a9f** (hr_transcript): Today HR sits with the employee's answers and clicks through the Zurich calculator, which gives the tariff code.
  - "The one that gives you the tariff code. I sit with the answers and click through it." — hr_transcript/T-012, Anna
- **F-hr_transcript-66fe15** (hr_transcript): Nothing beyond a normal postal address is needed: the address as one would write it on an envelope.
  - "No, no. Just a normal address, the way you would write it on an envelope." — hr_transcript/T-016, Anna
- **F-hr_transcript-845204** (hr_transcript): Correction: non-Swiss employees with a C permit are not subject to source tax; they are treated like Swiss people for this.
  - "No, that's actually not right." — hr_transcript/T-038, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — hr_transcript/T-038, Anna
- **F-hr_transcript-872bd7** (hr_transcript): The employee's first working day is needed for the pension fund; it is the most important item.
  - "I need their first working day. That's the number one thing" — hr_transcript/T-024, Anna
- **F-hr_transcript-ab8886** (hr_transcript): For employees living abroad the source tax calculator has many more questions; Germany has its own forms whose names Anna cannot recall. Leo noted the calculator will tell which questions apply.
  - "And with them the calculator gets much more complicated, there are more questions. Germany has its own forms, I can never remember what they're called." — hr_transcript/T-050, Anna
  - "Okay, that's fine, the calculator will tell us." — hr_transcript/T-051, Leo
- **F-hr_transcript-b6d9b3** (hr_transcript): Consolidated final rule: an employee is subject to source tax if they live abroad (home address country not Switzerland), regardless of nationality. If they live in Switzerland, they are subject only if they are not Swiss and do not hold a C permit, unless they are married to a spouse who is Swiss or holds a C permit and lives in Switzerland (then not subject).
  - "If you don't have a Swiss passport, you do source tax." — hr_transcript/T-010, Anna
  - "So, not the people with a C permit." — hr_transcript/T-038, Anna
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — hr_transcript/T-044, Anna
  - "Those people do source tax because they work here and they don't live here." — hr_transcript/T-048, Anna
- **F-hr_transcript-b84498** (hr_transcript): Source tax questions should only be asked to employees who are subject to source tax, not to everybody.
  - "Because I never know up front who has to answer those questions." — hr_transcript/T-008, Anna
  - "So who actually needs to answer them?" — hr_transcript/T-009, Leo
- **F-hr_transcript-c53552** (hr_transcript): HR would love the form to remind people to bring their permit on the first day; not decided (wording to be looked at later).
  - "What I would love is if the form could remind people to bring their permit. Half of them forget." — hr_transcript/T-042, Anna
  - "We can look at the wording later." — hr_transcript/T-043, Leo
- **F-hr_transcript-ce8ca4** (hr_transcript): The pension fund asks for the employee's civil status.
  - "Yes, the civil status. They ask for that." — hr_transcript/T-032, Anna
- **F-hr_transcript-d7431e** (hr_transcript): An employee married to someone Swiss or to someone with a C permit, where that spouse lives in Switzerland, is not subject to source tax (e.g. Tomás: Brazilian, B permit, Swiss wife, living in Winterthur → no source tax).
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — hr_transcript/T-044, Anna
  - "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." — hr_transcript/T-044, Anna
- **F-hr_transcript-d7a23b** (hr_transcript): Incident: Julia moved her first working day to 15 March, HR did not update it, the fund had a wrong insurance start date, leading to an unfriendly letter and weeks of fixing. This implies the insurance start date must follow changes to the first working day.
  - "She moved her first working day to the 15th of March, and I didn't update it." — hr_transcript/T-026, Anna
  - "It took weeks to fix." — hr_transcript/T-028, Anna
- **F-hr_transcript-e3721e** (hr_transcript): The employee should confirm the first working day, because it changes often (e.g. people negotiate an earlier exit with their old employer).
  - "I ask them to confirm it, because it moves more often than you'd think." — hr_transcript/T-024, Anna
  - "People negotiate with their old employer, they get out a week earlier." — hr_transcript/T-026, Anna
- **F-hr_transcript-e505f8** (hr_transcript): Whether the employee lives abroad can be derived from the country of the home address, which is relevant for source tax liability.
  - "Street, number, postcode, town, country." — hr_transcript/T-014, Anna
  - "Those people do source tax because they work here and they don't live here." — hr_transcript/T-048, Anna
- **F-hr_transcript-ec57d3** (hr_transcript): The address must be complete: street, house number, postcode, town and country, because HR posts many documents to employees.
  - "The full address. Street, number, postcode, town, country. We post a lot of documents to people, so it has to be complete." — hr_transcript/T-014, Anna
- **F-hr_transcript-f197d6** (hr_transcript): Unknown how the pension fund screen handles a registered partnership and whether the fund wants the partner's details too.
  - "I honestly don't know what the fund's screen does in that case, or if they want the partner's details too." — hr_transcript/T-036, Anna
- **F-hr_transcript-f3ce84** (hr_transcript): For married employees, the spouse's nationality, permit (if any) and whether the spouse lives in Switzerland are needed to determine source tax liability.
  - "So you need to know about the spouse as well." — hr_transcript/T-045, Leo
  - "Yes. Their nationality, their permit if they have one, and that they live here." — hr_transcript/T-046, Anna
- **F-hr_transcript-fdf50a** (hr_transcript): Exception: if the first working day is exactly the first of a month, insurance starts on that day.
  - "Unless somebody starts exactly on the first, of course, then it's just that day." — hr_transcript/T-028, Anna
- **F-pension_portal-0eed50** (pension_portal): When Civil status is Married and the spouse's date of birth is left empty, registration is rejected with 'Spouse's date of birth is required.'
  - "Married" — 07-married-missing-spouse.png (pension_portal/S07-E20)
  - "Spouse's date of birth is required." — 07-married-missing-spouse.png (pension_portal/S07-E23)
- **F-pension_portal-3432a9** (pension_portal): The Canton dropdown offers exactly the 26 Swiss cantons: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for living outside Switzerland.
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
- **F-pension_portal-39bab1** (pension_portal, inferred): The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected).
  - "Spouse's date of birth" — 05-married.png (pension_portal/S05-E21)
  - "Married" — 05-married.png (pension_portal/S05-E20)
  - "Spouse's date of birth" — 07-married-missing-spouse.png (pension_portal/S07-E21)
  - "Married" — 07-married-missing-spouse.png (pension_portal/S07-E20)
  - "Single" — 04-single.png (pension_portal/S04-E20)
- **F-pension_portal-3cfe89** (pension_portal): Fields marked with an asterisk are required; all visible fields on the form carry the marker.
  - "Fields marked * are required." — 01-empty.png (pension_portal/S01-E19)
- **F-pension_portal-3d1ae4** (pension_portal): The Civil status dropdown offers exactly: Single, Married, Divorced, Widowed.
  - "Civil status" — 03-civil-status-list.png (pension_portal/S03-E19)
  - "Single" — 03-civil-status-list.png (pension_portal/S03-E21)
  - "Married" — 03-civil-status-list.png (pension_portal/S03-E22)
  - "Divorced" — 03-civil-status-list.png (pension_portal/S03-E23)
  - "Widowed" — 03-civil-status-list.png (pension_portal/S03-E24)
- **F-pension_portal-44a27b** (pension_portal): Submitting the form with required fields empty shows the banner 'Please correct the highlighted fields.' and highlights each missing field with the message '<Field> is required.' (First name, Last name, Date of birth, Canton, Insurance start date, Civil status).
  - "Please correct the highlighted fields." — 06-required-errors.png (pension_portal/S06-E05)
  - "First name is required." — 06-required-errors.png (pension_portal/S06-E08)
  - "Last name is required." — 06-required-errors.png (pension_portal/S06-E10)
  - "Date of birth is required." — 06-required-errors.png (pension_portal/S06-E13)
  - "Canton is required." — 06-required-errors.png (pension_portal/S06-E16)
  - "Insurance start date is required." — 06-required-errors.png (pension_portal/S06-E20)
  - "Civil status is required." — 06-required-errors.png (pension_portal/S06-E23)
- **F-pension_portal-509cbe** (pension_portal): The pension fund registration form has a required 'Insurance start date' field (in the Insurance section).
  - "Insurance start date" — 01-empty.png (pension_portal/S01-E13)
  - "Insurance" — 01-empty.png (pension_portal/S01-E12)
- **F-pension_portal-587d3f** (pension_portal): The pension fund registration form has a required 'Canton' dropdown field (in the Employee section).
  - "Canton" — 01-empty.png (pension_portal/S01-E10)
  - "Employee" — 01-empty.png (pension_portal/S01-E05)
- **F-pension_portal-88b436** (pension_portal): The pension fund registration form has a required 'Date of birth' field for the employee.
  - "Date of birth" — 01-empty.png (pension_portal/S01-E08)
- **F-pension_portal-967bc9** (pension_portal): The employee's date of birth is entered in the format DD.MM.YYYY.
  - "DD.MM.YYYY" — 01-empty.png (pension_portal/S01-E09)
- **F-pension_portal-9b24c5** (pension_portal, inferred): The civil status list has no option for registered partnership or separated; it is unclear how such employees are to be registered.
  - "Civil status" — 03-civil-status-list.png (pension_portal/S03-E19)
  - "Widowed" — 03-civil-status-list.png (pension_portal/S03-E24)
- **F-pension_portal-a0065b** (pension_portal): The pension fund registration form has a required (when shown) 'Spouse's date of birth' field.
  - "Spouse's date of birth" — 05-married.png (pension_portal/S05-E21)
- **F-pension_portal-b359c3** (pension_portal, inferred): The label 'Canton' does not state whether it is the canton of residence or of work, and the list only contains Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. a cross-border commuter).
  - "Canton" — 01-empty.png (pension_portal/S01-E10)
  - "Zurich" — 02-canton-list.png (pension_portal/S02-E37)
- **F-pension_portal-b5c835** (pension_portal): The pension fund registration form has a required 'First name' text field.
  - "First name" — 01-empty.png (pension_portal/S01-E06)
- **F-pension_portal-c688e4** (pension_portal): The pension fund registration form has a required 'Last name' text field.
  - "Last name" — 01-empty.png (pension_portal/S01-E07)
- **F-pension_portal-dd8126** (pension_portal): The insurance start date is entered as DD.MM.YYYY and must be the 1st of a month.
  - "DD.MM.YYYY. Must be the 1st of a month." — 01-empty.png (pension_portal/S01-E14)
- **F-pension_portal-ec4512** (pension_portal): The pension fund registration form has a required 'Civil status' dropdown field.
  - "Civil status" — 01-empty.png (pension_portal/S01-E15)
- **F-pension_portal-ef28c3** (pension_portal): The spouse's date of birth is entered in the format DD.MM.YYYY.
  - "DD.MM.YYYY" — 05-married.png (pension_portal/S05-E23)
- **F-zh_source_tax_calculator-0137bf** (zh_source_tax_calculator): The spouse employment question is asked only when civil status is 'Verheiratet oder eingetragene Partnerschaft'.
  - "Ist der Ehegatte / eingetragene Partner erwerbstätig oder bezieht er/sie Ersatzeinkünfte?" — zh_source_tax_calculator/C-Q04
- **F-zh_source_tax_calculator-051bb9** (zh_source_tax_calculator): Civil status has two options: 'Verheiratet oder eingetragene Partnerschaft' (married or registered partnership) and 'Ledig, Geschieden, Getrennt, Verwitwet' (single, divorced, separated, widowed).
  - "Options: Verheiratet oder eingetragene Partnerschaft | Ledig, Geschieden, Getrennt, Verwitwet" — zh_source_tax_calculator/C-Q02
- **F-zh_source_tax_calculator-052c98** (zh_source_tax_calculator): For each child, the calculator asks whether the child is a minor or of age and in first education.
  - "Kind minderjährig oder volljährig und in Erstausbildung?" — zh_source_tax_calculator/C-Q07
  - "Section heading: 'Angaben zu den Kindern'" — zh_source_tax_calculator/C-Q07
- **F-zh_source_tax_calculator-087ae5** (zh_source_tax_calculator): Daily return reasonable options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q20
- **F-zh_source_tax_calculator-09b06d** (zh_source_tax_calculator): Child age status options: 'Minderjährig' | 'Volljährig und in Erstausbildung' | 'weder noch'.
  - "Options: Minderjährig | Volljährig und in Erstausbildung | weder noch" — zh_source_tax_calculator/C-Q07
- **F-zh_source_tax_calculator-0ff846** (zh_source_tax_calculator): More than 45 non-return days options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q23
- **F-zh_source_tax_calculator-103b19** (zh_source_tax_calculator): For married persons, the calculator asks whether there are biological or adopted children of the person or of the spouses/partners.
  - "Leibliche oder adoptierte Kinder der Person oder der Ehegatten bzw. Partner?" — zh_source_tax_calculator/C-Q05
- **F-zh_source_tax_calculator-208104** (zh_source_tax_calculator): The calculator asks for the person's denomination (Konfession).
  - "Konfession" — zh_source_tax_calculator/C-Q03
- **F-zh_source_tax_calculator-2eab9a** (zh_source_tax_calculator): Denomination sets the church-tax suffix of the tariff: 'Y' for röm.-kath., christ.-kath., evang.-ref.; 'N' for 'Keine oder andere'.
  - "Sets the church-tax suffix: Y = röm.-kath., christ.-kath., evang.-ref.; N = Keine oder andere" — zh_source_tax_calculator/C-Q03
  - "result Tarif: A0Y" — zh_source_tax_calculator/C-V01
  - "result Tarif: A0N" — zh_source_tax_calculator/C-V02
- **F-zh_source_tax_calculator-3058a4** (zh_source_tax_calculator): Married person, minor child in same household, shared custody: common household with the other parent counts the child (C1Y); no common household counts the child only if... observed: alternating care with other parent as main contributor -> 0 (C0Y), no alternating care -> 0 (C0Y).
  - ""Q10": "Ja", "Q16": "Ja"} -> result Tarif: C1Y" — zh_source_tax_calculator/C-V09
  - ""Q11": "Ja", "Q12": "Anderer Elternteil", "Q16": "Ja"} -> result Tarif: C0Y" — zh_source_tax_calculator/C-V10
  - ""Q10": "Nein", "Q11": "Nein", "Q16": "Ja"} -> result Tarif: C0Y" — zh_source_tax_calculator/C-V11
- **F-zh_source_tax_calculator-31d762** (zh_source_tax_calculator): Daily return to Germany (Q18) is asked only when income type is 'Erwerbseinkommen' and state of residence is Deutschland.
  - "Tägliche Rückkehr an den Hauptwohnsitz in Deutschland?" — zh_source_tax_calculator/C-Q18
- **F-zh_source_tax_calculator-32fec9** (zh_source_tax_calculator): Parental care (child not in household, single) options: Ja | Nein.
  - "Elterliche Sorge Options: Ja | Nein" — zh_source_tax_calculator/C-Q14
- **F-zh_source_tax_calculator-33ef31** (zh_source_tax_calculator): Q21 is asked only when daily return is reasonable (Q20 = Ja).
  - "Nachweis von mehr als 60 beruflich bedingten Nichtrückkehrtagen im Kalenderjahr beigebracht?" — zh_source_tax_calculator/C-Q21
- **F-zh_source_tax_calculator-38dd4a** (zh_source_tax_calculator): Single person, minor child in household with shared custody: common household with other parent and other parent main contributor -> A0N (not counted); no common household and no alternating care -> H1N.
  - ""Q10": "Ja", "Q12": "Anderer Elternteil", "Q16": "Ja"} -> result Tarif: A0N (Kind Ergebnis: A0)" — zh_source_tax_calculator/C-V18
  - ""Q10": "Nein", "Q11": "Nein", "Q16": "Ja"} -> result Tarif: H1N (Kind Ergebnis: H1)" — zh_source_tax_calculator/C-V19
- **F-zh_source_tax_calculator-3a75cc** (zh_source_tax_calculator): Child same household options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q08
- **F-zh_source_tax_calculator-42d590** (zh_source_tax_calculator): Child questions are shown only when the person has children (Q05 = Ja or Q06 = Ja), with one block per child headed 'Kind 1', 'Kind 2', ….
  - "Kind minderjährig oder volljährig und in Erstausbildung?" — zh_source_tax_calculator/C-Q07
- **F-zh_source_tax_calculator-4c65ae** (zh_source_tax_calculator): The calculator asks for the state of residence (Wohnsitzstaat).
  - "Wohnsitzstaat" — zh_source_tax_calculator/C-Q17
- **F-zh_source_tax_calculator-4d3ac0** (zh_source_tax_calculator): If a certificate of residence is provided (Ja), the cross-border (Grenzgänger) tariff applies with letter mapping A->L, B->M, C->N, H->P, G->Q; if not (Nein), the normal tariff applies.
  - "Ja -> cross-border (Grenzgänger) tariff: A->L, B->M, C->N, H->P, G->Q; Nein -> normal tariff" — zh_source_tax_calculator/C-Q19
  - "result Tarif: N1Y" — zh_source_tax_calculator/C-V34
  - "result Tarif: C1Y" — zh_source_tax_calculator/C-V35
- **F-zh_source_tax_calculator-509a7d** (zh_source_tax_calculator): Parental custody (shared/sole) is asked only when the child is 'Minderjährig' and lives in the same household, for both civil statuses.
  - "Elterliche Sorge Options: Geteiltes Sorgerecht | Alleiniges Sorgerecht" — zh_source_tax_calculator/C-Q09
- **F-zh_source_tax_calculator-50f74a** (zh_source_tax_calculator): Married person, adult child in first education: in same household with common household with other parent counts (B1N); not in household and not mainly maintained (Q15 = Nein) does not count (B0N).
  - ""Q08": "Ja", "Q10": "Ja", "Q16": "Ja"} -> result Tarif: B1N (Kind Ergebnis: B1)" — zh_source_tax_calculator/C-V14
  - ""Q15": "Nein", "Q16": "Ja"} -> result Tarif: B0N (Kind Ergebnis: B0)" — zh_source_tax_calculator/C-V15
- **F-zh_source_tax_calculator-52b67a** (zh_source_tax_calculator): Main residence in Switzerland or in 'Anderes Land' leaves the base tariff unchanged (e.g. A0N for a single person without children living in another country).
  - "CH or 'Anderes Land' -> base tariff." — zh_source_tax_calculator/C-N05
  - ""Q17": "Anderes Land"} -> result Tarif: A0N" — zh_source_tax_calculator/C-V42
- **F-zh_source_tax_calculator-562299** (zh_source_tax_calculator): Single person, adult child in first education mainly maintained (Q15 = Ja): not in household -> A1N; in household without common household with other parent -> H1N.
  - ""Q08": "Nein", "Q15": "Ja", "Q16": "Ja"} -> result Tarif: A1N (Kind Ergebnis: A1)" — zh_source_tax_calculator/C-V22
  - ""Q10": "Nein", "Q15": "Ja", "Q16": "Ja"} -> result Tarif: H1N (Kind Ergebnis: H1)" — zh_source_tax_calculator/C-V23
- **F-zh_source_tax_calculator-56e79b** (zh_source_tax_calculator): Married person, minor child not in household: shared custody + alternating care + person is main contributor counts the child (B1N); no shared custody does not count it (B0N).
  - ""Q13": "Ja", "Q11": "Ja", "Q12": "Quellensteuerpflichtige Person", "Q16": "Ja"} -> result Tarif: B1N (Kind Ergebnis: B1)" — zh_source_tax_calculator/C-V12
  - ""Q13": "Nein", "Q16": "Ja"} -> result Tarif: B0N (Kind Ergebnis: B0)" — zh_source_tax_calculator/C-V13
- **F-zh_source_tax_calculator-5725a8** (zh_source_tax_calculator): For each child, the calculator asks whether the child lives in the same household.
  - "Wohnsitz des Kindes im selben Haushalt?" — zh_source_tax_calculator/C-Q08
- **F-zh_source_tax_calculator-5f6820** (zh_source_tax_calculator): The certificate of residence question is asked only when the person returns daily to Germany (Q18 = Ja for earned income, or Q24 = Ja for replacement income).
  - "Ansässigkeitsbescheinigung beigebracht?" — zh_source_tax_calculator/C-Q19
- **F-zh_source_tax_calculator-64ac33** (zh_source_tax_calculator): Alternating care is asked when (child minor AND same household AND shared custody AND no common household with the other parent) OR (married AND child minor AND not same household AND Q13 shared custody = Ja) OR (single AND child minor AND not same household AND Q14 = Ja).
  - "Alternierende Obhut?" — zh_source_tax_calculator/C-Q11
- **F-zh_source_tax_calculator-64ac42** (zh_source_tax_calculator): Daily return to Germany options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q18
- **F-zh_source_tax_calculator-687e8b** (zh_source_tax_calculator): The calculator asks whether a certificate of residence (Ansässigkeitsbescheinigung) has been provided.
  - "Ansässigkeitsbescheinigung beigebracht?" — zh_source_tax_calculator/C-Q19
- **F-zh_source_tax_calculator-69edd5** (zh_source_tax_calculator): The calculator asks whether the person returns daily to the main residence in Germany.
  - "Tägliche Rückkehr an den Hauptwohnsitz in Deutschland?" — zh_source_tax_calculator/C-Q18
- **F-zh_source_tax_calculator-6dcf5c** (zh_source_tax_calculator): The common-household question is shown when (child minor AND same household AND shared custody) OR (child of age in first education AND same household).
  - "Gemeinsamer Haushalt mit dem anderen Elternteil?" — zh_source_tax_calculator/C-Q10
- **F-zh_source_tax_calculator-75cd87** (zh_source_tax_calculator): The single variant of the children question is shown only when civil status is 'Ledig, Geschieden, Getrennt, Verwitwet' and denomination has been answered.
  - "Leibliche oder adoptierte Kinder der Person?" — zh_source_tax_calculator/C-Q06
- **F-zh_source_tax_calculator-7b637b** (zh_source_tax_calculator): The calculator asks whether the spouse / registered partner is gainfully employed or receives replacement income.
  - "Ist der Ehegatte / eingetragene Partner erwerbstätig oder bezieht er/sie Ersatzeinkünfte?" — zh_source_tax_calculator/C-Q04
- **F-zh_source_tax_calculator-7c667f** (zh_source_tax_calculator): The child household question is shown only when the child is 'Minderjährig' or 'Volljährig und in Erstausbildung'.
  - "Wohnsitz des Kindes im selben Haushalt?" — zh_source_tax_calculator/C-Q08
- **F-zh_source_tax_calculator-7dcce6** (zh_source_tax_calculator): Q13 is shown only when civil status is married/registered partnership AND the child is 'Minderjährig' AND the child does not live in the same household.
  - "Geteiltes Sorgerecht" — zh_source_tax_calculator/C-Q13
- **F-zh_source_tax_calculator-823151** (zh_source_tax_calculator): Certificate of residence provided options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q19
- **F-zh_source_tax_calculator-89a9f1** (zh_source_tax_calculator): Earned income, residence in Germany: cross-border code applies with daily return + certificate, or without daily return when return is reasonable and no proof of >60 non-return days; every other Germany combination gives the base tariff.
  - "DE with daily return and an Ansässigkeitsbescheinigung, or DE without daily return, return reasonable and no proof of more than 60 non-return days -> cross-border code (A->L, B->M, C->N, H->P, G->Q). Every other DE combination -> base tariff." — zh_source_tax_calculator/C-N05
- **F-zh_source_tax_calculator-9007c3** (zh_source_tax_calculator): The calculator asks for the civil status (Zivilstand) of the person subject to source tax.
  - "Zivilstand" — zh_source_tax_calculator/C-Q02
  - "Section heading: 'Angaben zur quellensteuerpflichtigen Person'" — zh_source_tax_calculator/C-Q02
- **F-zh_source_tax_calculator-939b3b** (zh_source_tax_calculator): Larger financial contributor options: 'Quellensteuerpflichtige Person' (the person subject to source tax) | 'Anderer Elternteil' (other parent).
  - "Options: Quellensteuerpflichtige Person | Anderer Elternteil" — zh_source_tax_calculator/C-Q12
- **F-zh_source_tax_calculator-956f07** (zh_source_tax_calculator): For single persons with a minor child not in the household, the calculator asks 'Elterliche Sorge' with Ja/Nein (whether the person has parental custody).
  - "Same title as Q09, but with Ja/Nein options (internal name child-n__parentalCare)" — zh_source_tax_calculator/C-Q14
- **F-zh_source_tax_calculator-96658b** (zh_source_tax_calculator): For a single (non-married) person, any child counted with H gives an H tariff overall (e.g. A1 + H1 -> H2N). A child is counted with H when it lives in the household and the person has sole custody or is the main financial contributor.
  - "For a single person, any child counted with H gives an H tariff (e.g. A1 + H1 -> H2N)." — zh_source_tax_calculator/C-N04
  - "A child is counted with H when it lives in the household and the person has sole custody or is the main financial contributor." — zh_source_tax_calculator/C-N04
  - "result Tarif: H2N (Kind Ergebnis: A1; Kind Ergebnis: H1)" — zh_source_tax_calculator/C-V27
- **F-zh_source_tax_calculator-97139a** (zh_source_tax_calculator): For married/registered-partnership persons: spouse employed or receiving replacement income (Ja) gives tariff letter C; otherwise (Nein) gives tariff letter B.
  - "Ja -> C tariff; Nein -> B tariff" — zh_source_tax_calculator/C-Q04
  - "result Tarif: B0Y" — zh_source_tax_calculator/C-V03
  - "result Tarif: C0Y" — zh_source_tax_calculator/C-V05
- **F-zh_source_tax_calculator-981b6b** (zh_source_tax_calculator): The calculator asks whether the person returns daily to the main residence in Liechtenstein.
  - "Tägliche Rückkehr an den Hauptwohnsitz in Liechtenstein?" — zh_source_tax_calculator/C-Q22
- **F-zh_source_tax_calculator-987091** (zh_source_tax_calculator): Answering 'weder noch' ends the child block immediately and the child does not count for the tariff.
  - "'weder noch' ends the child block right away (child does not count)." — zh_source_tax_calculator/C-Q07
  - ""Q07": "weder noch", "Q16": "Ja"} -> result Tarif: B0N (Kind Ergebnis: B0)" — zh_source_tax_calculator/C-V16
- **F-zh_source_tax_calculator-a166c7** (zh_source_tax_calculator): Children question (married variant) options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q05
- **F-zh_source_tax_calculator-a2041b** (zh_source_tax_calculator): Daily return to Liechtenstein options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q22
- **F-zh_source_tax_calculator-a33b65** (zh_source_tax_calculator): The married variant of the children question is shown only when civil status is 'Verheiratet oder eingetragene Partnerschaft' and the spouse employment question has been answered.
  - "Leibliche oder adoptierte Kinder der Person oder der Ehegatten bzw. Partner?" — zh_source_tax_calculator/C-Q05
- **F-zh_source_tax_calculator-aaece6** (zh_source_tax_calculator): Q20 is asked only when income type is 'Erwerbseinkommen', state of residence is Deutschland and the person does not return daily (Q18 = Nein).
  - "Tägliche Rückkehr grundsätzlich zumutbar (weniger als 100km Fahrdistanz)?" — zh_source_tax_calculator/C-Q20
- **F-zh_source_tax_calculator-ab4e1e** (zh_source_tax_calculator): More than 45 non-return days (Ja) gives the normal tariff plus 'Unter Vorbehalt des Doppelbesteuerungsabkommens'; otherwise (Nein) 'Grundsätzlich keine Quellensteuerpflicht'.
  - "Ja -> normal tariff + 'Unter Vorbehalt des Doppelbesteuerungsabkommens'; Nein -> 'Grundsätzlich keine Quellensteuerpflicht'" — zh_source_tax_calculator/C-Q23
  - "result Tarif: C1Y / Unter Vorbehalt des Doppelbesteuerungsabkommens" — zh_source_tax_calculator/C-V40
- **F-zh_source_tax_calculator-ab8a06** (zh_source_tax_calculator): For non-married persons, the calculator asks whether the person has biological or adopted children.
  - "Leibliche oder adoptierte Kinder der Person?" — zh_source_tax_calculator/C-Q06
- **F-zh_source_tax_calculator-ad867a** (zh_source_tax_calculator): The larger-contributor question is asked when alternating care = Ja, OR for single persons when the child lives in the same household and there is a common household with the other parent; for married persons a common household with the other parent ends the child block without this question.
  - "Wer leistet den grösseren finanziellen Beitrag an den Unterhalt des Kindes?" — zh_source_tax_calculator/C-Q12
- **F-zh_source_tax_calculator-b008fe** (zh_source_tax_calculator): The calculator asks whether more than 50% of the child's maintenance is mainly provided (by the person).
  - "Wird zur Hauptsache (mehr als 50%) für den Kindsunterhalt aufgekommen?" — zh_source_tax_calculator/C-Q15
- **F-zh_source_tax_calculator-b62b85** (zh_source_tax_calculator): Children question (single variant) options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q06
- **F-zh_source_tax_calculator-b7154e** (zh_source_tax_calculator): Cross-border examples under earned income with residence in Germany, daily return and certificate: single no children Y -> L0Y; single with qualifying adult child -> L1N; married spouse not employed -> M0N; single with 1 or 3 H-children -> P1Y / P3N; married spouse employed with 1 child -> N1Y.
  - "result Tarif: L0Y" — zh_source_tax_calculator/C-V30
  - "result Tarif: L1N" — zh_source_tax_calculator/C-V31
  - "result Tarif: M0N" — zh_source_tax_calculator/C-V32
  - "result Tarif: P1Y" — zh_source_tax_calculator/C-V33
  - "result Tarif: P3N" — zh_source_tax_calculator/C-V29
  - "result Tarif: N1Y" — zh_source_tax_calculator/C-V34
- **F-zh_source_tax_calculator-b7fea8** (zh_source_tax_calculator): Denomination options: 'röm.-kath., christ.-kath., evang.-ref.' (Roman Catholic, Christian Catholic, Evangelical Reformed) or 'Keine oder andere' (none or other).
  - "Options: röm.-kath., christ.-kath., evang.-ref. | Keine oder andere" — zh_source_tax_calculator/C-Q03
- **F-zh_source_tax_calculator-b948fd** (zh_source_tax_calculator): Proof of more than 60 non-return days (Ja) gives the normal tariff; no proof (Nein) gives the cross-border tariff (L/M/N/P).
  - "Ja -> normal tariff; Nein -> cross-border tariff (L/M/N/P)" — zh_source_tax_calculator/C-Q21
  - ""Q21": "Nein"} -> result Tarif: N1Y" — zh_source_tax_calculator/C-V36
  - ""Q21": "Ja"} -> result Tarif: C1Y" — zh_source_tax_calculator/C-V37
- **F-zh_source_tax_calculator-bc1639** (zh_source_tax_calculator): If daily return is not reasonable (Q20 = Nein), the normal tariff applies.
  - "Nein -> normal tariff" — zh_source_tax_calculator/C-Q20
  - ""Q20": "Nein"} -> result Tarif: C1Y" — zh_source_tax_calculator/C-V38
- **F-zh_source_tax_calculator-c09dc1** (zh_source_tax_calculator): Parental custody options: 'Geteiltes Sorgerecht' (shared) | 'Alleiniges Sorgerecht' (sole).
  - "Options: Geteiltes Sorgerecht | Alleiniges Sorgerecht" — zh_source_tax_calculator/C-Q09
- **F-zh_source_tax_calculator-c2faa7** (zh_source_tax_calculator): Single person, minor child not in household: parental care Ja + alternating care + person main contributor -> H1N; parental care Nein -> A0N.
  - ""Q14": "Ja", "Q11": "Ja", "Q12": "Quellensteuerpflichtige Person", "Q16": "Ja"} -> result Tarif: H1N (Kind Ergebnis: H1)" — zh_source_tax_calculator/C-V20
  - ""Q14": "Nein", "Q16": "Ja"} -> result Tarif: A0N (Kind Ergebnis: A0)" — zh_source_tax_calculator/C-V21
- **F-zh_source_tax_calculator-c53a22** (zh_source_tax_calculator): A minor child in the same household with sole custody counts as a child (married: B1/C1; single: H1).
  - ""Q09": "Alleiniges Sorgerecht", "Q16": "Ja"} -> result Tarif: C1Y (Kind Ergebnis: C1)" — zh_source_tax_calculator/C-V07
  - ""Q09": "Alleiniges Sorgerecht", "Q16": "Ja"} -> result Tarif: H1Y (Kind Ergebnis: H1)" — zh_source_tax_calculator/C-V17
- **F-zh_source_tax_calculator-c78e0c** (zh_source_tax_calculator): A person with civil status 'Ledig, Geschieden, Getrennt, Verwitwet' and no counting children, resident in Switzerland, gets tariff letter A (e.g. A0Y / A0N).
  - ""Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "röm.-kath., christ.-kath., evang.-ref.", "Q06": "Nein", "Q16": "Ja"} -> result Tarif: A0Y" — zh_source_tax_calculator/C-V01
- **F-zh_source_tax_calculator-cb54d9** (zh_source_tax_calculator): Main maintenance (>50%) options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q15
- **F-zh_source_tax_calculator-cd1015** (zh_source_tax_calculator): Q15 is shown only when the child is 'Volljährig und in Erstausbildung' AND (child not in same household OR (same household AND no common household with the other parent)).
  - "Wird zur Hauptsache (mehr als 50%) für den Kindsunterhalt aufgekommen?" — zh_source_tax_calculator/C-Q15
- **F-zh_source_tax_calculator-cdd0b6** (zh_source_tax_calculator): The calculator asks who makes the larger financial contribution to the child's maintenance.
  - "Wer leistet den grösseren finanziellen Beitrag an den Unterhalt des Kindes?" — zh_source_tax_calculator/C-Q12
- **F-zh_source_tax_calculator-d2b3cf** (zh_source_tax_calculator): The calculator asks whether a daily return would in principle be reasonable (less than 100 km driving distance).
  - "Tägliche Rückkehr grundsätzlich zumutbar (weniger als 100km Fahrdistanz)?" — zh_source_tax_calculator/C-Q20
- **F-zh_source_tax_calculator-d2e516** (zh_source_tax_calculator): Shared custody (child not in household, married) options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q13
- **F-zh_source_tax_calculator-d62dd4** (zh_source_tax_calculator): State of residence options: Deutschland | Liechtenstein | Anderes Land (other country).
  - "Options: Deutschland | Liechtenstein | Anderes Land" — zh_source_tax_calculator/C-Q17
- **F-zh_source_tax_calculator-d79949** (zh_source_tax_calculator): The calculator asks whether there is a common household with the other parent.
  - "Gemeinsamer Haushalt mit dem anderen Elternteil?" — zh_source_tax_calculator/C-Q10
- **F-zh_source_tax_calculator-da19df** (zh_source_tax_calculator): The calculator asks whether there is alternating care (Alternierende Obhut).
  - "Alternierende Obhut?" — zh_source_tax_calculator/C-Q11
- **F-zh_source_tax_calculator-e22d17** (zh_source_tax_calculator): Q22 is asked only when income type is 'Erwerbseinkommen' and state of residence is Liechtenstein.
  - "Tägliche Rückkehr an den Hauptwohnsitz in Liechtenstein?" — zh_source_tax_calculator/C-Q22
- **F-zh_source_tax_calculator-e72e42** (zh_source_tax_calculator): Common household with other parent options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q10
- **F-zh_source_tax_calculator-e740d1** (zh_source_tax_calculator): Spouse employed / replacement income options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q04
- **F-zh_source_tax_calculator-e80d8f** (zh_source_tax_calculator): Daily return to Liechtenstein (Ja) results in 'Grundsätzlich keine Quellensteuerpflicht' (in principle no source tax liability), shown with 'Unter Vorbehalt des Doppelbesteuerungsabkommens'.
  - "Ja -> 'Grundsätzlich keine Quellensteuerpflicht'" — zh_source_tax_calculator/C-Q22
  - "result Grundsätzlich keine Quellensteuerpflicht / Unter Vorbehalt des Doppelbesteuerungsabkommens" — zh_source_tax_calculator/C-V39
- **F-zh_source_tax_calculator-e8ffac** (zh_source_tax_calculator): The calculator asks whether proof of more than 60 work-related non-return days in the calendar year has been provided.
  - "Nachweis von mehr als 60 beruflich bedingten Nichtrückkehrtagen im Kalenderjahr beigebracht?" — zh_source_tax_calculator/C-Q21
- **F-zh_source_tax_calculator-e96210** (zh_source_tax_calculator): The calculator asks whether there are more than 45 work-related non-return days in the calendar year.
  - "Mehr als 45 beruflich bedingte Nichtrückkehrtage im Kalenderjahr?" — zh_source_tax_calculator/C-Q23
- **F-zh_source_tax_calculator-ea3cd8** (zh_source_tax_calculator): Proof of >60 non-return days options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q21
- **F-zh_source_tax_calculator-ebd7b3** (zh_source_tax_calculator): Alternating care options: Ja | Nein.
  - "Options: Ja | Nein" — zh_source_tax_calculator/C-Q11
- **F-zh_source_tax_calculator-ecef37** (zh_source_tax_calculator): The tariff digit equals the number of children whose 'Kind Ergebnis' digit is 1 (e.g. three qualifying children of a married person with employed spouse -> C3Y).
  - "The final tariff's digit equals the number of children whose 'Kind Ergebnis' digit is 1." — zh_source_tax_calculator/C-N04
  - "result Tarif: C3Y" — zh_source_tax_calculator/C-V28
  - "result Tarif: H1N (Kind Ergebnis: H1; Kind Ergebnis: A0)" — zh_source_tax_calculator/C-V26
- **F-zh_source_tax_calculator-f29009** (zh_source_tax_calculator): The calculator asks whether the person's main residence is in Switzerland.
  - "Hauptwohnsitz in der Schweiz?" — zh_source_tax_calculator/C-Q16
  - "Section heading: 'Angaben zum Lebensmittelpunkt'" — zh_source_tax_calculator/C-Q16
- **F-zh_source_tax_calculator-f4ece9** (zh_source_tax_calculator): Q23 is asked only when the person does not return daily to Liechtenstein (Q22 = Nein).
  - "Mehr als 45 beruflich bedingte Nichtrückkehrtage im Kalenderjahr?" — zh_source_tax_calculator/C-Q23
- **F-zh_source_tax_calculator-f7f3ea** (zh_source_tax_calculator): For a minor child in the same household, the calculator asks about parental custody (Elterliche Sorge).
  - "Elterliche Sorge" — zh_source_tax_calculator/C-Q09
- **F-zh_source_tax_calculator-fb4a56** (zh_source_tax_calculator): Q14 is shown only when civil status is 'Ledig, Geschieden, Getrennt, Verwitwet' AND the child is 'Minderjährig' AND the child does not live in the same household.
  - "Elterliche Sorge Options: Ja | Nein" — zh_source_tax_calculator/C-Q14
- **F-zh_source_tax_calculator-fd9a15** (zh_source_tax_calculator): Child questions repeat per child; 'Ein weiteres Kind erfassen' adds another child block and 'Kind löschen' removes one; each completed block shows a 'Kind Ergebnis' code.
  - "A link button 'Ein weiteres Kind erfassen' adds another child block, and each block has a 'Kind löschen' button." — zh_source_tax_calculator/C-Q07
  - "Child questions repeat for each child (input names child-1__…, child-2__…)." — zh_source_tax_calculator/C-N04
- **F-zh_source_tax_calculator-fe0305** (zh_source_tax_calculator): For married persons with a minor child not in the household, the calculator asks whether there is shared custody (Geteiltes Sorgerecht, Ja/Nein).
  - "Geteiltes Sorgerecht Options: Ja | Nein" — zh_source_tax_calculator/C-Q13
- **G-01** (product owner guidance): Lonio collects onboarding data from a new employee **once** and reuses it for every receiving party. Asking too little blocks a registration; asking too much collects personal data we must not have (data minimisation). A question must only be asked when at least one receiving party needs the answer for this person.
- **G-08** (product owner guidance): Prefer asking for primary facts and **deriving** values (e.g. ask the first working day, derive the insurance start date) instead of asking the employee for values they cannot know.
- **G-09** (product owner guidance): Questionnaire language: English.
- **G-10** (product owner guidance): Business wording for values (used in allowed values and examples): countries by English name ("Switzerland", "Germany", "Liechtenstein"), permits as "B permit", "C permit", civil status exactly as the pension fund's list shows it ("Single", "Married", ...), dates as DD.MM.YYYY, yes/no as "yes"/"no".
