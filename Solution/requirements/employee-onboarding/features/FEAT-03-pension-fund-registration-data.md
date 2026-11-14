---
id: FEAT-03-pension-fund-registration-data
title: "Personal and family details for pension fund registration"
order: 3
stakeholders: [employee, hr, pension_fund]
stories: [US-03.1, US-03.2, US-03.3, US-03.4]
information: [first_name, last_name, date_of_birth, civil_status, spouse_date_of_birth, residence_canton]
rules: []
open_questions: [OQ-02, OQ-03, OQ-04]
---

# Personal and family details for pension fund registration

**Goal:** Lonio collects every field Pensionskasse Muster requires, including the spouse's date of birth for married employees, so that a registration is never blocked by missing data.

## Context
The pension fund portal requires first name, last name, date of birth, canton and civil status for every employee (F-SC-002 to F-SC-007, F-SC-010, F-SC-015). For married employees it also requires the spouse's date of birth and blocks the registration without it (F-TR-021, F-SC-012 to F-SC-014, F-SC-016). The civil status list shows only Single, Married, Divorced and Widowed (F-SC-011, G-07). HR's recollection of civil status matches the fund's list (F-TR-020, F-TR-022). Civil status is also an input for the source tax rule and the calculator (F-TR-029, F-TR-030). The fund offers only Swiss cantons and does not say whether it means the canton of residence or of work. Until the fund answers (OQ-02), the canton is asked only of employees living in Switzerland. It depends on address_country from FEAT-02. Registered partnerships, and portal behaviour for Divorced or Widowed, are still open.

**Stakeholders:** new employee, HR, pension fund

