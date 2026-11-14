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

## User stories

### US-04.1 – Ask nationality only of employees living in Switzerland
**As** new employee, **I want** to be asked my nationality only when it matters for whether I pay source tax, **so that** HR can tell whether I am Swiss without me giving my nationality when it changes nothing

Priority **P1** – Without nationality HR cannot tell Swiss employees from other employees living in Switzerland. Today Swiss employees get the source tax questions, get annoyed and call HR (F-TR-005). · Status: **inferred** · Sources: F-TR-005, F-TR-006, F-TR-034, F-TR-037, F-TR-038, F-TR-040, G-01

Covers: Nationality

**Acceptance criteria**

- **AC-04.1.1 Nationality is asked and required for employees living in Switzerland**
  - **Given** the country of the employee's home address is Switzerland
  - **When** the employee fills in the questionnaire
  - **Then** Lonio asks for the employee's nationality, the employee must answer it, and HR uses it to decide whether the employee is subject to source tax.
  - _Sources: F-TR-006, F-TR-037, F-TR-038, F-TR-040_

  | Example | Country of home address (country of residence) | → | Nationality | Checked |
  |---|---|---|---|---|
  | Tomás (F-TR-030), lives in Winterthur | Switzerland | → | required | ✅ |

- **AC-04.1.2 Nationality is not asked of employees living abroad**
  - **Given** the country of the employee's home address is not Switzerland
  - **When** the employee fills in the questionnaire
  - **Then** Lonio does not ask for the employee's nationality, because employees living abroad are subject to source tax whatever their nationality. Whether the Zurich calculator needs it after all is open (OQ-01).
  - _Sources: F-TR-034, F-TR-037, G-01_

  | Example | Country of home address (country of residence) | → | Nationality | Checked |
  |---|---|---|---|---|
  | Stefan (F-TR-034), Swiss, lives in Konstanz | Germany | → | not asked | ✅ |
  | Employee living in Liechtenstein (illustrative) | Liechtenstein | → | not asked | ✅ |

### US-04.2 – Ask the permit type only of non-Swiss employees living in Switzerland
**As** new employee, **I want** to be asked about my residence permit only if I live in Switzerland and am not Swiss, **so that** HR can see whether I hold a C permit and, if I do, treat me like a Swiss national for source tax

Priority **P1** – C permit holders are not subject to source tax (F-TR-025). Without the permit type they would be asked the source tax questions for no reason (F-TR-005). · Status: **inferred** · Sources: F-TR-025, F-TR-028, F-TR-037, F-TR-039, G-01

Covers: Permit type

**Acceptance criteria**

- **AC-04.2.1 Permit type is asked and required for non-Swiss employees living in Switzerland**
  - **Given** the employee lives in Switzerland and their nationality is not Swiss
  - **When** the employee fills in the questionnaire
  - **Then** Lonio asks which Swiss residence permit the employee holds, the employee must answer it, and HR uses it to decide whether the employee is subject to source tax.
  - _Sources: F-TR-025, F-TR-037, F-TR-039_

  | Example | Country of home address (country of residence) | Nationality | → | Permit type | Checked |
  |---|---|---|---|---|---|
  | Tomás (F-TR-030), Brazilian living in Winterthur | Switzerland | Brazil | → | required | ✅ |
  | Maria (F-TR-025), Portuguese, assumed to live in Switzerland (illustrative) | Switzerland | Portugal | → | required | ✅ |

- **AC-04.2.2 Permit type is not asked of Swiss employees or employees living abroad**
  - **Given** the employee is Swiss, or lives outside Switzerland
  - **When** the employee fills in the questionnaire
  - **Then** Lonio does not ask for a permit type, because the answer cannot change the source tax decision.
  - _Sources: F-TR-034, F-TR-037, G-01_

  | Example | Country of home address (country of residence) | Nationality | → | Permit type | Checked |
  |---|---|---|---|---|---|
  | Swiss employee living in Switzerland (illustrative) | Switzerland | Switzerland | → | not asked | ✅ |
  | Stefan (F-TR-034), lives in Konstanz | Germany | – | → | not asked | ✅ |

