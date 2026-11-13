# Traceability

Every requirement cites facts; every fact quotes its source verbatim. Quotes
are machine-checked against the normalized sources (`build/`).

## Requirement → facts

| Requirement | Facts / decisions |
|---|---|
| field `first_name` | F-SC-001, F-SC-015, F-TR-010 |
| field `last_name` | F-SC-002, F-SC-015, F-TR-010 |
| field `date_of_birth` | F-SC-003, F-SC-004, F-SC-015, G-09 |
| field `address_street` | F-TR-009, F-TR-010, F-TR-011 |
| field `address_house_number` | F-TR-010 |
| field `address_postcode` | F-TR-010, G-06 |
| field `address_town` | F-TR-010 |
| field `address_country` | F-TR-010, F-TR-037, F-TR-040, F-TR-043, F-TR-045, G-09 |
| field `residence_canton` | F-SC-005, F-SC-006, F-SC-015, F-SC-018 |
| field `nationality` | F-TR-040, F-TR-041, F-TR-037, G-01 |
| field `permit_type` | F-TR-025, F-TR-026, F-TR-040, F-TR-042, F-TR-029, G-10 |
| field `first_working_day` | F-TR-015, F-TR-016, F-TR-019, G-08 |
| field `civil_status` | F-TR-020, F-TR-022, F-SC-009, F-SC-010, F-SC-015, F-TR-031, F-TR-030, F-TR-023, F-SC-019, G-07, G-10 |
| field `spouse_date_of_birth` | F-TR-021, F-SC-011, F-SC-012, F-SC-013, F-SC-016, F-SC-020 |
| field `spouse_nationality` | F-TR-031, F-TR-033, F-TR-040, F-TR-044, F-TR-032 |
| field `spouse_permit_type` | F-TR-031, F-TR-034, F-TR-035, F-TR-044, G-10 |
| field `spouse_residence_country` | F-TR-031, F-TR-036, F-TR-044, F-TR-045 |
| field `spouse_employed` | F-TR-030, F-TR-007 |
| rule `subject_to_source_tax` | F-TR-040, F-TR-025, F-TR-031, F-TR-037, F-TR-005, F-TR-004, F-TR-006 |
| rule `insurance_start_date` | F-TR-017, F-TR-018, F-TR-019, F-SC-007, F-SC-008, F-SC-021, G-08 |
| notice `permit_reminder` | F-TR-029 |
| notice `first_working_day_confirm` | F-TR-015, F-TR-016, F-TR-019 |

## Facts