> ⚠ Open questions affecting this feature: [OQ-02](../open-questions.md#oq-02), [OQ-03](../open-questions.md#oq-03), [OQ-04](../open-questions.md#oq-04)

## User stories

### US-03.1 – Name and date of birth for the pension fund
**As** pension fund, **I want** to receive the new employee's first name, last name and date of birth, **so that** I can register the employee for occupational pension without the registration being rejected for missing required fields

Priority **P1** – These are required fields of the pension fund registration; if any is missing, the portal rejects the registration and highlights the field (F-SC-015), which blocks the registration. · Sources: F-SC-002, F-SC-003, F-SC-004, F-SC-005, F-SC-015, G-01

Covers: First name, Last name, Date of birth

**Acceptance criteria**

- **AC-03.1.1 First and last name are always asked and required**
  - **Given** a new employee is filling in the onboarding questionnaire
  - **When** they reach the personal details
  - **Then** they are asked for their first name and their last name; neither can be left empty, and both are made available for the pension fund registration.
  - _Sources: F-SC-002, F-SC-003, F-SC-015_
- **AC-03.1.2 Date of birth is always asked and required as a date**
  - **Given** a new employee is filling in the onboarding questionnaire
  - **When** they reach the personal details
  - **Then** they are asked for their date of birth as a day, month and year (shown as DD.MM.YYYY, e.g. 14.02.1990); it cannot be left empty and is made available for the pension fund registration.
  - _Sources: F-SC-004, F-SC-005, F-SC-015_
- **AC-03.1.3 Each detail is asked only once**
  - **Given** the employee has given their name and date of birth
  - **When** another part of the onboarding or another receiving party needs the same detail
  - **Then** the employee is not asked for it again; the earlier answer is reused.
  - _Sources: G-01_
### US-03.2 – Civil status from the pension fund's list
**As** pension fund, **I want** to receive the employee's civil status as one of the values my registration accepts, **so that** I can register the employee and know whether spouse details apply

Priority **P1** – Civil status is a required pension fund field; without it the registration is blocked (F-SC-010, F-SC-015). It is also an input for source tax (F-TR-029, F-TR-030). · Sources: F-SC-010, F-SC-011, F-SC-015, F-SC-018, F-TR-020, F-TR-022, F-TR-023, F-TR-024, F-TR-029, F-TR-030, G-07

Covers: Civil status

**Acceptance criteria**

- **AC-03.2.1 Civil status is always asked and required**
  - **Given** a new employee is filling in the onboarding questionnaire
  - **When** they reach the family details
  - **Then** they are asked for their civil status; it cannot be left empty and is made available for the pension fund registration.
  - _Sources: F-SC-010, F-SC-015, F-TR-020_
- **AC-03.2.2 Only the pension fund's civil status values are offered**
  - **Given** the employee is asked for their civil status
  - **When** they choose an answer
  - **Then** they can choose exactly one of: Single, Married, Divorced, Widowed, as the pension fund lists them; no other values are offered. How employees in a registered partnership or another status (e.g. separated) answer is open (OQ-03).
  - _Sources: F-SC-011, F-TR-022, G-07, F-TR-023, F-TR-024, F-SC-018_
- **AC-03.2.3 Civil status is reused for source tax and HR**
  - **Given** the employee has given their civil status
  - **When** the source tax decision or the source tax questions need it
  - **Then** the same answer is reused and the employee is not asked again.
  - _Sources: F-TR-029, F-TR-030, G-01_
### US-03.3 – Spouse's date of birth for married employees
**As** pension fund, **I want** to receive the spouse's date of birth for every married employee, and only for them, **so that** the registration of married employees is not blocked and no spouse data is collected without need

Priority **P1** – The portal blocks the registration of a married employee without the spouse's date of birth (F-SC-016). · Sources: F-TR-021, F-SC-012, F-SC-013, F-SC-014, F-SC-016, F-SC-018, G-01

Covers: Spouse's date of birth

**Acceptance criteria**

- **AC-03.3.1 Spouse's date of birth is asked and required only for married employees**
  - **Given** the employee has given their civil status
  - **When** the civil status is Married
  - **Then** the employee is asked for their husband's or wife's date of birth (DD.MM.YYYY), cannot leave it empty, and it is made available for the pension fund registration; for any other civil status it is not asked. Whether the fund needs spouse data for Divorced or Widowed is open (OQ-04).
  - _Sources: F-TR-021, F-SC-012, F-SC-013, F-SC-014, F-SC-016, F-SC-018, G-01_

  | Example | Civil status | → | Spouse's date of birth | Checked |
  |---|---|---|---|---|
  | Tomás, married, wife lives with him in Winterthur (F-TR-030) | Married | → | required | ✅ |
  | Single employee (illustrative) | Single | → | not asked | ✅ |
  | Divorced employee (illustrative) | Divorced | → | not asked | ✅ |
  | Widowed employee (illustrative) | Widowed | → | not asked | ✅ |

### US-03.4 – Canton for employees living in Switzerland
**As** pension fund, **I want** to receive a Swiss canton for the employee, **so that** I can complete the required canton field of the registration

Priority **P1** – Canton is a required pension fund field; without it the registration is blocked (F-SC-006, F-SC-015). · Status: **inferred** · Sources: F-SC-006, F-SC-007, F-SC-015, F-SC-017, G-01, G-07

Covers: Canton

**Acceptance criteria**

- **AC-03.4.1 Canton is asked and required only of employees living in Switzerland**
  - **Given** the employee has given the country of their home address
  - **When** the country is Switzerland
  - **Then** the employee is asked for their canton, cannot leave it empty, and it is made available for the pension fund registration; employees living outside Switzerland are not asked, until the fund clarifies whether it means the canton of residence or of work and what applies to employees living abroad (OQ-02).
  - _Sources: F-SC-006, F-SC-015, F-SC-017, G-01_

  | Example | Country of home address (country of residence) | → | Canton | Checked |
  |---|---|---|---|---|
  | Tomás, lives in Winterthur (F-TR-030) | Switzerland | → | required | ✅ |
  | Cross-border employee living in Germany (illustrative) | Germany | → | not asked | ✅ |
  | Employee living in Liechtenstein (illustrative) | Liechtenstein | → | not asked | ✅ |

- **AC-03.4.2 Only the fund's Swiss cantons are offered**
  - **Given** the employee is asked for their canton
  - **When** they choose an answer
  - **Then** they can choose exactly one of the 26 cantons the pension fund lists: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich.
  - _Sources: F-SC-007, G-07_
_Trace check: partial – The cited facts leave open whether the canton means residence or work and what applies to people abroad (F-SC-006, F-SC-017), so asking only Swiss-resident employees and naming the item residence_canton is an unbacked assumption._

## Information needed

The information this feature owns. Each piece is asked once and reused by
every stakeholder listed (see [information.md](../information.md) for all).

### First name
| | |
|---|---|
| **What?** | The new employee's first name. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required to register the employee with Pensionskasse Muster. |
| **Status · sources** | confirmed · F-SC-002, F-SC-015 |

### Last name
| | |
|---|---|
| **What?** | The new employee's last name. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required to register the employee with Pensionskasse Muster. |
| **Status · sources** | confirmed · F-SC-003, F-SC-015 |

### Date of birth
| | |
|---|---|
| **What?** | The new employee's date of birth. – Form: Date in the format DD.MM.YYYY |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required to register the employee with Pensionskasse Muster. |
| **Status · sources** | confirmed · F-SC-004, F-SC-005, F-SC-015 |

### Civil status
| | |
|---|---|
| **What?** | The employee's civil status, as listed by the pension fund. |
| **Allowed values** | Single · Married · Divorced · Widowed |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required field when registering the employee.<br>source tax office: For married employees the calculator asks different questions.<br>HR: Being married to a Swiss or C permit spouse living in Switzerland can exempt the employee from source tax. |
| **Status · sources** | confirmed · F-TR-020, F-TR-022, F-SC-010, F-SC-011, F-SC-015, F-TR-029, F-TR-030, F-TR-037, G-07 |
| **Notes** | The pension fund's list (precedence) confirms HR's recollection. Registered partnership is not in the list (OQ-03). |

### Spouse's date of birth
| | |
|---|---|
| **What?** | Date of birth of the employee's husband or wife. – Form: Date in the format DD.MM.YYYY |
| **When do we ask?** | Only if the employee is married |
| **When is it required?** | Whenever asked |
| **Depends on** | Civil status |
| **Who needs it?** | pension fund: The fund requires it for married employees and blocks registration without it. |
| **Status · sources** | confirmed · F-TR-021, F-SC-012, F-SC-013, F-SC-014, F-SC-016 |

### Canton
| | |
|---|---|
| **What?** | The canton the pension fund asks for when registering the employee. The portal does not say whether it is the canton of residence or of work. |
| **Allowed values** | Aargau · Appenzell Ausserrhoden · Appenzell Innerrhoden · Basel-Landschaft · Basel-Stadt · Bern · Fribourg · Geneva · Glarus · Graubünden · Jura · Lucerne · Neuchâtel · Nidwalden · Obwalden · Schaffhausen · Schwyz · Solothurn · St. Gallen · Thurgau · Ticino · Uri · Valais · Vaud · Zug · Zurich |
| **When do we ask?** | Only if the employee lives in Switzerland |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence) |
| **Who needs it?** | pension fund: Required field when registering the employee with Pensionskasse Muster. |
| **Status · sources** | inferred · F-SC-006, F-SC-007, F-SC-015, F-SC-017 |
| **Notes** | The fund requires a canton for every employee but lists only Swiss cantons; what applies to employees living abroad and whether it is the residence or work canton is open (OQ-02). |