- **AC-04.2.3 Permit choices and permit reminder are still open**
  - **Given** the sources name only the B permit and the C permit
  - **When** the permit question is shown to the employee
  - **Then** the answers include at least "B permit" and "C permit". The full list of permit types is still open (OQ-06). For the source tax decision, only C permit versus any other answer matters. HR wants the questionnaire to remind employees to bring their permit, but whether to add the reminder and its wording are still open (OQ-07).
  - _Sources: F-TR-025, F-TR-028, F-TR-039_
### US-04.3 – Ask spouse details only when they can exempt the employee
**As** HR, **I want** Lonio to collect the spouse's nationality, permit and country of residence only from married employees whose own status would otherwise make them subject to source tax, **so that** I no longer have to check the spouse case by hand and collect spouse details by email

Priority **P1** – Today HR checks this case by hand and collects the details by email, which 'takes forever' (F-TR-033). Without the spouse details, employees like Tomás are wrongly treated as subject to source tax. · Status: **inferred** · Sources: F-TR-030, F-TR-031, F-TR-032, F-TR-033, F-TR-037, G-01

Covers: Spouse's nationality, Spouse's permit type, Spouse's country of residence

**Acceptance criteria**

- **AC-04.3.1 Spouse's nationality is asked only when the spouse can change the outcome**
  - **Given** the employee is married, lives in Switzerland, is not Swiss and does not hold a C permit
  - **When** the employee fills in the questionnaire
  - **Then** Lonio asks for the spouse's nationality and the employee must answer it. Lonio does not ask it of any other employee, including employees who are married but Swiss, hold a C permit or live abroad. HR uses the answer for the source tax decision.
  - _Sources: F-TR-030, F-TR-031, F-TR-032, G-01_

  | Example | Country of home address (country of residence) | Nationality | Permit type | Civil status | → | Spouse's nationality | Checked |
  |---|---|---|---|---|---|---|---|
  | Tomás (F-TR-030), Brazilian, B permit, married | Switzerland | Brazil | B permit | Married | → | required | ✅ |
  | Single B permit holder in Switzerland (illustrative) | Switzerland | Italy | B permit | Single | → | not asked | ✅ |
  | Married C permit holder in Switzerland (illustrative) | Switzerland | Portugal | C permit | Married | → | not asked | ✅ |
  | Married Swiss employee in Switzerland (illustrative) | Switzerland | Switzerland | – | Married | → | not asked | ✅ |
  | Married employee living abroad (illustrative) | Germany | – | – | Married | → | not asked | ✅ |

- **AC-04.3.2 Spouse's permit type is asked only for a non-Swiss spouse and may be left empty**
  - **Given** the spouse's nationality is needed (AC-04.3.1) and the spouse is not Swiss
  - **When** the employee fills in the questionnaire
  - **Then** Lonio asks for the spouse's Swiss residence permit, if they have one. The employee may leave it empty if the spouse has no permit. Lonio does not ask it if the spouse is Swiss. The list of permit types is open (OQ-06).
  - _Sources: F-TR-031, F-TR-032, G-01_

  | Example | Country of home address (country of residence) | Nationality | Permit type | Civil status | Spouse's nationality | → | Spouse's permit type | Checked |
  |---|---|---|---|---|---|---|---|---|
  | Tomás (F-TR-030), wife is Swiss | Switzerland | Brazil | B permit | Married | Switzerland | → | not asked | ✅ |
  | B permit holder with an Italian spouse (illustrative) | Switzerland | Brazil | B permit | Married | Italy | → | optional | ✅ |

