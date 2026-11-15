# Review: employee-onboarding

**Verdict: NOT READY**

12 example simulations fail, all in US-06.6 (the full tariff code). The failures look like one format mismatch: the computed code is split into parts such as ['N', 1, 'Y'], and the expected value is the joined string 'N1Y'. The 'no tariff code' cases return None. This story is the main acceptance test for the computed code, so it must pass before build. The step order is also contradictory between feature.md and US-01.2. Technical terms leak into business prose against D-045. The open questions are non-blocking, but the calculator comparison is a go-live condition.

## Reviewer findings

1. **All US-06.6 examples fail (tariff code assembly)** – The full tariff code is the main output of the feature. Its acceptance examples do not pass, so the rule and the examples disagree. Most likely the rule returns the parts (letter, digit, church suffix) as a list instead of the joined string, and returns None where the spec says 'no tariff code'. The spec side could also be at fault.  
   Evidence: examples: AC-06.6.1 (6 cases), AC-06.6.2 (3 cases), AC-06.6.3 (3 cases). Example: tariff_code = ['N',1,'Y'], expected 'N1Y'. Example: tariff_code = None, expected 'no tariff code'. rule.tariff_letter: the cited fact maps G->Q, but the rule returns null for G.  
   Action: Fix the tariff_code expression so it joins letter, digit and suffix into one string. Decide how 'no tariff code' is represented, either null or an explicit marker, and align the example wording with that. Re-run the examples. Also resolve the G->Q handling in tariff_letter.
2. **Step order contradicts itself (8 vs 10 steps)** – Engineering cannot tell whether the Germany cross-border questions come before or after denomination and children. They also cannot tell whether there is a separate first-working-day step or a summary step.  
   Evidence: dev_refinement on feature.md: the flow table has 8 steps. The questionnaire_flow rule and AC-01.2.1 have 10 steps. trace_judge on rule.questionnaire_flow: the content of steps 1-5 and 7-10 is not backed by cited facts.  
   Action: Add a decision in decisions.yaml fixing the one authoritative step order. Regenerate feature.md and US-01.2 from it.
3. **Behaviour after an HR edit is undefined (US-01.6)** – If HR changes an answer so that new questions apply, those inputs were never asked. The derived tariff code and other results could be wrong or stale.  
   Evidence: dev_refinement on US-01.6 (major). Related: OQ-hr-side-follow-ups is non-blocking.  
   Action: Decide what derived results show while inputs are missing: no code, an 'incomplete' state, or the old value. Decide whether answers that no longer apply are discarded after an HR change, as they are on employee submission.
4. **Technical terms leak into business prose** – D-045 forbids internal rule ids and formula talk in the spec text.  
   Evidence: tech_leak in feature.md: '(discard_inapplicable_answers)' and '(read_only_after_submission)'. 'The expression ...' appears in feature.md and information.md, 2 times each.  
   Action: Reword in business language. Examples: 'each child adds 1 or 0 to the child count' and 'H applies if any child counts with H'. Remove the snake_case ids.
5. **Calculator coverage is unproven for unexplored and inferred paths** – Lonio now owns the tariff result. Unexplored paths could produce wrong codes. These are the residence block for A/B/H, more than 3 children, H3N/P3N, and the inferred child rows (US-07.3 to US-07.6).  
   Evidence: OQ-calculator-coverage (non-blocking). inferred_items: rule.child_result, rule.child_count, US-05.2, US-07.3 to US-07.6. fact_judge: partial on F-zh_source_tax_calculator-037b1c, 64ac33, dc0ae9, c8aa5e and 2754e8.  
   Action: Record a go-live condition: a domain expert compares the computed codes with the Zurich calculator. Confirm that the inferred rows are acceptable. Specify a maximum child count, or confirm 'no maximum'.
6. **Several claims are not backed by cited facts** – Traceability is weak for some rules. A reviewer cannot verify them from the sources.  
   Evidence: trace_judge: 'required' answers in US-07.1 to US-07.5. 'No maximum' children in AC-06.6.1. 'Children never change the letter for married employees' in US-06.4 and US-07.6. Uncited fact ids in calculator_residence, child_result and cross_border_tariff. The invented 01.04 date in US-03.3.  
   Action: Add the missing citations, or mark the items as inferred or decided via decisions.yaml. For example, cite D-034 and D-044. Remove or mark the invented example date.
7. **Source tax rule rests on hedged or unconfirmed statements** – The core rule for who is subject to source tax is built on a hedged answer from Anna ('I think so'), and the portal facts overstate what the units show.  
   Evidence: fact_judge: partial on F-hr_transcript-550840 and 5af8d0. Portal facts 39bab1 (spouse date of birth only when Married), 6d3630 and b359c3. Related open-question id OQ-source-tax-rule-confirmation appears in the changed elements.  
   Action: Get written confirmation from HR (Anna) of the final rule. Confirm what the portal does for Divorced and Widowed and for employees living abroad. Record the answers as decisions.
8. **Address required-fields and example inconsistencies** – The AC text and the examples disagree on which address fields are required. This produces ambiguous tests.  
   Evidence: US-02.2: AC-02.2.1 omits the house number, which D-042 makes required. The Germany example marks fields only 'asked'. US-05.2 and US-05.1 mix 'required' and 'asked'. US-01.2 shows civil status as '–' for Germany.  
   Action: Decide that all address fields are required, with 'no house number' as the only exception. Use one term ('required') in all examples. Fix the Germany civil-status example.
9. **Unspecified values and limits** – These are build-time decisions that nobody has made yet, and the spec does not cover them.  
   Evidence: dev_refinement info: permit reminder wording not given (US-01.4). Country and nationality list and stateless cases (US-05.1). Limits on the first working day and date of birth (US-03.1). Save and resume and confirmation (US-01.6). Spouse residence as yes/no under data minimisation (US-05.2). Keep-answers wording in D-036 versus AC-01.5.1.  
   Action: Record decisions: who provides the reminder wording and when, the country list, the date plausibility rules, and the save/confirm behaviour. Decide whether the spouse residence question is a yes/no or a country. Say whether keeping answers is a testable requirement.

## Numbers

342 source units → 177 facts → 35 information items, 18 business rules → one feature with 8 sections, 36 stories, 107 acceptance criteria; 2 open questions, 9 exclusions.

## Impact of this run

Stories added: US-04.4, US-05.4; changed: US-01.1, US-01.2, US-01.3, US-01.4, US-01.5, US-01.6, US-02.1, US-02.2, US-02.3, US-02.4, US-03.1, US-03.2, US-03.3, US-04.1, US-04.2, US-04.3, US-05.1, US-05.2, US-05.3, US-06.2, US-06.3, US-06.4, US-06.5, US-06.6, US-07.1, US-07.2, US-07.3, US-07.4, US-07.5, US-07.6, US-08.1, US-08.2, US-08.3, US-08.4; removed: -; unchanged: 0.

Knowledge elements changed: OQ-calculator-coverage, OQ-canton-abroad, OQ-civil-status-partnership, OQ-hr-side-follow-ups, OQ-source-tax-rule-confirmation, OQ-spouse-dob-other-status, address_country, address_house_number, address_postcode, address_street, address_town, base_tariff_letter, calculator_civil_status, calculator_residence, child_age_status, child_alternating_custody, child_common_household_other_parent, child_count, child_custody, child_main_financial_contributor, child_maintenance_over_50, child_parental_care, child_result, child_same_household, child_shared_custody, church_tax_suffix, civil_status, confession, cross_border_tariff, daily_return_germany, daily_return_liechtenstein, daily_return_reasonable, date_of_birth, discard_inapplicable_answers, first_name, first_working_day, has_children, holds_c_permit, insurance_start_date, last_name, liechtenstein_no_source_tax, nationality, non_return_days_45, non_return_days_60, pension_fund_canton, pension_fund_civil_status, permit_reminder, questionnaire_flow, read_only_after_submission, residence_canton, residence_certificate, spouse_date_of_birth, spouse_gainful_employment, spouse_holds_c_permit, spouse_nationality, spouse_residence_country, subject_to_source_tax, tariff_code, tariff_letter