| Fact | Source | Kind | Basis | Statement | Anchors |
|---|---|---|---|---|---|
| F-TR-001 | hr_transcript | context | explicit | Today HR collects onboarding data via a Word document and an Excel file, and then types everything into the receiving parties' portals by hand. | T-004 |
| F-TR-002 | hr_transcript | context | explicit | Manual onboarding is time-consuming: last month HR spent a full afternoon on two new hires. | T-004 |
| F-TR-003 | hr_transcript | context | explicit | Muster AG hires around twenty people per year (more in summer) and has about 150 employees, mostly in Zurich. | T-006 |
| F-TR-004 | hr_transcript | context | explicit | Source tax is HR's biggest pain point: because HR doesn't know in advance who must answer the source tax questions, the whole questionnaire is sent to everybody, which annoys Swiss employees. | T-008, T-008 |
| F-TR-005 | hr_transcript | condition | inferred | Source tax questions should be asked only to employees who are subject to source tax, not to everybody. | T-008, T-008 |
| F-TR-006 | hr_transcript | rule | explicit, superseded by F-TR-025, F-TR-037, F-TR-040 | Initial statement: all non-Swiss employees (anyone without a Swiss passport) are subject to source tax. | T-010 |
| F-TR-007 | hr_transcript | decision | explicit | The Zurich source tax calculator (canton website, yields the tariff code) is used for every employee regardless of where they actually belong; Anna acknowledges this is not exactly correct but it is what they do for now, and Leo agrees to keep it. | T-012, T-012, T-013 |
| F-TR-008 | hr_transcript | context | explicit | Today HR clicks through the Zurich calculator manually using the employee's answers. | T-012 |
| F-TR-009 | hr_transcript | field | explicit | HR needs the employee's full postal address. | T-014 |
| F-TR-010 | hr_transcript | format | explicit | The address must be complete with street, house number, postcode, town and country, because HR posts many documents to employees. | T-014 |
| F-TR-011 | hr_transcript | format | explicit | Nothing beyond a normal postal address (as written on an envelope) is needed for the address. | T-016 |
| F-TR-012 | hr_transcript | wish | explicit, superseded by F-TR-013 | Anna would like the form to ask for a photo for employee badges, since phone photos taken at reception are poor. | T-018, T-018 |
| F-TR-013 | hr_transcript | exclusion | explicit | No photo is collected for now; security is changing the badge system next year and the topic is postponed to next year. | T-020, T-021 |
| F-TR-014 | hr_transcript | context | explicit | Muster AG's pension fund is Pensionskasse Muster, which has an old portal; Anna will send screenshots of it. | T-022 |
| F-TR-015 | hr_transcript | field | explicit | The employee's first working day is needed (for the pension fund) and is the most important item; the employee should confirm it. | T-024 |
| F-TR-016 | hr_transcript | context | explicit | The first working day changes often, e.g. when people negotiate an earlier exit with their old employer; a missed update (Julia) caused a wrong date at the fund and weeks of fixing. | T-024, T-026, T-028 |
| F-TR-017 | hr_transcript | rule | explicit, superseded by F-TR-018, F-TR-019 | Pension fund insurance starts on the first day of the month following the first working day (e.g. first working day 15 March -> insurance start 1 April). | T-026 |
| F-TR-018 | hr_transcript | rule | explicit, superseded by F-TR-019 | Exception: if the first working day is exactly the first of a month, insurance starts on that same day. | T-028 |
| F-TR-019 | hr_transcript | rule | inferred | Consolidated: insurance_start_date is derived from first_working_day: if first_working_day is the 1st of a month, insurance starts that day; otherwise it starts on the 1st of the following month. It should be derived, not asked. | T-026, T-028 |
| F-TR-020 | hr_transcript | field | explicit | The pension fund asks for the employee's civil status. | T-032 |
| F-TR-021 | hr_transcript | condition | explicit | If the employee is married, the pension fund wants the spouse's date of birth. | T-032 |
| F-TR-022 | hr_transcript | option | explicit | Civil status options are, per Anna's uncertain recollection, single, married, divorced, and 'I think' widowed; she defers to the pension fund screenshots for the actual list. | T-034 |
| F-TR-023 | hr_transcript | context | explicit | At least one current employee (Daniel in finance) is in a registered partnership, so this civil status occurs in practice. | T-034 |
| F-TR-024 | hr_transcript | open | explicit | Unknown how the pension fund's screen handles registered partnership and whether the fund wants the partner's details (e.g. date of birth) in that case. | T-036 |
| F-TR-025 | hr_transcript | rule | explicit, superseded by F-TR-031, F-TR-037, F-TR-040 | Correction: non-Swiss employees holding a C permit are not subject to source tax; they are treated like Swiss people for this. | T-038, T-038, T-039 |
| F-TR-026 | hr_transcript | context | explicit | Example: Maria in sales is Portuguese with a C permit and does not pay source tax. | T-038 |
| F-TR-027 | hr_transcript | context | explicit | Anna offered to get numbers from the payroll person on how long the source tax process takes. | T-040 |
| F-TR-028 | hr_transcript | exclusion | explicit | Laptops/IT equipment are out of scope; IT has its own process. | T-042 |
| F-TR-029 | hr_transcript | wish | explicit | Anna would love the form to remind employees to bring their permit (on the first day), because half of them forget; wording to be looked at later, not decided. | T-042, T-043 |
| F-TR-030 | hr_transcript | field | explicit | For married employees subject to source tax, the Zurich calculator asks whether the spouse works. | T-044 |
| F-TR-031 | hr_transcript | rule | explicit, superseded by F-TR-037, F-TR-040 | An employee married to a Swiss national or to a C permit holder who lives in Switzerland is not subject to source tax (e.g. Tomás: Brazilian, B permit, Swiss wife, living in Winterthur). | T-044, T-044 |
| F-TR-032 | hr_transcript | context | explicit | Today HR checks the spouse exemption by hand and asks for spouse data by email, which takes very long. | T-044, T-046 |
| F-TR-033 | hr_transcript | field | explicit | For married employees (source tax determination), the spouse's nationality is needed. | T-045, T-046 |
| F-TR-034 | hr_transcript | field | explicit | For married employees (source tax determination), the spouse's permit type is needed if the spouse has one. | T-046 |
| F-TR-035 | hr_transcript | condition | inferred | The spouse's permit is only relevant when the spouse is not Swiss (Swiss nationals have no permit). | T-046 |
| F-TR-036 | hr_transcript | field | explicit | For married employees (source tax determination), whether the spouse lives in Switzerland is needed. | T-046 |
| F-TR-037 | hr_transcript | rule | explicit, superseded by F-TR-040 | Employees who live abroad and work in Switzerland are always subject to source tax, regardless of nationality (e.g. Stefan, Swiss, lives in Konstanz; a warehouse employee lives in Liechtenstein). | T-048, T-048, T-049, T-050 |
| F-TR-038 | hr_transcript | context | explicit | Muster AG has a few employees living across the border (Germany, Liechtenstein). | T-048 |
| F-TR-039 | hr_transcript | open | explicit | For employees living abroad the calculator asks more questions (Germany has its own forms); Anna cannot name them, and Leo defers to the calculator for the details. | T-050, T-051 |
| F-TR-040 | hr_transcript | rule | inferred | Consolidated final rule (Anna hedged completeness with 'I think'): an employee is subject to source tax if residence_country is not CH (regardless of nationality). If living in CH: not subject if nationality is CH; not subject if permit_type is C; not subject if married to a spouse who is Swiss or holds a C permit and lives in CH; otherwise subject. | T-010, T-038, T-044, T-048, T-048 |
| F-TR-041 | hr_transcript | field | inferred | The employee's nationality is needed to determine source tax liability. | T-010 |
| F-TR-042 | hr_transcript | field | inferred | Non-Swiss employees' permit type (at least whether it is a C permit) is needed to determine source tax liability. | T-038 |
| F-TR-043 | hr_transcript | field | inferred | The employee's country of residence is needed to determine source tax liability (living abroad means always subject). | T-048 |
| F-TR-044 | hr_transcript | condition | inferred | Spouse nationality, permit and residence only need to be asked when the employee is married and the spouse exemption could apply (i.e. employee is non-Swiss without C permit and lives in CH). | T-044, T-048 |
| F-TR-045 | hr_transcript | rule | inferred | 'Lives here' in Anna's statements means living in Switzerland. | T-044, T-048 |
| F-TR-046 | hr_transcript | context | explicit | Anna asked when the product will be available; Leo will reply this week after reviewing the screenshots. | T-052, T-053 |
| F-SC-001 | pension_portal | field | explicit | The pension fund registration form has a required 'First name' text field. | S01-E10, S01-E23 |
| F-SC-002 | pension_portal | field | explicit | The pension fund registration form has a required 'Last name' text field. | S01-E11 |
| F-SC-003 | pension_portal | field | explicit | The pension fund registration form has a required 'Date of birth' field (text input). | S01-E12 |
| F-SC-004 | pension_portal | format | explicit | Date of birth is entered in the format DD.MM.YYYY. | S01-E13 |
| F-SC-005 | pension_portal | field | explicit | The pension fund registration form has a required 'Canton' dropdown. | S01-E14, S01-E15 |
| F-SC-006 | pension_portal | option | explicit | The Canton dropdown offers exactly 26 Swiss cantons: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for living outside Switzerland. | S02-E14, S02-E16, S02-E17, S02-E18, S02-E19, S02-E20, S02-E21, S02-E22, S02-E23, S02-E24, S02-E25, S02-E26, S02-E27, S02-E28, S02-E29, S02-E30, S02-E31, S02-E32, S02-E33, S02-E34, S02-E35, S02-E36, S02-E37, S02-E38, S02-E39, S02-E40, S02-E41 |
| F-SC-007 | pension_portal | field | explicit | The pension fund registration form has a required 'Insurance start date' field in the 'Insurance' section. | S01-E17, S01-E16 |
| F-SC-008 | pension_portal | format | explicit | Insurance start date is entered as DD.MM.YYYY and must be the 1st of a month. | S01-E18 |
| F-SC-009 | pension_portal | field | explicit | The pension fund registration form has a required 'Civil status' dropdown. | S01-E19, S01-E20 |
| F-SC-010 | pension_portal | option | explicit | The Civil status dropdown offers exactly four options: Single, Married, Divorced, Widowed. | S03-E19, S03-E21, S03-E22, S03-E23, S03-E24 |
| F-SC-011 | pension_portal | field | explicit | The pension fund registration form has a 'Spouse's date of birth' field, marked required when shown. | S05-E21 |
| F-SC-012 | pension_portal | format | explicit | Spouse's date of birth is entered in the format DD.MM.YYYY. | S05-E23 |
| F-SC-013 | pension_portal | condition | explicit | 'Spouse's date of birth' appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in 01, 02, 03, 06 (civil status not selected). | S05-E20, S05-E21, S07-E20, S07-E21, S04-E20 |
| F-SC-014 | pension_portal | rule | explicit | Submitting the form with missing required fields shows the banner 'Please correct the highlighted fields.' and highlights each empty required field. | S06-E05 |
| F-SC-015 | pension_portal | rule | explicit | Each missing required field shows an error of the form '<Field label> is required.': 'First name is required.', 'Last name is required.', 'Date of birth is required.', 'Canton is required.', 'Insurance start date is required.', 'Civil status is required.' | S06-E09, S06-E12, S06-E16, S06-E19, S06-E24, S06-E27 |
| F-SC-016 | pension_portal | rule | explicit | When Civil status is Married and Spouse's date of birth is empty, registration is rejected with 'Spouse's date of birth is required.' | S07-E20, S07-E24 |
| F-SC-017 | pension_portal | context | explicit | The form is the 'Register new employee' page of the Pensionskasse Muster employer portal, used by the employer Muster AG under 'Insured persons'. | S01-E01, S01-E08, S01-E03, S01-E06 |
| F-SC-018 | pension_portal | open | inferred | The Canton dropdown lists only Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. cross-border commuter), and whether 'Canton' means residence canton or work canton. | S02-E14, S02-E41 |
| F-SC-019 | pension_portal | open | inferred | The Civil status list has no option for registered partnership, separated, or other statuses; it is open how employees with such statuses are registered and whether a partner's date of birth is then needed. | S03-E21, S03-E24 |
| F-SC-020 | pension_portal | open | inferred | No screenshot shows the form with Civil status 'Divorced' or 'Widowed'; whether Spouse's date of birth is hidden for those values is assumed but not proven. | S03-E23, S03-E24 |
| F-SC-021 | pension_portal | open | inferred | The portal requires an insurance start date on the 1st of a month but does not say how it relates to the first working day (e.g. 1st of the start month or next month); the derivation rule insurance_start_date is open. | S01-E18 |
| F-SC-022 | pension_portal | open | inferred | No screenshot shows the error for an invalid date format or an insurance start date that is not the 1st of a month; the wording and any other date constraints (e.g. past/future limits) are unknown. | S06-E23 |
