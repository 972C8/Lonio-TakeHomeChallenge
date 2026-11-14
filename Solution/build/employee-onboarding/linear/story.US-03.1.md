# [US-03.1] Name and date of birth for the pension fund

**As** pension fund, **I want** to receive the new employee's first name, last name and date of birth, **so that** I can register the employee for occupational pension without the registration being rejected for missing required fields

Priority P1: These are required fields of the pension fund registration; if any is missing, the portal rejects the registration and highlights the field (F-SC-015), which blocks the registration.

## Acceptance criteria

**AC-03.1.1 First and last name are always asked and required**
- Given a new employee is filling in the onboarding questionnaire
- When they reach the personal details
- Then they are asked for their first name and their last name; neither can be left empty, and both are made available for the pension fund registration.

**AC-03.1.2 Date of birth is always asked and required as a date**
- Given a new employee is filling in the onboarding questionnaire
- When they reach the personal details
- Then they are asked for their date of birth as a day, month and year (shown as DD.MM.YYYY, e.g. 14.02.1990); it cannot be left empty and is made available for the pension fund registration.

**AC-03.1.3 Each detail is asked only once**
- Given the employee has given their name and date of birth
- When another part of the onboarding or another receiving party needs the same detail
- Then the employee is not asked for it again; the earlier answer is reused.

+++ Evidence

- F-SC-002: The pension fund registration requires the employee's first name (text input, marked required). — "First name" (S01-E10) — "Fields marked * are required." (S01-E23)
- F-SC-003: The pension fund registration requires the employee's last name (text input, marked required). — "Last name" (S01-E11)
- F-SC-004: The pension fund registration requires the employee's date of birth (text input, marked required). — "Date of birth" (S01-E12)
- F-SC-005: The employee's date of birth is entered in the format DD.MM.YYYY. — "DD.MM.YYYY" (S01-E13)
- F-SC-015: Submitting the form with required fields empty shows the banner 'Please correct the highlighted fields.', highlights each empty field and shows a per-field error of the form '<Field> is required.' (First name, Last name, Date of birth, Canton, Insurance start date, Civil status). — "Please correct the highlighted fields." (S06-E05) — "First name is required." (S06-E09) — "Last name is required." (S06-E12) — "Date of birth is required." (S06-E16) — "Canton is required." (S06-E19) — "Insurance start date is required." (S06-E24) — "Civil status is required." (S06-E27)
- G-01

Spec: `requirements/employee-onboarding/features/FEAT-03-pension-fund-registration-data.md`
+++
