---
id: FEAT-02-home-address
title: "Complete home address and country of residence"
order: 2
stakeholders: [employee, hr, source_tax]
stories: [US-02.1, US-02.2]
information: [address_street, address_house_number, address_postcode, address_town, address_country]
rules: []
open_questions: []
---

# Complete home address and country of residence

**Goal:** Every new employee gives a complete postal address once, so HR can post documents, and its country tells the other steps whether the employee lives in Switzerland.

## Context
HR posts many documents to employees and needs the complete address as written on an envelope: street, number, postcode, town and country, with no extra parts (F-TR-009, F-TR-010). The country of the home address is also the employee's country of residence (F-TR-040, G-09). Several later questions depend on it. Employees living abroad are always subject to source tax (F-TR-034, F-TR-037), and the pension fund canton is asked only of employees living in Switzerland. This feature therefore comes before the pension and source tax features that depend on it.

**Stakeholders:** new employee, HR, source tax office


## User stories

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

## Information needed

The information this feature owns. Each piece is asked once and reused by
every stakeholder listed (see [information.md](../information.md) for all).

### Street
| | |
|---|---|
| **What?** | Street of the employee's home address. – Form: Part of a complete postal address, as written on an envelope: street, number, postcode, town and country, with no extra parts. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: HR posts many documents to employees, so the address must be complete. |
| **Status · sources** | confirmed · F-TR-009, F-TR-010 |

### House number
| | |
|---|---|
| **What?** | House number of the employee's home address. – Form: Part of a complete postal address, as written on an envelope. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: HR posts many documents to employees, so the address must be complete. |
| **Status · sources** | confirmed · F-TR-009, F-TR-010 |
| **Notes** | HR named the number as part of the full address; whether every address has a house number is not discussed. |

### Postcode
| | |
|---|---|
| **What?** | Postcode of the employee's home address. – Form: Part of a complete postal address, as written on an envelope. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: HR posts many documents to employees, so the address must be complete. |
| **Status · sources** | confirmed · F-TR-009, F-TR-010 |

### Town
| | |
|---|---|
| **What?** | Town of the employee's home address. – Form: Part of a complete postal address, as written on an envelope. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: HR posts many documents to employees, so the address must be complete. |
| **Status · sources** | confirmed · F-TR-009, F-TR-010 |

### Country of home address (country of residence)
| | |
|---|---|
| **What?** | Country of the employee's home address. It is also the employee's country of residence, which decides whether the employee lives in Switzerland for the source tax rules. – Form: Part of a complete postal address, as written on an envelope. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: HR posts many documents to employees, so the address must be complete; and to decide whether the employee is subject to source tax (employees living abroad always are).<br>source tax office: Employees living abroad are always subject to source tax, and the calculator asks them more questions. |
| **Status · sources** | inferred · F-TR-009, F-TR-010, F-TR-034, F-TR-037, F-TR-040, F-TR-036, G-09 |
| **Notes** | Using the address country as country of residence is an inference (F-TR-040) confirmed by the product owner convention (G-09). |

## Evidence
- **F-TR-009** (hr_transcript): HR needs the employee's full address: street, house number, postcode, town and country.
  - "Yes, I need the address, obviously. The full address. Street, number, postcode, town, country." — T-014, Anna
- **F-TR-010** (hr_transcript): The address must be complete, because HR posts many documents to employees. It is a normal postal address, as you would write it on an envelope, with no extra parts.
  - "We post a lot of documents to people, so it has to be complete." — T-014, Anna
  - "No, no. Just a normal address, the way you would write it on an envelope." — T-016, Anna
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
- **F-TR-040** (hr_transcript, inferred): 'Lives here' in the source tax rules means living in Switzerland. The employee's country of residence can be taken from the country of the home address.
  - "Those people do source tax because they work here and they don't live here." — T-048, Anna
  - "and they live in Winterthur." — T-044, Anna
- **G-01** (product owner guidance): Lonio collects onboarding data from a new employee **once** and reuses it for every receiving party. Asking too little blocks a registration; asking too much collects personal data we must not have (data minimisation). A question must only be asked when at least one receiving party needs the answer for this person.
- **G-09** (product owner guidance): Questionnaire language: English.
