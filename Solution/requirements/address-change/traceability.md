# Traceability

Every story, criterion, information item and rule cites facts; every fact
quotes its source verbatim, and the quotes are machine-checked against the
sources.

## Stories → sources

| Story | Acceptance criteria | Sources |
|---|---|---|
| US-01.1 Report the street, house number, postcode and town of the new address | AC-01.1.1, AC-01.1.2, AC-01.1.3 | F-TR-001, F-TR-002, F-TR-003, F-TR-004, F-TR-006, F-TR-013, F-TR-016, F-TR-009, G-01 |
| US-01.2 Report the country of the new address | AC-01.2.1, AC-01.2.2, AC-01.2.3 | F-TR-005, F-TR-006, F-TR-010, F-TR-016, G-02 |
| US-02.1 Report the date from which the new address applies | AC-02.1.1, AC-02.1.2, AC-02.1.3 | F-TR-007, F-TR-008, F-TR-018, G-02 |
| US-02.2 Accept late reports up to three months back | AC-02.2.1, AC-02.2.2, AC-02.2.3 | F-TR-019, F-TR-020, F-TR-021, G-02 |
| US-03.1 Payroll is informed when an employee moves abroad | AC-03.1.1, AC-03.1.2 | F-TR-010, F-TR-011, F-TR-012 |
| US-03.2 Payroll is not involved in moves within Switzerland | AC-03.2.1 | F-TR-013, F-TR-016, G-01 |
| US-04.1 HR receives the new canton when the employee moves to a different canton | AC-04.1.1, AC-04.1.2, AC-04.1.3 | F-TR-014, F-TR-016, F-TR-017 |
| US-04.2 Employee is not asked for a canton when it is not needed | AC-04.2.1, AC-04.2.2 | F-TR-015, F-TR-016, G-01 |
| US-04.3 HR knows the previous canton for moves within Switzerland | AC-04.3.1, AC-04.3.2, AC-04.3.3 | F-TR-017, F-TR-014, G-01 |

## Information and rules → sources

| Element | Sources |
|---|---|
| Street of the new address | F-TR-001, F-TR-006, F-TR-013, F-TR-016 |
| House number of the new address | F-TR-002, F-TR-006, F-TR-016 |
| Postcode of the new address | F-TR-003, F-TR-006, F-TR-016 |
| Town of the new address | F-TR-004, F-TR-006, F-TR-016 |
| Country of the new address | F-TR-005, F-TR-006, F-TR-010, F-TR-011, G-02 |
| Valid from | F-TR-007, F-TR-008, F-TR-018, F-TR-019, G-02 |
| New canton | F-TR-014, F-TR-015, F-TR-016, G-01 |
| Previous canton | F-TR-017, F-TR-014, G-01 |
| rule: Payroll must be informed of a move abroad | F-TR-011, F-TR-012, F-TR-010 |
| rule: Move to a different canton | F-TR-014, F-TR-015, F-TR-016, F-TR-017 |
| rule: Valid-from date at most three months in the past | F-TR-019, F-TR-020, F-TR-021 |

## Facts

| Fact | Source | Kind | Basis | Statement | Anchors |
|---|---|---|---|---|---|
| F-TR-001 | hr_meeting | field | explicit | HR needs the street of the employee's new address. | T-002 |
| F-TR-002 | hr_meeting | field | explicit | HR needs the house number of the employee's new address. | T-002 |
| F-TR-003 | hr_meeting | field | explicit | HR needs the postcode of the employee's new address. | T-002 |
| F-TR-004 | hr_meeting | field | explicit | HR needs the town of the employee's new address. | T-002 |
| F-TR-005 | hr_meeting | field | explicit | HR needs the country of the employee's new address. | T-002 |
| F-TR-006 | hr_meeting | format | explicit | The new address consists of street, house number, postcode, town and country. | T-002 |
| F-TR-007 | hr_meeting | field | explicit | HR needs the date from which the new address is valid. | T-002 |
| F-TR-008 | hr_meeting | context | explicit | Payslips are sent out on the 25th, so HR needs the valid-from date to know which address to use. | T-002 |
| F-TR-009 | hr_meeting | exclusion | explicit | The reason for the move must not be asked; it is private. | T-004 |
| F-TR-010 | hr_meeting | condition | explicit | For a move abroad, HR needs the new country of residence. | T-006 |
| F-TR-011 | hr_meeting | rule | explicit | If the employee moves abroad, payroll must be informed, because the employee may then be subject to source tax. | T-006, T-006 |
| F-TR-012 | hr_meeting | rule | explicit | An employee moving abroad may become subject to source tax (hedged: 'may'). | T-006 |
| F-TR-013 | hr_meeting | condition | explicit, superseded by F-TR-014 | For a move within Switzerland, only the address is needed. | T-007, T-008 |
| F-TR-014 | hr_meeting | condition | explicit | If the employee moves to a different Swiss canton, the new canton is also needed, for the tax office. | T-008 |
| F-TR-015 | hr_meeting | condition | explicit | For a move within the same canton, the new canton is not asked. | T-008 |
| F-TR-016 | hr_meeting | rule | inferred | Final rule for Swiss moves: always ask the new address; additionally ask the new canton only when the canton changes (needed for the tax office); not for moves within the same canton. | T-008, T-008, T-008 |
| F-TR-017 | hr_meeting | field | inferred | To determine whether the canton changes, the previous canton (or current canton) must be known; the stakeholder did not state how. | T-008 |
| F-TR-018 | hr_meeting | rule | explicit | The valid-from date is always required. | T-009, T-010 |
| F-TR-019 | hr_meeting | rule | explicit | The valid-from date may be in the past, but not more than three months ago. | T-010 |
| F-TR-020 | hr_meeting | context | explicit | Employees often report their move late. | T-010 |
| F-TR-021 | hr_meeting | open | inferred | No upper limit for a future valid-from date was stated. | T-010 |
| F-TR-022 | hr_meeting | context | explicit | Sara thinks the list of requirements is complete for now (hedged). | T-012 |
