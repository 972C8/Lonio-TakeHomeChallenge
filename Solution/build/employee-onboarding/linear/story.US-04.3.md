# [US-04.3] Ask spouse details only when they can exempt the employee

**As** HR, **I want** Lonio to collect the spouse's nationality, permit and country of residence only from married employees whose own status would otherwise make them subject to source tax, **so that** I no longer have to check the spouse case by hand and collect spouse details by email

Priority P1: Today HR checks this case by hand and collects the details by email, which 'takes forever' (F-TR-033). Without the spouse details, employees like Tomás are wrongly treated as subject to source tax.

## Acceptance criteria

**AC-04.3.1 Spouse's nationality is asked only when the spouse can change the outcome**
- Given the employee is married, lives in Switzerland, is not Swiss and does not hold a C permit
- When the employee fills in the questionnaire
- Then Lonio asks for the spouse's nationality and the employee must answer it. Lonio does not ask it of any other employee, including employees who are married but Swiss, hold a C permit or live abroad. HR uses the answer for the source tax decision.

| Example | Country of home address (country of residence) | Nationality | Permit type | Civil status | → | Spouse's nationality |
|---|---|---|---|---|---|---|
| Tomás (F-TR-030), Brazilian, B permit, married | Switzerland | Brazil | B permit | Married | → | required |
| Single B permit holder in Switzerland | Switzerland | Italy | B permit | Single | → | not asked |
| Married C permit holder in Switzerland | Switzerland | Portugal | C permit | Married | → | not asked |
| Married Swiss employee in Switzerland | Switzerland | Switzerland | – | Married | → | not asked |
| Married employee living abroad | Germany | – | – | Married | → | not asked |

**AC-04.3.2 Spouse's permit type is asked only for a non-Swiss spouse and may be left empty**
- Given the spouse's nationality is needed (AC-04.3.1) and the spouse is not Swiss
- When the employee fills in the questionnaire
- Then Lonio asks for the spouse's Swiss residence permit, if they have one. The employee may leave it empty if the spouse has no permit. Lonio does not ask it if the spouse is Swiss. The list of permit types is open (OQ-06).

| Example | Country of home address (country of residence) | Nationality | Permit type | Civil status | Spouse's nationality | → | Spouse's permit type |
|---|---|---|---|---|---|---|---|
| Tomás (F-TR-030), wife is Swiss | Switzerland | Brazil | B permit | Married | Switzerland | → | not asked |
| B permit holder with an Italian spouse | Switzerland | Brazil | B permit | Married | Italy | → | optional |

**AC-04.3.3 Spouse's country of residence is asked only if the spouse is Swiss or holds a C permit**
- Given the spouse's nationality is needed (AC-04.3.1)
- When the spouse is Swiss or holds a C permit
- Then Lonio asks where the spouse lives and the employee must answer it. Lonio does not ask it if the spouse is neither Swiss nor a C permit holder, because then the spouse cannot exempt the employee.

| Example | Country of home address (country of residence) | Nationality | Permit type | Civil status | Spouse's nationality | Spouse's permit type | → | Spouse's country of residence |
|---|---|---|---|---|---|---|---|---|
| Tomás (F-TR-030), Swiss wife in Winterthur | Switzerland | Brazil | B permit | Married | Switzerland | – | → | required |
| Spouse is Italian with a C permit | Switzerland | Brazil | B permit | Married | Italy | C permit | → | required |
| Spouse is Italian with a B permit | Switzerland | Brazil | B permit | Married | Italy | B permit | → | not asked |

+++ Evidence

- F-TR-030: Addition: an employee married to someone who is Swiss or holds a C permit, and who lives in Switzerland, is not subject to source tax. Example: Tomás, Brazilian with a B permit, whose Swiss wife lives with him in Winterthur. — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (T-044) — "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." (T-044)
- F-TR-031: To decide on source tax, HR needs the spouse's nationality, the spouse's permit (if they have one), and whether the spouse lives in Switzerland. — "So you need to know about the spouse as well." (T-045) — "Yes. Their nationality, their permit if they have one, and that they live here." (T-046)
- F-TR-032: Spouse nationality, permit and residence are only needed for married employees whose own status would otherwise make them subject to source tax: non-Swiss, no C permit, living in Switzerland. The spouse permit is only needed if the spouse is not Swiss. — "it also changes who has to do it at all." (T-044) — "Their nationality, their permit if they have one, and that they live here." (T-046)
- F-TR-033: Today HR checks the spouse case by hand and collects spouse details by email, which takes a long time. — "I always have to check that one by hand." (T-044) — "I ask them by email, and it takes forever." (T-046)
- F-TR-037: Consolidated final rule. (1) An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. (2) An employee living in Switzerland who is Swiss or holds a C permit is not subject. (3) An employee living in Switzerland who is non-Swiss without a C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. (4) Otherwise the employee is subject. The stakeholder hedged on completeness ('I think that's it'). — "If you don't have a Swiss passport, you do source tax." (T-010) — "So, not the people with a C permit. They're treated like Swiss people for this." (T-038) — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (T-044) — "Those people do source tax because they work here and they don't live here." (T-048) — "I think that's it." (T-048)
- G-01

Spec: `requirements/employee-onboarding/features/FEAT-04-source-tax-liability.md`
+++