## Evidence
- **F-SC-002** (pension_portal): The pension fund registration requires the employee's first name (text input, marked required).
  - "First name" — 01-empty.png (S01-E10)
  - "Fields marked * are required." — 01-empty.png (S01-E23)
- **F-SC-003** (pension_portal): The pension fund registration requires the employee's last name (text input, marked required).
  - "Last name" — 01-empty.png (S01-E11)
- **F-SC-004** (pension_portal): The pension fund registration requires the employee's date of birth (text input, marked required).
  - "Date of birth" — 01-empty.png (S01-E12)
- **F-SC-005** (pension_portal): The employee's date of birth is entered in the format DD.MM.YYYY.
  - "DD.MM.YYYY" — 01-empty.png (S01-E13)
- **F-SC-006** (pension_portal): The pension fund registration requires a canton (dropdown in the Employee section, marked required); the portal does not label whether it is the residence or work canton.
  - "Canton" — 01-empty.png (S01-E14)
  - "Employee" — 01-empty.png (S01-E09)
- **F-SC-007** (pension_portal): The Canton dropdown offers exactly these 26 options: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for living outside Switzerland.
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
- **F-SC-010** (pension_portal): The pension fund registration requires the employee's civil status (dropdown, marked required).
  - "Civil status" — 01-empty.png (S01-E19)
- **F-SC-011** (pension_portal): The Civil status dropdown offers exactly these options: Single, Married, Divorced, Widowed.
  - "Civil status" — 03-civil-status-list.png (S03-E19)
  - "Single" — 03-civil-status-list.png (S03-E21)
  - "Married" — 03-civil-status-list.png (S03-E22)
  - "Divorced" — 03-civil-status-list.png (S03-E23)
  - "Widowed" — 03-civil-status-list.png (S03-E24)
- **F-SC-012** (pension_portal): The pension fund registration has a 'Spouse's date of birth' field (text input) that is marked required when it is shown.
  - "Spouse's date of birth" — 05-married.png (S05-E21)
- **F-SC-013** (pension_portal): The spouse's date of birth is entered in the format DD.MM.YYYY.
  - "DD.MM.YYYY" — 05-married.png (S05-E23)
- **F-SC-014** (pension_portal): The 'Spouse's date of birth' field appears only when civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in the empty forms (01, 02, 03, 06).
  - "Married" — 05-married.png (S05-E20)
  - "Spouse's date of birth" — 05-married.png (S05-E21)
  - "Married" — 07-married-missing-spouse.png (S07-E20)
  - "Spouse's date of birth" — 07-married-missing-spouse.png (S07-E21)
  - "Single" — 04-single.png (S04-E20)
