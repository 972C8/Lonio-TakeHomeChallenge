# Linear sync plan (DRY RUN) – Employee onboarding questionnaire

Project: **Employee onboarding questionnaire**  
Milestones: About you, Your address, Nationality and permit, Your start, Civil status, Your spouse

| Action | Count |
|---|---|
| create | 29 |
| update | 0 |
| cancel | 0 |
| unchanged | 0 |

## Create

- `field.first_name` → "[first_name] First name" · milestone: About you · labels: requirement, inferred, pension_fund, employer_hr
- `field.last_name` → "[last_name] Last name" · milestone: About you · labels: requirement, inferred, pension_fund, employer_hr
- `field.date_of_birth` → "[date_of_birth] Date of birth" · milestone: About you · labels: requirement, confirmed, pension_fund
- `field.address_street` → "[address_street] Street" · milestone: Your address · labels: requirement, confirmed, employer_hr
- `field.address_house_number` → "[address_house_number] House number" · milestone: Your address · labels: requirement, confirmed, employer_hr
- `field.address_postcode` → "[address_postcode] Postcode" · milestone: Your address · labels: requirement, confirmed, employer_hr
- `field.address_town` → "[address_town] Town" · milestone: Your address · labels: requirement, confirmed, employer_hr
- `field.address_country` → "[address_country] Country" · milestone: Your address · labels: requirement, inferred, employer_hr, source_tax
- `field.residence_canton` → "[residence_canton] Canton" · milestone: Your address · labels: requirement, inferred, pension_fund
- `field.nationality` → "[nationality] Nationality" · milestone: Nationality and permit · labels: requirement, inferred, source_tax
- `field.permit_type` → "[permit_type] Residence permit" · milestone: Nationality and permit · labels: requirement, inferred, source_tax
- `field.first_working_day` → "[first_working_day] First working day" · milestone: Your start · labels: requirement, inferred, pension_fund
- `field.civil_status` → "[civil_status] Civil status" · milestone: Civil status · labels: requirement, confirmed, pension_fund, source_tax
- `field.spouse_date_of_birth` → "[spouse_date_of_birth] Spouse's date of birth" · milestone: Your spouse · labels: requirement, inferred, pension_fund
- `field.spouse_nationality` → "[spouse_nationality] Spouse's nationality" · milestone: Your spouse · labels: requirement, inferred, source_tax
- `field.spouse_permit_type` → "[spouse_permit_type] Spouse's residence permit" · milestone: Your spouse · labels: requirement, inferred, source_tax
- `field.spouse_residence_country` → "[spouse_residence_country] Spouse's country of residence" · milestone: Your spouse · labels: requirement, inferred, source_tax
- `field.spouse_employed` → "[spouse_employed] Spouse employed" · milestone: Your spouse · labels: requirement, inferred, source_tax
- `rule.subject_to_source_tax` → "[subject_to_source_tax] Derived rule" · labels: requirement, derived-rule, inferred
- `rule.insurance_start_date` → "[insurance_start_date] Derived rule" · labels: requirement, derived-rule, confirmed
- `open.OQ-01` → "[OQ-01] Decision needed: What should go in the pension fund's required 'Canton' field for employees who live abroad? And does the field mean the canton of residence or the canton of work?" · labels: needs-decision, blocking
- `open.OQ-02` → "[OQ-02] Decision needed: How should a registered partnership (and legal separation) be recorded? Does it count as 'married' for the pension fund and for the source tax spouse exemption, and does the fund want the partner's date of birth?" · labels: needs-decision, blocking
- `open.OQ-03` → "[OQ-03] Decision needed: What is the full list of permit types to offer (for the employee and the spouse)?" · labels: needs-decision, blocking
- `open.OQ-04` → "[OQ-04] Decision needed: Which questions does the Zurich source tax calculator ask to determine the tariff code, including the extra questions and German-specific forms for residents abroad?" · labels: needs-decision, blocking
- `open.OQ-05` → "[OQ-05] Decision needed: Is the source tax liability rule complete? HR said 'I think that's it'." · labels: needs-decision
- `open.OQ-06` → "[OQ-06] Decision needed: Is the postal address always the home address, so that its country can be used as the country of residence for source tax?" · labels: needs-decision
- `open.OQ-07` → "[OQ-07] Decision needed: What exact wording should the permit reminder use, and who should see it?" · labels: needs-decision
- `open.OQ-08` → "[OQ-08] Decision needed: Should HR pre-fill the first working day so the employee only confirms it, or does the employee enter it? And how are later changes captured?" · labels: needs-decision
- `open.OQ-09` → "[OQ-09] Decision needed: Does the pension portal also ask for a spouse's date of birth when civil status is Divorced or Widowed?" · labels: needs-decision

Nothing was sent to Linear. Ownership: the pipeline owns issue content; engineering owns status, assignee, estimate and cycle.