- **AC-04.3.3 Spouse's country of residence is asked only if the spouse is Swiss or holds a C permit**
  - **Given** the spouse's nationality is needed (AC-04.3.1)
  - **When** the spouse is Swiss or holds a C permit
  - **Then** Lonio asks where the spouse lives and the employee must answer it. Lonio does not ask it if the spouse is neither Swiss nor a C permit holder, because then the spouse cannot exempt the employee.
  - _Sources: F-TR-030, F-TR-031, F-TR-032, G-01_

  | Example | Country of home address (country of residence) | Nationality | Permit type | Civil status | Spouse's nationality | Spouse's permit type | → | Spouse's country of residence | Checked |
  |---|---|---|---|---|---|---|---|---|---|
  | Tomás (F-TR-030), Swiss wife in Winterthur | Switzerland | Brazil | B permit | Married | Switzerland | – | → | required | ✅ |
  | Spouse is Italian with a C permit (illustrative) | Switzerland | Brazil | B permit | Married | Italy | C permit | → | required | ✅ |
  | Spouse is Italian with a B permit (illustrative) | Switzerland | Brazil | B permit | Married | Italy | B permit | → | not asked | ✅ |

### US-04.4 – Decide whether the employee is subject to source tax
**As** HR, **I want** Lonio to decide from the employee's answers whether they are subject to source tax, **so that** I know up front who has to answer the source tax questions, and Swiss employees and other exempt employees are not bothered with them

Priority **P1** – HR never knows up front who has to answer the source tax questions, and Swiss employees get annoyed and call HR (F-TR-005). This decision controls whether the whole source tax step is asked. · Status: **inferred** · Sources: F-TR-005, F-TR-006, F-TR-007, F-TR-008, F-TR-025, F-TR-029, F-TR-030, F-TR-034, F-TR-036, F-TR-037, F-TR-040, G-05

Covers: Subject to source tax

**Acceptance criteria**

- **AC-04.4.1 Employees living abroad are always subject**
  - **Given** the country of the employee's home address is not Switzerland
  - **When** Lonio decides on source tax
  - **Then** the employee is subject to source tax, whatever their nationality.
  - _Sources: F-TR-034, F-TR-037, F-TR-040_

  | Example | Country of home address (country of residence) | → | Subject to source tax | Checked |
  |---|---|---|---|---|
  | Stefan (F-TR-034), Swiss, lives in Konstanz | Germany | → | yes | ✅ |

- **AC-04.4.2 Swiss nationals and C permit holders living in Switzerland are not subject**
  - **Given** the employee lives in Switzerland
  - **When** the employee is Swiss or holds a C permit
  - **Then** the employee is not subject to source tax. C permit holders are treated like Swiss nationals.
  - _Sources: F-TR-006, F-TR-025, F-TR-037_

  | Example | Country of home address (country of residence) | Nationality | Permit type | → | Subject to source tax | Checked |
  |---|---|---|---|---|---|---|
  | Swiss employee living in Switzerland (illustrative) | Switzerland | Switzerland | – | → | no | ✅ |
  | Maria (F-TR-025), Portuguese with a C permit, assumed to live in Switzerland (illustrative) | Switzerland | Portugal | C permit | → | no | ✅ |

- **AC-04.4.3 Spouse exemption for other foreigners living in Switzerland**
  - **Given** the employee lives in Switzerland, is not Swiss and does not hold a C permit
  - **When** Lonio decides on source tax
  - **Then** the employee is not subject only if they are married to a spouse who is Swiss or holds a C permit and who lives in Switzerland. In every other case the employee is subject.
  - _Sources: F-TR-025, F-TR-030, F-TR-037_

  | Example | Country of home address (country of residence) | Nationality | Permit type | Civil status | Spouse's nationality | Spouse's country of residence | Spouse's permit type | → | Subject to source tax | Checked |
  |---|---|---|---|---|---|---|---|---|---|---|
  | Tomás (F-TR-030), Brazilian, B permit, Swiss wife in Winterthur | Switzerland | Brazil | B permit | Married | Switzerland | Switzerland | – | → | no | ✅ |
  | Spouse is Italian with a C permit and lives in Switzerland (illustrative) | Switzerland | Brazil | B permit | Married | Italy | Switzerland | C permit | → | no | ✅ |
  | Swiss spouse lives in Germany (illustrative) | Switzerland | Brazil | B permit | Married | Switzerland | Germany | – | → | yes | ✅ |
  | Spouse is Italian with a B permit (illustrative) | Switzerland | Brazil | B permit | Married | Italy | – | B permit | → | yes | ✅ |
  | Single B permit holder in Switzerland (illustrative) | Switzerland | Italy | B permit | Single | – | – | – | → | yes | ✅ |