## Errors (12)

- [examples] `AC-06.6.1 / Calculator: married, spouse works, one child, daily return with certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3)` tariff_code = ['N', 1, 'Y'], expected 'N1Y'
- [examples] `AC-06.6.1 / Calculator: same, without certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3)` tariff_code = ['C', 1, 'Y'], expected 'C1Y'
- [examples] `AC-06.6.1 / Single cross-border commuter, no children (D-001 example L0Y)` tariff_code = ['L', 0, 'Y'], expected 'L0Y'
- [examples] `AC-06.6.1 / Single non-Swiss resident of Switzerland, no church` tariff_code = ['A', 0, 'N'], expected 'A0N'
- [examples] `AC-06.6.1 / Calculator: married, spouse does not work, child neither (zh_source_tax_calculator/F-zh_source_tax_calculator-abe889)` tariff_code = ['B', 0, 'N'], expected 'B0N'
- [examples] `AC-06.6.1 / Living in another country, single, no church` tariff_code = ['A', 0, 'N'], expected 'A0N'
- [examples] `AC-06.6.2 / Tomás (hr_transcript/F-hr_transcript-b90bd9)` tariff_code = None, expected 'no tariff code'
- [examples] `AC-06.6.2 / Maria (hr_transcript/F-hr_transcript-845204)` tariff_code = None, expected 'no tariff code'
- [examples] `AC-06.6.2 / Swiss citizen living in Switzerland` tariff_code = None, expected 'no tariff code'
- [examples] `AC-06.6.3 / Liechtenstein, daily return` tariff_code = None, expected 'no tariff code'
- [examples] `AC-06.6.3 / Liechtenstein, at most 45 non-return days` tariff_code = None, expected 'no tariff code'
- [examples] `AC-06.6.3 / Calculator: Liechtenstein, more than 45 days, married, spouse works, one child (zh_source_tax_calculator/F-zh_source_tax_calculator-cc19c7)` tariff_code = ['C', 1, 'Y'], expected 'C1Y'

## Examples executed against the knowledge model (222/234 pass)

