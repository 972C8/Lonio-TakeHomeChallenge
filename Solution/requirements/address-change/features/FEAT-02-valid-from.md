---
id: FEAT-02-valid-from
title: "Date from which the new address applies"
order: 2
stakeholders: [employee, hr]
stories: [US-02.1, US-02.2]
information: [valid_from]
rules: [valid_from_within_three_months]
open_questions: [OQ-02, OQ-03]
---

# Date from which the new address applies

**Goal:** HR knows from which date to use the new address, in particular for the payslips sent out on the 25th, and still accepts moves reported late within a fixed window.

## Context
HR needs to know which address applies when documents go out, especially the payslips sent on the 25th (F-TR-007, F-TR-008, F-TR-018). People often report their move late, so a valid-from date in the past must be accepted, but not more than three months back (F-TR-019, F-TR-020). The meeting set no limit for future dates (F-TR-021). Dates use the format DD.MM.YYYY (G-02). Still open: the exact cut-off, how older dates are handled, and whether there is a future limit.

**Stakeholders:** employee, HR

> ⚠ Open questions affecting this feature: [OQ-02](../open-questions.md#oq-02), [OQ-03](../open-questions.md#oq-03)

## User stories

### US-02.1 – Report the date from which the new address applies
**As** HR, **I want** every address change to include the date from which the new address applies, **so that** I know which address to use for documents, in particular the payslips sent out on the 25th

Priority **P1** – HR states the date is always required and that without it they cannot do anything, so the process is blocked without it (F-TR-018); it decides the address on payslips (F-TR-008). · Sources: F-TR-007, F-TR-008, F-TR-018, G-02

Covers: Valid from

**Acceptance criteria**

- **AC-02.1.1 Valid-from date is always asked and cannot be left empty**
  - **Given** an employee reports a change of address, whether within Switzerland or abroad
  - **When** the employee gives the details of the move
  - **Then** the employee is always asked from which date the new address applies, and the report cannot be completed without this date
  - _Sources: F-TR-007, F-TR-018_

  | Example | Country of the new address | Valid from | → | Valid from | Checked |
  |---|---|---|---|---|---|
  | Move within Switzerland (illustrative) | Switzerland | 01.12.2026 | → | required | ✅ |
  | Move abroad (illustrative) | Germany | 01.01.2027 | → | required | ✅ |

- **AC-02.1.2 Valid-from date is given as a calendar date in the agreed wording**
  - **Given** an employee states from which date the new address applies
  - **When** the date is recorded and shown
  - **Then** it is a single calendar date written as DD.MM.YYYY (for example 01.12.2026)
  - _Sources: G-02_
- **AC-02.1.3 HR receives the valid-from date with the new address**
  - **Given** an employee has completed an address change report
  - **When** HR receives the report
  - **Then** HR sees the valid-from date together with the new address, so it can decide which address applies to documents going out, such as the payslips on the 25th
  - _Sources: F-TR-007, F-TR-008_
### US-02.2 – Accept late reports up to three months back
**As** employee, **I want** to report my move even if the move has already happened, as long as it was not more than three months ago, **so that** a late report is still accepted and HR can correct my address, while HR is not asked to handle moves that lie too far back

Priority **P1** – Late reporting is common (F-TR-020); without accepting past dates many real reports could not be made, and HR set an explicit three-month limit (F-TR-019). · Status: **inferred** · Sources: F-TR-019, F-TR-020, F-TR-021, G-02

Covers: Valid from, Valid-from date at most three months in the past

**Acceptance criteria**

- **AC-02.2.1 Past date within three months is accepted**
  - **Given** an employee reports a move whose valid-from date is in the past, on or after the date three months before the day of reporting
  - **When** the employee gives the valid-from date
  - **Then** the date is accepted and the report can be completed
  - _Sources: F-TR-019, F-TR-020_

  | Example | today | Valid from | → | Valid-from date at most three months in the past | Checked |
  |---|---|---|---|---|---|
  | Reported about six weeks late (illustrative) | 14.11.2026 | 01.10.2026 | → | yes | ✅ |
  | Exactly three months back (cut-off to be confirmed, see OQ-03) (illustrative) | 14.11.2026 | 14.08.2026 | → | yes | ✅ |

- **AC-02.2.2 Date more than three months back is not accepted**
  - **Given** an employee reports a move whose valid-from date is before the date three months before the day of reporting
  - **When** the employee gives the valid-from date
  - **Then** the date is not accepted and the employee is told that a valid-from date may lie at most three months in the past; what happens to such a report afterwards (rejected or passed to HR for manual handling) is still open, see OQ-03
  - _Sources: F-TR-019_

  | Example | today | Valid from | → | Valid-from date at most three months in the past | Checked |
  |---|---|---|---|---|---|
  | One day beyond the three-month window (illustrative) | 14.11.2026 | 13.08.2026 | → | no | ✅ |
  | Reported about five months late (illustrative) | 14.11.2026 | 01.06.2026 | → | no | ✅ |

- **AC-02.2.3 Today and future dates are accepted**
  - **Given** an employee reports a move that applies from today or from a date in the future
  - **When** the employee gives the valid-from date
  - **Then** the date is accepted; no latest future date applies until HR confirms whether one is needed (see OQ-02)
  - _Sources: F-TR-021_

  | Example | today | Valid from | → | Valid-from date at most three months in the past | Checked |
  |---|---|---|---|---|---|
  | Move applies from today (illustrative) | 14.11.2026 | 14.11.2026 | → | yes | ✅ |
  | Move announced several months ahead (illustrative) | 14.11.2026 | 01.04.2027 | → | yes | ✅ |

_Trace check: partial – The exact three-month boundary (on or after the same date three months back) and telling the employee about the limit are not stated in F-TR-019, which only says 'not more than three months ago'._

## Information needed

The information this feature owns. Each piece is asked once and reused by
every stakeholder listed (see [information.md](../information.md) for all).

### Valid from
| | |
|---|---|
| **What?** | The date from which the new address applies. – Form: Date in the format DD.MM.YYYY. |
| **When do we ask?** | Always |
| **When is it required?** | Always. It may be in the past, but not more than three months ago (see rule valid_from_within_three_months). |
| **Depends on** | nothing |
| **Who needs it?** | HR: Know which address to use for documents, in particular the payslips sent out on the 25th. |
| **Status · sources** | confirmed · F-TR-007, F-TR-008, F-TR-018, F-TR-019, G-02 |

## Business rules

### Valid-from date at most three months in the past
The valid-from date may be in the past, because people often report late, but not more than three months before the day the employee reports the move. The meeting set no limit for future dates.

| # | Valid from compared with three months before today | → Result | Sources |
|---|---|---|---|
| 1 | On or after the date three months before today | Accepted | F-TR-019 |
| 2 | Before the date three months before today | Not accepted | F-TR-019 |

_Status: confirmed · Sources: F-TR-019, F-TR-020, F-TR-021_

## Evidence
- **F-TR-007** (hr_meeting): HR needs the date from which the new address is valid.
  - "And the date from which it is valid" — T-002, Sara
- **F-TR-008** (hr_meeting): Payslips are sent out on the 25th, so HR needs the valid-from date to know which address to use.
  - "because payslips go out on the 25th and we need to know which address to use." — T-002, Sara
- **F-TR-018** (hr_meeting): The valid-from date is always required.
  - "Is the valid-from date always required?" — T-009, Leo
  - "Always. Without it I can't do anything." — T-010, Sara
- **F-TR-019** (hr_meeting): The valid-from date may be in the past, but not more than three months ago.
  - "It can be in the past, people often tell us late, but not more than three months ago." — T-010, Sara
- **F-TR-020** (hr_meeting): Employees often report their move late.
  - "people often tell us late" — T-010, Sara
- **F-TR-021** (hr_meeting, inferred): No upper limit for a future valid-from date was stated.
  - "It can be in the past, people often tell us late, but not more than three months ago." — T-010, Sara
- **G-02** (product owner guidance): Business wording for values: countries by English name ("Switzerland", "Germany"), dates as DD.MM.YYYY, yes/no as "yes"/"no".