- **AC-04.4.4 Only employees subject to source tax get the source tax questions**
  - **Given** Lonio has decided whether the employee is subject to source tax
  - **When** the employee continues the questionnaire
  - **Then** only employees who are subject are asked the source tax tariff questions; employees who are not subject are not asked them. The tariff questions themselves (including the different questions for married employees and the extra questions for employees living abroad) are not yet defined (OQ-01, blocking). For now, the Zurich calculator applies to every subject employee (OQ-08).
  - _Sources: F-TR-005, F-TR-007, F-TR-008, F-TR-029, F-TR-036, G-05_
- **AC-04.4.5 Rule completeness to be confirmed by HR**
  - **Given** HR hedged on whether the rule is complete ('I think that's it')
  - **When** the decision rule is released
  - **Then** HR has checked the decision rules against real cases (Stefan, Maria, Tomás). Any missing case is handled through OQ-05, not by inventing new rules.
  - _Sources: F-TR-025, F-TR-037_
_Trace check: partial – AC-04.4.5 states that HR has checked the rules against Stefan, Maria and Tomás and that gaps go through OQ-05, but the facts only show HR hedging ('I think that's it') and say nothing about such a check or that handling; the other criteria are backed by F-TR-005/025/030/034/037/040._

## Information needed

The information this feature owns. Each piece is asked once and reused by
every stakeholder listed (see [information.md](../information.md) for all).

### Nationality
| | |
|---|---|
| **What?** | The employee's nationality (whether they hold a Swiss passport). |
| **When do we ask?** | Only if the employee lives in Switzerland |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence) |
| **Who needs it?** | HR: To decide whether an employee living in Switzerland is subject to source tax (Swiss nationals are not). |
| **Status · sources** | inferred · F-TR-038, F-TR-006, F-TR-037, F-TR-034, G-01 |
| **Notes** | For employees living abroad nationality does not change whether they are subject to source tax, so per data minimisation it is not asked of them. This may change once the Zurich calculator's questions are known (see OQ-01). |

### Permit type
| | |
|---|---|
| **What?** | The type of Swiss residence permit the non-Swiss employee holds, e.g. B permit or C permit. |
| **When do we ask?** | Only if the employee lives in Switzerland and is not Swiss |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence), Nationality |
| **Who needs it?** | HR: To decide whether the employee is subject to source tax (C permit holders are treated like Swiss nationals). |
| **Status · sources** | inferred · F-TR-039, F-TR-025, F-TR-037, G-01 |
| **Notes** | Sources name only B permit and C permit; the full list of permit types is not defined (see OQ-06). HR wished for a reminder to bring the permit (see OQ-07). |

### Spouse's nationality
| | |
|---|---|
| **What?** | Nationality of the employee's husband or wife (whether they are Swiss). |
| **When do we ask?** | Only if the employee is married, lives in Switzerland, is not Swiss and does not hold a C permit |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence), Civil status, Nationality, Permit type |
| **Who needs it?** | HR: To decide whether the employee is exempt from source tax because the spouse is Swiss and lives in Switzerland. |
| **Status · sources** | inferred · F-TR-030, F-TR-031, F-TR-032, F-TR-033, F-TR-037, G-01 |

### Spouse's permit type
| | |
|---|---|
| **What?** | Type of Swiss residence permit the non-Swiss spouse holds, if any (e.g. C permit). |
| **When do we ask?** | Only if spouse details are needed for source tax and the spouse is not Swiss |
| **When is it required?** | May be left empty if the spouse has no permit |
| **Depends on** | Country of home address (country of residence), Civil status, Nationality, Permit type, Spouse's nationality |
| **Who needs it?** | HR: To decide whether the employee is exempt from source tax because the spouse holds a C permit and lives in Switzerland. |
| **Status · sources** | inferred · F-TR-030, F-TR-031, F-TR-032, F-TR-037, G-01 |
| **Notes** | HR said 'their permit if they have one', so the spouse may have none. Permit list not defined (OQ-06). |