- ✅ AC-01.1.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.1.1 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.1.1 / Swiss citizen living abroad, like Stefan (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-01.1.1 / Swiss resident with Swiss citizenship (spec)
- ✅ AC-01.1.1 / Single non-Swiss resident without C permit (spec)
- ✅ AC-01.1.1 / Married to a non-Swiss spouse without C permit (spec)
- ✅ AC-01.1.1 / Married to a C permit holder living abroad (spec)
- ✅ AC-01.1.1 / Registered partner of a Swiss national living in Switzerland (spec)
- ✅ AC-01.1.1 / Separated non-Swiss resident without C permit (spec)
- ✅ AC-01.1.2 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.1.2 / Married employee living in Liechtenstein (spec)
- ✅ AC-01.2.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-01.2.1 / Employee living in Germany (spec)
- ✅ AC-01.2.2 / Liechtenstein, daily return (spec)
- ✅ AC-01.2.2 / Liechtenstein, no daily return, at most 45 non-return days (spec)
- ✅ AC-01.2.2 / Liechtenstein, more than 45 non-return days (spec)
- ✅ AC-01.3.1 / Civil status used by fund and source tax (spec)
- ✅ AC-01.3.2 / Divorced employee (spec)
- ✅ AC-01.3.2 / Widowed employee (spec)
- ✅ AC-01.3.2 / Registered partner, like Daniel (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-01.3.2 / Separated employee (spec)
- ✅ AC-01.4.1 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.4.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.4.1 / Swiss citizen living abroad, like Stefan (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-01.4.1 / Employee living in Liechtenstein (spec)
- ✅ AC-01.4.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-01.5.2 / Civil status changed from Married to Single (spec)
- ✅ AC-01.5.2 / Country changed from Switzerland to Germany (spec)
- ✅ AC-01.5.2 / Liechtenstein resident changed to daily return (spec)
- ✅ AC-02.1.1 / Employee living in Switzerland (spec)
- ✅ AC-02.1.1 / Employee living in Germany (spec)
- ✅ AC-02.1.2 / Employee living in Liechtenstein (spec)
- ✅ AC-02.2.1 / Employee living in Switzerland (spec)
- ✅ AC-02.2.1 / Employee living in Germany (spec)
- ✅ AC-02.3.2 / Stefan, Swiss citizen living abroad (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-02.3.2 / Employee living in Liechtenstein (spec)
- ✅ AC-02.3.2 / Employee living in another country (spec)
- ✅ AC-02.3.2 / Employee living in Switzerland (spec)
- ✅ AC-02.4.1 / Employee living in Switzerland (spec)
- ✅ AC-02.4.1 / Stefan, Swiss citizen living abroad (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-02.4.1 / Employee living in Liechtenstein (spec)
- ✅ AC-02.4.2 / Living in Switzerland, canton Bern (spec)
- ✅ AC-02.4.2 / Living in Switzerland, canton Zurich (spec)
- ✅ AC-02.4.2 / Stefan, Swiss citizen living abroad (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-02.4.2 / Living in Liechtenstein (spec)
- ✅ AC-02.4.2 / Living in another country (spec)
- ✅ AC-03.1.1 / Mid-month start, as in Julia's case (hr_transcript/F-hr_transcript-e18e66) (spec)
- ✅ AC-03.1.1 / Start on the 1st of a month (spec)
- ✅ AC-03.1.2 / Contract starts on Saturday 1 August (Swiss National Day) (spec)
- ✅ AC-03.2.2 / Start on 1 April (spec)
- ✅ AC-03.2.2 / Contractual start on Saturday 1 August (public holiday) (spec)
- ✅ AC-03.2.3 / Julia, start on 15 March (hr_transcript/F-hr_transcript-30d25c) (spec)
- ✅ AC-03.2.3 / Start on the 2nd of a month (spec)
- ✅ AC-03.2.3 / Start on the last day of the year (spec)
- ✅ AC-03.2.4 / Contractual start on Sunday 15 March (spec)
- ✅ AC-03.3.1 / Moved from 01.04 to 15.03, as Julia did (hr_transcript/F-hr_transcript-e18e66) (spec)
- ✅ AC-03.3.1 / Moved from 15.03 to 01.03 (earlier exit from old employer) (spec)
- ✅ AC-03.3.2 / HR moves the start from 15.03 to 01.05 (spec)
- ✅ AC-03.3.2 / HR moves the start from 01.05 to 20.04 (spec)
- ✅ AC-04.1.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-04.1.1 / Single employee (spec)
- ✅ AC-04.2.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-04.2.1 / Married employee (spec)
- ✅ AC-04.2.1 / Separated employee (spec)
- ✅ AC-04.2.2 / Single employee (spec)
- ✅ AC-04.2.2 / Divorced employee (spec)
- ✅ AC-04.2.2 / Widowed employee (spec)
- ✅ AC-04.3.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-04.3.1 / Married employee (spec)
- ✅ AC-04.3.2 / Single employee (spec)
- ✅ AC-04.3.2 / Divorced employee (spec)
- ✅ AC-04.3.2 / Widowed employee (spec)
- ✅ AC-04.3.2 / Separated employee (spec)
- ✅ AC-04.4.1 / Single employee (spec)
- ✅ AC-04.4.1 / Married employee (spec)
- ✅ AC-04.4.1 / Divorced employee (spec)
- ✅ AC-04.4.1 / Widowed employee (spec)
- ✅ AC-04.4.2 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-04.4.2 / Separated employee (spec)
- ✅ AC-05.1.1 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.1.1 / Swiss citizen living abroad, like Stefan (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.1.1 / Employee living in Liechtenstein (spec)
- ✅ AC-05.1.2 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.1.2 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.1.2 / Swiss employee living in Switzerland (spec)
- ✅ AC-05.2.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.1 / Registered partnership, non-Swiss without C permit (spec)
- ✅ AC-05.2.1 / Separated, non-Swiss without C permit (spec)
- ✅ AC-05.2.1 / Married C permit holder (spec)
- ✅ AC-05.2.1 / Married, living abroad (spec)
- ✅ AC-05.2.2 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.2 / Non-Swiss spouse (spec)
- ✅ AC-05.2.3 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.3 / Spouse with C permit (spec)
- ✅ AC-05.2.3 / Spouse neither Swiss nor C permit holder (spec)
- ✅ AC-05.3.1 / Swiss citizen living abroad, like Stefan (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.3.1 / Employee living in Liechtenstein (spec)
- ✅ AC-05.3.1 / Employee living in another country (spec)
- ✅ AC-05.3.2 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.3.2 / Swiss employee (also a dual national) (spec)
- ✅ AC-05.3.3 / Single, non-Swiss without C permit (spec)
- ✅ AC-05.3.3 / Separated, non-Swiss without C permit (spec)
- ✅ AC-05.3.3 / Widowed, non-Swiss without C permit (spec)
- ✅ AC-05.3.4 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.3.4 / Registered partner with C permit living in Switzerland (spec)
- ✅ AC-05.3.4 / Swiss spouse living abroad (spec)
- ✅ AC-05.3.4 / Spouse neither Swiss nor C permit holder (spec)
- ✅ AC-05.4.1 / Living in Switzerland (spec)
- ✅ AC-05.4.1 / Living in Konstanz (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.4.1 / Living in Liechtenstein (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.4.1 / Living in France (spec)
- ✅ AC-06.2.1 / Lives in Germany (spec)
- ✅ AC-06.2.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-06.2.1 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-06.2.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-06.2.1 / Non-Swiss single resident without C permit (spec)
- ✅ AC-06.2.1 / Liechtenstein, daily return (spec)
- ✅ AC-06.2.1 / Liechtenstein, at most 45 non-return days (spec)
- ✅ AC-06.2.1 / Liechtenstein, more than 45 non-return days (spec)
- ✅ AC-06.2.3 / Church member living in Germany (spec)
- ✅ AC-06.2.3 / No church membership, living in Germany (spec)
- ✅ AC-06.3.1 / Married, living in Germany (spec)
- ✅ AC-06.3.1 / Registered partnership, living in Germany (spec)
- ✅ AC-06.3.1 / Separated, living in Germany (spec)
- ✅ AC-06.3.1 / Divorced, living in Germany (spec)
- ✅ AC-06.3.1 / Single non-Swiss resident without C permit (spec)
- ✅ AC-06.3.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-06.3.1 / Married non-Swiss resident, spouse without C permit (spec)
- ✅ AC-06.3.1 / Married, Liechtenstein, daily return (spec)
- ✅ AC-06.3.1 / Married, Liechtenstein, more than 45 non-return days (spec)
- ✅ AC-06.4.1 / Married, spouse works (spec)
- ✅ AC-06.4.1 / Married, spouse does not work (spec)
- ✅ AC-06.4.1 / Registered partnership, partner works (spec)
- ✅ AC-06.4.1 / Married, spouse works, minor child with sole custody (spec)
- ✅ AC-06.4.2 / Single, no children (spec)
- ✅ AC-06.4.2 / Separated, no children (spec)
- ✅ AC-06.4.2 / Widowed, no children (spec)
- ✅ AC-06.4.2 / Divorced, minor child in household with sole custody (spec)
- ✅ AC-06.4.2 / Single, child neither minor nor in first education (spec)
- ✅ AC-06.5.1 / Married, spouse works, daily return with certificate (spec)
- ✅ AC-06.5.1 / Married, spouse does not work, daily return with certificate (spec)
- ✅ AC-06.5.1 / Single, no children, daily return with certificate (spec)
- ✅ AC-06.5.1 / Divorced, minor child with sole custody, daily return with certificate (spec)
- ✅ AC-06.5.1 / Married, spouse works, no daily return, reasonable, at most 60 days (spec)
- ✅ AC-06.5.2 / Married, daily return without certificate (spec)
- ✅ AC-06.5.2 / Married, daily return, certificate not yet (spec)
- ✅ AC-06.5.2 / Married, no daily return, not reasonable (spec)
- ✅ AC-06.5.2 / Married, no daily return, reasonable, more than 60 days (spec)
- ✅ AC-06.5.2 / Single non-Swiss resident of Switzerland (spec)
- ✅ AC-06.5.2 / Single, living in another country (spec)
- ❌ AC-06.6.1 / Calculator: married, spouse works, one child, daily return with certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec): tariff_code = ['N', 1, 'Y'], expected 'N1Y'
- ❌ AC-06.6.1 / Calculator: same, without certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec): tariff_code = ['C', 1, 'Y'], expected 'C1Y'
- ❌ AC-06.6.1 / Single cross-border commuter, no children (D-001 example L0Y) (spec): tariff_code = ['L', 0, 'Y'], expected 'L0Y'
- ❌ AC-06.6.1 / Single non-Swiss resident of Switzerland, no church (spec): tariff_code = ['A', 0, 'N'], expected 'A0N'
- ❌ AC-06.6.1 / Calculator: married, spouse does not work, child neither (zh_source_tax_calculator/F-zh_source_tax_calculator-abe889) (spec): tariff_code = ['B', 0, 'N'], expected 'B0N'
- ❌ AC-06.6.1 / Living in another country, single, no church (spec): tariff_code = ['A', 0, 'N'], expected 'A0N'
- ❌ AC-06.6.2 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec): tariff_code = None, expected 'no tariff code'
- ❌ AC-06.6.2 / Maria (hr_transcript/F-hr_transcript-845204) (spec): tariff_code = None, expected 'no tariff code'
- ❌ AC-06.6.2 / Swiss citizen living in Switzerland (spec): tariff_code = None, expected 'no tariff code'
- ❌ AC-06.6.3 / Liechtenstein, daily return (spec): tariff_code = None, expected 'no tariff code'
- ❌ AC-06.6.3 / Liechtenstein, at most 45 non-return days (spec): tariff_code = None, expected 'no tariff code'
- ❌ AC-06.6.3 / Calculator: Liechtenstein, more than 45 days, married, spouse works, one child (zh_source_tax_calculator/F-zh_source_tax_calculator-cc19c7) (spec): tariff_code = ['C', 1, 'Y'], expected 'C1Y'
- ✅ AC-07.1.1 / Lives in Germany, single (spec)
- ✅ AC-07.1.1 / Lives in Switzerland, not Swiss, no C permit, single (spec)
- ✅ AC-07.1.1 / Lives in Liechtenstein, more than 45 non-return days (spec)
- ✅ AC-07.1.2 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-07.1.2 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-07.1.2 / Swiss employee living in Switzerland (spec)
- ✅ AC-07.1.3 / Liechtenstein, daily return (spec)
- ✅ AC-07.1.3 / Liechtenstein, no daily return, at most 45 non-return days (spec)
- ✅ AC-07.1.5 / Germany, single, no children (spec)
- ✅ AC-07.2.2 / Germany, married, has children (spec)
- ✅ AC-07.2.3 / Calculator: married, child neither → B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-abe889) (spec)
- ✅ AC-07.2.4 / Minor child (spec)
- ✅ AC-07.2.4 / Adult child in first education (spec)
- ✅ AC-07.3.1 / Single, minor in household (spec)
- ✅ AC-07.3.2 / Calculator: married, sole custody → C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-d75286) (spec)
- ✅ AC-07.3.2 / Calculator: single, sole custody → H1 (zh_source_tax_calculator/F-zh_source_tax_calculator-300c72) (spec)
- ✅ AC-07.3.2 / Registered partnership, sole custody (spec)
- ✅ AC-07.3.2 / Separated, sole custody (spec)
- ✅ AC-07.3.3 / Calculator: married, shared custody, common household → C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-5d8fb0) (spec)
- ✅ AC-07.3.3 / Single, common household, employee main contributor (inferred) (spec)
- ✅ AC-07.3.3 / Calculator: single, common household, other parent main contributor → A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-5686d7) (spec)
- ✅ AC-07.3.4 / Calculator: married, no alternating custody → C0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-a4d358) (spec)
- ✅ AC-07.3.4 / Calculator: single, no alternating custody → H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc0ae9) (spec)
- ✅ AC-07.3.4 / Married, alternating custody, employee main contributor (inferred) (spec)
- ✅ AC-07.3.4 / Calculator: single, alternating custody, employee main contributor → H (zh_source_tax_calculator/F-zh_source_tax_calculator-300c72) (spec)
- ✅ AC-07.3.4 / Calculator: married, alternating custody, other parent main contributor → C0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-a4d358) (spec)
- ✅ AC-07.3.4 / Single, alternating custody, other parent main contributor (inferred) (spec)
- ✅ AC-07.4.1 / Registered partnership, minor elsewhere (spec)
- ✅ AC-07.4.1 / Separated, minor elsewhere (spec)
- ✅ AC-07.4.2 / Calculator: married, no shared custody → B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.2 / Calculator: single, no parental care → A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.3 / Calculator: married, shared custody, alternating, employee main contributor → B1N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.3 / Calculator: single, parental care, alternating, employee main contributor → H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.3 / Married, alternating, other parent main contributor (inferred) (spec)
- ✅ AC-07.4.3 / Widowed, parental care, no alternating custody (inferred) (spec)
- ✅ AC-07.5.1 / Adult child in household (spec)
- ✅ AC-07.5.2 / Calculator: married, adult in household, common household → B1N (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.2 / Single, common household, employee main contributor (inferred) (spec)
- ✅ AC-07.5.2 / Single, common household, other parent main contributor (inferred) (spec)
- ✅ AC-07.5.3 / Calculator: single, no common household, more than 50% → H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.3 / Married, no common household, more than 50% (inferred) (spec)
- ✅ AC-07.5.3 / No common household, not more than 50% (inferred) (spec)
- ✅ AC-07.5.4 / Calculator: single, adult elsewhere, more than 50% → A1N (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.4 / Married, adult elsewhere, more than 50% (inferred) (spec)
- ✅ AC-07.5.4 / Calculator: married, adult elsewhere, not more than 50% → B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.6.1 / Child that counts adds 1 (spec)
- ✅ AC-07.6.1 / Child counted with H adds 1 (spec)
- ✅ AC-07.6.1 / Child that does not count adds 0 (spec)
- ✅ AC-07.6.1 / No children gives 0 (spec)
- ✅ AC-08.1.2 / Employee living in Switzerland (Swiss) (spec)
- ✅ AC-08.1.2 / Employee living in France (other country) (spec)
- ✅ AC-08.2.1 / Employee living in Germany (spec)
- ✅ AC-08.2.1 / Employee living in Liechtenstein (spec)
- ✅ AC-08.2.2 / Daily return to Germany (spec)
- ✅ AC-08.2.2 / No daily return to Germany (spec)
- ✅ AC-08.2.3 / Calculator: daily return with certificate gives N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-08.2.3 / Calculator: daily return without certificate gives C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-08.2.3 / Certificate not yet available counts as no (spec)
- ✅ AC-08.3.1 / Germany, no daily return (spec)
- ✅ AC-08.3.1 / Germany, daily return (spec)
- ✅ AC-08.3.2 / Daily return reasonable (spec)
- ✅ AC-08.3.2 / Daily return not reasonable (spec)
- ✅ AC-08.3.3 / Calculator: reasonable, not more than 60 days gives N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-08.3.3 / Calculator: reasonable, more than 60 days gives C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-08.3.3 / Calculator: daily return not reasonable gives C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-08.4.1 / Liechtenstein resident (spec)
- ✅ AC-08.4.1 / Liechtenstein, no daily return (spec)
- ✅ AC-08.4.1 / Liechtenstein, daily return (spec)
- ✅ AC-08.4.1 / Employee living in Germany (spec)
- ✅ AC-08.4.2 / Calculator: daily return to Liechtenstein (zh_source_tax_calculator/F-zh_source_tax_calculator-fb87f1) (spec)
- ✅ AC-08.4.2 / Calculator: no daily return, at most 45 days (zh_source_tax_calculator/F-zh_source_tax_calculator-fb87f1) (spec)
- ✅ AC-08.4.3 / Calculator: more than 45 days gives C1Y with DTA reservation (zh_source_tax_calculator/F-zh_source_tax_calculator-cc19c7) (spec)

## Open questions (need your decision)

- **OQ-calculator-coverage**: Does Lonio's computed tariff code match the Zurich calculator for the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N examples, inferred per-child rows)? → recommended: Non-blocking for the spec, but a go-live condition: domain expert comparison before release.
- **OQ-hr-side-follow-ups**: How does HR see the Liechtenstein DTA flag and change the first working day or other answers after submission? → recommended: Note for the later HR-side spec; not blocking the questionnaire.

## Inferred items to confirm

- item.spouse_nationality
- item.spouse_holds_c_permit
- item.spouse_residence_country
- rule.child_result
- rule.child_count
- story.US-05.2
- story.US-07.3
- story.US-07.4
- story.US-07.5
- story.US-07.6
- fact F-hr_transcript-3edf89: HR needs the employee's name. Leo asked about 'Name, address' and Anna answered 'Yes', but she only elaborated on the address.
- fact F-hr_transcript-e18e66: When the first working day changes, the insurance start date given to the pension fund must be re-derived and updated. A missed update (Julia) caused a wrong date at the fund, an unfriendly letter and weeks of fixing.
- fact F-hr_transcript-54d011: The spouse's nationality, permit and residence only matter for source tax when the employee is married. They are presumably only needed when the employee would otherwise be subject to source tax (non-Swiss, no C permit, living in Switzerland).
- fact F-pension_portal-6d3630: No screenshot shows the form with Civil status 'Divorced' or 'Widowed'; it is unknown whether Spouse's date of birth (or any other field) appears for those values.
- fact F-pension_portal-b359c3: The portal does not say whether 'Canton' means canton of residence or of work, and the list offers no option for employees living outside Switzerland; how to register such employees is unknown.
- fact F-pension_portal-3a97ab: The portal requires an insurance start date on the 1st of a month but does not show how it relates to the employee's first working day (e.g. which 1st of a month to choose when work starts mid-month); the derivation rule is unknown.
- fact F-pension_portal-e45e5b: No screenshot shows the validation error for an insurance start date that is not the 1st of a month or for a malformed date; its behaviour and wording are unknown.
- fact F-zh_source_tax_calculator-2eab9a: Confession sets the church-tax suffix of the tariff: Y for röm.-kath./christ.-kath./evang.-ref., N for none or other (e.g. A0Y vs A0N).
- fact F-zh_source_tax_calculator-97139a: For married/registered partners, a spouse who is employed or receives replacement income leads to tariff C; otherwise tariff B.
- fact F-zh_source_tax_calculator-a4d358: Married, minor child in household, shared custody, no common household: alternating custody with the other parent as main contributor, or no alternating custody, gives C0Y (child not counted).
- fact F-zh_source_tax_calculator-dc0ae9: Single, minor child in household, shared custody, no common household and no alternating custody gives H1N (child counted with H).
- fact F-zh_source_tax_calculator-cc19c7: Liechtenstein residents without daily return and more than 45 non-return days get the normal tariff plus 'Unter Vorbehalt des Doppelbesteuerungsabkommens'.

## Dev refinement questions (12)

- [major] `feature.md` The step order contradicts itself. The flow table in feature.md has 8 steps: name, date of birth and first working day together in step 1, then one cross-border step 5 for Germany and Liechtenstein that comes before denomination and children, and a permit-reminder step 8. The 'Questionnaire flow overview' rule and US-01.2 AC-01.2.1 have 10 steps: first working day as its own step 2, Liechtenstein cross-border as step 6, Germany cross-border as step 9 after children, and a 'Summary and submission' step 10. Which order is correct? In particular, are the Germany cross-border questions asked before or after denomination and children, and is there a separate summary step?
- [major] `stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md` Results are 'always derived again from the latest answers'. If HR changes an answer after submission so that new questions now apply, the inputs were never asked. Examples: Single becomes Married (spouse's date of birth, spouse employment), a move from Switzerland to Germany (daily return, certificate), a new child (child block). What should the derived results show while those inputs are missing: no tariff code, an 'incomplete' state, or the old value? Do answers that no longer apply after an HR change get discarded, as they do on employee submission?
- [major] `stories/US-06.6-compute-and-record-the-full-source-tax-tariff-code.md` Every example in AC-06.6.1, AC-06.6.2 and AC-06.6.3 is marked ❌ under 'Checked', while all other stories show ✅. Are these expected tariff codes (N1Y, C1Y, L0Y, A0N, B0N, 'no tariff code', C1Y with the double taxation agreement note) known to be wrong, or just not checked yet? They are the main acceptance tests for the computed code.
- [minor] `stories/US-02.2-collect-a-complete-postal-home-address.md` AC-02.2.1 lists only street, postcode, town and country as required. Its Germany example marks every address field, including country, as only 'asked', while the Switzerland example marks them all 'required'. AC-02.2.2 and D-042 make the house number required too. Are all address fields required for every employee, whatever the country, with 'no house number' as the only way around the house number?
- [minor] `stories/US-01.5-discard-answers-that-no-longer-apply-on-submission.md` D-036 says answers that no longer apply 'may be kept' until submission. AC-01.5.1 makes it a requirement that the previous answer 'is still there'. Is keeping them a must (testable acceptance criterion), or optional?
- [minor] `stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md` In AC-01.2.1, the example 'Employee living in Germany' shows Civil status as '–' in the results, while civil status is always asked of everyone (US-04.1). Is this a mistake in the example, or is civil status meant to be skipped in some case?
- [minor] `stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md` Before submission, can the employee save partway and come back later, and is there a review/summary of all answers before the final submit? After submission, does the employee get a confirmation? Submission is final (read-only), so these decide what the employee can check before locking it.
- [minor] `stories/US-03.1-employee-confirms-the-first-working-day.md` Are there business limits on the first working day, e.g. it must not be in the past or more than N months ahead? Is there a plausibility check on the employee's and spouse's dates of birth (minimum working age)? The pension fund only requires the DD.MM.YYYY format.
- [minor] `stories/US-05.1-ask-nationality-and-c-permit-only-of-employees-living-in.md` Nationality (and the country of the home address and of the spouse's residence) is 'a country by English name'. Which list of countries/nationalities should be offered, and how do stateless employees or employees with unclear status answer the nationality question? Only 'Switzerland vs not' matters for the rule.
- [minor] `stories/US-05.2-ask-the-spouse-s-nationality-c-permit-and-residence-only.md` The example tables mix 'required' and 'asked' as expected results for questions the text says must be answered. Examples: spouse nationality 'required' for Tomás vs 'asked' for the registered partner; spouse residence 'required' vs 'asked'; in US-05.1, C permit 'required' for Maria vs 'asked' for Tomás. Is there a real difference (i.e. may some of these be left empty), or are they the same?
- [minor] `stories/US-05.2-ask-the-spouse-s-nationality-c-permit-and-residence-only.md` The spouse's country of residence matters only as 'lives in Switzerland or not'. Under data minimisation (G-01), should we ask the full country, or only 'Does your spouse/partner live in Switzerland? yes/no'?
- [minor] `stories/US-01.4-remind-non-swiss-employees-and-employees-living-abroad-to.md` The permit reminder is 'worded by HR', but no text is given. Who provides the final wording and when (before build or configurable later)? Is it shown only at the end, or also elsewhere (e.g. in a confirmation)?

## Technical vocabulary found in the spec (5)

- `feature.md` "Answers to questions that no longer apply are discarded on submission (discard_inapplicable_answers), and the questionnaire becomes read-only for the employee (read_only_after_submission)." - Internal snake_case rule ids appear in business prose. D-045 forbids this.
- `feature.md` "The expression gives each child's contribution (1 or 0), summed over all children." - Refers to an internal formula ('expression') rather than business language. D-045 forbids this.
- `feature.md` "The expression is per child; H applies if any child gives H." - Refers to an internal formula ('expression') rather than business language.
- `information.md` "The expression gives each child's contribution (1 or 0), summed over all children." - Refers to an internal formula ('expression') rather than business language.
- `information.md` "The expression is per child; H applies if any child gives H." - Refers to an internal formula ('expression') rather than business language.

## Coverage

158/342 source units cited; 143/177 facts used.

Uncited units (confirm they are irrelevant):

- hr_transcript/T-000: HR meeting transcript Everyone and everything here is fictional. Anna is the HR manager at Muster AG. Leo works in product at Lonio.
- hr_transcript/T-001: Can you hear me okay? You're a bit quiet.
- hr_transcript/T-002: Is this better? I'm in the small meeting room, the big one is taken. Sorry, let me just close the door.
- hr_transcript/T-003: Much better. So, thanks for making the time. The idea today is simple. We want your new employees to give us everything once, so that you stop chasing them for 
- hr_transcript/T-004: Yes, please. Right now it's a mess. I have a Word document, then an Excel file, and then I type everything into the portals by hand. Last month I spent a full a
- hr_transcript/T-005: Okay. And how many people do you hire in a year?
- hr_transcript/T-006: Around twenty. More in summer. We're about a hundred and fifty people now, mostly here in Zurich.
- hr_transcript/T-007: Good. Let's start with the biggest pain. What takes you the most time?
- hr_transcript/T-011: Okay, that's clear. And the questionnaire itself is what?
- hr_transcript/T-015: Anything else on the address?
- hr_transcript/T-017: Great. Do you also want a photo? Some customers ask for one.
- hr_transcript/T-019: It could. Do you want that from day one?
- hr_transcript/T-022: We're with Pensionskasse Muster. They have a portal, it's quite old. I'll send you some screenshots of it after this call, that's easier than me explaining it.
- hr_transcript/T-023: Perfect. What do you need for the fund that you don't have?
- hr_transcript/T-025: It moves?
- hr_transcript/T-027: Ouch.
- hr_transcript/T-029: Sorry, one second, someone's at my door. [pause] Okay, I'm back, sorry. Where were we?
- hr_transcript/T-030: The Julia story. It doesn't matter.
- hr_transcript/T-031: Right. What else about the employee affects the fund? Are they married, things like that?
- hr_transcript/T-033: And what are the options in that list?
- hr_transcript/T-035: How did you enter him?
- hr_transcript/T-037: Okay. Noted. Can I go back to source tax? You said all non-Swiss employees.
- hr_transcript/T-041: Sure, send it if it's easy. Do people need anything from you on the first day? Laptops, things like that? I just want to see if that belongs in the same form.
- hr_transcript/T-047: Okay. Anything else on who needs to do it? I'd rather hear all of it now.
- hr_transcript/T-052: Only the timing. When can we have this?
- hr_transcript/T-053: I'll come back to you on that this week, once we've gone through your screenshots.
- hr_transcript/T-054: Good. I'll send them after lunch. Thanks, Leo.
- hr_transcript/T-055: Thanks, Anna. Talk soon.
- pension_portal/S01-E01: Pensionskasse Muster
- pension_portal/S01-E02: Employer portal · Muster AG · Log out
- pension_portal/S01-E03: Home > Insured persons > Register new employee
- pension_portal/S01-E04: Register new employee
- pension_portal/S01-E05: Employee
- pension_portal/S01-E17: Cancel
- pension_portal/S01-E18: Register
- pension_portal/S02-E01: Pensionskasse Muster
- pension_portal/S02-E02: Employer portal · Muster AG · Log out
- pension_portal/S02-E03: Home > Insured persons > Register new employee
- pension_portal/S02-E04: Register new employee
- pension_portal/S02-E05: Employee
- pension_portal/S02-E06: First name
- pension_portal/S02-E07: Last name
- pension_portal/S02-E08: Date of birth
- pension_portal/S02-E09: DD.MM.YYYY
- pension_portal/S02-E11: Please select
- pension_portal/S02-E38: Insurance
- pension_portal/S02-E39: Insurance start date
- pension_portal/S02-E40: Civil status
- pension_portal/S02-E41: Cancel
- pension_portal/S02-E42: Register
- pension_portal/S02-E43: Fields marked * are required.
- pension_portal/S03-E01: Pensionskasse Muster
- pension_portal/S03-E02: Employer portal · Muster AG · Log out
- pension_portal/S03-E03: Home > Insured persons > Register new employee
- pension_portal/S03-E04: Register new employee
- pension_portal/S03-E05: Employee
- pension_portal/S03-E06: First name
- pension_portal/S03-E07: Lena
- pension_portal/S03-E08: Last name
- pension_portal/S03-E09: Keller
- pension_portal/S03-E10: Date of birth
- pension_portal/S03-E11: 14.02.1991
- pension_portal/S03-E12: DD.MM.YYYY
- pension_portal/S03-E13: Canton
- pension_portal/S03-E14: Zurich
- pension_portal/S03-E15: Insurance
- pension_portal/S03-E16: Insurance start date
- pension_portal/S03-E17: 01.05.2026
- pension_portal/S03-E18: DD.MM.YYYY. Must be the 1st of a month.
- pension_portal/S03-E20: Please select
- pension_portal/S03-E25: Cancel
- pension_portal/S03-E26: Register
- pension_portal/S03-E27: Fields marked * are required.
- pension_portal/S04-E01: Pensionskasse Muster
- pension_portal/S04-E02: Employer portal · Muster AG · Log out
- pension_portal/S04-E03: Home > Insured persons > Register new employee
- pension_portal/S04-E04: Register new employee
- pension_portal/S04-E05: Employee
- pension_portal/S04-E06: First name
- pension_portal/S04-E07: Lena
- pension_portal/S04-E08: Last name
- pension_portal/S04-E09: Keller
- pension_portal/S04-E10: Date of birth
- pension_portal/S04-E11: 14.02.1991
- pension_portal/S04-E12: DD.MM.YYYY
- pension_portal/S04-E13: Canton
- pension_portal/S04-E14: Zurich
- pension_portal/S04-E15: Insurance
- pension_portal/S04-E16: Insurance start date
- pension_portal/S04-E17: 01.05.2026
- pension_portal/S04-E18: DD.MM.YYYY. Must be the 1st of a month.
- pension_portal/S04-E19: Civil status
- pension_portal/S04-E21: Cancel
- pension_portal/S04-E22: Register
- pension_portal/S04-E23: Fields marked * are required.
- pension_portal/S05-E01: Pensionskasse Muster
- pension_portal/S05-E02: Employer portal · Muster AG · Log out
- pension_portal/S05-E03: Home > Insured persons > Register new employee
- pension_portal/S05-E04: Register new employee
- pension_portal/S05-E05: Employee
- pension_portal/S05-E06: First name
- pension_portal/S05-E07: Marco
- pension_portal/S05-E08: Last name
- pension_portal/S05-E09: Rossi
- pension_portal/S05-E10: Date of birth
- pension_portal/S05-E11: 03.09.1985
- pension_portal/S05-E12: DD.MM.YYYY
- pension_portal/S05-E13: Canton
- pension_portal/S05-E14: Bern
- pension_portal/S05-E15: Insurance
- pension_portal/S05-E16: Insurance start date
- pension_portal/S05-E17: 01.06.2026
- pension_portal/S05-E18: DD.MM.YYYY. Must be the 1st of a month.
- pension_portal/S05-E19: Civil status
- pension_portal/S05-E22: 22.11.1987
- pension_portal/S05-E24: Cancel
- pension_portal/S05-E25: Register
- pension_portal/S05-E26: Fields marked * are required.
- pension_portal/S06-E01: Pensionskasse Muster
- pension_portal/S06-E02: Employer portal · Muster AG · Log out
- pension_portal/S06-E03: Home > Insured persons > Register new employee
- pension_portal/S06-E04: Register new employee
- pension_portal/S06-E06: Employee
- pension_portal/S06-E07: First name
- pension_portal/S06-E09: Last name
- pension_portal/S06-E11: Date of birth
- pension_portal/S06-E12: DD.MM.YYYY
- pension_portal/S06-E14: Canton
- pension_portal/S06-E15: Please select
- pension_portal/S06-E17: Insurance
- pension_portal/S06-E18: Insurance start date
- pension_portal/S06-E19: DD.MM.YYYY. Must be the 1st of a month.
- pension_portal/S06-E21: Civil status
- pension_portal/S06-E22: Please select
- pension_portal/S06-E24: Cancel
- pension_portal/S06-E25: Register
- pension_portal/S06-E26: Fields marked * are required.
- pension_portal/S07-E01: Pensionskasse Muster
- pension_portal/S07-E02: Employer portal · Muster AG · Log out
- pension_portal/S07-E03: Home > Insured persons > Register new employee
- pension_portal/S07-E04: Register new employee
- pension_portal/S07-E05: Employee
- pension_portal/S07-E06: First name
- pension_portal/S07-E07: Marco
- pension_portal/S07-E08: Last name
- pension_portal/S07-E09: Rossi
- pension_portal/S07-E10: Date of birth
- pension_portal/S07-E11: 03.09.1985
- pension_portal/S07-E12: DD.MM.YYYY
- pension_portal/S07-E13: Canton
- pension_portal/S07-E14: Bern
- pension_portal/S07-E15: Insurance
- pension_portal/S07-E16: Insurance start date
- pension_portal/S07-E17: 01.06.2026
- pension_portal/S07-E18: DD.MM.YYYY. Must be the 1st of a month.
- pension_portal/S07-E19: Civil status
- pension_portal/S07-E22: 
- pension_portal/S07-E23: DD.MM.YYYY
- pension_portal/S07-E25: Cancel
- pension_portal/S07-E26: Register
- pension_portal/S07-E27: Fields marked * are required.
- zh_source_tax_calculator/C-Q24: Tägliche Rückkehr an den Hauptwohnsitz in Deutschland während oder vor Bezug der Ersatzeinkünfte? Options: Ja | Nein
- zh_source_tax_calculator/C-Q25: Tägliche Rückkehr grundsätzlich zumutbar während oder vor Bezug der Ersatzeinkünfte (weniger als 100km Fahrdistanz)? Options: Ja | Nein
- zh_source_tax_calculator/C-Q26: Nachweis von mehr als 60 beruflich bedingten Nichtrückkehrtagen im Kalenderjahr beigebracht während oder vor Bezug der Ersatzeinkünfte? Options: Ja | Nein
- zh_source_tax_calculator/C-Q27: Tägliche Rückkehr an den Hauptwohnsitz in Liechtenstein während oder vor Bezug der Ersatzeinkünfte? Options: Ja | Nein
- zh_source_tax_calculator/C-Q28: Mehr als 45 beruflich bedingte Nichtrückkehrtage im Kalenderjahr während oder vor Bezug der Ersatzeinkünfte? Options: Ja | Nein
- zh_source_tax_calculator/C-V04: Answers {"Q01": "Erwerbseinkommen", "Q02": "Verheiratet oder eingetragene Partnerschaft", "Q03": "Keine oder andere", "Q04": "Nein", "Q05": "Nein", "Q16": "Ja"}
- zh_source_tax_calculator/C-V06: Answers {"Q01": "Erwerbseinkommen", "Q02": "Verheiratet oder eingetragene Partnerschaft", "Q03": "Keine oder andere", "Q04": "Ja", "Q05": "Nein", "Q16": "Ja"} -
- zh_source_tax_calculator/C-V24: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "weder noch", "Q16": "Ja"} 
- zh_source_tax_calculator/C-V25: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "Minderjährig (Kind 1) + Mi
- zh_source_tax_calculator/C-V26: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "Kind 1: Minderjährig; Kind
- zh_source_tax_calculator/C-V27: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "Kind 1: Volljährig und in 
- zh_source_tax_calculator/C-V29: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "Minderjährig (Kind 1-3)", 
- zh_source_tax_calculator/C-V30: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "röm.-kath., christ.-kath., evang.-ref.", "Q06": "Nein", "Q16": "Nei
- zh_source_tax_calculator/C-V31: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "Volljährig und in Erstausb
- zh_source_tax_calculator/C-V32: Answers {"Q01": "Erwerbseinkommen", "Q02": "Verheiratet oder eingetragene Partnerschaft", "Q03": "Keine oder andere", "Q04": "Nein", "Q05": "Nein", "Q16": "Nein
- zh_source_tax_calculator/C-V33: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "röm.-kath., christ.-kath., evang.-ref.", "Q06": "Ja", "Q07": "Minde
- zh_source_tax_calculator/C-V45: Answers {"Q01": "Ersatzeinkünfte", "Q16": "Nein", "Q17": "Deutschland", "Q24": "Ja", "Q19": "Nein"} -> result Tarif: G
- zh_source_tax_calculator/C-V46: Answers {"Q01": "Ersatzeinkünfte", "Q16": "Nein", "Q17": "Deutschland", "Q24": "Nein", "Q25": "Ja", "Q26": "Nein"} -> result Tarif: Q
- zh_source_tax_calculator/C-V47: Answers {"Q01": "Ersatzeinkünfte", "Q16": "Nein", "Q17": "Deutschland", "Q24": "Nein", "Q25": "Ja", "Q26": "Ja"} -> result Tarif: G
- zh_source_tax_calculator/C-V48: Answers {"Q01": "Ersatzeinkünfte", "Q16": "Nein", "Q17": "Deutschland", "Q24": "Nein", "Q25": "Nein"} -> result Tarif: G
- zh_source_tax_calculator/C-V51: Answers {"Q01": "Ersatzeinkünfte", "Q16": "Nein", "Q17": "Liechtenstein", "Q27": "Nein", "Q28": "Nein"} -> result Grundsätzlich keine Quellensteuerpflicht / Unt
- zh_source_tax_calculator/C-N01: The calculator is an Angular app (app-root, ng 11, assets from www.services.zh.ch/app/quest/tarifbestimmung/prod/) rendered inline in the section 'Tarifrechner 
- zh_source_tax_calculator/C-N08: The answer value in V25–V29 summarises repeated per-child answers (Kind 1/2/3) because the schema allows one value per question id.

## Other warnings (41)

- [fact_judge] `F-hr_transcript-34494f` partial: Leo's 'We'll keep that for now' supports agreement, but 'online tariff calculator' and 'canton of Zurich' are okay; 'acknowledges not exactly how it works' is fine—minor: Leo agreed is supported, so only the 'questionnaire is the calculator' equation is slightly inferred. | The source tax questionnaire is the canton of Zurich's online tariff calculator, which outputs the tariff code. HR uses the Zurich calculator for everybody and acknowledges that this is not exactly how it works. Leo agreed to keep it that way for now.
- [fact_judge] `F-hr_transcript-550840` partial: Leo's summary and Anna's 'I think so' are supported, but 'later added more conditions' is not shown in these units. | Leo summarised the rule as 'non-Swiss, but not with a C permit'. Anna only answered 'I think so' (hedged), and later added more conditions.
- [fact_judge] `F-hr_transcript-a45422` partial: Manual check and email asking are supported, but the email being for the spouse details 'takes forever' is fine; 'I ask them by email' fits, though the exemption check by hand is stated only for the Tomás case. | Today HR checks the spouse exemption by hand and asks for the spouse details by email, which takes forever.
- [fact_judge] `F-hr_transcript-5af8d0` partial: Gist is a reasonable synthesis, but 'here' = Switzerland is an assumption, and the claim that the spouse exemption applies only to Swiss-resident employees is not stated; also 'I think' hedge is Anna's at T-048. | Consolidated final rule. An employee who lives abroad (outside Switzerland) is subject to source tax regardless of nationality. An employee who lives in Switzerland is subject only if they are non-Swiss without a C permit and are not married to a Swiss national or C-permit holder who lives in Switzerland. Note: Anna said 'here', which is read as Switzerland. Her 'I think' hedges remain.
- [fact_judge] `F-pension_portal-39bab1` partial: Units show the field absent for Single and present for Married, but screenshots 01, 02, 03 and 06 are not in these units, and Divorced/Widowed are never shown, so 'only when Married' is overstated. | The 'Spouse's date of birth' field appears only when Civil status is 'Married' (shown in screenshots 05 and 07, both with Married); it is absent in screenshot 04 (Civil status 'Single') and in screenshots 01, 02, 03 and 06 (Civil status not selected).
- [fact_judge] `F-pension_portal-6d3630` partial: Units show only the civil-status dropdown list, so the absence of any Divorced/Widowed form screenshot cannot be confirmed from them. | No screenshot shows the form with Civil status 'Divorced' or 'Widowed'; it is unknown whether Spouse's date of birth (or any other field) appears for those values.
- [fact_judge] `F-pension_portal-b359c3` partial: Units show only part of the canton list (Zug, Zurich) and no help text; the lack of an outside-Switzerland option and the ambiguity are not fully verifiable. | The portal does not say whether 'Canton' means canton of residence or of work, and the list offers no option for employees living outside Switzerland; how to register such employees is unknown.
- [fact_judge] `F-pension_portal-e45e5b` partial: Only the required-field error is visible in these units; absence of other error screenshots cannot be confirmed. | No screenshot shows the validation error for an insurance start date that is not the 1st of a month or for a malformed date; its behaviour and wording are unknown.
- [fact_judge] `F-zh_source_tax_calculator-037b1c` partial: Vectors show A0Y/A0N for single without children with Q16=Ja, but the units never state that Q16 means residence in Switzerland. | A single/divorced/separated/widowed person without counted children with earned income and residence in Switzerland gets tariff A (A0Y/A0N).
- [fact_judge] `F-zh_source_tax_calculator-64ac33` partial: Conditions match, but Q14's meaning ('parental care') is not shown in the units, so that label is an unverified gloss. | Alternating custody is asked only for a minor child when: (in household, shared custody, no common household with other parent) or (married, not in household, shared custody Q13 = Ja) or (non-married, not in household, parental care Q14 = Ja).
- [fact_judge] `F-zh_source_tax_calculator-dc0ae9` partial: V19 gives H1N for these answers, but the units don't give the Q10/Q11 question texts, so mapping them to 'common household' and 'alternating custody' is inferred. | Single, minor child in household, shared custody, no common household and no alternating custody gives H1N (child counted with H).
- [fact_judge] `F-zh_source_tax_calculator-c8aa5e` partial: Q21 help lists only L/M/N/P for the cross-border outcome; adding Q is not stated for this branch. | Germany resident without daily return: if return is not reasonable -> normal tariff; if reasonable and >60 non-return days proven -> normal tariff; if reasonable and no proof -> cross-border tariff (L/M/N/P, Q).
- [fact_judge] `F-zh_source_tax_calculator-2754e8` partial: Outcomes match the vectors, but these units never state that Q19 is the certificate (Ansässigkeitsbescheinigung) question. | Replacement income, Germany: daily return with certificate -> Q; daily return without certificate -> G; no daily return, reasonable, no >60-day proof -> Q; with proof -> G; not reasonable -> G.
- [coverage] `F-pension_portal-e45e5b` fact not used anywhere in the spec: No screenshot shows the validation error for an insurance start date that is not the 1st of a month or for a malformed date; its behaviour and wording are unknown.
- [trace_judge] `item.has_children` partial: The purpose 'possibly tariff H' is not backed by any cited fact; only the child digit is supported.
- [trace_judge] `item.child_same_household` partial: The 'per-child result' purpose and the 'repeated per child' form are not backed by the cited facts, which only cover the question, its options and when it is shown.
- [trace_judge] `item.child_custody` partial: The question, options and display conditions are backed, but the purpose 'sole custody makes the child count (tariff H for single persons)' is not in any cited fact.
- [trace_judge] `item.child_main_financial_contributor` partial: The question, options and conditions are backed, but the purpose 'main contributor can count the child (tariff H for single persons)' is not in any cited fact.
- [trace_judge] `rule.questionnaire_flow` partial: The cited facts back only English, ask-once, the Liechtenstein ordering and the full tariff code; the content of steps 1-5, 7-10 and the 'Swiss with Swiss citizenship or C permit never see source tax questions' claim are not in the cited facts.
- [trace_judge] `rule.calculator_residence` partial: The 'Other country (base tariff, no further residence questions)' row cites F-...-f86c6b, which is not among the cited facts, so 'base tariff, no further residence questions' is unbacked.
- [trace_judge] `rule.child_result` partial: The 'Neither' → 'does not count' row cites F-...-abe889, which is not among the cited facts; the other rows are backed or marked inferred under D-046/D-009.
- [trace_judge] `rule.cross_border_tariff` partial: The Germany rows are backed, but the 'Switzerland, Liechtenstein or other country → normal tariff' row cites f86c6b and cc19c7, which are not among the cited facts.
- [trace_judge] `rule.tariff_letter` partial: The cited fact also maps G->Q for the cross-border tariff, but the rule and its expression omit G and return null for it.
- [trace_judge] `story.US-01.2` partial: The Germany cross-border step, the nationality/C-permit step, and the always-asked name and date of birth are not backed by the cited facts (D-005 and the pension-portal facts are not cited).
- [trace_judge] `story.US-01.3` partial: Country of residence being needed by HR, the pension fund and source tax is not backed by the cited facts, and the separated example's 'spouse nationality not asked' has no cited support.
- [trace_judge] `story.US-01.4` partial: The permit reminder rule is backed by D-010 and D-038, but the non-illustrative Maria and Tomás examples rely on transcript facts that are not cited.
- [trace_judge] `story.US-02.1` partial: The pension fund's required fields are backed, but HR using the name to address the documents it posts is not in the cited quote, which covers only the address.
- [trace_judge] `story.US-02.2` partial: AC-02.2.1 lists only street, postcode, town and country as required, leaving out the house number, which D-042 makes required and which its own Switzerland example marks required.
- [trace_judge] `story.US-03.3` partial: The non-illustrative example 'Moved from 01.04 to 15.03' invents the original 01.04 date, because the fact only says Julia moved her date to 15 March.
- [trace_judge] `story.US-04.3` partial: AC-04.3.3 and the priority reason say the calculator's civil status drives the spouse questions on the married path and the tariff letter, but no cited fact describes those calculator steps; the cited facts give only the two civil status groups and the spouse exemption.
- [trace_judge] `story.US-06.4` partial: The claims that children never change the letter for married employees, and that a single employee whose child does not count with H gets A, are not stated in the cited facts, which only cover the no-children case and the H-child case.
- [trace_judge] `story.US-06.6` partial: AC-06.6.1 says the child digit has 'no maximum', but the cited facts do not back this; D-044 is not cited there and the calculator facts say more than 3 children is untested.
- [trace_judge] `story.US-07.1` partial: No cited fact says the children answer is 'required' or 'recorded for HR' (D-034 is not cited), and AC-07.1.2 adds registered partnership with a Swiss or C-permit spouse, which the cited source-tax facts do not mention.
- [trace_judge] `story.US-07.2` partial: The 'an answer is required' claims in AC-07.2.2 and AC-07.2.4 are not backed by any cited fact, which only give the calculator's options.
- [trace_judge] `story.US-07.3` partial: The 'answer is required' claims are not backed by cited facts, and the non-illustrative 'single, alternating custody, employee main contributor → H' example (shown as Divorced) is not an observed calculator row in the cited facts.
- [trace_judge] `story.US-07.4` partial: The 'answer is required' claims are not backed by cited facts, and the 'does not count' cases for alternating custody are only inferred, not observed.
- [trace_judge] `story.US-07.5` partial: The 'required' claims are not backed by cited facts, and the registered-partnership and separated equivalences in the AC wording are only covered by assumption.
- [trace_judge] `story.US-07.6` partial: AC-07.6.2's claim that married employees and registered partners never get 'counts with H' is not stated in the cited facts, which only describe H for single, divorced, separated or widowed persons.
- [dev_refinement] `feature.md` The step order contradicts itself. The flow table in feature.md has 8 steps: name, date of birth and first working day together in step 1, then one cross-border step 5 for Germany and Liechtenstein that comes before denomination and children, and a permit-reminder step 8. The 'Questionnaire flow overview' rule and US-01.2 AC-01.2.1 have 10 steps: first working day as its own step 2, Liechtenstein cross-border as step 6, Germany cross-border as step 9 after children, and a 'Summary and submission' step 10. Which order is correct? In particular, are the Germany cross-border questions asked before or after denomination and children, and is there a separate summary step?
- [dev_refinement] `stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md` Results are 'always derived again from the latest answers'. If HR changes an answer after submission so that new questions now apply, the inputs were never asked. Examples: Single becomes Married (spouse's date of birth, spouse employment), a move from Switzerland to Germany (daily return, certificate), a new child (child block). What should the derived results show while those inputs are missing: no tariff code, an 'incomplete' state, or the old value? Do answers that no longer apply after an HR change get discarded, as they do on employee submission?
- [dev_refinement] `stories/US-06.6-compute-and-record-the-full-source-tax-tariff-code.md` Every example in AC-06.6.1, AC-06.6.2 and AC-06.6.3 is marked ❌ under 'Checked', while all other stories show ✅. Are these expected tariff codes (N1Y, C1Y, L0Y, A0N, B0N, 'no tariff code', C1Y with the double taxation agreement note) known to be wrong, or just not checked yet? They are the main acceptance tests for the computed code.

## Run

Stages run: knowledge.raw, feature.plan, sections/SEC-03-employment-start, sections/SEC-02-personal-details-address, sections/SEC-04-civil-status-spouse, sections/SEC-05-source-tax-liability, sections/SEC-01-questionnaire-flow, sections/SEC-08-cross-border-residence, sections/SEC-06-source-tax-tariff-basics, sections/SEC-07-source-tax-children, feature.flow, judge_trace, dev_refinement, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator, judge_facts

LLM cost this run: $9.22

Tokens this run: 1,080,931 in 29 agent calls (58 input, 50,048 cache read, 847,421 cache write, 183,404 output)
