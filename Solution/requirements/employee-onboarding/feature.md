---
id: employee-onboarding
title: "Employee onboarding questionnaire"
stakeholders: [employee, hr, pension_fund, source_tax]
sections: [SEC-01-first-working-day-insurance-start, SEC-02-home-address, SEC-03-pension-fund-registration-data, SEC-04-source-tax-liability]
stories: [US-01.1, US-01.2, US-02.1, US-02.2, US-03.1, US-03.2, US-03.3, US-03.4, US-04.1, US-04.2, US-04.3, US-04.4]
---

# Employee onboarding questionnaire

**Goal:** Define what Lonio asks a new employee during onboarding: which information, in which steps and order, and under which conditions - asking each piece of information once and reusing it for every receiving party.

## Context
HR calls the first working day the most important item. It often changes, so HR asks the employee to confirm it (F-TR-014, F-TR-015). The pension fund requires an insurance start date that is always the 1st of a month (F-SC-008, F-SC-009). HR works it out by hand: if the first working day is the 1st of a month, insurance starts that day, otherwise on the 1st of the following month (F-TR-016, F-TR-017, F-TR-018). Once, an outdated first working day led to a wrong insurance start date at the fund (F-TR-019). Employees cannot know the insurance start date, so Lonio asks only for the primary fact and derives the date (G-08). The employee is not asked for the insurance start date (EX-05).

HR posts many documents to employees and needs the complete address as written on an envelope: street, number, postcode, town and country, with no extra parts (F-TR-009, F-TR-010). The country of the home address is also the employee's country of residence (F-TR-040, G-09). Several later questions depend on it. Employees living abroad are always subject to source tax (F-TR-034, F-TR-037), and the pension fund canton is asked only of employees living in Switzerland. This feature therefore comes before the pension and source tax features that depend on it.

The pension fund portal requires first name, last name, date of birth, canton and civil status for every employee (F-SC-002 to F-SC-007, F-SC-010, F-SC-015). For married employees it also requires the spouse's date of birth and blocks the registration without it (F-TR-021, F-SC-012 to F-SC-014, F-SC-016). The civil status list shows only Single, Married, Divorced and Widowed (F-SC-011, G-07). HR's recollection of civil status matches the fund's list (F-TR-020, F-TR-022). Civil status is also an input for the source tax rule and the calculator (F-TR-029, F-TR-030). The fund offers only Swiss cantons and does not say whether it means the canton of residence or of work. Until the fund answers (OQ-02), the canton is asked only of employees living in Switzerland. It depends on address_country from FEAT-02. Registered partnerships, and portal behaviour for Divorced or Widowed, are still open.

HR decides by hand whether an employee is subject to source tax. Employees living abroad always are. Swiss nationals and C permit holders living in Switzerland are not. Other foreigners living in Switzerland are not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland (F-TR-005, F-TR-006, F-TR-025, F-TR-030, F-TR-034, F-TR-037). Data minimisation means each of these questions is asked only when its answer can change the outcome (G-01). The rule uses address_country (FEAT-02) and civil_status (FEAT-03). The tariff questions of the Zurich calculator have not been analysed yet (OQ-01, blocking). Until they are, this feature delivers the subject or not-subject decision that gates them. HR is not sure the rule is complete (OQ-05). The permit list is undefined (OQ-06). HR wished for a permit reminder because half of new employees forget to bring it (F-TR-028, OQ-07). Using the Zurich calculator for every employee is an agreed simplification (F-TR-008, G-05, OQ-08).

**Stakeholders:** new employee, HR, pension fund, source tax office

## Contents

