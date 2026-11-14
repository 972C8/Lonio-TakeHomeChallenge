# [FEAT-04] Decide whether the employee is subject to source tax

---
id: FEAT-04-source-tax-liability
title: "Decide whether the employee is subject to source tax"
order: 4
stakeholders: [employee, hr, source_tax]
stories: [US-04.1, US-04.2, US-04.3, US-04.4]
information: [nationality, permit_type, spouse_nationality, spouse_permit_type, spouse_residence_country]
rules: [subject_to_source_tax]
open_questions: [OQ-01, OQ-05, OQ-06, OQ-07, OQ-08]
---

# Decide whether the employee is subject to source tax

**Goal:** Lonio asks only the questions needed to decide whether an employee is subject to source tax, so that only those employees get the source tax questions and nobody gives nationality, permit or spouse data that is not needed.

## Context
HR decides by hand whether an employee is subject to source tax. Employees living abroad always are. Swiss nationals and C permit holders living in Switzerland are not. Other foreigners living in Switzerland are not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland (F-TR-005, F-TR-006, F-TR-025, F-TR-030, F-TR-034, F-TR-037). Data minimisation means each of these questions is asked only when its answer can change the outcome (G-01). The rule uses address_country (FEAT-02) and civil_status (FEAT-03). The tariff questions of the Zurich calculator have not been analysed yet (OQ-01, blocking). Until they are, this feature delivers the subject or not-subject decision that gates them. HR is not sure the rule is complete (OQ-05). The permit list is undefined (OQ-06). HR wished for a permit reminder because half of new employees forget to bring it (F-TR-028, OQ-07). Using the Zurich calculator for every employee is an agreed simplification (F-TR-008, G-05, OQ-08).

**Stakeholders:** new employee, HR, source tax office

> ⚠ Open questions affecting this feature: [OQ-01](../open-questions.md#oq-01), [OQ-05](../open-questions.md#oq-05), [OQ-06](../open-questions.md#oq-06), [OQ-07](../open-questions.md#oq-07), [OQ-08](../open-questions.md#oq-08)


