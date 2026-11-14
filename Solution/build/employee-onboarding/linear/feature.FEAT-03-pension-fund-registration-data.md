# [FEAT-03] Personal and family details for pension fund registration

---
id: FEAT-03-pension-fund-registration-data
title: "Personal and family details for pension fund registration"
order: 3
stakeholders: [employee, hr, pension_fund]
stories: [US-03.1, US-03.2, US-03.3, US-03.4]
information: [first_name, last_name, date_of_birth, civil_status, spouse_date_of_birth, residence_canton]
rules: []
open_questions: [OQ-02, OQ-03, OQ-04]
---

# Personal and family details for pension fund registration

**Goal:** Lonio collects every field Pensionskasse Muster requires, including the spouse's date of birth for married employees, so that a registration is never blocked by missing data.

## Context
The pension fund portal requires first name, last name, date of birth, canton and civil status for every employee (F-SC-002 to F-SC-007, F-SC-010, F-SC-015). For married employees it also requires the spouse's date of birth and blocks the registration without it (F-TR-021, F-SC-012 to F-SC-014, F-SC-016). The civil status list shows only Single, Married, Divorced and Widowed (F-SC-011, G-07). HR's recollection of civil status matches the fund's list (F-TR-020, F-TR-022). Civil status is also an input for the source tax rule and the calculator (F-TR-029, F-TR-030). The fund offers only Swiss cantons and does not say whether it means the canton of residence or of work. Until the fund answers (OQ-02), the canton is asked only of employees living in Switzerland. It depends on address_country from FEAT-02. Registered partnerships, and portal behaviour for Divorced or Widowed, are still open.

**Stakeholders:** new employee, HR, pension fund

> ⚠ Open questions affecting this feature: [OQ-02](../open-questions.md#oq-02), [OQ-03](../open-questions.md#oq-03), [OQ-04](../open-questions.md#oq-04)


