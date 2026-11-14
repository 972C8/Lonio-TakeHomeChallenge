# [US-01.2] Insurance start date is derived from the confirmed first working day

**As** pension fund, **I want** to receive an insurance start date that is the 1st of a month and follows from the employee's latest confirmed first working day, **so that** the employee is insured from the correct date and registrations do not need weeks of correction

Priority P1: The insurance start date is required for registration (F-SC-008); a wrong date already caused an incident with an unfriendly letter and weeks of fixing (F-TR-019).

## Acceptance criteria

**AC-01.2.1 Employee is not asked for the insurance start date**
- Given a new employee is going through onboarding
- When they answer the questionnaire
- Then they are never asked for an insurance start date; Lonio works it out from the confirmed first working day

**AC-01.2.2 First working day on the 1st of a month: insurance starts that day**
- Given the confirmed first working day is the 1st of a month
- When Lonio derives the insurance start date
- Then the insurance start date is the same day as the first working day

| Example | First working day | → | Pension insurance start date |
|---|---|---|---|
| Starts on the 1st of a month | 01.04.2026 | → | 01.04.2026 |
| Starts on 1st January | 01.01.2027 | → | 01.01.2027 |

**AC-01.2.3 First working day not on the 1st: insurance starts on the 1st of the following month**
- Given the confirmed first working day is any day other than the 1st of a month
- When Lonio derives the insurance start date
- Then the insurance start date is the 1st of the month after the first working day, also across a year end

| Example | First working day | → | Pension insurance start date |
|---|---|---|---|
| Julia (F-TR-019) | 15.03.2026 | → | 01.04.2026 |
| Starts on the 2nd of a month | 02.03.2026 | → | 01.04.2026 |
| Starts on the last day of a month | 31.01.2026 | → | 01.02.2026 |
| Starts in December (year end) | 15.12.2026 | → | 01.01.2027 |

**AC-01.2.4 Insurance start date follows the latest confirmed first working day**
- Given the employee's first working day has moved and the employee confirmed the new date
- When Lonio derives the insurance start date
- Then the insurance start date is based on the newly confirmed first working day, never on an earlier, outdated one

| Example | First working day | → | Pension insurance start date |
|---|---|---|---|
| Julia moved her start to 15 March (F-TR-019) | 15.03.2026 | → | 01.04.2026 |

**AC-01.2.5 Insurance start date meets the fund's requirements**
- Given an insurance start date has been derived
- When it is made available for the pension fund registration
- Then it is always the 1st of a month and is given as DD.MM.YYYY, as the fund requires

+++ Evidence

- F-SC-008: The pension fund registration requires an insurance start date (text input in the Insurance section, marked required). — "Insurance start date" (S01-E17) — "Insurance" (S01-E16)
- F-SC-009: The insurance start date is entered as DD.MM.YYYY and must be the 1st of a month. — "DD.MM.YYYY. Must be the 1st of a month." (S01-E18)
- F-TR-015: The first working day often changes, for example when new hires negotiate leaving their old employer a week earlier. — "People negotiate with their old employer, they get out a week earlier." (T-026)
- F-TR-016: First version: pension fund insurance starts on the first day of the month after the first working day. Example: a first working day of 15.03 gives an insurance start of 01.04. — "because insurance starts on the first of the following month. So for her that was the first of April" (T-026)
- F-TR-017: Exception: if the first working day is exactly the first day of a month, insurance starts on that same day. — "Unless somebody starts exactly on the first, of course, then it's just that day." (T-028)
- F-TR-018: Final rule: the insurance start date is derived from the first working day. If the first working day is the 1st of a month, insurance starts that day. Otherwise it starts on the 1st of the following month. The employee is not asked for it. — "because insurance starts on the first of the following month." (T-026) — "Unless somebody starts exactly on the first, of course, then it's just that day." (T-028)
- F-TR-019: Incident: Julia moved her first working day to 15 March, HR did not update it, and the fund ended up with a wrong insurance start date (it should have been 1 April). This led to an unfriendly letter and took weeks to fix. It shows that the insurance start date must follow the latest confirmed first working day. — "She moved her first working day to the 15th of March, and I didn't update it." (T-026) — "I got a very unfriendly letter." (T-026) — "It took weeks to fix." (T-028)
- G-08

Spec: `requirements/employee-onboarding/features/FEAT-01-first-working-day-insurance-start.md`
+++