### Spouse's country of residence
| | |
|---|---|
| **What?** | The country where the employee's husband or wife lives (whether they live in Switzerland). |
| **When do we ask?** | Only if spouse details are needed for source tax and the spouse is Swiss or holds a C permit |
| **When is it required?** | Whenever asked |
| **Depends on** | Country of home address (country of residence), Civil status, Nationality, Permit type, Spouse's nationality, Spouse's permit type |
| **Who needs it?** | HR: The spouse exemption from source tax only applies if the spouse lives in Switzerland. |
| **Status · sources** | inferred · F-TR-030, F-TR-031, F-TR-032, F-TR-037, G-01 |
| **Notes** | Only asked when the answer can change the outcome (data minimisation). |

## Business rules

### Subject to source tax
An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. An employee living in Switzerland who is Swiss or holds a C permit is not subject. An employee living in Switzerland who is not Swiss and has no C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. Every other employee is subject. Only employees subject to source tax are asked the source tax questions.

| # | Country of residence | Nationality | Permit type | Civil status | Spouse Swiss or C permit | Spouse lives in Switzerland | → Result | Sources |
|---|---|---|---|---|---|---|---|---|
| 1 | Not Switzerland | any | any | any | any | any | Subject to source tax | F-TR-034, F-TR-037 |
| 2 | Switzerland | Swiss | - | any | any | any | Not subject | F-TR-006, F-TR-037 |
| 3 | Switzerland | Not Swiss | C permit | any | any | any | Not subject | F-TR-025, F-TR-037 |
| 4 | Switzerland | Not Swiss | Not C permit | Married | yes | yes | Not subject | F-TR-030, F-TR-037 |
| 5 | Switzerland | Not Swiss | Not C permit | Married | yes | no | Subject to source tax | F-TR-030, F-TR-037 |
| 6 | Switzerland | Not Swiss | Not C permit | Married | no | - | Subject to source tax | F-TR-030, F-TR-037 |
| 7 | Switzerland | Not Swiss | Not C permit | Not married | - | - | Subject to source tax | F-TR-025, F-TR-037 |

_Status: inferred · Sources: F-TR-005, F-TR-006, F-TR-025, F-TR-030, F-TR-034, F-TR-037, F-TR-040_

## Evidence
- **F-TR-005** (hr_transcript, inferred): Source tax questions should only be asked to employees who are subject to source tax, not to everybody.
  - "Because I never know up front who has to answer those questions." — T-008, Anna
  - "the Swiss people get annoyed, and they call me." — T-008, Anna
- **F-TR-006** (hr_transcript): First version: all non-Swiss employees (anyone without a Swiss passport) are subject to source tax.
  - "All the non-Swiss employees. Simple as that. If you don't have a Swiss passport, you do source tax." — T-010, Anna
- **F-TR-007** (hr_transcript): HR uses the Zurich tariff calculator on the canton's website to get the tariff code, clicking through it with the employee's answers.
  - "I use the Zurich calculator on the canton's website. The one that gives you the tariff code." — T-012, Anna
- **F-TR-008** (hr_transcript): For now, the Zurich calculator is used for every employee subject to source tax. The stakeholder knows this is not exactly how it works, and the interviewer agreed to keep it this way.
  - "For everybody I use Zurich, by the way. I know it's not exactly how it works, but that's what we do for now." — T-012, Anna
  - "We'll keep that for now." — T-013, Leo
- **F-TR-025** (hr_transcript): Correction: employees with a C permit are not subject to source tax and are treated like Swiss nationals (example: Maria, Portuguese with a C permit). So the rule becomes non-Swiss, except C permit holders. Asked if that was everything, the stakeholder answered only 'I think so'.
  - "So, not the people with a C permit. They're treated like Swiss people for this." — T-038, Anna
  - "Okay, so non-Swiss, but not with a C permit." — T-039, Leo
  - "I think so." — T-040, Anna
- **F-TR-028** (hr_transcript): The stakeholder would love the form to remind employees to bring their permit, because half of them forget. Not decided: the interviewer deferred the wording to later.
  - "What I would love is if the form could remind people to bring their permit. Half of them forget." — T-042, Anna
  - "We can look at the wording later." — T-043, Leo
