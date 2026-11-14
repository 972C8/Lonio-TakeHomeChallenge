# Traceability

Every story, criterion, information item and rule cites facts; every fact
quotes its source verbatim, and the quotes are machine-checked against the
sources.

## Stories → sources

| Story | Acceptance criteria | Sources |
|---|---|---|
| US-01.1 Employee confirms their first working day | AC-01.1.1, AC-01.1.2, AC-01.1.3 | F-TR-014, F-TR-015, F-TR-019, G-01 |
| US-01.2 Insurance start date is derived from the confirmed first working day | AC-01.2.1, AC-01.2.2, AC-01.2.3, AC-01.2.4, AC-01.2.5 | F-TR-016, F-TR-017, F-TR-018, F-TR-019, F-SC-008, F-SC-009, G-08 |
| US-02.1 Complete postal address for HR mail | AC-02.1.1, AC-02.1.2, AC-02.1.3 | F-TR-009, F-TR-010 |
| US-02.2 Country of home address as country of residence | AC-02.2.1, AC-02.2.2, AC-02.2.3, AC-02.2.4 | F-TR-034, F-TR-036, F-TR-037, F-TR-040, G-09 |
| US-03.1 Name and date of birth for the pension fund | AC-03.1.1, AC-03.1.2, AC-03.1.3 | F-SC-002, F-SC-003, F-SC-004, F-SC-005, F-SC-015, G-01 |
| US-03.2 Civil status from the pension fund's list | AC-03.2.1, AC-03.2.2, AC-03.2.3 | F-SC-010, F-SC-011, F-SC-015, F-SC-018, F-TR-020, F-TR-022, F-TR-023, F-TR-024, F-TR-029, F-TR-030, G-07 |
| US-03.3 Spouse's date of birth for married employees | AC-03.3.1 | F-TR-021, F-SC-012, F-SC-013, F-SC-014, F-SC-016, F-SC-018, G-01 |
| US-03.4 Canton for employees living in Switzerland | AC-03.4.1, AC-03.4.2 | F-SC-006, F-SC-007, F-SC-015, F-SC-017, G-01, G-07 |
| US-04.1 Ask nationality only of employees living in Switzerland | AC-04.1.1, AC-04.1.2 | F-TR-005, F-TR-006, F-TR-034, F-TR-037, F-TR-038, F-TR-040, G-01 |
| US-04.2 Ask the permit type only of non-Swiss employees living in Switzerland | AC-04.2.1, AC-04.2.2, AC-04.2.3 | F-TR-025, F-TR-028, F-TR-037, F-TR-039, G-01 |
| US-04.3 Ask spouse details only when they can exempt the employee | AC-04.3.1, AC-04.3.2, AC-04.3.3 | F-TR-030, F-TR-031, F-TR-032, F-TR-033, F-TR-037, G-01 |
| US-04.4 Decide whether the employee is subject to source tax | AC-04.4.1, AC-04.4.2, AC-04.4.3, AC-04.4.4, AC-04.4.5 | F-TR-005, F-TR-006, F-TR-007, F-TR-008, F-TR-025, F-TR-029, F-TR-030, F-TR-034, F-TR-036, F-TR-037, F-TR-040, G-05 |

## Information and rules → sources

| Element | Sources |
|---|---|
| First name | F-SC-002, F-SC-015 |
| Last name | F-SC-003, F-SC-015 |
| Date of birth | F-SC-004, F-SC-005, F-SC-015 |
| Street | F-TR-009, F-TR-010 |
| House number | F-TR-009, F-TR-010 |
| Postcode | F-TR-009, F-TR-010 |
| Town | F-TR-009, F-TR-010 |
| Country of home address (country of residence) | F-TR-009, F-TR-010, F-TR-034, F-TR-037, F-TR-040, F-TR-036, G-09 |
| Nationality | F-TR-038, F-TR-006, F-TR-037, F-TR-034, G-01 |
| Permit type | F-TR-039, F-TR-025, F-TR-037, G-01 |
| Canton | F-SC-006, F-SC-007, F-SC-015, F-SC-017 |
| First working day | F-TR-014, F-TR-015, F-TR-018, F-TR-019, F-SC-008, G-08 |
| Civil status | F-TR-020, F-TR-022, F-SC-010, F-SC-011, F-SC-015, F-TR-029, F-TR-030, F-TR-037, G-07 |
| Spouse's date of birth | F-TR-021, F-SC-012, F-SC-013, F-SC-014, F-SC-016 |
| Spouse's nationality | F-TR-030, F-TR-031, F-TR-032, F-TR-033, F-TR-037, G-01 |
| Spouse's permit type | F-TR-030, F-TR-031, F-TR-032, F-TR-037, G-01 |
| Spouse's country of residence | F-TR-030, F-TR-031, F-TR-032, F-TR-037, G-01 |
| rule: Subject to source tax | F-TR-005, F-TR-006, F-TR-025, F-TR-030, F-TR-034, F-TR-037, F-TR-040 |
| rule: Pension insurance start date | F-TR-016, F-TR-017, F-TR-018, F-TR-019, F-SC-008, F-SC-009, G-08 |

