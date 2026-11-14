# [US-03.2] Civil status from the pension fund's list

**As** pension fund, **I want** to receive the employee's civil status as one of the values my registration accepts, **so that** I can register the employee and know whether spouse details apply

Priority P1: Civil status is a required pension fund field; without it the registration is blocked (F-SC-010, F-SC-015). It is also an input for source tax (F-TR-029, F-TR-030).

## Acceptance criteria

**AC-03.2.1 Civil status is always asked and required**
- Given a new employee is filling in the onboarding questionnaire
- When they reach the family details
- Then they are asked for their civil status; it cannot be left empty and is made available for the pension fund registration.

**AC-03.2.2 Only the pension fund's civil status values are offered**
- Given the employee is asked for their civil status
- When they choose an answer
- Then they can choose exactly one of: Single, Married, Divorced, Widowed, as the pension fund lists them; no other values are offered. How employees in a registered partnership or another status (e.g. separated) answer is open (OQ-03).

**AC-03.2.3 Civil status is reused for source tax and HR**
- Given the employee has given their civil status
- When the source tax decision or the source tax questions need it
- Then the same answer is reused and the employee is not asked again.

+++ Evidence

- F-SC-010: The pension fund registration requires the employee's civil status (dropdown, marked required). — "Civil status" (S01-E19)
- F-SC-011: The Civil status dropdown offers exactly these options: Single, Married, Divorced, Widowed. — "Civil status" (S03-E19) — "Single" (S03-E21) — "Married" (S03-E22) — "Divorced" (S03-E23) — "Widowed" (S03-E24)
- F-SC-015: Submitting the form with required fields empty shows the banner 'Please correct the highlighted fields.', highlights each empty field and shows a per-field error of the form '<Field> is required.' (First name, Last name, Date of birth, Canton, Insurance start date, Civil status). — "Please correct the highlighted fields." (S06-E05) — "First name is required." (S06-E09) — "Last name is required." (S06-E12) — "Date of birth is required." (S06-E16) — "Canton is required." (S06-E19) — "Insurance start date is required." (S06-E24) — "Civil status is required." (S06-E27)
- F-SC-018: No screenshot shows the form with civil status Divorced or Widowed, so it is unknown whether any extra fields (e.g. spouse data) appear for those values; the list also has no option such as registered partnership or separated, and it is unclear how such cases are to be registered. — "Divorced" (S03-E23) — "Widowed" (S03-E24)
- F-TR-020: The pension fund asks for the employee's civil status. — "Yes, the civil status. They ask for that." (T-032)
- F-TR-022: Civil status options, from the stakeholder's memory and not confirmed: Single, Married, Divorced, and she thinks Widowed. She deferred to the pension fund screenshots for the actual list. — "I'd have to look. You'll see it in the screenshots. Single, married, divorced, I think widowed." (T-034)
- F-TR-023: One current employee (Daniel, in finance) is in a registered partnership. He was entered before the current HR manager's time. — "we do have one colleague in a registered partnership. Daniel, in finance." (T-034) — "That was before my time." (T-036)
- F-TR-024: Unresolved: how the pension fund's screen handles a registered partnership, and whether the fund wants the partner's details. — "I honestly don't know what the fund's screen does in that case, or if they want the partner's details too." (T-036)
- F-TR-029: For married employees, the source tax calculator asks different questions, for example whether the husband or wife works. — "It changes the questions in the calculator, yes. Whether the husband or wife works." (T-044)
- F-TR-030: Addition: an employee married to someone who is Swiss or holds a C permit, and who lives in Switzerland, is not subject to source tax. Example: Tomás, Brazilian with a B permit, whose Swiss wife lives with him in Winterthur. — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (T-044) — "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." (T-044)
- G-01
- G-07

Spec: `requirements/employee-onboarding/features/FEAT-03-pension-fund-registration-data.md`
+++