- **F-SC-015** (pension_portal): Submitting the form with required fields empty shows the banner 'Please correct the highlighted fields.', highlights each empty field and shows a per-field error of the form '<Field> is required.' (First name, Last name, Date of birth, Canton, Insurance start date, Civil status).
  - "Please correct the highlighted fields." — 06-required-errors.png (S06-E05)
  - "First name is required." — 06-required-errors.png (S06-E09)
  - "Last name is required." — 06-required-errors.png (S06-E12)
  - "Date of birth is required." — 06-required-errors.png (S06-E16)
  - "Canton is required." — 06-required-errors.png (S06-E19)
  - "Insurance start date is required." — 06-required-errors.png (S06-E24)
  - "Civil status is required." — 06-required-errors.png (S06-E27)
- **F-SC-016** (pension_portal): When civil status is Married and the spouse's date of birth is left empty, the portal blocks registration with the error 'Spouse's date of birth is required.'
  - "Married" — 07-married-missing-spouse.png (S07-E20)
  - "Spouse's date of birth is required." — 07-married-missing-spouse.png (S07-E24)
- **F-SC-017** (pension_portal, inferred): The Canton dropdown only lists Swiss cantons; it is unclear what to enter for an employee who lives abroad (e.g. a cross-border commuter living in Germany), and whether the field means the residence canton or the work canton.
  - "Canton" — 02-canton-list.png (S02-E14)
  - "Zurich" — 02-canton-list.png (S02-E41)
- **F-SC-018** (pension_portal, inferred): No screenshot shows the form with civil status Divorced or Widowed, so it is unknown whether any extra fields (e.g. spouse data) appear for those values; the list also has no option such as registered partnership or separated, and it is unclear how such cases are to be registered.
  - "Divorced" — 03-civil-status-list.png (S03-E23)
  - "Widowed" — 03-civil-status-list.png (S03-E24)
- **F-TR-020** (hr_transcript): The pension fund asks for the employee's civil status.
  - "Yes, the civil status. They ask for that." — T-032, Anna
- **F-TR-021** (hr_transcript): If the employee is married, the pension fund wants the date of birth of the husband or wife.
  - "And if someone is married, they want the date of birth of the husband or wife." — T-032, Anna
- **F-TR-022** (hr_transcript): Civil status options, from the stakeholder's memory and not confirmed: Single, Married, Divorced, and she thinks Widowed. She deferred to the pension fund screenshots for the actual list.
  - "I'd have to look. You'll see it in the screenshots. Single, married, divorced, I think widowed." — T-034, Anna
- **F-TR-023** (hr_transcript): One current employee (Daniel, in finance) is in a registered partnership. He was entered before the current HR manager's time.
  - "we do have one colleague in a registered partnership. Daniel, in finance." — T-034, Anna
  - "That was before my time." — T-036, Anna
- **F-TR-024** (hr_transcript): Unresolved: how the pension fund's screen handles a registered partnership, and whether the fund wants the partner's details.
  - "I honestly don't know what the fund's screen does in that case, or if they want the partner's details too." — T-036, Anna
- **F-TR-029** (hr_transcript): For married employees, the source tax calculator asks different questions, for example whether the husband or wife works.
  - "It changes the questions in the calculator, yes. Whether the husband or wife works." — T-044, Anna
- **F-TR-030** (hr_transcript): Addition: an employee married to someone who is Swiss or holds a C permit, and who lives in Switzerland, is not subject to source tax. Example: Tomás, Brazilian with a B permit, whose Swiss wife lives with him in Winterthur.
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." — T-044, Anna
- **F-TR-037** (hr_transcript, inferred): Consolidated final rule. (1) An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. (2) An employee living in Switzerland who is Swiss or holds a C permit is not subject. (3) An employee living in Switzerland who is non-Swiss without a C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. (4) Otherwise the employee is subject. The stakeholder hedged on completeness ('I think that's it').
  - "If you don't have a Swiss passport, you do source tax." — T-010, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — T-038, Anna
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Those people do source tax because they work here and they don't live here." — T-048, Anna
  - "I think that's it." — T-048, Anna
- **G-01** (product owner guidance): Lonio collects onboarding data from a new employee **once** and reuses it for every receiving party. Asking too little blocks a registration; asking too much collects personal data we must not have (data minimisation). A question must only be asked when at least one receiving party needs the answer for this person.
- **G-07** (product owner guidance): The pension fund screenshots show dropdowns with **all** their options.
