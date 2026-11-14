# [US-03.4] Canton for employees living in Switzerland

**As** pension fund, **I want** to receive a Swiss canton for the employee, **so that** I can complete the required canton field of the registration

Priority P1: Canton is a required pension fund field; without it the registration is blocked (F-SC-006, F-SC-015).

## Acceptance criteria

**AC-03.4.1 Canton is asked and required only of employees living in Switzerland**
- Given the employee has given the country of their home address
- When the country is Switzerland
- Then the employee is asked for their canton, cannot leave it empty, and it is made available for the pension fund registration; employees living outside Switzerland are not asked, until the fund clarifies whether it means the canton of residence or of work and what applies to employees living abroad (OQ-02).

| Example | Country of home address (country of residence) | → | Canton |
|---|---|---|---|
| Tomás, lives in Winterthur (F-TR-030) | Switzerland | → | required |
| Cross-border employee living in Germany | Germany | → | not asked |
| Employee living in Liechtenstein | Liechtenstein | → | not asked |

**AC-03.4.2 Only the fund's Swiss cantons are offered**
- Given the employee is asked for their canton
- When they choose an answer
- Then they can choose exactly one of the 26 cantons the pension fund lists: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich.

+++ Evidence

- F-SC-006: The pension fund registration requires a canton (dropdown in the Employee section, marked required); the portal does not label whether it is the residence or work canton. — "Canton" (S01-E14) — "Employee" (S01-E09)
- F-SC-007: The Canton dropdown offers exactly these 26 options: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for living outside Switzerland. — "Canton" (S02-E14) — "Aargau" (S02-E16) — "Appenzell Ausserrhoden" (S02-E17) — "Appenzell Innerrhoden" (S02-E18) — "Basel-Landschaft" (S02-E19) — "Basel-Stadt" (S02-E20) — "Bern" (S02-E21) — "Fribourg" (S02-E22) — "Geneva" (S02-E23) — "Glarus" (S02-E24) — "Graubünden" (S02-E25) — "Jura" (S02-E26) — "Lucerne" (S02-E27) — "Neuchâtel" (S02-E28) — "Nidwalden" (S02-E29) — "Obwalden" (S02-E30) — "Schaffhausen" (S02-E31) — "Schwyz" (S02-E32) — "Solothurn" (S02-E33) — "St. Gallen" (S02-E34) — "Thurgau" (S02-E35) — "Ticino" (S02-E36) — "Uri" (S02-E37) — "Valais" (S02-E38) — "Vaud" (S02-E39) — "Zug" (S02-E40) — "Zurich" (S02-E41)
- F-SC-015: Submitting the form with required fields empty shows the banner 'Please correct the highlighted fields.', highlights each empty field and shows a per-field error of the form '<Field> is required.' (First name, Last name, Date of birth, Canton, Insurance start date, Civil status). — "Please correct the highlighted fields." (S06-E05) — "First name is required." (S06-E09) — "Last name is required." (S06-E12) — "Date of birth is required." (S06-E16) — "Canton is required." (S06-E19) — "Insurance start date is required." (S06-E24) — "Civil status is required." (S06-E27)
- F-SC-017: The Canton dropdown only lists Swiss cantons; it is unclear what to enter for an employee who lives abroad (e.g. a cross-border commuter living in Germany), and whether the field means the residence canton or the work canton. — "Canton" (S02-E14) — "Zurich" (S02-E41)
- G-01
- G-07

Spec: `requirements/employee-onboarding/features/FEAT-03-pension-fund-registration-data.md`
+++
