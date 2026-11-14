# [US-04.2] Ask the permit type only of non-Swiss employees living in Switzerland

**As** new employee, **I want** to be asked about my residence permit only if I live in Switzerland and am not Swiss, **so that** HR can see whether I hold a C permit and, if I do, treat me like a Swiss national for source tax

Priority P1: C permit holders are not subject to source tax (F-TR-025). Without the permit type they would be asked the source tax questions for no reason (F-TR-005).

## Acceptance criteria

**AC-04.2.1 Permit type is asked and required for non-Swiss employees living in Switzerland**
- Given the employee lives in Switzerland and their nationality is not Swiss
- When the employee fills in the questionnaire
- Then Lonio asks which Swiss residence permit the employee holds, the employee must answer it, and HR uses it to decide whether the employee is subject to source tax.

| Example | Country of home address (country of residence) | Nationality | → | Permit type |
|---|---|---|---|---|
| Tomás (F-TR-030), Brazilian living in Winterthur | Switzerland | Brazil | → | required |
| Maria (F-TR-025), Portuguese, assumed to live in Switzerland | Switzerland | Portugal | → | required |

**AC-04.2.2 Permit type is not asked of Swiss employees or employees living abroad**
- Given the employee is Swiss, or lives outside Switzerland
- When the employee fills in the questionnaire
- Then Lonio does not ask for a permit type, because the answer cannot change the source tax decision.

| Example | Country of home address (country of residence) | Nationality | → | Permit type |
|---|---|---|---|---|
| Swiss employee living in Switzerland | Switzerland | Switzerland | → | not asked |
| Stefan (F-TR-034), lives in Konstanz | Germany | – | → | not asked |

**AC-04.2.3 Permit choices and permit reminder are still open**
- Given the sources name only the B permit and the C permit
- When the permit question is shown to the employee
- Then the answers include at least "B permit" and "C permit". The full list of permit types is still open (OQ-06). For the source tax decision, only C permit versus any other answer matters. HR wants the questionnaire to remind employees to bring their permit, but whether to add the reminder and its wording are still open (OQ-07).

+++ Evidence

- F-TR-025: Correction: employees with a C permit are not subject to source tax and are treated like Swiss nationals (example: Maria, Portuguese with a C permit). So the rule becomes non-Swiss, except C permit holders. Asked if that was everything, the stakeholder answered only 'I think so'. — "So, not the people with a C permit. They're treated like Swiss people for this." (T-038) — "Okay, so non-Swiss, but not with a C permit." (T-039) — "I think so." (T-040)
- F-TR-028: The stakeholder would love the form to remind employees to bring their permit, because half of them forget. Not decided: the interviewer deferred the wording to later. — "What I would love is if the form could remind people to bring their permit. Half of them forget." (T-042) — "We can look at the wording later." (T-043)
- F-TR-034: Addition: employees who live abroad and work in Switzerland are always subject to source tax, whatever their nationality. Example: Stefan is Swiss, lives in Konstanz, and is still subject. — "Those people do source tax because they work here and they don't live here." (T-048) — "And there it doesn't matter what passport you have, by the way." (T-048) — "So someone living abroad and working here always does it?" (T-049) — "Yes." (T-050)
- F-TR-037: Consolidated final rule. (1) An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. (2) An employee living in Switzerland who is Swiss or holds a C permit is not subject. (3) An employee living in Switzerland who is non-Swiss without a C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. (4) Otherwise the employee is subject. The stakeholder hedged on completeness ('I think that's it'). — "If you don't have a Swiss passport, you do source tax." (T-010) — "So, not the people with a C permit. They're treated like Swiss people for this." (T-038) — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (T-044) — "Those people do source tax because they work here and they don't live here." (T-048) — "I think that's it." (T-048)
- F-TR-039: Non-Swiss employees' permit type (e.g. B permit, C permit) is needed to decide whether they are subject to source tax. — "She has a C permit. So, not the people with a C permit." (T-038)
- G-01

Spec: `requirements/employee-onboarding/features/FEAT-04-source-tax-liability.md`
+++
