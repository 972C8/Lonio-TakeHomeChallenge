---
id: FEAT-03-payroll-move-abroad
title: "Inform payroll about moves abroad"
order: 3
stakeholders: [employee, hr, payroll]
stories: [US-03.1, US-03.2]
information: []
rules: [payroll_must_be_informed]
open_questions: [OQ-04, OQ-05]
---

# Inform payroll about moves abroad

**Goal:** Payroll is reliably informed whenever an employee moves abroad, so it can check whether source tax applies, and is not involved in moves within Switzerland.

## Context
An employee who moves abroad may become subject to source tax, so payroll has to be told (F-TR-010, F-TR-011, F-TR-012). For moves within Switzerland payroll does not need to know (F-TR-013, F-TR-016), so it should not be informed (G-01). The decision uses the new country captured in FEAT-01 and the valid-from date from FEAT-02. Only HR was interviewed. Payroll's own information needs and how cross-border employees are handled are still open (F-TR-022).

**Stakeholders:** employee, HR, payroll

> ⚠ Open questions affecting this feature: [OQ-04](../open-questions.md#oq-04), [OQ-05](../open-questions.md#oq-05)

## User stories

### US-03.1 – Payroll is informed when an employee moves abroad
**As** payroll, **I want** to be informed whenever an employee reports a move to a country other than Switzerland, **so that** I can check whether the employee is now subject to source tax and handle it correctly

Priority **P1** – HR states payroll 'has to be informed' of moves abroad; a missed notification puts the source-tax obligation at risk (F-TR-011, F-TR-012). · Sources: F-TR-010, F-TR-011, F-TR-012

Covers: Country of the new address, Payroll must be informed of a move abroad

**Acceptance criteria**

- **AC-03.1.1 Move abroad informs payroll**
  - **Given** an employee reports a change of address and the country of the new address is any country other than Switzerland
  - **When** the employee submits the address change
  - **Then** payroll is informed of the move abroad, including the new country of residence, so it can check whether source tax applies. Whether payroll needs any further information from the employee for this check is still open (see OQ-05).
  - _Sources: F-TR-010, F-TR-011, F-TR-012_

  | Example | Country of the new address | → | Country of the new address | Payroll must be informed of a move abroad | Checked |
  |---|---|---|---|---|---|
  | Move to Germany (illustrative) | Germany | → | asked | yes | ✅ |
  | Move to France (illustrative) | France | → | – | yes | ✅ |

- **AC-03.1.2 Country is always known for the payroll decision**
  - **Given** an employee reports a change of address
  - **When** the employee fills in the new address
  - **Then** the country of the new address is always asked and must be given, written as its English name (e.g. "Switzerland", "Germany"), so it is always clear whether payroll has to be informed. The country is received by HR and, for moves abroad, by payroll.
  - _Sources: F-TR-010, F-TR-011, G-02_

  | Example | Country of the new address | → | Country of the new address | Checked |
  |---|---|---|---|---|
  | Country always asked (illustrative) | Switzerland | → | required | ✅ |

_Trace check: partial – The facts say payroll must be informed of a move abroad, but nothing says payroll receives the new country of residence (F-TR-010 is about HR's need)._

### US-03.2 – Payroll is not involved in moves within Switzerland
**As** employee, **I want** my move within Switzerland not to be passed on to payroll, **so that** my personal data is shared only with those who need it for my case

Priority **P2** – Data-minimisation principle (G-01); HR said only the address is needed for Swiss moves (F-TR-013, F-TR-016). No incident or blocked process is reported. · Status: **inferred** · Sources: F-TR-013, F-TR-016, G-01

Covers: Country of the new address, Payroll must be informed of a move abroad

**Acceptance criteria**

- **AC-03.2.1 Move within Switzerland does not inform payroll**
  - **Given** an employee reports a change of address and the country of the new address is Switzerland
  - **When** the employee submits the address change
  - **Then** payroll is not informed of the move; HR handles the address change (and, if the canton changes, the tax office notification) on its own. How employees who currently live abroad and move into Switzerland or within their foreign country are treated is still open (see OQ-04).
  - _Sources: F-TR-013, F-TR-016, G-01_

  | Example | Country of the new address | → | Payroll must be informed of a move abroad | Checked |
  |---|---|---|---|---|
  | Move within Switzerland (illustrative) | Switzerland | → | no | ✅ |

## Information needed

The information this feature owns. Each piece is asked once and reused by
every stakeholder listed (see [information.md](../information.md) for all).

## Business rules

### Payroll must be informed of a move abroad
If the employee moves abroad (the new country is not Switzerland), payroll must be informed, because the employee may then be subject to source tax. For moves within Switzerland, payroll does not have to be informed.

| # | Country of the new address | → Result | Sources |
|---|---|---|---|
| 1 | Switzerland | Payroll does not have to be informed | F-TR-013, F-TR-016 |
| 2 | Any other country | Payroll must be informed (the employee may be subject to source tax) | F-TR-011, F-TR-012 |

_Status: confirmed · Sources: F-TR-011, F-TR-012, F-TR-010_

## Evidence
- **F-TR-010** (hr_meeting): For a move abroad, HR needs the new country of residence.
  - "So for a move abroad I need the new country of residence" — T-006, Sara
- **F-TR-011** (hr_meeting): If the employee moves abroad, payroll must be informed, because the employee may then be subject to source tax.
  - "If somebody moves abroad, payroll needs to know, because then they may have to do source tax." — T-006, Sara
  - "and payroll has to be informed." — T-006, Sara
- **F-TR-012** (hr_meeting): An employee moving abroad may become subject to source tax (hedged: 'may').
  - "because then they may have to do source tax." — T-006, Sara
- **F-TR-013** (hr_meeting): For a move within Switzerland, only the address is needed.
  - "And moves within Switzerland?" — T-007, Leo
  - "Then it's only the address." — T-008, Sara
- **F-TR-016** (hr_meeting, inferred): Final rule for Swiss moves: always ask the new address; additionally ask the new canton only when the canton changes (needed for the tax office); not for moves within the same canton.
  - "Then it's only the address." — T-008, Sara
  - "if someone moves to a different canton, we need the new canton too, for the tax office." — T-008, Sara
  - "Within the same canton, no." — T-008, Sara
- **F-TR-022** (hr_meeting): Sara thinks the list of requirements is complete for now (hedged).
  - "I think that's all for now." — T-012, Sara
- **G-01** (product owner guidance): Ask only what a stakeholder needs for this person (data minimisation).
- **G-02** (product owner guidance): Business wording for values: countries by English name ("Switzerland", "Germany"), dates as DD.MM.YYYY, yes/no as "yes"/"no".
