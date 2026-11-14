---
id: FEAT-04-canton-change
title: "Capture a change of canton for the tax office"
order: 4
stakeholders: [employee, hr]
stories: [US-04.1, US-04.2, US-04.3]
information: [new_canton, previous_canton]
rules: [canton_changes]
open_questions: [OQ-01]
---

# Capture a change of canton for the tax office

**Goal:** When an employee moves to a different Swiss canton, HR gets the new canton and can pass the change to the tax office, without asking for the canton in any other case.

## Context
For a move within Switzerland to a different canton, HR has to pass the new canton to the tax office (F-TR-014, F-TR-016). If the move stays in the same canton or goes abroad, the canton is not needed and must not be asked (F-TR-015, G-01). To see whether the canton changes, the previous canton is compared with the new one (F-TR-017). The previous canton might already be in HR's records. How the change is detected is not yet decided, and this blocks the feature (OQ-01). It comes last because it depends on the country from FEAT-01 and on that decision.

**Stakeholders:** employee, HR

> ⚠ Open questions affecting this feature: [OQ-01](../open-questions.md#oq-01)

## User stories

### US-04.1 – HR receives the new canton when the employee moves to a different canton
**As** HR, **I want** to receive the new canton whenever an employee moves within Switzerland to a different canton, **so that** I can pass the change of canton to the tax office

Priority **P1** – HR states the new canton is needed for the tax office (F-TR-014); without it HR cannot meet its reporting duty for a change of canton. Delivery is blocked until OQ-01 is decided. · Status: **inferred** · Sources: F-TR-014, F-TR-016, F-TR-017

Covers: New canton, Move to a different canton

**Acceptance criteria**

- **AC-04.1.1 New canton is asked and required when the canton changes**
  - **Given** an employee reports a move whose new country is Switzerland and whose new canton differs from the previous canton
  - **When** the employee reports the change of address
  - **Then** the new canton is asked and must be given; the move counts as a change of canton. How the change is recognised before the new canton is known is still open (see OQ-01).
  - _Sources: F-TR-014, F-TR-016, F-TR-017_

  | Example | Country of the new address | Previous canton | New canton | → | New canton | Move to a different canton | Checked |
  |---|---|---|---|---|---|---|---|
  | Move from Bern to Zurich (illustrative) | Switzerland | Bern | Zurich | → | required | yes | ✅ |

- **AC-04.1.2 HR receives the new canton for the tax office**
  - **Given** an employee has reported a move to a different Swiss canton and given the new canton
  - **When** the report is submitted
  - **Then** HR receives the new canton together with the new address, so it can pass the change of canton to the tax office. No other stakeholder receives the new canton.
  - _Sources: F-TR-014, F-TR-016_
- **AC-04.1.3 Form of the new canton**
  - **Given** the new canton is asked
  - **When** the employee gives the new canton
  - **Then** the employee names a Swiss canton. The sources define no further list or wording for cantons.
  - _Sources: F-TR-014_
### US-04.2 – Employee is not asked for a canton when it is not needed
**As** employee, **I want** not to be asked for a new canton when I move within the same canton or abroad, **so that** I only give information that HR actually needs for me

Priority **P2** – Data minimisation is a product guideline (G-01) and HR explicitly said the canton is not needed within the same canton (F-TR-015); asking anyway causes no blocked process but adds needless questions. · Status: **inferred** · Sources: F-TR-015, F-TR-016, G-01

Covers: New canton, Move to a different canton

**Acceptance criteria**

- **AC-04.2.1 No new canton for a move within the same canton**
  - **Given** an employee moves within Switzerland and stays in the same canton
  - **When** the employee reports the change of address
  - **Then** only the new address is asked; the new canton is not asked and the move does not count as a change of canton. How this is recognised without asking for the canton is still open (see OQ-01).
  - _Sources: F-TR-015, F-TR-016, G-01_

  | Example | Country of the new address | Previous canton | New canton | → | New canton | Move to a different canton | Checked |
  |---|---|---|---|---|---|---|---|
  | Move within Zurich (illustrative) | Switzerland | Zurich | Zurich | → | not asked | no | ✅ |

- **AC-04.2.2 No new canton for a move abroad**
  - **Given** an employee moves to a country other than Switzerland
  - **When** the employee reports the change of address
  - **Then** the new canton is not asked and the change-of-canton rule does not apply.
  - _Sources: F-TR-016, G-01_

  | Example | Country of the new address | → | New canton | Move to a different canton | Checked |
  |---|---|---|---|---|---|
  | Move to Germany (illustrative) | Germany | → | not asked | no | ✅ |

### US-04.3 – HR knows the previous canton for moves within Switzerland
**As** HR, **I want** the employee's previous canton to be known for every move within Switzerland, **so that** I can tell whether the canton changes and the new canton is asked only when needed

Priority **P1** – The change of canton cannot be determined without the previous canton (F-TR-017), so US-04.1 and US-04.2 depend on it; how it is obtained is the blocking open question OQ-01. · Status: **inferred** · Sources: F-TR-017, F-TR-014, G-01

Covers: Previous canton, Move to a different canton

**Acceptance criteria**

- **AC-04.3.1 Previous canton is needed for moves within Switzerland**
  - **Given** an employee reports a move whose new country is Switzerland
  - **When** the change of address is reported
  - **Then** the previous canton is known and must be available so HR can compare it with the new canton. Whether the employee is asked for it or HR takes it from its own employee records is still open (see OQ-01); following data minimisation, the employee should not be asked for what HR already holds.
  - _Sources: F-TR-017, G-01_

  | Example | Country of the new address | → | Previous canton | Checked |
  |---|---|---|---|---|
  | Swiss move (illustrative) | Switzerland | → | required | ✅ |

- **AC-04.3.2 Previous canton is not needed for moves abroad**
  - **Given** an employee moves to a country other than Switzerland
  - **When** the change of address is reported
  - **Then** the previous canton is not asked, because no change of canton has to be determined.
  - _Sources: F-TR-017, G-01_

  | Example | Country of the new address | → | Previous canton | Checked |
  |---|---|---|---|---|
  | Move to Germany (illustrative) | Germany | → | not asked | ✅ |

- **AC-04.3.3 Previous canton is used only to detect the change**
  - **Given** the previous canton is known for a move within Switzerland
  - **When** HR processes the report
  - **Then** the previous canton is used by HR only to tell whether the canton changes; it is not passed to any other stakeholder.
  - _Sources: F-TR-017, G-01_
_Trace check: partial – AC-04.3.3 claims the previous canton is used only by HR and not passed to any other stakeholder, which F-TR-017 and G-01 do not state; AC-04.3.2 (not asked abroad) is also only inferred, and the P1 priority is not backed by the facts._

## Information needed

The information this feature owns. Each piece is asked once and reused by
every stakeholder listed (see [information.md](../information.md) for all).

### New canton
| | |
|---|---|
| **What?** | The Swiss canton the employee is moving to. Only needed if the employee moves to a different canton. |
| **When do we ask?** | Only if the employee moves within Switzerland to a different canton than before. Not asked if the move stays in the same canton or is abroad. |
| **When is it required?** | Whenever it is asked |
| **Depends on** | Country of the new address, Previous canton |
| **Who needs it?** | HR: Pass the change of canton to the tax office. |
| **Status · sources** | inferred · F-TR-014, F-TR-015, F-TR-016, G-01 |
| **Notes** | The meeting did not say how a canton change is found out before the new canton is known (see OQ-01). The internal condition can only check this once both cantons are known. |

### Previous canton
| | |
|---|---|
| **What?** | The Swiss canton the employee lived in before the move. It is used only to tell whether the canton changes. |
| **When do we ask?** | Only for moves within Switzerland. It is open whether the employee is asked or HR takes it from its own employee records (see OQ-01). |
| **When is it required?** | For moves within Switzerland, so HR can tell whether the canton changes |
| **Depends on** | Country of the new address |
| **Who needs it?** | HR: Tell whether the employee moves to a different canton, so the new canton is asked only when needed. |
| **Status · sources** | inferred · F-TR-017, F-TR-014, G-01 |
| **Notes** | Data minimisation (G-01) suggests not asking the employee if HR already has this information. |

## Business rules

### Move to a different canton
A move within Switzerland changes canton when the new canton is different from the previous canton. Only then is the new canton needed for the tax office.

| # | Country of the new address | New canton compared with previous canton | → Result | Sources |
|---|---|---|---|---|
| 1 | Switzerland | Different | Canton changes – new canton is needed for the tax office | F-TR-014, F-TR-016 |
| 2 | Switzerland | Same | Canton does not change – new canton is not asked | F-TR-015, F-TR-016 |
| 3 | Any other country | – | Not applicable (move abroad) – new canton is not asked | F-TR-010, F-TR-016 |

_Status: inferred · Sources: F-TR-014, F-TR-015, F-TR-016, F-TR-017_

## Evidence
- **F-TR-014** (hr_meeting): If the employee moves to a different Swiss canton, the new canton is also needed, for the tax office.
  - "if someone moves to a different canton, we need the new canton too, for the tax office." — T-008, Sara
- **F-TR-015** (hr_meeting): For a move within the same canton, the new canton is not asked.
  - "Within the same canton, no." — T-008, Sara
- **F-TR-016** (hr_meeting, inferred): Final rule for Swiss moves: always ask the new address; additionally ask the new canton only when the canton changes (needed for the tax office); not for moves within the same canton.
  - "Then it's only the address." — T-008, Sara
  - "if someone moves to a different canton, we need the new canton too, for the tax office." — T-008, Sara
  - "Within the same canton, no." — T-008, Sara
- **F-TR-017** (hr_meeting, inferred): To determine whether the canton changes, the previous canton (or current canton) must be known; the stakeholder did not state how.
  - "if someone moves to a different canton, we need the new canton too" — T-008, Sara
- **G-01** (product owner guidance): Ask only what a stakeholder needs for this person (data minimisation).
