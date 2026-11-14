# Linear sync plan (DRY RUN) – Employee onboarding questionnaire

Project: **Employee onboarding questionnaire** · mapping file: `problems/employee-onboarding/linear_map.yaml` (none yet: first publish)

| Action | Count |
|---|---|
| create | 27 |
| update (+ change comment) | 0 |
| cancel or flag (removed from spec) | 0 |
| unchanged | 0 |

Payload previews (exact titles and descriptions): `build/employee-onboarding/linear/`

## Create

- project document `document.README` → "Overview"
- project document `document.information` → "Information catalogue"
- project document `document.out-of-scope` → "Out of scope"
- parent issue + milestone `feature.FEAT-01-first-working-day-insurance-start` → "[FEAT-01] Confirmed first working day and derived pension insurance start date" · labels: spec:feature
- sub-issue `story.US-01.1` → "[US-01.1] Employee confirms their first working day" · parent: `feature.FEAT-01-first-working-day-insurance-start` · priority: Urgent · labels: spec:P1, spec:stakeholder/hr
- sub-issue `story.US-01.2` → "[US-01.2] Insurance start date is derived from the confirmed first working day" · parent: `feature.FEAT-01-first-working-day-insurance-start` · priority: Urgent · labels: spec:P1, spec:stakeholder/pension_fund
- parent issue + milestone `feature.FEAT-02-home-address` → "[FEAT-02] Complete home address and country of residence" · labels: spec:feature
- sub-issue `story.US-02.1` → "[US-02.1] Complete postal address for HR mail" · parent: `feature.FEAT-02-home-address` · priority: Urgent · labels: spec:P1, spec:stakeholder/hr
- sub-issue `story.US-02.2` → "[US-02.2] Country of home address as country of residence" · parent: `feature.FEAT-02-home-address` · priority: Urgent · labels: spec:P1, spec:stakeholder/source_tax, spec:inferred
- parent issue + milestone `feature.FEAT-03-pension-fund-registration-data` → "[FEAT-03] Personal and family details for pension fund registration" · labels: spec:feature
- sub-issue `story.US-03.1` → "[US-03.1] Name and date of birth for the pension fund" · parent: `feature.FEAT-03-pension-fund-registration-data` · priority: Urgent · labels: spec:P1, spec:stakeholder/pension_fund
- sub-issue `story.US-03.2` → "[US-03.2] Civil status from the pension fund's list" · parent: `feature.FEAT-03-pension-fund-registration-data` · priority: Urgent · labels: spec:P1, spec:stakeholder/pension_fund
- sub-issue `story.US-03.3` → "[US-03.3] Spouse's date of birth for married employees" · parent: `feature.FEAT-03-pension-fund-registration-data` · priority: Urgent · labels: spec:P1, spec:stakeholder/pension_fund
- sub-issue `story.US-03.4` → "[US-03.4] Canton for employees living in Switzerland" · parent: `feature.FEAT-03-pension-fund-registration-data` · priority: Urgent · labels: spec:P1, spec:stakeholder/pension_fund, spec:inferred
- parent issue + milestone `feature.FEAT-04-source-tax-liability` → "[FEAT-04] Decide whether the employee is subject to source tax" · labels: spec:feature
- sub-issue `story.US-04.1` → "[US-04.1] Ask nationality only of employees living in Switzerland" · parent: `feature.FEAT-04-source-tax-liability` · priority: Urgent · labels: spec:P1, spec:stakeholder/employee, spec:inferred
- sub-issue `story.US-04.2` → "[US-04.2] Ask the permit type only of non-Swiss employees living in Switzerland" · parent: `feature.FEAT-04-source-tax-liability` · priority: Urgent · labels: spec:P1, spec:stakeholder/employee, spec:inferred
- sub-issue `story.US-04.3` → "[US-04.3] Ask spouse details only when they can exempt the employee" · parent: `feature.FEAT-04-source-tax-liability` · priority: Urgent · labels: spec:P1, spec:stakeholder/hr, spec:inferred
- sub-issue `story.US-04.4` → "[US-04.4] Decide whether the employee is subject to source tax" · parent: `feature.FEAT-04-source-tax-liability` · priority: Urgent · labels: spec:P1, spec:stakeholder/hr, spec:inferred
- issue `open.OQ-01` → "[OQ-01] Decision needed: Which questions does the Zurich source tax calculator ask to set the tariff code, with which options and under which conditions (including the different questions for married employees, such as whether the spouse works, and the extra questions and German forms for employees living abroad)?" · labels: spec:needs-decision, spec:blocking
- issue `open.OQ-02` → "[OQ-02] Decision needed: Does the pension fund's 'Canton' mean the canton of residence or of work, and what should be entered for employees living abroad, given that only Swiss cantons are offered?" · labels: spec:needs-decision, spec:blocking
- issue `open.OQ-03` → "[OQ-03] Decision needed: How should an employee in a registered partnership (or other status not in the list, e.g. separated) be registered with the pension fund, does the fund want the partner's details, and does a registered partnership count as married for the source tax spouse rule?" · labels: spec:needs-decision
- issue `open.OQ-04` → "[OQ-04] Decision needed: Does the pension fund portal show extra fields (e.g. spouse data) when civil status is Divorced or Widowed?" · labels: spec:needs-decision
- issue `open.OQ-05` → "[OQ-05] Decision needed: Is the source tax rule complete? HR answered 'I think so' / 'I think that's it'." · labels: spec:needs-decision
- issue `open.OQ-06` → "[OQ-06] Decision needed: Which permit types may the employee and spouse choose from? Sources mention only the B permit and the C permit." · labels: spec:needs-decision
- issue `open.OQ-07` → "[OQ-07] Decision needed: Should the questionnaire remind employees to bring their permit, and with which wording?" · labels: spec:needs-decision
- issue `open.OQ-08` → "[OQ-08] Decision needed: The Zurich calculator is used for every employee subject to source tax, though HR knows this is not exactly correct. Should this be revisited?" · labels: spec:needs-decision

Before applying, the publisher also compares each issue's current description with the last published hash; issues edited in Linear are not overwritten but flagged in review.md.

Nothing was sent to Linear. The pipeline owns issue content and its `spec:` labels; engineering owns status, assignee, estimate, cycle and all other labels.
