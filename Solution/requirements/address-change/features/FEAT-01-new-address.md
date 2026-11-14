---
id: FEAT-01-new-address
title: "Capture the new address"
order: 1
stakeholders: [employee, hr]
stories: [US-01.1, US-01.2]
information: [new_street, new_house_number, new_postcode, new_town, new_country]
rules: []
open_questions: [OQ-06]
---

# Capture the new address

**Goal:** HR gets the complete new address of a moving employee so master data is updated and documents such as payslips reach the right address.

## Context
When an employee moves, HR has to update the employee master data and send documents to the new address (F-TR-001, F-TR-006, F-TR-013). The new address is street, house number, postcode, town and country, all needed every time (F-TR-016). The country also shows whether the move is within Switzerland or abroad, which the payroll and canton features depend on (F-TR-010). Countries are written by their English names (G-02). Only what HR needs is asked (G-01). The reason for the move is explicitly excluded (EX-01, F-TR-009). This feature comes first because every other feature builds on the new address, and especially on the country.

**Stakeholders:** employee, HR

> ⚠ Open questions affecting this feature: [OQ-06](../open-questions.md#oq-06)

## User stories

### US-01.1 – Report the street, house number, postcode and town of the new address
**As** HR, **I want** every employee who reports a move to give me the street, house number, postcode and town of their new address, **so that** I can update the employee master data and send documents such as payslips to the correct address

Priority **P1** – Without the new address HR cannot update master data and documents such as payslips go to the wrong address. Every other part of the address change depends on it. · Sources: F-TR-001, F-TR-002, F-TR-003, F-TR-004, F-TR-006, F-TR-013, F-TR-016, F-TR-009, G-01

Covers: Street of the new address, House number of the new address, Postcode of the new address, Town of the new address

**Acceptance criteria**

- **AC-01.1.1 Street, house number, postcode and town are always asked and must be given**
  - **Given** an employee reports a change of address
  - **When** they give their new address
  - **Then** they are asked for the street, house number, postcode and town of the new address, whether the move is within Switzerland or abroad, and the report cannot be completed while any of these four is missing
  - _Sources: F-TR-001, F-TR-002, F-TR-003, F-TR-004, F-TR-006, F-TR-013, F-TR-016_

  | Example | Country of the new address | → | Street of the new address | House number of the new address | Postcode of the new address | Town of the new address | Checked |
  |---|---|---|---|---|---|---|---|
  | Move within Switzerland (illustrative) | Switzerland | → | required | required | required | required | ✅ |
  | Move abroad (illustrative) | Germany | → | required | required | required | required | ✅ |

- **AC-01.1.2 HR receives the new address**
  - **Given** an employee has completed their change of address report
  - **When** HR looks at the report
  - **Then** HR has the street, house number, postcode and town of the new address and can update the master data and send documents such as payslips there
  - _Sources: F-TR-001, F-TR-002, F-TR-003, F-TR-004, F-TR-006_
- **AC-01.1.3 The reason for the move is never asked**
  - **Given** an employee reports a change of address
  - **When** they go through the questions
  - **Then** they are not asked why they are moving, because that is private and HR does not want to know it
  - _Sources: F-TR-009, G-01_
_Trace check: partial – The facts back the four address items, the Swiss and abroad cases and the reason never being asked, but they don't support the payslip purpose or the 'cannot be completed while any is missing' requirement._

### US-01.2 – Report the country of the new address
**As** HR, **I want** every employee who reports a move to give me the country of their new address, written by its English name, **so that** I have the complete address for master data and documents, and I can tell whether the move is within Switzerland or abroad

Priority **P1** – The country completes the address and decides whether the move is abroad; the payroll (source tax) and canton steps depend on it. · Sources: F-TR-005, F-TR-006, F-TR-010, F-TR-016, G-02

Covers: Country of the new address

**Acceptance criteria**

- **AC-01.2.1 The country is always asked and must be given**
  - **Given** an employee reports a change of address
  - **When** they give their new address
  - **Then** they are asked for the country of the new address, and the report cannot be completed without it, whether the move is within Switzerland or abroad
  - _Sources: F-TR-005, F-TR-006, F-TR-010, F-TR-016_

  | Example | Country of the new address | → | Country of the new address | Checked |
  |---|---|---|---|---|
  | Move within Switzerland (illustrative) | Switzerland | → | required | ✅ |
  | Move abroad (illustrative) | Germany | → | required | ✅ |

- **AC-01.2.2 Countries are written by their English names**
  - **Given** an employee gives the country of the new address
  - **When** the country is recorded
  - **Then** it is shown by its English name, for example "Switzerland" or "Germany". Whether employees choose from a fixed list of countries or from all countries is still open (see OQ-06); until it is decided, no country is excluded
  - _Sources: G-02, F-TR-005_
- **AC-01.2.3 HR receives the country and can tell a move abroad from a move within Switzerland**
  - **Given** an employee has completed their change of address report
  - **When** HR looks at the report
  - **Then** HR has the country of the new address, can use it for master data and documents, and can see whether the move is within Switzerland or abroad (the new country of residence)
  - _Sources: F-TR-005, F-TR-010_
## Information needed

The information this feature owns. Each piece is asked once and reused by
every stakeholder listed (see [information.md](../information.md) for all).

### Street of the new address
| | |
|---|---|
| **What?** | The street of the address the employee is moving to. – Form: Part of the new address: street, number, postcode, town and country. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Update the employee's master data and send documents (e.g. payslips) to the correct address. |
| **Status · sources** | confirmed · F-TR-001, F-TR-006, F-TR-013, F-TR-016 |

### House number of the new address
| | |
|---|---|
| **What?** | The house number of the address the employee is moving to. – Form: Part of the new address: street, number, postcode, town and country. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Update the employee's master data and send documents to the correct address. |
| **Status · sources** | confirmed · F-TR-002, F-TR-006, F-TR-016 |
| **Notes** | The meeting did not discuss addresses without a house number; whether it may be left empty is not stated. |

### Postcode of the new address
| | |
|---|---|
| **What?** | The postcode of the address the employee is moving to. – Form: Part of the new address: street, number, postcode, town and country. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Update the employee's master data and send documents to the correct address. |
| **Status · sources** | confirmed · F-TR-003, F-TR-006, F-TR-016 |

### Town of the new address
| | |
|---|---|
| **What?** | The town of the address the employee is moving to. – Form: Part of the new address: street, number, postcode, town and country. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Update the employee's master data and send documents to the correct address. |
| **Status · sources** | confirmed · F-TR-004, F-TR-006, F-TR-016 |

### Country of the new address
| | |
|---|---|
| **What?** | The country the employee is moving to (the new country of residence). It shows whether the move is within Switzerland or abroad. – Form: Part of the new address: street, number, postcode, town and country. Country written as its English name, e.g. "Switzerland", "Germany". |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Update the employee's master data and send documents to the correct address; tell whether the move is within Switzerland or abroad.<br>payroll: Find out about moves abroad, because the employee may then be subject to source tax. |
| **Status · sources** | confirmed · F-TR-005, F-TR-006, F-TR-010, F-TR-011, G-02 |

## Evidence
- **F-TR-001** (hr_meeting): HR needs the street of the employee's new address.
  - "Street, number, postcode, town and country." — T-002, Sara
- **F-TR-002** (hr_meeting): HR needs the house number of the employee's new address.
  - "Street, number, postcode, town and country." — T-002, Sara
- **F-TR-003** (hr_meeting): HR needs the postcode of the employee's new address.
  - "Street, number, postcode, town and country." — T-002, Sara
- **F-TR-004** (hr_meeting): HR needs the town of the employee's new address.
  - "Street, number, postcode, town and country." — T-002, Sara
- **F-TR-005** (hr_meeting): HR needs the country of the employee's new address.
  - "Street, number, postcode, town and country." — T-002, Sara
- **F-TR-006** (hr_meeting): The new address consists of street, house number, postcode, town and country.
  - "The new address, obviously. Street, number, postcode, town and country." — T-002, Sara
- **F-TR-009** (hr_meeting): The reason for the move must not be asked; it is private.
  - "No, we don't want to know why people move. That's private. Please don't ask that." — T-004, Sara
- **F-TR-010** (hr_meeting): For a move abroad, HR needs the new country of residence.
  - "So for a move abroad I need the new country of residence" — T-006, Sara
- **F-TR-011** (hr_meeting): If the employee moves abroad, payroll must be informed, because the employee may then be subject to source tax.
  - "If somebody moves abroad, payroll needs to know, because then they may have to do source tax." — T-006, Sara
  - "and payroll has to be informed." — T-006, Sara
- **F-TR-013** (hr_meeting): For a move within Switzerland, only the address is needed.
  - "And moves within Switzerland?" — T-007, Leo
  - "Then it's only the address." — T-008, Sara
- **F-TR-016** (hr_meeting, inferred): Final rule for Swiss moves: always ask the new address; additionally ask the new canton only when the canton changes (needed for the tax office); not for moves within the same canton.
  - "Then it's only the address." — T-008, Sara
  - "if someone moves to a different canton, we need the new canton too, for the tax office." — T-008, Sara
  - "Within the same canton, no." — T-008, Sara
- **G-01** (product owner guidance): Ask only what a stakeholder needs for this person (data minimisation).
- **G-02** (product owner guidance): Business wording for values: countries by English name ("Switzerland", "Germany"), dates as DD.MM.YYYY, yes/no as "yes"/"no".
