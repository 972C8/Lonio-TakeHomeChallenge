# [US-04.1] Ask nationality only of employees living in Switzerland

**As** new employee, **I want** to be asked my nationality only when it matters for whether I pay source tax, **so that** HR can tell whether I am Swiss without me giving my nationality when it changes nothing

Priority P1: Without nationality HR cannot tell Swiss employees from other employees living in Switzerland. Today Swiss employees get the source tax questions, get annoyed and call HR (F-TR-005).

## Acceptance criteria

**AC-04.1.1 Nationality is asked and required for employees living in Switzerland**
- Given the country of the employee's home address is Switzerland
- When the employee fills in the questionnaire
- Then Lonio asks for the employee's nationality, the employee must answer it, and HR uses it to decide whether the employee is subject to source tax.

| Example | Country of home address (country of residence) | → | Nationality |
|---|---|---|---|
| Tomás (F-TR-030), lives in Winterthur | Switzerland | → | required |

**AC-04.1.2 Nationality is not asked of employees living abroad**
- Given the country of the employee's home address is not Switzerland
- When the employee fills in the questionnaire
- Then Lonio does not ask for the employee's nationality, because employees living abroad are subject to source tax whatever their nationality. Whether the Zurich calculator needs it after all is open (OQ-01).

| Example | Country of home address (country of residence) | → | Nationality |
|---|---|---|---|
| Stefan (F-TR-034), Swiss, lives in Konstanz | Germany | → | not asked |
| Employee living in Liechtenstein | Liechtenstein | → | not asked |

+++ Evidence

- F-TR-005: Source tax questions should only be asked to employees who are subject to source tax, not to everybody. — "Because I never know up front who has to answer those questions." (T-008) — "the Swiss people get annoyed, and they call me." (T-008)
- F-TR-006: First version: all non-Swiss employees (anyone without a Swiss passport) are subject to source tax. — "All the non-Swiss employees. Simple as that. If you don't have a Swiss passport, you do source tax." (T-010)
- F-TR-034: Addition: employees who live abroad and work in Switzerland are always subject to source tax, whatever their nationality. Example: Stefan is Swiss, lives in Konstanz, and is still subject. — "Those people do source tax because they work here and they don't live here." (T-048) — "And there it doesn't matter what passport you have, by the way." (T-048) — "So someone living abroad and working here always does it?" (T-049) — "Yes." (T-050)
- F-TR-037: Consolidated final rule. (1) An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. (2) An employee living in Switzerland who is Swiss or holds a C permit is not subject. (3) An employee living in Switzerland who is non-Swiss without a C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. (4) Otherwise the employee is subject. The stakeholder hedged on completeness ('I think that's it'). — "If you don't have a Swiss passport, you do source tax." (T-010) — "So, not the people with a C permit. They're treated like Swiss people for this." (T-038) — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (T-044) — "Those people do source tax because they work here and they don't live here." (T-048) — "I think that's it." (T-048)
- F-TR-038: The employee's nationality is needed to decide whether they are subject to source tax. — "If you don't have a Swiss passport, you do source tax." (T-010)
- F-TR-040: 'Lives here' in the source tax rules means living in Switzerland. The employee's country of residence can be taken from the country of the home address. — "Those people do source tax because they work here and they don't live here." (T-048) — "and they live in Winterthur." (T-044)
- G-01

Spec: `requirements/employee-onboarding/features/FEAT-04-source-tax-liability.md`
+++
