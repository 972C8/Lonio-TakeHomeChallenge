# [US-03.3] Spouse's date of birth for married employees

**As** pension fund, **I want** to receive the spouse's date of birth for every married employee, and only for them, **so that** the registration of married employees is not blocked and no spouse data is collected without need

Priority P1: The portal blocks the registration of a married employee without the spouse's date of birth (F-SC-016).

## Acceptance criteria

**AC-03.3.1 Spouse's date of birth is asked and required only for married employees**
- Given the employee has given their civil status
- When the civil status is Married
- Then the employee is asked for their husband's or wife's date of birth (DD.MM.YYYY), cannot leave it empty, and it is made available for the pension fund registration; for any other civil status it is not asked. Whether the fund needs spouse data for Divorced or Widowed is open (OQ-04).

| Example | Civil status | → | Spouse's date of birth |
|---|---|---|---|
| Tomás, married, wife lives with him in Winterthur (F-TR-030) | Married | → | required |
| Single employee | Single | → | not asked |
| Divorced employee | Divorced | → | not asked |
| Widowed employee | Widowed | → | not asked |

+++ Evidence

- F-SC-012: The pension fund registration has a 'Spouse's date of birth' field (text input) that is marked required when it is shown. — "Spouse's date of birth" (S05-E21)
- F-SC-013: The spouse's date of birth is entered in the format DD.MM.YYYY. — "DD.MM.YYYY" (S05-E23)
- F-SC-014: The 'Spouse's date of birth' field appears only when civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in the empty forms (01, 02, 03, 06). — "Married" (S05-E20) — "Spouse's date of birth" (S05-E21) — "Married" (S07-E20) — "Spouse's date of birth" (S07-E21) — "Single" (S04-E20)
- F-SC-016: When civil status is Married and the spouse's date of birth is left empty, the portal blocks registration with the error 'Spouse's date of birth is required.' — "Married" (S07-E20) — "Spouse's date of birth is required." (S07-E24)
- F-SC-018: No screenshot shows the form with civil status Divorced or Widowed, so it is unknown whether any extra fields (e.g. spouse data) appear for those values; the list also has no option such as registered partnership or separated, and it is unclear how such cases are to be registered. — "Divorced" (S03-E23) — "Widowed" (S03-E24)
- F-TR-021: If the employee is married, the pension fund wants the date of birth of the husband or wife. — "And if someone is married, they want the date of birth of the husband or wife." (T-032)
- G-01

Spec: `requirements/employee-onboarding/features/FEAT-03-pension-fund-registration-data.md`
+++