## Facts

| Fact | Source | Kind | Basis | Statement | Anchors |
|---|---|---|---|---|---|
| F-TR-001 | hr_transcript | context | explicit | The goal is for new employees to give their information once, so that HR stops chasing them for the same information several times. The stakeholder agreed to this goal. | T-003, T-004 |
| F-TR-002 | hr_transcript | context | explicit | Today HR uses a Word document and an Excel file, then types everything into the receiving parties' portals by hand. Last month this took a full afternoon for two new hires. | T-004, T-004 |
| F-TR-003 | hr_transcript | context | explicit | Muster AG hires around twenty people a year, more in summer. It has about 150 employees, mostly in Zurich. | T-006 |
| F-TR-004 | hr_transcript | context | explicit | Source tax takes HR the most time. HR does not know up front who must answer the source tax questions, so today it sends the whole questionnaire to everybody, and Swiss employees get annoyed. | T-008, T-008 |
| F-TR-005 | hr_transcript | condition | inferred | Source tax questions should only be asked to employees who are subject to source tax, not to everybody. | T-008, T-008 |
| F-TR-006 | hr_transcript | rule | explicit, superseded by F-TR-025, F-TR-037 | First version: all non-Swiss employees (anyone without a Swiss passport) are subject to source tax. | T-010 |
| F-TR-007 | hr_transcript | context | explicit | HR uses the Zurich tariff calculator on the canton's website to get the tariff code, clicking through it with the employee's answers. | T-012 |
| F-TR-008 | hr_transcript | decision | explicit | For now, the Zurich calculator is used for every employee subject to source tax. The stakeholder knows this is not exactly how it works, and the interviewer agreed to keep it this way. | T-012, T-013 |
| F-TR-009 | hr_transcript | field | explicit | HR needs the employee's full address: street, house number, postcode, town and country. | T-014 |
| F-TR-010 | hr_transcript | format | explicit | The address must be complete, because HR posts many documents to employees. It is a normal postal address, as you would write it on an envelope, with no extra parts. | T-014, T-016 |
| F-TR-011 | hr_transcript | wish | explicit, superseded by F-TR-012 | The stakeholder would like the form to ask for a photo of the employee for badges. Today reception takes badge photos with a phone and they come out badly. | T-018, T-018 |
| F-TR-012 | hr_transcript | exclusion | explicit | No photo will be collected for now, because security is changing the badge system next year. The topic will be revisited next year. | T-020, T-021 |
| F-TR-013 | hr_transcript | context | explicit | Muster AG's pension fund is Pensionskasse Muster. It has an old portal, and HR will send screenshots of it. | T-022, T-022 |
| F-TR-014 | hr_transcript | field | explicit | HR needs the employee's first working day for the pension fund. It is the most important item, and HR asks the employee to confirm it because it changes often. | T-024 |
| F-TR-015 | hr_transcript | context | explicit | The first working day often changes, for example when new hires negotiate leaving their old employer a week earlier. | T-026 |
| F-TR-016 | hr_transcript | rule | explicit, superseded by F-TR-017, F-TR-018 | First version: pension fund insurance starts on the first day of the month after the first working day. Example: a first working day of 15.03 gives an insurance start of 01.04. | T-026 |
| F-TR-017 | hr_transcript | rule | explicit, superseded by F-TR-018 | Exception: if the first working day is exactly the first day of a month, insurance starts on that same day. | T-028 |
| F-TR-018 | hr_transcript | rule | inferred | Final rule: the insurance start date is derived from the first working day. If the first working day is the 1st of a month, insurance starts that day. Otherwise it starts on the 1st of the following month. The employee is not asked for it. | T-026, T-028 |
| F-TR-019 | hr_transcript | context | inferred | Incident: Julia moved her first working day to 15 March, HR did not update it, and the fund ended up with a wrong insurance start date (it should have been 1 April). This led to an unfriendly letter and took weeks to fix. It shows that the insurance start date must follow the latest confirmed first working day. | T-026, T-026, T-028 |
| F-TR-020 | hr_transcript | field | explicit | The pension fund asks for the employee's civil status. | T-032 |
| F-TR-021 | hr_transcript | condition | explicit | If the employee is married, the pension fund wants the date of birth of the husband or wife. | T-032 |
| F-TR-022 | hr_transcript | option | explicit | Civil status options, from the stakeholder's memory and not confirmed: Single, Married, Divorced, and she thinks Widowed. She deferred to the pension fund screenshots for the actual list. | T-034 |
| F-TR-023 | hr_transcript | context | explicit | One current employee (Daniel, in finance) is in a registered partnership. He was entered before the current HR manager's time. | T-034, T-036 |
| F-TR-024 | hr_transcript | open | explicit | Unresolved: how the pension fund's screen handles a registered partnership, and whether the fund wants the partner's details. | T-036 |
| F-TR-025 | hr_transcript | rule | explicit, superseded by F-TR-030, F-TR-037 | Correction: employees with a C permit are not subject to source tax and are treated like Swiss nationals (example: Maria, Portuguese with a C permit). So the rule becomes non-Swiss, except C permit holders. Asked if that was everything, the stakeholder answered only 'I think so'. | T-038, T-039, T-040 |
| F-TR-026 | hr_transcript | context | explicit | The stakeholder offered to get numbers on how long the process takes from their payroll person. | T-040 |
| F-TR-027 | hr_transcript | exclusion | explicit | Laptops and IT equipment are out of scope. IT has its own process. | T-042 |
| F-TR-028 | hr_transcript | wish | explicit | The stakeholder would love the form to remind employees to bring their permit, because half of them forget. Not decided: the interviewer deferred the wording to later. | T-042, T-043 |
| F-TR-029 | hr_transcript | rule | explicit | For married employees, the source tax calculator asks different questions, for example whether the husband or wife works. | T-044 |
| F-TR-030 | hr_transcript | rule | explicit, superseded by F-TR-034, F-TR-037 | Addition: an employee married to someone who is Swiss or holds a C permit, and who lives in Switzerland, is not subject to source tax. Example: Tomás, Brazilian with a B permit, whose Swiss wife lives with him in Winterthur. | T-044, T-044 |
| F-TR-031 | hr_transcript | field | explicit | To decide on source tax, HR needs the spouse's nationality, the spouse's permit (if they have one), and whether the spouse lives in Switzerland. | T-045, T-046 |
| F-TR-032 | hr_transcript | condition | inferred | Spouse nationality, permit and residence are only needed for married employees whose own status would otherwise make them subject to source tax: non-Swiss, no C permit, living in Switzerland. The spouse permit is only needed if the spouse is not Swiss. | T-044, T-046 |
| F-TR-033 | hr_transcript | context | explicit | Today HR checks the spouse case by hand and collects spouse details by email, which takes a long time. | T-044, T-046 |
| F-TR-034 | hr_transcript | rule | explicit, superseded by F-TR-037 | Addition: employees who live abroad and work in Switzerland are always subject to source tax, whatever their nationality. Example: Stefan is Swiss, lives in Konstanz, and is still subject. | T-048, T-048, T-049, T-050 |
| F-TR-035 | hr_transcript | context | explicit | Some employees live across the border, for example in Konstanz (Germany) and in Liechtenstein. | T-048 |
| F-TR-036 | hr_transcript | rule | explicit | For employees living abroad, the source tax calculator asks more questions. Germany has its own forms, which the stakeholder cannot name. The interviewer said the calculator will define these questions. | T-050, T-050, T-051 |
| F-TR-037 | hr_transcript | rule | inferred | Consolidated final rule. (1) An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. (2) An employee living in Switzerland who is Swiss or holds a C permit is not subject. (3) An employee living in Switzerland who is non-Swiss without a C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. (4) Otherwise the employee is subject. The stakeholder hedged on completeness ('I think that's it'). | T-010, T-038, T-044, T-048, T-048 |
| F-TR-038 | hr_transcript | field | inferred | The employee's nationality is needed to decide whether they are subject to source tax. | T-010 |
| F-TR-039 | hr_transcript | field | inferred | Non-Swiss employees' permit type (e.g. B permit, C permit) is needed to decide whether they are subject to source tax. | T-038 |
| F-TR-040 | hr_transcript | rule | inferred | 'Lives here' in the source tax rules means living in Switzerland. The employee's country of residence can be taken from the country of the home address. | T-048, T-044 |
| F-TR-041 | hr_transcript | context | explicit | The stakeholder asked when the product can be delivered. The interviewer will reply this week, after reviewing the screenshots. | T-052, T-053 |
| F-SC-001 | pension_portal | context | explicit | The source is the 'Register new employee' page of the Pensionskasse Muster employer portal, used by the employer Muster AG to register new insured employees. | S01-E01, S01-E02, S01-E03, S01-E08 |
| F-SC-002 | pension_portal | field | explicit | The pension fund registration requires the employee's first name (text input, marked required). | S01-E10, S01-E23 |
| F-SC-003 | pension_portal | field | explicit | The pension fund registration requires the employee's last name (text input, marked required). | S01-E11 |
| F-SC-004 | pension_portal | field | explicit | The pension fund registration requires the employee's date of birth (text input, marked required). | S01-E12 |
| F-SC-005 | pension_portal | format | explicit | The employee's date of birth is entered in the format DD.MM.YYYY. | S01-E13 |
| F-SC-006 | pension_portal | field | explicit | The pension fund registration requires a canton (dropdown in the Employee section, marked required); the portal does not label whether it is the residence or work canton. | S01-E14, S01-E09 |
| F-SC-007 | pension_portal | option | explicit | The Canton dropdown offers exactly these 26 options: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for living outside Switzerland. | S02-E14, S02-E16, S02-E17, S02-E18, S02-E19, S02-E20, S02-E21, S02-E22, S02-E23, S02-E24, S02-E25, S02-E26, S02-E27, S02-E28, S02-E29, S02-E30, S02-E31, S02-E32, S02-E33, S02-E34, S02-E35, S02-E36, S02-E37, S02-E38, S02-E39, S02-E40, S02-E41 |
| F-SC-008 | pension_portal | field | explicit | The pension fund registration requires an insurance start date (text input in the Insurance section, marked required). | S01-E17, S01-E16 |
| F-SC-009 | pension_portal | format | explicit | The insurance start date is entered as DD.MM.YYYY and must be the 1st of a month. | S01-E18 |
| F-SC-010 | pension_portal | field | explicit | The pension fund registration requires the employee's civil status (dropdown, marked required). | S01-E19 |
| F-SC-011 | pension_portal | option | explicit | The Civil status dropdown offers exactly these options: Single, Married, Divorced, Widowed. | S03-E19, S03-E21, S03-E22, S03-E23, S03-E24 |
| F-SC-012 | pension_portal | field | explicit | The pension fund registration has a 'Spouse's date of birth' field (text input) that is marked required when it is shown. | S05-E21 |
| F-SC-013 | pension_portal | format | explicit | The spouse's date of birth is entered in the format DD.MM.YYYY. | S05-E23 |
| F-SC-014 | pension_portal | condition | explicit | The 'Spouse's date of birth' field appears only when civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in the empty forms (01, 02, 03, 06). | S05-E20, S05-E21, S07-E20, S07-E21, S04-E20 |
| F-SC-015 | pension_portal | rule | explicit | Submitting the form with required fields empty shows the banner 'Please correct the highlighted fields.', highlights each empty field and shows a per-field error of the form '<Field> is required.' (First name, Last name, Date of birth, Canton, Insurance start date, Civil status). | S06-E05, S06-E09, S06-E12, S06-E16, S06-E19, S06-E24, S06-E27 |
| F-SC-016 | pension_portal | rule | explicit | When civil status is Married and the spouse's date of birth is left empty, the portal blocks registration with the error 'Spouse's date of birth is required.' | S07-E20, S07-E24 |
| F-SC-017 | pension_portal | open | inferred | The Canton dropdown only lists Swiss cantons; it is unclear what to enter for an employee who lives abroad (e.g. a cross-border commuter living in Germany), and whether the field means the residence canton or the work canton. | S02-E14, S02-E41 |
| F-SC-018 | pension_portal | open | inferred | No screenshot shows the form with civil status Divorced or Widowed, so it is unknown whether any extra fields (e.g. spouse data) appear for those values; the list also has no option such as registered partnership or separated, and it is unclear how such cases are to be registered. | S03-E23, S03-E24 |
| F-SC-019 | pension_portal | open | inferred | The portal requires an insurance start date that is the 1st of a month, but does not say how it relates to the employee's first working day (e.g. whether a mid-month start rounds to the same or the next month's 1st); the derivation rule is open. | S01-E18 |
| F-SC-020 | pension_portal | open | inferred | No screenshot shows the error for a badly formatted date or for an insurance start date that is not the 1st of a month, so the wording and behaviour of these errors are unknown. | S06-E23 |