| Section | Stories |
|---|---|
| [1. Confirmed first working day and derived pension insurance start date](#SEC-01-first-working-day-insurance-start) | US-01.1, US-01.2 |
| [2. Complete home address and country of residence](#SEC-02-home-address) | US-02.1, US-02.2 |
| [3. Personal and family details for pension fund registration](#SEC-03-pension-fund-registration-data) | US-03.1, US-03.2, US-03.3, US-03.4 |
| [4. Decide whether the employee is subject to source tax](#SEC-04-source-tax-liability) | US-04.1, US-04.2, US-04.3, US-04.4 |

<a id="SEC-01-first-working-day-insurance-start"></a>

## 1. Confirmed first working day and derived pension insurance start date

Every new employee confirms their first working day, and Lonio works out the pension insurance start date from it, so the fund never gets a wrong or outdated start date.

### US-01.1 – Employee confirms their first working day
**As** HR, **I want** every new employee to confirm their first working day themselves during onboarding, **so that** I always work with the latest agreed start date, even when it moved after the contract was signed, and can register the employee with the pension fund correctly

Priority **P1** – HR calls it 'the number one thing'; it changes often, and an outdated date once caused a wrong registration at the pension fund, an unfriendly letter and weeks of fixing (F-TR-014, F-TR-019). · Sources: F-TR-014, F-TR-015, F-TR-019, G-01

Covers: First working day

**Acceptance criteria**

- **AC-01.1.1 First working day is asked of every employee and is required**
  - **Given** a new employee is going through onboarding
  - **When** they reach the employment details
  - **Then** they are asked to confirm their first working day at Muster AG, whatever their other answers, and cannot finish onboarding without giving it
  - _Sources: F-TR-014_

  | Example | First working day | → | First working day | Checked |
  |---|---|---|---|---|
  | Julia (F-TR-019) | 15.03.2026 | → | required | ✅ |

- **AC-01.1.2 Employee gives the date as actually agreed, as a calendar date**
  - **Given** the employee's start date may have moved since the contract was signed (e.g. they left their old employer a week earlier)
  - **When** the employee answers the first working day question
  - **Then** they give the start date as currently agreed with Muster AG, as a full date in the form DD.MM.YYYY, so it reflects the latest confirmed first working day
  - _Sources: F-TR-014, F-TR-015, G-10_
- **AC-01.1.3 First working day is available to HR and the pension fund**
  - **Given** the employee has confirmed their first working day
  - **When** onboarding data is handed on to the receiving parties
  - **Then** HR receives the confirmed first working day, and it is the basis for the insurance start date the pension fund needs
  - _Sources: F-TR-014, F-SC-008, G-04_
### US-01.2 – Insurance start date is derived from the confirmed first working day
**As** pension fund, **I want** to receive an insurance start date that is the 1st of a month and follows from the employee's latest confirmed first working day, **so that** the employee is insured from the correct date and registrations do not need weeks of correction

Priority **P1** – The insurance start date is required for registration (F-SC-008); a wrong date already caused an incident with an unfriendly letter and weeks of fixing (F-TR-019). · Sources: F-TR-016, F-TR-017, F-TR-018, F-TR-019, F-SC-008, F-SC-009, G-08

Covers: First working day, Pension insurance start date

**Acceptance criteria**

- **AC-01.2.1 Employee is not asked for the insurance start date**
  - **Given** a new employee is going through onboarding
  - **When** they answer the questionnaire
  - **Then** they are never asked for an insurance start date; Lonio works it out from the confirmed first working day
  - _Sources: F-TR-018, G-08_
- **AC-01.2.2 First working day on the 1st of a month: insurance starts that day**
  - **Given** the confirmed first working day is the 1st of a month
  - **When** Lonio derives the insurance start date
  - **Then** the insurance start date is the same day as the first working day
  - _Sources: F-TR-017, F-TR-018_

  | Example | First working day | → | Pension insurance start date | Checked |
  |---|---|---|---|---|
  | Starts on the 1st of a month (illustrative) | 01.04.2026 | → | 01.04.2026 | ✅ |
  | Starts on 1st January (illustrative) | 01.01.2027 | → | 01.01.2027 | ✅ |

- **AC-01.2.3 First working day not on the 1st: insurance starts on the 1st of the following month**
  - **Given** the confirmed first working day is any day other than the 1st of a month
  - **When** Lonio derives the insurance start date
  - **Then** the insurance start date is the 1st of the month after the first working day, also across a year end
  - _Sources: F-TR-016, F-TR-018_

  | Example | First working day | → | Pension insurance start date | Checked |
  |---|---|---|---|---|
  | Julia (F-TR-019) | 15.03.2026 | → | 01.04.2026 | ✅ |
  | Starts on the 2nd of a month (illustrative) | 02.03.2026 | → | 01.04.2026 | ✅ |
  | Starts on the last day of a month (illustrative) | 31.01.2026 | → | 01.02.2026 | ✅ |
  | Starts in December (year end) (illustrative) | 15.12.2026 | → | 01.01.2027 | ✅ |

- **AC-01.2.4 Insurance start date follows the latest confirmed first working day**
  - **Given** the employee's first working day has moved and the employee confirmed the new date
  - **When** Lonio derives the insurance start date
  - **Then** the insurance start date is based on the newly confirmed first working day, never on an earlier, outdated one
  - _Sources: F-TR-015, F-TR-019_

  | Example | First working day | → | Pension insurance start date | Checked |
  |---|---|---|---|---|
  | Julia moved her start to 15 March (F-TR-019) | 15.03.2026 | → | 01.04.2026 | ✅ |

- **AC-01.2.5 Insurance start date meets the fund's requirements**
  - **Given** an insurance start date has been derived
  - **When** it is made available for the pension fund registration
  - **Then** it is always the 1st of a month and is given as DD.MM.YYYY, as the fund requires
  - _Sources: F-SC-008, F-SC-009_
### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### First working day
| | |
|---|---|
| **What?** | The employee's confirmed first working day at Muster AG. The insurance start date is derived from it, so it must always reflect the latest confirmed date. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Most important item; HR asks the employee to confirm it because it often changes.<br>pension fund: Basis for the insurance start date the fund requires. |
| **Status · sources** | confirmed · F-TR-014, F-TR-015, F-TR-018, F-TR-019, F-SC-008, G-08 |
| **Notes** | The employee confirms it. A wrong or outdated first working day once led to a wrong insurance start date at the fund (F-TR-019). |

### Business rules in this section

#### Pension insurance start date
The insurance start date is derived from the latest confirmed first working day and is not asked. If the first working day is the 1st of a month, insurance starts that day; otherwise it starts on the 1st of the following month (e.g. first working day 15.03.2026 gives 01.04.2026). The result is always the 1st of a month, as the fund requires, in the format DD.MM.YYYY.

| # | First working day | → Result | Sources |
|---|---|---|---|
| 1 | Is the 1st of a month | Insurance starts on the first working day | F-TR-017, F-TR-018 |
| 2 | Is not the 1st of a month | Insurance starts on the 1st of the following month | F-TR-016, F-TR-018 |

_Status: confirmed · Sources: F-TR-016, F-TR-017, F-TR-018, F-TR-019, F-SC-008, F-SC-009, G-08_

<a id="SEC-02-home-address"></a>

## 2. Complete home address and country of residence

Every new employee gives a complete postal address once, so HR can post documents, and its country tells the other steps whether the employee lives in Switzerland.

### US-02.1 – Complete postal address for HR mail
**As** HR, **I want** every new employee to give their complete home address (street, house number, postcode, town and country) as it would be written on an envelope, **so that** I can post documents to the employee without chasing missing address parts

Priority **P1** – HR posts many documents to employees and states the address 'has to be complete'; an incomplete address blocks HR's postal communication (F-TR-010). · Sources: F-TR-009, F-TR-010

Covers: Street, House number, Postcode, Town, Country of home address (country of residence)

**Acceptance criteria**

- **AC-02.1.1 All address parts are always asked and required**
  - **Given** a new employee is filling in the onboarding questionnaire
  - **When** they reach the home address step
  - **Then** they are asked for street, house number, postcode, town and country of their home address, and cannot complete the step while any of these five parts is empty
  - _Sources: F-TR-009, F-TR-010_

  | Example | Country of home address (country of residence) | → | Street | House number | Postcode | Town | Country of home address (country of residence) | Checked |
  |---|---|---|---|---|---|---|---|---|
  | Employee living in Switzerland (illustrative) | Switzerland | → | required | required | required | required | required | ✅ |
  | Employee living abroad (illustrative) | Germany | → | required | required | required | required | required | ✅ |

- **AC-02.1.2 Normal postal address with no extra parts**
  - **Given** a new employee is at the home address step
  - **When** they enter their address
  - **Then** only the parts of a normal postal address as written on an envelope are asked (street, house number, postcode, town, country); no further address parts are asked
  - _Sources: F-TR-010_
- **AC-02.1.3 Address is asked once and received by HR**
  - **Given** a new employee has completed the home address step
  - **When** the onboarding data is made available to the receiving parties
  - **Then** HR receives the complete home address, and the employee is not asked for the address again in any later step
  - _Sources: F-TR-009, F-TR-010, G-01_
### US-02.2 – Country of home address as country of residence
**As** source tax office, **I want** the country of the employee's home address to be used as their country of residence, **so that** employees living abroad are recognised as subject to source tax and only the questions relevant to where the employee lives are asked later

Priority **P1** – Whether the employee lives in Switzerland decides source tax liability (F-TR-034, F-TR-037) and which later questions are asked; without it later steps cannot be determined. · Status: **inferred** · Sources: F-TR-034, F-TR-036, F-TR-037, F-TR-040, G-09

Covers: Country of home address (country of residence)

**Acceptance criteria**

- **AC-02.2.1 Country of residence is not asked separately**
  - **Given** a new employee has given the country of their home address
  - **When** a later step needs to know whether the employee lives in Switzerland
  - **Then** the country of the home address is used as the country of residence and the employee is not asked a separate question about where they live
  - _Sources: F-TR-040, G-09, G-01_
- **AC-02.2.2 Employees living abroad are subject to source tax whatever their nationality**
  - **Given** a new employee's home address is outside Switzerland
  - **When** the questionnaire determines the following steps
  - **Then** the employee is treated as subject to source tax, is not asked their nationality or the pension fund canton, and source tax and HR receive the country of residence
  - _Sources: F-TR-034, F-TR-037, F-TR-040_

  | Example | Country of home address (country of residence) | → | Nationality | Canton | Subject to source tax | Checked |
  |---|---|---|---|---|---|---|
  | Stefan, Swiss, lives in Konstanz (F-TR-034) | Germany | → | not asked | not asked | yes | ✅ |
  | Employee living in Liechtenstein (illustrative) | Liechtenstein | → | not asked | not asked | yes | ✅ |

- **AC-02.2.3 Employees living in Switzerland continue to nationality and canton**
  - **Given** a new employee's home address is in Switzerland
  - **When** the questionnaire determines the following steps
  - **Then** the employee is asked their nationality and the pension fund canton, which decide the later source tax and pension steps
  - _Sources: F-TR-037, F-TR-040_

  | Example | Country of home address (country of residence) | → | Nationality | Canton | Checked |
  |---|---|---|---|---|---|
  | Employee living in Winterthur (illustrative) | Switzerland | → | asked | asked | ✅ |

- **AC-02.2.4 Address comes before dependent steps**
  - **Given** a new employee starts the onboarding questionnaire
  - **When** the steps are presented
  - **Then** the home address step comes before the pension and source tax steps that depend on the country of residence; the additional source tax questions for employees living abroad are defined by the Zurich calculator and remain open (OQ-01)
  - _Sources: F-TR-036, F-TR-040_
_Trace check: partial – The cited facts never mention a pension fund canton question or say it is skipped for residents abroad and asked for residents in Switzerland (AC-02.2.2, AC-02.2.3), and the claim that source tax and HR receive the country of residence is not backed either._

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Street
| | |
|---|---|
| **What?** | Street of the employee's home address. – Form: Part of a complete postal address, as written on an envelope: street, number, postcode, town and country, with no extra parts. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: HR posts many documents to employees, so the address must be complete. |
| **Status · sources** | confirmed · F-TR-009, F-TR-010 |

#### House number
| | |
|---|---|
| **What?** | House number of the employee's home address. – Form: Part of a complete postal address, as written on an envelope. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: HR posts many documents to employees, so the address must be complete. |
| **Status · sources** | confirmed · F-TR-009, F-TR-010 |
| **Notes** | HR named the number as part of the full address; whether every address has a house number is not discussed. |

#### Postcode
| | |
|---|---|
| **What?** | Postcode of the employee's home address. – Form: Part of a complete postal address, as written on an envelope. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: HR posts many documents to employees, so the address must be complete. |
| **Status · sources** | confirmed · F-TR-009, F-TR-010 |

#### Town
| | |
|---|---|
| **What?** | Town of the employee's home address. – Form: Part of a complete postal address, as written on an envelope. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: HR posts many documents to employees, so the address must be complete. |
| **Status · sources** | confirmed · F-TR-009, F-TR-010 |

#### Country of home address (country of residence)
| | |
|---|---|
| **What?** | Country of the employee's home address. It is also the employee's country of residence, which decides whether the employee lives in Switzerland for the source tax rules. – Form: Part of a complete postal address, as written on an envelope. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: HR posts many documents to employees, so the address must be complete; and to decide whether the employee is subject to source tax (employees living abroad always are).<br>source tax office: Employees living abroad are always subject to source tax, and the calculator asks them more questions. |
| **Status · sources** | inferred · F-TR-009, F-TR-010, F-TR-034, F-TR-037, F-TR-040, F-TR-036, G-09 |
| **Notes** | Using the address country as country of residence is an inference (F-TR-040) confirmed by the product owner convention (G-09). |

<a id="SEC-03-pension-fund-registration-data"></a>

## 3. Personal and family details for pension fund registration

Lonio collects every field Pensionskasse Muster requires, including the spouse's date of birth for married employees, so that a registration is never blocked by missing data.

> ⚠ Open questions affecting this section: [OQ-02](open-questions.md#oq-02), [OQ-03](open-questions.md#oq-03), [OQ-04](open-questions.md#oq-04)
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

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### First name
| | |
|---|---|
| **What?** | The new employee's first name. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required to register the employee with Pensionskasse Muster. |
| **Status · sources** | confirmed · F-SC-002, F-SC-015 |

#### Last name
| | |
|---|---|
| **What?** | The new employee's last name. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required to register the employee with Pensionskasse Muster. |
| **Status · sources** | confirmed · F-SC-003, F-SC-015 |

#### Date of birth
| | |
|---|---|
| **What?** | The new employee's date of birth. – Form: Date in the format DD.MM.YYYY |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | pension fund: Required to register the employee with Pensionskasse Muster. |
| **Status · sources** | confirmed · F-SC-004, F-SC-005, F-SC-015 |

#### Civil status
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

#### Spouse's date of birth
| | |
|---|---|
| **What?** | Date of birth of the employee's husband or wife. – Form: Date in the format DD.MM.YYYY |
| **When do we ask?** | Only if the employee is married |
| **When is it required?** | Whenever asked |
| **Depends on** | Civil status |
| **Who needs it?** | pension fund: The fund requires it for married employees and blocks registration without it. |
| **Status · sources** | confirmed · F-TR-021, F-SC-012, F-SC-013, F-SC-014, F-SC-016 |

#### Canton
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

<a id="SEC-04-source-tax-liability"></a>

## 4. Decide whether the employee is subject to source tax

Lonio asks only the questions needed to decide whether an employee is subject to source tax, so that only those employees get the source tax questions and nobody gives nationality, permit or spouse data that is not needed.

> ⚠ Open questions affecting this section: [OQ-01](open-questions.md#oq-01), [OQ-05](open-questions.md#oq-05), [OQ-06](open-questions.md#oq-06), [OQ-07](open-questions.md#oq-07), [OQ-08](open-questions.md#oq-08)
### US-04.1 – Ask nationality only of employees living in Switzerland
**As** new employee, **I want** to be asked my nationality only when it matters for whether I pay source tax, **so that** HR can tell whether I am Swiss without me giving my nationality when it changes nothing

Priority **P1** – Without nationality HR cannot tell Swiss employees from other employees living in Switzerland. Today Swiss employees get the source tax questions, get annoyed and call HR (F-TR-005). · Status: **inferred** · Sources: F-TR-005, F-TR-006, F-TR-034, F-TR-037, F-TR-038, F-TR-040, G-01

Covers: Nationality

**Acceptance criteria**

- **AC-04.1.1 Nationality is asked and required for employees living in Switzerland**
  - **Given** the country of the employee's home address is Switzerland
  - **When** the employee fills in the questionnaire
  - **Then** Lonio asks for the employee's nationality, the employee must answer it, and HR uses it to decide whether the employee is subject to source tax.
  - _Sources: F-TR-006, F-TR-037, F-TR-038, F-TR-040_

  | Example | Country of home address (country of residence) | → | Nationality | Checked |
  |---|---|---|---|---|
  | Tomás (F-TR-030), lives in Winterthur | Switzerland | → | required | ✅ |

- **AC-04.1.2 Nationality is not asked of employees living abroad**
  - **Given** the country of the employee's home address is not Switzerland
  - **When** the employee fills in the questionnaire
  - **Then** Lonio does not ask for the employee's nationality, because employees living abroad are subject to source tax whatever their nationality. Whether the Zurich calculator needs it after all is open (OQ-01).
  - _Sources: F-TR-034, F-TR-037, G-01_

  | Example | Country of home address (country of residence) | → | Nationality | Checked |
  |---|---|---|---|---|
  | Stefan (F-TR-034), Swiss, lives in Konstanz | Germany | → | not asked | ✅ |
  | Employee living in Liechtenstein (illustrative) | Liechtenstein | → | not asked | ✅ |

### US-04.2 – Ask the permit type only of non-Swiss employees living in Switzerland
**As** new employee, **I want** to be asked about my residence permit only if I live in Switzerland and am not Swiss, **so that** HR can see whether I hold a C permit and, if I do, treat me like a Swiss national for source tax

Priority **P1** – C permit holders are not subject to source tax (F-TR-025). Without the permit type they would be asked the source tax questions for no reason (F-TR-005). · Status: **inferred** · Sources: F-TR-025, F-TR-028, F-TR-037, F-TR-039, G-01

Covers: Permit type

**Acceptance criteria**

- **AC-04.2.1 Permit type is asked and required for non-Swiss employees living in Switzerland**
  - **Given** the employee lives in Switzerland and their nationality is not Swiss
  - **When** the employee fills in the questionnaire
  - **Then** Lonio asks which Swiss residence permit the employee holds, the employee must answer it, and HR uses it to decide whether the employee is subject to source tax.
  - _Sources: F-TR-025, F-TR-037, F-TR-039_

  | Example | Country of home address (country of residence) | Nationality | → | Permit type | Checked |
  |---|---|---|---|---|---|
  | Tomás (F-TR-030), Brazilian living in Winterthur | Switzerland | Brazil | → | required | ✅ |
  | Maria (F-TR-025), Portuguese, assumed to live in Switzerland (illustrative) | Switzerland | Portugal | → | required | ✅ |

- **AC-04.2.2 Permit type is not asked of Swiss employees or employees living abroad**
  - **Given** the employee is Swiss, or lives outside Switzerland
  - **When** the employee fills in the questionnaire
  - **Then** Lonio does not ask for a permit type, because the answer cannot change the source tax decision.
  - _Sources: F-TR-034, F-TR-037, G-01_

  | Example | Country of home address (country of residence) | Nationality | → | Permit type | Checked |
  |---|---|---|---|---|---|
  | Swiss employee living in Switzerland (illustrative) | Switzerland | Switzerland | → | not asked | ✅ |
  | Stefan (F-TR-034), lives in Konstanz | Germany | – | → | not asked | ✅ |

- **AC-04.2.3 Permit choices and permit reminder are still open**
  - **Given** the sources name only the B permit and the C permit
  - **When** the permit question is shown to the employee
  - **Then** the answers include at least "B permit" and "C permit". The full list of permit types is still open (OQ-06). For the source tax decision, only C permit versus any other answer matters. HR wants the questionnaire to remind employees to bring their permit, but whether to add the reminder and its wording are still open (OQ-07).
  - _Sources: F-TR-025, F-TR-028, F-TR-039_
### US-04.3 – Ask spouse details only when they can exempt the employee
**As** HR, **I want** Lonio to collect the spouse's nationality, permit and country of residence only from married employees whose own status would otherwise make them subject to source tax, **so that** I no longer have to check the spouse case by hand and collect spouse details by email

Priority **P1** – Today HR checks this case by hand and collects the details by email, which 'takes forever' (F-TR-033). Without the spouse details, employees like Tomás are wrongly treated as subject to source tax. · Status: **inferred** · Sources: F-TR-030, F-TR-031, F-TR-032, F-TR-033, F-TR-037, G-01

Covers: Spouse's nationality, Spouse's permit type, Spouse's country of residence

**Acceptance criteria**

- **AC-04.3.1 Spouse's nationality is asked only when the spouse can change the outcome**
  - **Given** the employee is married, lives in Switzerland, is not Swiss and does not hold a C permit
  - **When** the employee fills in the questionnaire
  - **Then** Lonio asks for the spouse's nationality and the employee must answer it. Lonio does not ask it of any other employee, including employees who are married but Swiss, hold a C permit or live abroad. HR uses the answer for the source tax decision.
  - _Sources: F-TR-030, F-TR-031, F-TR-032, G-01_

  | Example | Country of home address (country of residence) | Nationality | Permit type | Civil status | → | Spouse's nationality | Checked |
  |---|---|---|---|---|---|---|---|
  | Tomás (F-TR-030), Brazilian, B permit, married | Switzerland | Brazil | B permit | Married | → | required | ✅ |
  | Single B permit holder in Switzerland (illustrative) | Switzerland | Italy | B permit | Single | → | not asked | ✅ |
  | Married C permit holder in Switzerland (illustrative) | Switzerland | Portugal | C permit | Married | → | not asked | ✅ |
  | Married Swiss employee in Switzerland (illustrative) | Switzerland | Switzerland | – | Married | → | not asked | ✅ |
  | Married employee living abroad (illustrative) | Germany | – | – | Married | → | not asked | ✅ |

- **AC-04.3.2 Spouse's permit type is asked only for a non-Swiss spouse and may be left empty**
  - **Given** the spouse's nationality is needed (AC-04.3.1) and the spouse is not Swiss
  - **When** the employee fills in the questionnaire
  - **Then** Lonio asks for the spouse's Swiss residence permit, if they have one. The employee may leave it empty if the spouse has no permit. Lonio does not ask it if the spouse is Swiss. The list of permit types is open (OQ-06).
  - _Sources: F-TR-031, F-TR-032, G-01_

  | Example | Country of home address (country of residence) | Nationality | Permit type | Civil status | Spouse's nationality | → | Spouse's permit type | Checked |
  |---|---|---|---|---|---|---|---|---|
  | Tomás (F-TR-030), wife is Swiss | Switzerland | Brazil | B permit | Married | Switzerland | → | not asked | ✅ |
  | B permit holder with an Italian spouse (illustrative) | Switzerland | Brazil | B permit | Married | Italy | → | optional | ✅ |

- **AC-04.3.3 Spouse's country of residence is asked only if the spouse is Swiss or holds a C permit**
  - **Given** the spouse's nationality is needed (AC-04.3.1)
  - **When** the spouse is Swiss or holds a C permit
  - **Then** Lonio asks where the spouse lives and the employee must answer it. Lonio does not ask it if the spouse is neither Swiss nor a C permit holder, because then the spouse cannot exempt the employee.
  - _Sources: F-TR-030, F-TR-031, F-TR-032, G-01_

  | Example | Country of home address (country of residence) | Nationality | Permit type | Civil status | Spouse's nationality | Spouse's permit type | → | Spouse's country of residence | Checked |
  |---|---|---|---|---|---|---|---|---|---|
  | Tomás (F-TR-030), Swiss wife in Winterthur | Switzerland | Brazil | B permit | Married | Switzerland | – | → | required | ✅ |
  | Spouse is Italian with a C permit (illustrative) | Switzerland | Brazil | B permit | Married | Italy | C permit | → | required | ✅ |
  | Spouse is Italian with a B permit (illustrative) | Switzerland | Brazil | B permit | Married | Italy | B permit | → | not asked | ✅ |

### US-04.4 – Decide whether the employee is subject to source tax
**As** HR, **I want** Lonio to decide from the employee's answers whether they are subject to source tax, **so that** I know up front who has to answer the source tax questions, and Swiss employees and other exempt employees are not bothered with them

Priority **P1** – HR never knows up front who has to answer the source tax questions, and Swiss employees get annoyed and call HR (F-TR-005). This decision controls whether the whole source tax step is asked. · Status: **inferred** · Sources: F-TR-005, F-TR-006, F-TR-007, F-TR-008, F-TR-025, F-TR-029, F-TR-030, F-TR-034, F-TR-036, F-TR-037, F-TR-040, G-05

Covers: Subject to source tax

**Acceptance criteria**

- **AC-04.4.1 Employees living abroad are always subject**
  - **Given** the country of the employee's home address is not Switzerland
  - **When** Lonio decides on source tax
  - **Then** the employee is subject to source tax, whatever their nationality.
  - _Sources: F-TR-034, F-TR-037, F-TR-040_

  | Example | Country of home address (country of residence) | → | Subject to source tax | Checked |
  |---|---|---|---|---|
  | Stefan (F-TR-034), Swiss, lives in Konstanz | Germany | → | yes | ✅ |

- **AC-04.4.2 Swiss nationals and C permit holders living in Switzerland are not subject**
  - **Given** the employee lives in Switzerland
  - **When** the employee is Swiss or holds a C permit
  - **Then** the employee is not subject to source tax. C permit holders are treated like Swiss nationals.
  - _Sources: F-TR-006, F-TR-025, F-TR-037_

  | Example | Country of home address (country of residence) | Nationality | Permit type | → | Subject to source tax | Checked |
  |---|---|---|---|---|---|---|
  | Swiss employee living in Switzerland (illustrative) | Switzerland | Switzerland | – | → | no | ✅ |
  | Maria (F-TR-025), Portuguese with a C permit, assumed to live in Switzerland (illustrative) | Switzerland | Portugal | C permit | → | no | ✅ |

- **AC-04.4.3 Spouse exemption for other foreigners living in Switzerland**
  - **Given** the employee lives in Switzerland, is not Swiss and does not hold a C permit
  - **When** Lonio decides on source tax
  - **Then** the employee is not subject only if they are married to a spouse who is Swiss or holds a C permit and who lives in Switzerland. In every other case the employee is subject.
  - _Sources: F-TR-025, F-TR-030, F-TR-037_

  | Example | Country of home address (country of residence) | Nationality | Permit type | Civil status | Spouse's nationality | Spouse's country of residence | Spouse's permit type | → | Subject to source tax | Checked |
  |---|---|---|---|---|---|---|---|---|---|---|
  | Tomás (F-TR-030), Brazilian, B permit, Swiss wife in Winterthur | Switzerland | Brazil | B permit | Married | Switzerland | Switzerland | – | → | no | ✅ |
  | Spouse is Italian with a C permit and lives in Switzerland (illustrative) | Switzerland | Brazil | B permit | Married | Italy | Switzerland | C permit | → | no | ✅ |
  | Swiss spouse lives in Germany (illustrative) | Switzerland | Brazil | B permit | Married | Switzerland | Germany | – | → | yes | ✅ |
  | Spouse is Italian with a B permit (illustrative) | Switzerland | Brazil | B permit | Married | Italy | – | B permit | → | yes | ✅ |
  | Single B permit holder in Switzerland (illustrative) | Switzerland | Italy | B permit | Single | – | – | – | → | yes | ✅ |

- **AC-04.4.4 Only employees subject to source tax get the source tax questions**
  - **Given** Lonio has decided whether the employee is subject to source tax
  - **When** the employee continues the questionnaire
  - **Then** only employees who are subject are asked the source tax tariff questions; employees who are not subject are not asked them. The tariff questions themselves (including the different questions for married employees and the extra questions for employees living abroad) are not yet defined (OQ-01, blocking). For now, the Zurich calculator applies to every subject employee (OQ-08).
  - _Sources: F-TR-005, F-TR-007, F-TR-008, F-TR-029, F-TR-036, G-05_
- **AC-04.4.5 Rule completeness to be confirmed by HR**
  - **Given** HR hedged on whether the rule is complete ('I think that's it')
  - **When** the decision rule is released
  - **Then** HR has checked the decision rules against real cases (Stefan, Maria, Tomás). Any missing case is handled through OQ-05, not by inventing new rules.
  - _Sources: F-TR-025, F-TR-037_
_Trace check: partial – AC-04.4.5 states that HR has checked the rules against Stefan, Maria and Tomás and that gaps go through OQ-05, but the facts only show HR hedging ('I think that's it') and say nothing about such a check or that handling; the other criteria are backed by F-TR-005/025/030/034/037/040._

### Information needed in this section

Each piece is asked once and reused by every stakeholder listed (all of it is
also in [information.md](information.md)).

#### Nationality
| | |
|---|---|
| **What?** | The employee's nationality (whether they hold a Swiss passport). |
| **When do we ask?** | Only if the employee lives in Switzerland |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence) |
| **Who needs it?** | HR: To decide whether an employee living in Switzerland is subject to source tax (Swiss nationals are not). |
| **Status · sources** | inferred · F-TR-038, F-TR-006, F-TR-037, F-TR-034, G-01 |
| **Notes** | For employees living abroad nationality does not change whether they are subject to source tax, so per data minimisation it is not asked of them. This may change once the Zurich calculator's questions are known (see OQ-01). |

#### Permit type
| | |
|---|---|
| **What?** | The type of Swiss residence permit the non-Swiss employee holds, e.g. B permit or C permit. |
| **When do we ask?** | Only if the employee lives in Switzerland and is not Swiss |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence), Nationality |
| **Who needs it?** | HR: To decide whether the employee is subject to source tax (C permit holders are treated like Swiss nationals). |
| **Status · sources** | inferred · F-TR-039, F-TR-025, F-TR-037, G-01 |
| **Notes** | Sources name only B permit and C permit; the full list of permit types is not defined (see OQ-06). HR wished for a reminder to bring the permit (see OQ-07). |

#### Spouse's nationality
| | |
|---|---|
| **What?** | Nationality of the employee's husband or wife (whether they are Swiss). |
| **When do we ask?** | Only if the employee is married, lives in Switzerland, is not Swiss and does not hold a C permit |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence), Civil status, Nationality, Permit type |
| **Who needs it?** | HR: To decide whether the employee is exempt from source tax because the spouse is Swiss and lives in Switzerland. |
| **Status · sources** | inferred · F-TR-030, F-TR-031, F-TR-032, F-TR-033, F-TR-037, G-01 |

#### Spouse's permit type
| | |
|---|---|
| **What?** | Type of Swiss residence permit the non-Swiss spouse holds, if any (e.g. C permit). |
| **When do we ask?** | Only if spouse details are needed for source tax and the spouse is not Swiss |
| **When is it required?** | May be left empty if the spouse has no permit |
| **Depends on** | Country of home address (country of residence), Civil status, Nationality, Permit type, Spouse's nationality |
| **Who needs it?** | HR: To decide whether the employee is exempt from source tax because the spouse holds a C permit and lives in Switzerland. |
| **Status · sources** | inferred · F-TR-030, F-TR-031, F-TR-032, F-TR-037, G-01 |
| **Notes** | HR said 'their permit if they have one', so the spouse may have none. Permit list not defined (OQ-06). |

#### Spouse's country of residence
| | |
|---|---|
| **What?** | The country where the employee's husband or wife lives (whether they live in Switzerland). |
| **When do we ask?** | Only if spouse details are needed for source tax and the spouse is Swiss or holds a C permit |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence), Civil status, Nationality, Permit type, Spouse's nationality, Spouse's permit type |
| **Who needs it?** | HR: The spouse exemption from source tax only applies if the spouse lives in Switzerland. |
| **Status · sources** | inferred · F-TR-030, F-TR-031, F-TR-032, F-TR-037, G-01 |
| **Notes** | Only asked when the answer can change the outcome (data minimisation). |

### Business rules in this section

#### Subject to source tax
An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. An employee living in Switzerland who is Swiss or holds a C permit is not subject. An employee living in Switzerland who is not Swiss and has no C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. Every other employee is subject. Only employees subject to source tax are asked the source tax questions.

| # | Country of residence | Nationality | Permit type | Civil status | Spouse Swiss or C permit | Spouse lives in Switzerland | → Result | Sources |
|---|---|---|---|---|---|---|---|---|
| 1 | Not Switzerland | any | any | any | any | any | Subject to source tax | F-TR-034, F-TR-037 |
| 2 | Switzerland | Swiss | - | any | any | any | Not subject | F-TR-006, F-TR-037 |
| 3 | Switzerland | Not Swiss | C permit | any | any | any | Not subject | F-TR-025, F-TR-037 |
| 4 | Switzerland | Not Swiss | Not C permit | Married | yes | yes | Not subject | F-TR-030, F-TR-037 |
| 5 | Switzerland | Not Swiss | Not C permit | Married | yes | no | Subject to source tax | F-TR-030, F-TR-037 |
| 6 | Switzerland | Not Swiss | Not C permit | Married | no | - | Subject to source tax | F-TR-030, F-TR-037 |
| 7 | Switzerland | Not Swiss | Not C permit | Not married | - | - | Subject to source tax | F-TR-025, F-TR-037 |

_Status: inferred · Sources: F-TR-005, F-TR-006, F-TR-025, F-TR-030, F-TR-034, F-TR-037, F-TR-040_

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
- **F-SC-008** (pension_portal): The pension fund registration requires an insurance start date (text input in the Insurance section, marked required).
  - "Insurance start date" — 01-empty.png (S01-E17)
  - "Insurance" — 01-empty.png (S01-E16)
- **F-SC-009** (pension_portal): The insurance start date is entered as DD.MM.YYYY and must be the 1st of a month.
  - "DD.MM.YYYY. Must be the 1st of a month." — 01-empty.png (S01-E18)
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
- **F-TR-005** (hr_transcript, inferred): Source tax questions should only be asked to employees who are subject to source tax, not to everybody.
  - "Because I never know up front who has to answer those questions." — T-008, Anna
  - "the Swiss people get annoyed, and they call me." — T-008, Anna
- **F-TR-006** (hr_transcript): First version: all non-Swiss employees (anyone without a Swiss passport) are subject to source tax.
  - "All the non-Swiss employees. Simple as that. If you don't have a Swiss passport, you do source tax." — T-010, Anna
- **F-TR-007** (hr_transcript): HR uses the Zurich tariff calculator on the canton's website to get the tariff code, clicking through it with the employee's answers.
  - "I use the Zurich calculator on the canton's website. The one that gives you the tariff code." — T-012, Anna
- **F-TR-008** (hr_transcript): For now, the Zurich calculator is used for every employee subject to source tax. The stakeholder knows this is not exactly how it works, and the interviewer agreed to keep it this way.
  - "For everybody I use Zurich, by the way. I know it's not exactly how it works, but that's what we do for now." — T-012, Anna
  - "We'll keep that for now." — T-013, Leo
- **F-TR-009** (hr_transcript): HR needs the employee's full address: street, house number, postcode, town and country.
  - "Yes, I need the address, obviously. The full address. Street, number, postcode, town, country." — T-014, Anna
- **F-TR-010** (hr_transcript): The address must be complete, because HR posts many documents to employees. It is a normal postal address, as you would write it on an envelope, with no extra parts.
  - "We post a lot of documents to people, so it has to be complete." — T-014, Anna
  - "No, no. Just a normal address, the way you would write it on an envelope." — T-016, Anna
- **F-TR-014** (hr_transcript): HR needs the employee's first working day for the pension fund. It is the most important item, and HR asks the employee to confirm it because it changes often.
  - "I need their first working day. That's the number one thing, and I ask them to confirm it, because it moves more often than you'd think." — T-024, Anna
- **F-TR-015** (hr_transcript): The first working day often changes, for example when new hires negotiate leaving their old employer a week earlier.
  - "People negotiate with their old employer, they get out a week earlier." — T-026, Anna
- **F-TR-016** (hr_transcript): First version: pension fund insurance starts on the first day of the month after the first working day. Example: a first working day of 15.03 gives an insurance start of 01.04.
  - "because insurance starts on the first of the following month. So for her that was the first of April" — T-026, Anna
- **F-TR-017** (hr_transcript): Exception: if the first working day is exactly the first day of a month, insurance starts on that same day.
  - "Unless somebody starts exactly on the first, of course, then it's just that day." — T-028, Anna
- **F-TR-018** (hr_transcript, inferred): Final rule: the insurance start date is derived from the first working day. If the first working day is the 1st of a month, insurance starts that day. Otherwise it starts on the 1st of the following month. The employee is not asked for it.
  - "because insurance starts on the first of the following month." — T-026, Anna
  - "Unless somebody starts exactly on the first, of course, then it's just that day." — T-028, Anna
- **F-TR-019** (hr_transcript, inferred): Incident: Julia moved her first working day to 15 March, HR did not update it, and the fund ended up with a wrong insurance start date (it should have been 1 April). This led to an unfriendly letter and took weeks to fix. It shows that the insurance start date must follow the latest confirmed first working day.
  - "She moved her first working day to the 15th of March, and I didn't update it." — T-026, Anna
  - "I got a very unfriendly letter." — T-026, Anna
  - "It took weeks to fix." — T-028, Anna
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
- **F-TR-025** (hr_transcript): Correction: employees with a C permit are not subject to source tax and are treated like Swiss nationals (example: Maria, Portuguese with a C permit). So the rule becomes non-Swiss, except C permit holders. Asked if that was everything, the stakeholder answered only 'I think so'.
  - "So, not the people with a C permit. They're treated like Swiss people for this." — T-038, Anna
  - "Okay, so non-Swiss, but not with a C permit." — T-039, Leo
  - "I think so." — T-040, Anna
- **F-TR-028** (hr_transcript): The stakeholder would love the form to remind employees to bring their permit, because half of them forget. Not decided: the interviewer deferred the wording to later.
  - "What I would love is if the form could remind people to bring their permit. Half of them forget." — T-042, Anna
  - "We can look at the wording later." — T-043, Leo
- **F-TR-029** (hr_transcript): For married employees, the source tax calculator asks different questions, for example whether the husband or wife works.
  - "It changes the questions in the calculator, yes. Whether the husband or wife works." — T-044, Anna
- **F-TR-030** (hr_transcript): Addition: an employee married to someone who is Swiss or holds a C permit, and who lives in Switzerland, is not subject to source tax. Example: Tomás, Brazilian with a B permit, whose Swiss wife lives with him in Winterthur.
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." — T-044, Anna
- **F-TR-031** (hr_transcript): To decide on source tax, HR needs the spouse's nationality, the spouse's permit (if they have one), and whether the spouse lives in Switzerland.
  - "So you need to know about the spouse as well." — T-045, Leo
  - "Yes. Their nationality, their permit if they have one, and that they live here." — T-046, Anna
- **F-TR-032** (hr_transcript, inferred): Spouse nationality, permit and residence are only needed for married employees whose own status would otherwise make them subject to source tax: non-Swiss, no C permit, living in Switzerland. The spouse permit is only needed if the spouse is not Swiss.
  - "it also changes who has to do it at all." — T-044, Anna
  - "Their nationality, their permit if they have one, and that they live here." — T-046, Anna
- **F-TR-033** (hr_transcript): Today HR checks the spouse case by hand and collects spouse details by email, which takes a long time.
  - "I always have to check that one by hand." — T-044, Anna
  - "I ask them by email, and it takes forever." — T-046, Anna
- **F-TR-034** (hr_transcript): Addition: employees who live abroad and work in Switzerland are always subject to source tax, whatever their nationality. Example: Stefan is Swiss, lives in Konstanz, and is still subject.
  - "Those people do source tax because they work here and they don't live here." — T-048, Anna
  - "And there it doesn't matter what passport you have, by the way." — T-048, Anna
  - "So someone living abroad and working here always does it?" — T-049, Leo
  - "Yes." — T-050, Anna
- **F-TR-036** (hr_transcript): For employees living abroad, the source tax calculator asks more questions. Germany has its own forms, which the stakeholder cannot name. The interviewer said the calculator will define these questions.
  - "And with them the calculator gets much more complicated, there are more questions." — T-050, Anna
  - "Germany has its own forms, I can never remember what they're called." — T-050, Anna
  - "the calculator will tell us." — T-051, Leo
- **F-TR-037** (hr_transcript, inferred): Consolidated final rule. (1) An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. (2) An employee living in Switzerland who is Swiss or holds a C permit is not subject. (3) An employee living in Switzerland who is non-Swiss without a C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. (4) Otherwise the employee is subject. The stakeholder hedged on completeness ('I think that's it').
  - "If you don't have a Swiss passport, you do source tax." — T-010, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — T-038, Anna
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Those people do source tax because they work here and they don't live here." — T-048, Anna
  - "I think that's it." — T-048, Anna
- **F-TR-038** (hr_transcript, inferred): The employee's nationality is needed to decide whether they are subject to source tax.
  - "If you don't have a Swiss passport, you do source tax." — T-010, Anna
- **F-TR-039** (hr_transcript, inferred): Non-Swiss employees' permit type (e.g. B permit, C permit) is needed to decide whether they are subject to source tax.
  - "She has a C permit. So, not the people with a C permit." — T-038, Anna
- **F-TR-040** (hr_transcript, inferred): 'Lives here' in the source tax rules means living in Switzerland. The employee's country of residence can be taken from the country of the home address.
  - "Those people do source tax because they work here and they don't live here." — T-048, Anna
  - "and they live in Winterthur." — T-044, Anna
- **G-01** (product owner guidance): Lonio collects onboarding data from a new employee **once** and reuses it for every receiving party. Asking too little blocks a registration; asking too much collects personal data we must not have (data minimisation). A question must only be asked when at least one receiving party needs the answer for this person.
- **G-04** (product owner guidance): Scope of these feature specs: what Lonio asks the new employee (which information, in which order, under which conditions, required or not) and the business rules derived from the answers. How collected data is transmitted to each receiving party (exports, portal entry, change notifications) is a separate topic; each information item documents which stakeholder needs it and why.
- **G-05** (product owner guidance): Simplifications given by the assignment: Switzerland has exactly one source tax system (Zurich's) and exactly one pension fund (Pensionskasse Muster).
- **G-07** (product owner guidance): The pension fund screenshots show dropdowns with **all** their options.
- **G-08** (product owner guidance): Prefer asking for primary facts and **deriving** values (e.g. ask the first working day, derive the insurance start date) instead of asking the employee for values they cannot know.
- **G-09** (product owner guidance): Questionnaire language: English.
- **G-10** (product owner guidance): Business wording for values (used in allowed values and examples): countries by English name ("Switzerland", "Germany", "Liechtenstein"), permits as "B permit", "C permit", civil status exactly as the pension fund's list shows it ("Single", "Married", ...), dates as DD.MM.YYYY, yes/no as "yes"/"no".
