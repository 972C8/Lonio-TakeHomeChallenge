# [US-01.1] Employee confirms their first working day

**As** HR, **I want** every new employee to confirm their first working day themselves during onboarding, **so that** I always work with the latest agreed start date, even when it moved after the contract was signed, and can register the employee with the pension fund correctly

Priority P1: HR calls it 'the number one thing'; it changes often, and an outdated date once caused a wrong registration at the pension fund, an unfriendly letter and weeks of fixing (F-TR-014, F-TR-019).

## Acceptance criteria

**AC-01.1.1 First working day is asked of every employee and is required**
- Given a new employee is going through onboarding
- When they reach the employment details
- Then they are asked to confirm their first working day at Muster AG, whatever their other answers, and cannot finish onboarding without giving it

| Example | First working day | → | First working day |
|---|---|---|---|
| Julia (F-TR-019) | 15.03.2026 | → | required |

**AC-01.1.2 Employee gives the date as actually agreed, as a calendar date**
- Given the employee's start date may have moved since the contract was signed (e.g. they left their old employer a week earlier)
- When the employee answers the first working day question
- Then they give the start date as currently agreed with Muster AG, as a full date in the form DD.MM.YYYY, so it reflects the latest confirmed first working day

**AC-01.1.3 First working day is available to HR and the pension fund**
- Given the employee has confirmed their first working day
- When onboarding data is handed on to the receiving parties
- Then HR receives the confirmed first working day, and it is the basis for the insurance start date the pension fund needs

+++ Evidence

- F-SC-008: The pension fund registration requires an insurance start date (text input in the Insurance section, marked required). — "Insurance start date" (S01-E17) — "Insurance" (S01-E16)
- F-TR-014: HR needs the employee's first working day for the pension fund. It is the most important item, and HR asks the employee to confirm it because it changes often. — "I need their first working day. That's the number one thing, and I ask them to confirm it, because it moves more often than you'd think." (T-024)
- F-TR-015: The first working day often changes, for example when new hires negotiate leaving their old employer a week earlier. — "People negotiate with their old employer, they get out a week earlier." (T-026)
- F-TR-019: Incident: Julia moved her first working day to 15 March, HR did not update it, and the fund ended up with a wrong insurance start date (it should have been 1 April). This led to an unfriendly letter and took weeks to fix. It shows that the insurance start date must follow the latest confirmed first working day. — "She moved her first working day to the 15th of March, and I didn't update it." (T-026) — "I got a very unfriendly letter." (T-026) — "It took weeks to fix." (T-028)
- G-01
- G-04
- G-10

Spec: `requirements/employee-onboarding/features/FEAT-01-first-working-day-insurance-start.md`
+++