- **F-TR-029** (hr_transcript): For married employees, the source tax calculator asks different questions, for example whether the husband or wife works.
  - "It changes the questions in the calculator, yes. Whether the husband or wife works." — T-044, Anna
- **F-TR-030** (hr_transcript): Addition: an employee married to someone who is Swiss or holds a C permit, and who lives in Switzerland, is not subject to source tax. Example: Tomás, Brazilian with a B permit, whose Swiss wife lives with him in Winterthur.
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." — T-044, Anna
- **F-TR-031** (hr_transcript): To decide on source tax, HR needs the spouse's nationality, the spouse's permit (if they have one), and whether the spouse lives in Switzerland.
  - "So you need to know about the spouse as well." — T-045, Leo
  - "Yes. Their nationality, their permit if they have one, and that they live here." — T-046, Anna
- **F-TR-032** (hr_transcript, inferred): Spouse nationality, permit and residence are only needed for married employees whose own status would otherwise make them subject to source tax: non-Swiss, no C permit, living in Switzerland. The spouse permit is only needed if the spouse is not Swiss.
  - "it also changes who has to do it at all." — T-044, Anna
  - "Their nationality, their permit if they have one, and that they live here." — T-046, Anna
- **F-TR-033** (hr_transcript): Today HR checks the spouse case by hand and collects spouse details by email, which takes a long time.
  - "I always have to check that one by hand." — T-044, Anna
  - "I ask them by email, and it takes forever." — T-046, Anna
- **F-TR-034** (hr_transcript): Addition: employees who live abroad and work in Switzerland are always subject to source tax, whatever their nationality. Example: Stefan is Swiss, lives in Konstanz, and is still subject.
  - "Those people do source tax because they work here and they don't live here." — T-048, Anna
  - "And there it doesn't matter what passport you have, by the way." — T-048, Anna
  - "So someone living abroad and working here always does it?" — T-049, Leo
  - "Yes." — T-050, Anna
- **F-TR-036** (hr_transcript): For employees living abroad, the source tax calculator asks more questions. Germany has its own forms, which the stakeholder cannot name. The interviewer said the calculator will define these questions.
  - "And with them the calculator gets much more complicated, there are more questions." — T-050, Anna
  - "Germany has its own forms, I can never remember what they're called." — T-050, Anna
  - "the calculator will tell us." — T-051, Leo
- **F-TR-037** (hr_transcript, inferred): Consolidated final rule. (1) An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. (2) An employee living in Switzerland who is Swiss or holds a C permit is not subject. (3) An employee living in Switzerland who is non-Swiss without a C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. (4) Otherwise the employee is subject. The stakeholder hedged on completeness ('I think that's it').
  - "If you don't have a Swiss passport, you do source tax." — T-010, Anna
  - "So, not the people with a C permit. They're treated like Swiss people for this." — T-038, Anna
  - "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." — T-044, Anna
  - "Those people do source tax because they work here and they don't live here." — T-048, Anna
  - "I think that's it." — T-048, Anna
- **F-TR-038** (hr_transcript, inferred): The employee's nationality is needed to decide whether they are subject to source tax.
  - "If you don't have a Swiss passport, you do source tax." — T-010, Anna
- **F-TR-039** (hr_transcript, inferred): Non-Swiss employees' permit type (e.g. B permit, C permit) is needed to decide whether they are subject to source tax.
  - "She has a C permit. So, not the people with a C permit." — T-038, Anna
- **F-TR-040** (hr_transcript, inferred): 'Lives here' in the source tax rules means living in Switzerland. The employee's country of residence can be taken from the country of the home address.
  - "Those people do source tax because they work here and they don't live here." — T-048, Anna
  - "and they live in Winterthur." — T-044, Anna
- **G-01** (product owner guidance): Lonio collects onboarding data from a new employee **once** and reuses it for every receiving party. Asking too little blocks a registration; asking too much collects personal data we must not have (data minimisation). A question must only be asked when at least one receiving party needs the answer for this person.
- **G-05** (product owner guidance): Simplifications given by the assignment: Switzerland has exactly one source tax system (Zurich's) and exactly one pension fund (Pensionskasse Muster).
