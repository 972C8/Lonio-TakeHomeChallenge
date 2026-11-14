---
id: FEAT-01-first-working-day-insurance-start
title: "Confirmed first working day and derived pension insurance start date"
order: 1
stakeholders: [employee, hr, pension_fund]
stories: [US-01.1, US-01.2]
information: [first_working_day]
rules: [insurance_start_date]
open_questions: []
---

# Confirmed first working day and derived pension insurance start date

**Goal:** Every new employee confirms their first working day, and Lonio works out the pension insurance start date from it, so the fund never gets a wrong or outdated start date.

## Context
HR calls the first working day the most important item. It often changes, so HR asks the employee to confirm it (F-TR-014, F-TR-015). The pension fund requires an insurance start date that is always the 1st of a month (F-SC-008, F-SC-009). HR works it out by hand: if the first working day is the 1st of a month, insurance starts that day, otherwise on the 1st of the following month (F-TR-016, F-TR-017, F-TR-018). Once, an outdated first working day led to a wrong insurance start date at the fund (F-TR-019). Employees cannot know the insurance start date, so Lonio asks only for the primary fact and derives the date (G-08). The employee is not asked for the insurance start date (EX-05).

**Stakeholders:** new employee, HR, pension fund


## User stories

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
## Information needed

The information this feature owns. Each piece is asked once and reused by
every stakeholder listed (see [information.md](../information.md) for all).

### First working day
| | |
|---|---|
| **What?** | The employee's confirmed first working day at Muster AG. The insurance start date is derived from it, so it must always reflect the latest confirmed date. |
| **When do we ask?** | Always |
| **When is it required?** | Always |
| **Depends on** | nothing |
| **Who needs it?** | HR: Most important item; HR asks the employee to confirm it because it often changes.<br>pension fund: Basis for the insurance start date the fund requires. |
| **Status · sources** | confirmed · F-TR-014, F-TR-015, F-TR-018, F-TR-019, F-SC-008, G-08 |
| **Notes** | The employee confirms it. A wrong or outdated first working day once led to a wrong insurance start date at the fund (F-TR-019). |

## Business rules

### Pension insurance start date
The insurance start date is derived from the latest confirmed first working day and is not asked. If the first working day is the 1st of a month, insurance starts that day; otherwise it starts on the 1st of the following month (e.g. first working day 15.03.2026 gives 01.04.2026). The result is always the 1st of a month, as the fund requires, in the format DD.MM.YYYY.

| # | First working day | → Result | Sources |
|---|---|---|---|
| 1 | Is the 1st of a month | Insurance starts on the first working day | F-TR-017, F-TR-018 |
| 2 | Is not the 1st of a month | Insurance starts on the 1st of the following month | F-TR-016, F-TR-018 |

_Status: confirmed · Sources: F-TR-016, F-TR-017, F-TR-018, F-TR-019, F-SC-008, F-SC-009, G-08_

## Evidence
- **F-SC-008** (pension_portal): The pension fund registration requires an insurance start date (text input in the Insurance section, marked required).
  - "Insurance start date" — 01-empty.png (S01-E17)
  - "Insurance" — 01-empty.png (S01-E16)
- **F-SC-009** (pension_portal): The insurance start date is entered as DD.MM.YYYY and must be the 1st of a month.
  - "DD.MM.YYYY. Must be the 1st of a month." — 01-empty.png (S01-E18)
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
- **G-01** (product owner guidance): Lonio collects onboarding data from a new employee **once** and reuses it for every receiving party. Asking too little blocks a registration; asking too much collects personal data we must not have (data minimisation). A question must only be asked when at least one receiving party needs the answer for this person.
- **G-04** (product owner guidance): Scope of these feature specs: what Lonio asks the new employee (which information, in which order, under which conditions, required or not) and the business rules derived from the answers. How collected data is transmitted to each receiving party (exports, portal entry, change notifications) is a separate topic; each information item documents which stakeholder needs it and why.
- **G-08** (product owner guidance): Prefer asking for primary facts and **deriving** values (e.g. ask the first working day, derive the insurance start date) instead of asking the employee for values they cannot know.
- **G-10** (product owner guidance): Business wording for values (used in allowed values and examples): countries by English name ("Switzerland", "Germany", "Liechtenstein"), permits as "B permit", "C permit", civil status exactly as the pension fund's list shows it ("Single", "Married", ...), dates as DD.MM.YYYY, yes/no as "yes"/"no".
