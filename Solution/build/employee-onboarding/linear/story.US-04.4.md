# [US-04.4] Decide whether the employee is subject to source tax

**As** HR, **I want** Lonio to decide from the employee's answers whether they are subject to source tax, **so that** I know up front who has to answer the source tax questions, and Swiss employees and other exempt employees are not bothered with them

Priority P1: HR never knows up front who has to answer the source tax questions, and Swiss employees get annoyed and call HR (F-TR-005). This decision controls whether the whole source tax step is asked.

## Acceptance criteria

**AC-04.4.1 Employees living abroad are always subject**
- Given the country of the employee's home address is not Switzerland
- When Lonio decides on source tax
- Then the employee is subject to source tax, whatever their nationality.

| Example | Country of home address (country of residence) | → | Subject to source tax |
|---|---|---|---|
| Stefan (F-TR-034), Swiss, lives in Konstanz | Germany | → | yes |

**AC-04.4.2 Swiss nationals and C permit holders living in Switzerland are not subject**
- Given the employee lives in Switzerland
- When the employee is Swiss or holds a C permit
- Then the employee is not subject to source tax. C permit holders are treated like Swiss nationals.

| Example | Country of home address (country of residence) | Nationality | Permit type | → | Subject to source tax |
|---|---|---|---|---|---|
| Swiss employee living in Switzerland | Switzerland | Switzerland | – | → | no |
| Maria (F-TR-025), Portuguese with a C permit, assumed to live in Switzerland | Switzerland | Portugal | C permit | → | no |

**AC-04.4.3 Spouse exemption for other foreigners living in Switzerland**
- Given the employee lives in Switzerland, is not Swiss and does not hold a C permit
- When Lonio decides on source tax
- Then the employee is not subject only if they are married to a spouse who is Swiss or holds a C permit and who lives in Switzerland. In every other case the employee is subject.

| Example | Country of home address (country of residence) | Nationality | Permit type | Civil status | Spouse's nationality | Spouse's country of residence | Spouse's permit type | → | Subject to source tax |
|---|---|---|---|---|---|---|---|---|---|
| Tomás (F-TR-030), Brazilian, B permit, Swiss wife in Winterthur | Switzerland | Brazil | B permit | Married | Switzerland | Switzerland | – | → | no |
| Spouse is Italian with a C permit and lives in Switzerland | Switzerland | Brazil | B permit | Married | Italy | Switzerland | C permit | → | no |
| Swiss spouse lives in Germany | Switzerland | Brazil | B permit | Married | Switzerland | Germany | – | → | yes |
| Spouse is Italian with a B permit | Switzerland | Brazil | B permit | Married | Italy | – | B permit | → | yes |
| Single B permit holder in Switzerland | Switzerland | Italy | B permit | Single | – | – | – | → | yes |

**AC-04.4.4 Only employees subject to source tax get the source tax questions**
- Given Lonio has decided whether the employee is subject to source tax
- When the employee continues the questionnaire
- Then only employees who are subject are asked the source tax tariff questions; employees who are not subject are not asked them. The tariff questions themselves (including the different questions for married employees and the extra questions for employees living abroad) are not yet defined (OQ-01, blocking). For now, the Zurich calculator applies to every subject employee (OQ-08).

**AC-04.4.5 Rule completeness to be confirmed by HR**
- Given HR hedged on whether the rule is complete ('I think that's it')
- When the decision rule is released
- Then HR has checked the decision rules against real cases (Stefan, Maria, Tomás). Any missing case is handled through OQ-05, not by inventing new rules.

+++ Evidence

- F-TR-005: Source tax questions should only be asked to employees who are subject to source tax, not to everybody. — "Because I never know up front who has to answer those questions." (T-008) — "the Swiss people get annoyed, and they call me." (T-008)
- F-TR-006: First version: all non-Swiss employees (anyone without a Swiss passport) are subject to source tax. — "All the non-Swiss employees. Simple as that. If you don't have a Swiss passport, you do source tax." (T-010)
- F-TR-007: HR uses the Zurich tariff calculator on the canton's website to get the tariff code, clicking through it with the employee's answers. — "I use the Zurich calculator on the canton's website. The one that gives you the tariff code." (T-012)
- F-TR-008: For now, the Zurich calculator is used for every employee subject to source tax. The stakeholder knows this is not exactly how it works, and the interviewer agreed to keep it this way. — "For everybody I use Zurich, by the way. I know it's not exactly how it works, but that's what we do for now." (T-012) — "We'll keep that for now." (T-013)
- F-TR-025: Correction: employees with a C permit are not subject to source tax and are treated like Swiss nationals (example: Maria, Portuguese with a C permit). So the rule becomes non-Swiss, except C permit holders. Asked if that was everything, the stakeholder answered only 'I think so'. — "So, not the people with a C permit. They're treated like Swiss people for this." (T-038) — "Okay, so non-Swiss, but not with a C permit." (T-039) — "I think so." (T-040)
- F-TR-029: For married employees, the source tax calculator asks different questions, for example whether the husband or wife works. — "It changes the questions in the calculator, yes. Whether the husband or wife works." (T-044)
- F-TR-030: Addition: an employee married to someone who is Swiss or holds a C permit, and who lives in Switzerland, is not subject to source tax. Example: Tomás, Brazilian with a B permit, whose Swiss wife lives with him in Winterthur. — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (T-044) — "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." (T-044)
- F-TR-034: Addition: employees who live abroad and work in Switzerland are always subject to source tax, whatever their nationality. Example: Stefan is Swiss, lives in Konstanz, and is still subject. — "Those people do source tax because they work here and they don't live here." (T-048) — "And there it doesn't matter what passport you have, by the way." (T-048) — "So someone living abroad and working here always does it?" (T-049) — "Yes." (T-050)
- F-TR-036: For employees living abroad, the source tax calculator asks more questions. Germany has its own forms, which the stakeholder cannot name. The interviewer said the calculator will define these questions. — "And with them the calculator gets much more complicated, there are more questions." (T-050) — "Germany has its own forms, I can never remember what they're called." (T-050) — "the calculator will tell us." (T-051)
- F-TR-037: Consolidated final rule. (1) An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. (2) An employee living in Switzerland who is Swiss or holds a C permit is not subject. (3) An employee living in Switzerland who is non-Swiss without a C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. (4) Otherwise the employee is subject. The stakeholder hedged on completeness ('I think that's it'). — "If you don't have a Swiss passport, you do source tax." (T-010) — "So, not the people with a C permit. They're treated like Swiss people for this." (T-038) — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (T-044) — "Those people do source tax because they work here and they don't live here." (T-048) — "I think that's it." (T-048)
- F-TR-040: 'Lives here' in the source tax rules means living in Switzerland. The employee's country of residence can be taken from the country of the home address. — "Those people do source tax because they work here and they don't live here." (T-048) — "and they live in Winterthur." (T-044)
- G-05

Spec: `requirements/employee-onboarding/features/FEAT-04-source-tax-liability.md`
+++
