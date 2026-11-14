# [US-02.2] Country of home address as country of residence

**As** source tax office, **I want** the country of the employee's home address to be used as their country of residence, **so that** employees living abroad are recognised as subject to source tax and only the questions relevant to where the employee lives are asked later

Priority P1: Whether the employee lives in Switzerland decides source tax liability (F-TR-034, F-TR-037) and which later questions are asked; without it later steps cannot be determined.

## Acceptance criteria

**AC-02.2.1 Country of residence is not asked separately**
- Given a new employee has given the country of their home address
- When a later step needs to know whether the employee lives in Switzerland
- Then the country of the home address is used as the country of residence and the employee is not asked a separate question about where they live

**AC-02.2.2 Employees living abroad are subject to source tax whatever their nationality**
- Given a new employee's home address is outside Switzerland
- When the questionnaire determines the following steps
- Then the employee is treated as subject to source tax, is not asked their nationality or the pension fund canton, and source tax and HR receive the country of residence

| Example | Country of home address (country of residence) | → | Nationality | Canton | Subject to source tax |
|---|---|---|---|---|---|
| Stefan, Swiss, lives in Konstanz (F-TR-034) | Germany | → | not asked | not asked | yes |
| Employee living in Liechtenstein | Liechtenstein | → | not asked | not asked | yes |

**AC-02.2.3 Employees living in Switzerland continue to nationality and canton**
- Given a new employee's home address is in Switzerland
- When the questionnaire determines the following steps
- Then the employee is asked their nationality and the pension fund canton, which decide the later source tax and pension steps

| Example | Country of home address (country of residence) | → | Nationality | Canton |
|---|---|---|---|---|
| Employee living in Winterthur | Switzerland | → | asked | asked |

**AC-02.2.4 Address comes before dependent steps**
- Given a new employee starts the onboarding questionnaire
- When the steps are presented
- Then the home address step comes before the pension and source tax steps that depend on the country of residence; the additional source tax questions for employees living abroad are defined by the Zurich calculator and remain open (OQ-01)

+++ Evidence

- F-TR-034: Addition: employees who live abroad and work in Switzerland are always subject to source tax, whatever their nationality. Example: Stefan is Swiss, lives in Konstanz, and is still subject. — "Those people do source tax because they work here and they don't live here." (T-048) — "And there it doesn't matter what passport you have, by the way." (T-048) — "So someone living abroad and working here always does it?" (T-049) — "Yes." (T-050)
- F-TR-036: For employees living abroad, the source tax calculator asks more questions. Germany has its own forms, which the stakeholder cannot name. The interviewer said the calculator will define these questions. — "And with them the calculator gets much more complicated, there are more questions." (T-050) — "Germany has its own forms, I can never remember what they're called." (T-050) — "the calculator will tell us." (T-051)
- F-TR-037: Consolidated final rule. (1) An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. (2) An employee living in Switzerland who is Swiss or holds a C permit is not subject. (3) An employee living in Switzerland who is non-Swiss without a C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. (4) Otherwise the employee is subject. The stakeholder hedged on completeness ('I think that's it'). — "If you don't have a Swiss passport, you do source tax." (T-010) — "So, not the people with a C permit. They're treated like Swiss people for this." (T-038) — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (T-044) — "Those people do source tax because they work here and they don't live here." (T-048) — "I think that's it." (T-048)
- F-TR-040: 'Lives here' in the source tax rules means living in Switzerland. The employee's country of residence can be taken from the country of the home address. — "Those people do source tax because they work here and they don't live here." (T-048) — "and they live in Winterthur." (T-044)
- G-01
- G-09

Spec: `requirements/employee-onboarding/features/FEAT-02-home-address.md`
+++
