# Review: employee-onboarding

**Verdict: NOT READY**

Not ready. The tariff_code rule fails lint because its expression uses a `+` (BinOp) that the expression language doesn't allow. That one error makes 14 examples fail (all of AC-06.6.x and AC-06.7.3), including the main acceptance tests for the computed tariff code. A US-01.6 contradiction and a technical-vocabulary leak are also open. The other items are caveats: weak traceability on several items, two non-blocking open questions, and inconsistent 'asked' and 'required' wording.

## Reviewer findings

1. **tariff_code rule does not evaluate (lint error); 14 examples fail** – The tariff code is the core output of the feature. The expression concatenates tariff_letter + child_count + church_tax_suffix with `+`, which the expression language rejects. No tariff code can be computed, and the 14 examples that expect one all fail.  
   Evidence: lint rule.tariff_code; examples AC-06.6.1 (7 cases), AC-06.6.2 (3), AC-06.6.3 (3), AC-06.7.3 'Employee answers no'. All show 'construct BinOp not allowed'.  
   Action: Rewrite the rule using the allowed constructs, e.g. a concat/format function, or one if_else branch per letter/digit/suffix. If concatenation is needed, add it to the expression language. Re-run the examples; there should be no expectation changes.
2. **The tariff rule does not implement the statement or table for the Liechtenstein >45 days and incomplete cases** – The statement says the more-than-45-days case carries a 'subject to the double taxation agreement' note and that an incomplete questionnaire gives 'incomplete - HR must complete' (D-048). The expression yields neither. Fixing the BinOp alone would still leave the rule short of its own spec.  
   Evidence: trace_judge rule.tariff_code; AC-06.6.3 'more than 45 non-return days' expects C0Y; AC-01.6.3 / D-048  
   Action: Decide in decisions.yaml how the DTA note and the incomplete result are represented (extra output field or text), and add both to the rule. Cite fb87f1 and cc19c7 in the rule.
3. **AC-01.6.2 contradicts AC-01.6.3** – After submission the questionnaire is read-only. The example nevertheless expects 'Denomination: asked' once HR records a change, while D-048 says the result becomes 'incomplete - HR must complete'. Engineering cannot tell whether the questionnaire reopens for the employee.  
   Evidence: dev_refinement US-01.6 (major); AC-01.6.1, AC-01.6.2, AC-01.6.3, D-048  
   Action: Decide whether HR completes the missing answer or the employee is asked again. Then fix the example, or AC-01.6.3, accordingly.
4. **Implementation vocabulary leaks into the spec** – D-045 forbids the word 'expression' in business text, and the 'ISO 3166' list name is implementation vocabulary. Engineering decisions should not be fixed in the spec.  
   Evidence: tech_leak feature.md and information.md ('The expression gives, per child…'); item.address_country, item.nationality, item.spouse_nationality, AC-02.3.1 ('ISO 3166')  
   Action: Reword the child-count note in business terms, e.g. 'the digit is the number of counted children'. Replace 'ISO 3166 country list' with 'list of countries'. Leave the standard to engineering.
5. **Facts cited by examples and conditions are not in the cited-fact lists** – Several story examples, items and rules rely on facts that are not in their cited sets. Most of these are the Maria and Tomás examples. This weakens traceability. Two claims are unbacked: Liechtenstein never gets the cross-border tariff, and Swiss nationals are exempt.  
   Evidence: trace_judge US-01.2, US-01.4, US-06.2, US-06.3, US-06.5, US-06.6, US-06.7, US-08.2 (AC-08.2.4), rule.cross_border_tariff, rule.questionnaire_flow, item.spouse_gainful_employment, item.has_children  
   Action: Add the missing source_refs (845204, b90bd9, 3f2c2a, cc19c7, d75286, 300c72, 97139a). Then confirm in decisions.yaml the Liechtenstein cross-border rule and the Swiss-national exemption, which no source states.
6. **Purpose claims and one rule row are unsupported or overstated** – Several purposes are stated as business rules without a source, and one rule row contradicts its source. Engineers will take them as confirmed.  
   Evidence: trace_judge item.child_main_financial_contributor ('H tariff'), item.non_return_days_60, item.daily_return_reasonable, item.first_working_day (age reference date), AC-03.1.4 ('HR plans the start'), US-06.2 (denomination not part of fund registration), rule.pension_fund_civil_status (partner date of birth also for Separated and Married, but D-003 covers registered partnership only)  
   Action: Either back each claim with a decision or source, or soften or remove it. For pension_fund_civil_status, confirm in decisions.yaml which civil statuses need the partner's date of birth.
7. **Inconsistent blocking behaviour and 'asked' versus 'required'** – The stories disagree on whether a missing required answer blocks the next step or only submission. The expected-result vocabulary also differs between stories, and '–' is undefined. Test cases will be ambiguous.  
   Evidence: dev_refinement US-01.8 (US-02.1/02.2 vs AC-01.8.3/US-04.1); US-01.2 vs US-05.1/05.2  
   Action: Decide on one rule: block only submission, which fits the save-and-resume in US-01.7. Define 'asked' versus 'required' and the meaning of '–', then align the stories.
8. **Certificate-of-residence semantics are unclear** – The item is named 'handed in' and the calculator asks 'beigebracht', but the story asks whether the employee 'has' a certificate. This changes the meaning of yes/no/not yet, and what HR expects afterwards.  
   Evidence: dev_refinement US-08.2; trace_judge item.residence_certificate  
   Action: Decide in decisions.yaml what 'yes', 'no' and 'not yet' mean, and when HR expects a certificate.
9. **Non-blocking open questions need owners before go-live** – The tariff code may differ from the Zurich calculator on unexplored paths. Several facts are only partly verified, and the pension portal form for Divorced and Widowed is unknown. The portal facts for the start date and canton are unused or unverified. The Germany questions for people living abroad are not specified.  
   Evidence: OQ-calculator-coverage, OQ-fund-divorced-widowed; fact_judge F-pension_portal-39bab1, -6d3630, -b359c3, -e45e5b; coverage F-pension_portal-3a97ab, F-hr_transcript-8595fb; US-03.1 date window  
   Action: Assign a domain expert to compare computed codes with the calculator before go-live. Ask the fund or HR to check the portal. Clarify how the insurance start date derives from the first working day, and what happens when the first working day is in the past.
10. **Inferred items remain unconfirmed** – Several rules and stories are inferred and rely on 'inferred, go-live check' examples. They also carry gaps such as Q14 being read as parental care, and Q16 being read as residence in Switzerland.  
   Evidence: inferred_items (spouse_nationality, church_tax_suffix, child_result, base_tariff_letter, US-05.2, US-07.3 to 07.5 and others); fact_judge F-zh_source_tax_calculator-64ac33, -037b1c, -dc0ae9, -2754e8  
   Action: Have HR or a domain expert confirm the inferred items and the calculator-question meanings, and record them in decisions.yaml.

## Numbers

342 source units → 177 facts → 35 information items, 18 business rules → one feature with 8 sections, 39 stories, 120 acceptance criteria; 2 open questions, 11 exclusions.

## Impact of this run

Stories added: US-01.7, US-01.8, US-06.7; changed: US-01.1, US-01.2, US-01.3, US-01.4, US-01.5, US-01.6, US-02.1, US-02.2, US-02.3, US-02.4, US-03.1, US-03.2, US-03.3, US-04.1, US-04.2, US-04.3, US-04.4, US-05.1, US-05.2, US-05.3, US-05.4, US-06.2, US-06.3, US-06.4, US-06.5, US-06.6, US-07.1, US-07.2, US-07.3, US-07.4, US-07.5, US-07.6, US-08.1, US-08.2, US-08.3, US-08.4; removed: -; unchanged: 0.

Knowledge elements changed: OQ-calculator-coverage, OQ-fund-divorced-widowed, OQ-hr-side-follow-ups, address_country, address_house_number, address_postcode, address_street, address_town, base_tariff_letter, calculator_civil_status, calculator_residence, child_age_status, child_alternating_custody, child_common_household_other_parent, child_count, child_custody, child_main_financial_contributor, child_maintenance_over_50, child_parental_care, child_result, child_same_household, child_shared_custody, church_tax_suffix, civil_status, confession, cross_border_tariff, daily_return_germany, daily_return_liechtenstein, daily_return_reasonable, date_of_birth, discard_inapplicable_answers, first_name, first_working_day, has_children, holds_c_permit, insurance_start_date, last_name, liechtenstein_no_source_tax, nationality, non_return_days_45, non_return_days_60, pension_fund_canton, pension_fund_civil_status, permit_reminder, questionnaire_flow, read_only_after_submission, residence_canton, residence_certificate, spouse_date_of_birth, spouse_gainful_employment, spouse_holds_c_permit, spouse_nationality, spouse_residence_country, subject_to_source_tax, tariff_code, tariff_letter

## Errors (14)

- [lint] `rule.tariff_code` expression: construct BinOp not allowed in 'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))'
- [examples] `AC-06.7.3 / Employee answers no` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'A0N'
- [examples] `AC-06.6.1 / Calculator case C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-d75286)` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'C1Y'
- [examples] `AC-06.6.1 / Calculator case N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3)` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'N1Y'
- [examples] `AC-06.6.1 / Cross-border commuter L0Y (example from D-001)` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'L0Y'
- [examples] `AC-06.6.1 / Calculator case H1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-300c72)` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'H1Y'
- [examples] `AC-06.6.1 / Calculator case A0N, other country (zh_source_tax_calculator/F-zh_source_tax_calculator-f86c6b)` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'A0N'
- [examples] `AC-06.6.1 / Calculator case B0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a)` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'B0Y'
- [examples] `AC-06.6.2 / Maria (hr_transcript/F-hr_transcript-845204): Portuguese, C permit` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'no tariff code'
- [examples] `AC-06.6.2 / Tomás (hr_transcript/F-hr_transcript-b90bd9): Swiss wife, living in Winterthur` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'no tariff code'
- [examples] `AC-06.6.2 / Swiss national living in Switzerland` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'no tariff code'
- [examples] `AC-06.6.3 / Liechtenstein resident who returns daily` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'in principle no source tax liability, subject to the double taxation agreement'
- [examples] `AC-06.6.3 / Liechtenstein resident, at most 45 non-return days` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'in principle no source tax liability, subject to the double taxation agreement'
- [examples] `AC-06.6.3 / Liechtenstein resident, more than 45 non-return days` tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'C0Y'

## Examples executed against the knowledge model (257/270 pass)

- ✅ AC-01.1.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.1.1 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.1.1 / Stefan, Swiss living abroad, country assumed Germany (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-01.1.1 / Swiss employee living in Switzerland (spec)
- ✅ AC-01.1.1 / Non-Swiss, no C permit, single, living in Switzerland (spec)
- ✅ AC-01.1.1 / Non-Swiss in a registered partnership with a non-Swiss partner without C permit (spec)
- ✅ AC-01.1.2 / Married, living in Germany (spec)
- ✅ AC-01.1.2 / Separated, living in Germany (spec)
- ✅ AC-01.1.3 / Liechtenstein, daily return (spec)
- ✅ AC-01.1.3 / Liechtenstein, no daily return, at most 45 days (spec)
- ✅ AC-01.1.3 / Liechtenstein, no daily return, more than 45 days (spec)
- ✅ AC-01.2.2 / Any employee (spec)
- ✅ AC-01.2.3 / Living in Switzerland (spec)
- ✅ AC-01.2.3 / Stefan, Swiss living abroad, country assumed Germany (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-01.2.4 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.2.4 / Swiss employee living in Switzerland (spec)
- ✅ AC-01.2.4 / Stateless employee living in Switzerland (spec)
- ✅ AC-01.2.4 / Stefan, Swiss living abroad, country assumed Germany (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-01.2.5 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.2.5 / Married C-permit holder (spec)
- ✅ AC-01.2.5 / Non-Swiss spouse without C permit (spec)
- ✅ AC-01.2.5 / Married, living in Germany (spec)
- ✅ AC-01.2.5 / Divorced (spec)
- ✅ AC-01.2.5 / Separated Swiss employee (spec)
- ✅ AC-01.2.6 / Living in Germany (spec)
- ✅ AC-01.2.6 / Living in Liechtenstein (spec)
- ✅ AC-01.2.6 / Living in France (spec)
- ✅ AC-01.2.6 / Living in Switzerland (spec)
- ✅ AC-01.2.7 / Subject, living in Germany (spec)
- ✅ AC-01.2.7 / Swiss employee in Switzerland (spec)
- ✅ AC-01.3.1 / Civil status asked once for everyone (spec)
- ✅ AC-01.4.1 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.4.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.4.1 / Stefan, Swiss living abroad, country assumed Germany (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-01.4.1 / Swiss employee living in Switzerland (spec)
- ✅ AC-01.5.2 / Moved the home address from Germany to Switzerland before submitting; Germany cross-border and source tax answers are discarded (spec)
- ✅ AC-01.5.2 / Changed civil status from Married to Divorced before submitting; spouse date of birth is discarded (spec)
- ✅ AC-01.6.2 / Tomás (hr_transcript/F-hr_transcript-b90bd9) as submitted (spec)
- ✅ AC-01.6.2 / Tomás after HR records that his wife no longer lives in Switzerland (spec)
- ✅ AC-02.1.1 / Any employee: name required (spec)
- ✅ AC-02.1.1 / Employee living abroad: name required too (spec)
- ✅ AC-02.1.2 / Any employee: date of birth required (spec)
- ✅ AC-02.2.1 / Employee living in Switzerland (spec)
- ✅ AC-02.2.1 / Employee living in Germany (spec)
- ✅ AC-02.2.2 / House number required for any employee (spec)
- ✅ AC-02.3.1 / Country required for every employee (spec)
- ✅ AC-02.3.2 / Stefan, Swiss, living abroad (hr_transcript/F-hr_transcript-3f2c2a; country assumed) (spec)
- ✅ AC-02.3.2 / Employee living in Liechtenstein (spec)
- ✅ AC-02.3.2 / Employee living in France (spec)
- ✅ AC-02.3.3 / Employee living in Switzerland (spec)
- ✅ AC-02.4.1 / Living in Switzerland, canton Bern (spec)
- ✅ AC-02.4.1 / Living in Switzerland, canton Zurich (spec)
- ✅ AC-02.4.2 / Living in Germany (spec)
- ✅ AC-02.4.2 / Living in Liechtenstein (spec)
- ✅ AC-03.1.1 / Any new employee (spec)
- ✅ AC-03.2.2 / Start on the 1st of a month (spec)
- ✅ AC-03.2.2 / Contractual start on a Saturday and Swiss National Day (spec)
- ✅ AC-03.2.3 / Julia (hr_transcript/F-hr_transcript-e18e66), start moved to 15 March (year assumed) (spec)
- ✅ AC-03.2.3 / Start on the 2nd of a month (spec)
- ✅ AC-03.2.3 / Start at the end of the year (spec)
- ✅ AC-03.3.1 / Julia (hr_transcript/F-hr_transcript-e18e66): start moved to 15 March, from an originally agreed 01.03.2026 (original date and year assumed) (spec)
- ✅ AC-03.3.1 / Start moved one week earlier, from 08.06.2026 to 01.06.2026 after negotiating an earlier exit (spec)
- ✅ AC-04.1.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-04.1.1 / Single employee living in Switzerland (spec)
- ✅ AC-04.1.1 / Married employee living in Germany (spec)
- ✅ AC-04.2.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-04.2.1 / Married employee (spec)
- ✅ AC-04.2.1 / Separated employee (spec)
- ✅ AC-04.2.1 / Single employee (spec)
- ✅ AC-04.2.1 / Divorced employee (spec)
- ✅ AC-04.2.1 / Widowed employee (spec)
- ✅ AC-04.3.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-04.3.1 / Married (spec)
- ✅ AC-04.3.1 / Single (spec)
- ✅ AC-04.3.1 / Divorced (spec)
- ✅ AC-04.3.1 / Widowed (spec)
- ✅ AC-04.3.1 / Separated (spec)
- ✅ AC-04.4.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-04.4.1 / Separated (spec)
- ✅ AC-04.4.1 / Single (spec)
- ✅ AC-04.4.1 / Married (spec)
- ✅ AC-04.4.1 / Divorced (spec)
- ✅ AC-04.4.1 / Widowed (spec)
- ✅ AC-05.1.1 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.1.1 / Stefan, Swiss citizen living abroad (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.1.1 / Employee living in Liechtenstein (spec)
- ✅ AC-05.1.3 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.1.3 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.1.3 / Swiss national living in Switzerland (spec)
- ✅ AC-05.1.3 / Stateless employee living in Switzerland (spec)
- ✅ AC-05.1.3 / Employee living in Germany (spec)
- ✅ AC-05.2.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.1 / Registered partner without C permit (spec)
- ✅ AC-05.2.1 / Separated employee without C permit (spec)
- ✅ AC-05.2.1 / Divorced employee without C permit (spec)
- ✅ AC-05.2.1 / Married employee with C permit (spec)
- ✅ AC-05.2.1 / Married Swiss national living in Switzerland (spec)
- ✅ AC-05.2.1 / Married employee living in Germany (spec)
- ✅ AC-05.2.2 / Tomás, Swiss wife (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.2 / Spouse from Italy (spec)
- ✅ AC-05.2.3 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.3 / Spouse with C permit (spec)
- ✅ AC-05.2.3 / Spouse without C permit (spec)
- ✅ AC-05.3.1 / Employee living in Konstanz (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.3.1 / Stefan, Swiss citizen living abroad (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.3.1 / Employee living in France (spec)
- ✅ AC-05.3.2 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.3.2 / Swiss national living in Switzerland (spec)
- ✅ AC-05.3.3 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.3.3 / Registered partner of a C-permit holder living in Switzerland (spec)
- ✅ AC-05.3.3 / Swiss spouse not living in Switzerland (spec)
- ✅ AC-05.3.3 / Spouse neither Swiss nor C-permit holder (spec)
- ✅ AC-05.3.4 / Single employee (spec)
- ✅ AC-05.3.4 / Separated employee (spec)
- ✅ AC-05.3.4 / Divorced employee (spec)
- ✅ AC-05.3.4 / Widowed employee (spec)
- ✅ AC-05.4.1 / Employee living in Konstanz (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.4.1 / Employee living in Switzerland (spec)
- ✅ AC-05.4.1 / Employee living in Liechtenstein (spec)
- ✅ AC-05.4.1 / Employee living in France (spec)
- ✅ AC-08.1.1 / Calculator: main residence in Switzerland (zh_source_tax_calculator/F-aedb40) (spec)
- ✅ AC-08.1.1 / Calculator option Deutschland (zh_source_tax_calculator/F-d62dd4) (spec)
- ✅ AC-08.1.1 / Calculator option Liechtenstein (zh_source_tax_calculator/F-d62dd4) (spec)
- ✅ AC-08.1.1 / Employee living in France (spec)
- ✅ AC-08.1.1 / Employee living in Austria (spec)
- ✅ AC-08.1.2 / Living in Switzerland (spec)
- ✅ AC-08.1.2 / Calculator: 'Anderes Land' gives the base tariff (zh_source_tax_calculator/F-f86c6b) (spec)
- ✅ AC-08.1.3 / Calculator: Germany shows the daily return question (zh_source_tax_calculator/F-31d762) (spec)
- ✅ AC-08.1.3 / Calculator: Liechtenstein shows the daily return question (zh_source_tax_calculator/F-e22d17) (spec)
- ✅ AC-08.2.1 / Living in Germany (spec)
- ✅ AC-08.2.1 / Living in Liechtenstein (spec)
- ✅ AC-08.2.2 / Calculator: certificate question after daily return 'Ja' (zh_source_tax_calculator/F-5f6820) (spec)
- ✅ AC-08.2.2 / No daily return - no certificate question (spec)
- ✅ AC-08.2.3 / Calculator: daily return and certificate gives N1Y (zh_source_tax_calculator/F-993db3) (spec)
- ✅ AC-08.2.3 / Calculator: daily return without certificate gives C1Y (zh_source_tax_calculator/F-993db3) (spec)
- ✅ AC-08.2.3 / New hire without certificate yet (spec)
- ✅ AC-08.2.4 / Calculator: 'Anderes Land' gives the base tariff (zh_source_tax_calculator/F-f86c6b) (spec)
- ✅ AC-08.2.4 / Living in Switzerland (spec)
- ✅ AC-08.2.4 / Calculator: Liechtenstein over 45 days gives the normal tariff (zh_source_tax_calculator/F-cc19c7) (spec)
- ✅ AC-08.3.1 / Calculator: asked after daily return 'Nein' (zh_source_tax_calculator/F-aaece6) (spec)
- ✅ AC-08.3.1 / Daily return - not asked (spec)
- ✅ AC-08.3.2 / Calculator: asked after reasonable 'Ja' (zh_source_tax_calculator/F-33ef31) (spec)
- ✅ AC-08.3.2 / Return not reasonable - not asked (spec)
- ✅ AC-08.3.3 / Calculator: not reasonable gives C1Y (zh_source_tax_calculator/F-c8aa5e) (spec)
- ✅ AC-08.3.3 / Calculator: reasonable and more than 60 days gives C1Y (zh_source_tax_calculator/F-c8aa5e) (spec)
- ✅ AC-08.3.3 / Calculator: reasonable and not more than 60 days gives N1Y (zh_source_tax_calculator/F-c8aa5e) (spec)
- ✅ AC-08.4.1 / Calculator: Liechtenstein shows the daily return question (zh_source_tax_calculator/F-e22d17) (spec)
- ✅ AC-08.4.1 / Living in Germany (spec)
- ✅ AC-08.4.2 / Calculator: asked after daily return 'Nein' (zh_source_tax_calculator/F-f4ece9) (spec)
- ✅ AC-08.4.2 / Daily return - not asked (spec)
- ✅ AC-08.4.3 / Calculator: daily return 'Ja' (zh_source_tax_calculator/F-fb87f1) (spec)
- ✅ AC-08.4.3 / Calculator: not more than 45 days (zh_source_tax_calculator/F-fb87f1) (spec)
- ✅ AC-08.4.4 / Calculator: more than 45 days gives C1Y with DTA note (zh_source_tax_calculator/F-cc19c7) (spec)
- ✅ AC-08.4.4 / Living in Germany - Liechtenstein rule does not apply (spec)
- ✅ AC-06.2.1 / Maria (hr_transcript/F-hr_transcript-845204): Portuguese, C permit (spec)
- ✅ AC-06.2.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9): Brazilian, B permit, Swiss wife, lives in Winterthur (spec)
- ✅ AC-06.2.1 / Swiss national living in Switzerland (spec)
- ✅ AC-06.2.1 / Non-Swiss without C permit living in Switzerland (spec)
- ✅ AC-06.2.1 / Employee living in France (abroad) (spec)
- ✅ AC-06.2.1 / Liechtenstein resident who returns daily (spec)
- ✅ AC-06.2.1 / Liechtenstein resident, no daily return, at most 45 non-return days (spec)
- ✅ AC-06.2.1 / Liechtenstein resident, no daily return, more than 45 non-return days (spec)
- ✅ AC-06.2.3 / Calculator case A0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-2eab9a) (spec)
- ✅ AC-06.2.3 / Calculator case A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-2eab9a) (spec)
- ✅ AC-06.3.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9): married, not subject (spouse exemption) (spec)
- ✅ AC-06.3.1 / Married, subject to source tax, non-Swiss spouse without C permit (spec)
- ✅ AC-06.3.1 / Registered partner living abroad (cf. Daniel, hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-06.3.1 / Separated employee subject to source tax (spec)
- ✅ AC-06.3.1 / Divorced employee subject to source tax (spec)
- ✅ AC-06.3.1 / Widowed employee subject to source tax (spec)
- ✅ AC-06.3.1 / Married Liechtenstein resident who returns daily (spec)
- ✅ AC-06.3.1 / Married Liechtenstein resident with more than 45 non-return days (spec)
- ✅ AC-06.7.1 / Maria (hr_transcript/F-hr_transcript-845204): C permit, not subject (spec)
- ✅ AC-06.7.1 / Single employee living abroad (spec)
- ✅ AC-06.7.1 / Married employee subject to source tax (spec)
- ✅ AC-06.7.1 / Liechtenstein resident with at most 45 non-return days (spec)
- ✅ AC-06.7.1 / Liechtenstein resident with more than 45 non-return days (spec)
- ❌ AC-06.7.3 / Employee answers no (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'A0N'
- ✅ AC-06.7.3 / Employee answers yes (spec)
- ✅ AC-06.4.1 / Calculator case C0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-06.4.1 / Calculator case B0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-06.4.1 / Registered partner with a working partner (cf. Daniel, hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-06.4.2 / Calculator case A0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-037b1c) (spec)
- ✅ AC-06.4.2 / Calculator case H1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-300c72): minor child in household, sole custody (spec)
- ✅ AC-06.4.2 / Calculator case A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-5686d7): other parent is main contributor (spec)
- ✅ AC-06.4.2 / Separated employee without children (spec)
- ✅ AC-06.4.2 / Divorced employee, minor child in household with sole custody (spec)
- ✅ AC-06.4.3 / Calculator case A0N, other country (zh_source_tax_calculator/F-zh_source_tax_calculator-f86c6b) (spec)
- ✅ AC-06.5.1 / Calculator case C1Y, daily return without certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-06.5.1 / Certificate of residence 'not yet' (spec)
- ✅ AC-06.5.1 / Calculator case C1Y, daily return not reasonable (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-06.5.1 / Calculator case C1Y, more than 60 non-return days (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-06.5.1 / Liechtenstein resident with more than 45 non-return days (spec)
- ✅ AC-06.5.2 / Calculator case N1Y, daily return with certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-06.5.2 / Calculator case N1Y, reasonable return, at most 60 days (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-06.5.2 / Single cross-border commuter: A becomes L (spec)
- ✅ AC-06.5.2 / Married, spouse not working: B becomes M (spec)
- ✅ AC-06.5.2 / Single parent: H becomes P (spec)
- ❌ AC-06.6.1 / Calculator case C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-d75286) (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'C1Y'
- ❌ AC-06.6.1 / Calculator case N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'N1Y'
- ❌ AC-06.6.1 / Cross-border commuter L0Y (example from D-001) (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'L0Y'
- ❌ AC-06.6.1 / Calculator case H1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-300c72) (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'H1Y'
- ❌ AC-06.6.1 / Calculator case A0N, other country (zh_source_tax_calculator/F-zh_source_tax_calculator-f86c6b) (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'A0N'
- ❌ AC-06.6.1 / Calculator case B0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'B0Y'
- ❌ AC-06.6.2 / Maria (hr_transcript/F-hr_transcript-845204): Portuguese, C permit (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'no tariff code'
- ❌ AC-06.6.2 / Tomás (hr_transcript/F-hr_transcript-b90bd9): Swiss wife, living in Winterthur (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'no tariff code'
- ❌ AC-06.6.2 / Swiss national living in Switzerland (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'no tariff code'
- ❌ AC-06.6.3 / Liechtenstein resident who returns daily (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'in principle no source tax liability, subject to the double taxation agreement'
- ❌ AC-06.6.3 / Liechtenstein resident, at most 45 non-return days (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'in principle no source tax liability, subject to the double taxation agreement'
- ❌ AC-06.6.3 / Liechtenstein resident, more than 45 non-return days (spec): tariff_code = 'ERROR: construct BinOp not allowed in \'if_else(not subject_to_source_tax, "no tariff code", if_else(liechtenstein_no_source_tax, "in principle no source tax liability, subject to the double taxation agreement", tariff_letter + child_count + church_tax_suffix))\'', expected 'C0Y'
- ✅ AC-07.1.1 / Employee living in Germany with children (spec)
- ✅ AC-07.1.1 / Employee living in Germany without children (spec)
- ✅ AC-07.1.1 / Swiss employee living in Switzerland (spec)
- ✅ AC-07.1.1 / Maria, Portuguese with C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-07.1.1 / Tomás, Brazilian married to a Swiss wife in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-07.1.1 / Liechtenstein resident returning daily (spec)
- ✅ AC-07.1.1 / Liechtenstein resident with more than 45 non-return days and children (spec)
- ✅ AC-07.2.2 / Minor child (spec)
- ✅ AC-07.2.2 / Adult child in first education (spec)
- ✅ AC-07.2.3 / Calculator run B0N, married, child 'weder noch' (zh_source_tax_calculator/F-zh_source_tax_calculator-abe889) (spec)
- ✅ AC-07.2.3 / Single employee, child neither minor nor in first education (spec)
- ✅ AC-07.3.1 / Sole custody ends the questions (spec)
- ✅ AC-07.3.1 / Married, shared custody, common household: no contributor question (spec)
- ✅ AC-07.3.1 / Single, shared custody, common household: contributor asked (spec)
- ✅ AC-07.3.1 / No common household, alternating custody (spec)
- ✅ AC-07.3.1 / No common household, no alternating custody (spec)
- ✅ AC-07.3.2 / Calculator run C1Y, married, sole custody (zh_source_tax_calculator/F-zh_source_tax_calculator-d75286) (spec)
- ✅ AC-07.3.2 / Calculator run C1Y, married, shared custody, common household (zh_source_tax_calculator/F-zh_source_tax_calculator-5d8fb0) (spec)
- ✅ AC-07.3.2 / Calculator run C0Y, married, no alternating custody (zh_source_tax_calculator/F-zh_source_tax_calculator-a4d358) (spec)
- ✅ AC-07.3.2 / Calculator run C0Y, married, alternating custody, other parent contributes more (zh_source_tax_calculator/F-zh_source_tax_calculator-a4d358) (spec)
- ✅ AC-07.3.2 / Married, alternating custody, employee contributes more (inferred, go-live check) (spec)
- ✅ AC-07.3.3 / Calculator run H1Y, single, sole custody (zh_source_tax_calculator/F-zh_source_tax_calculator-300c72) (spec)
- ✅ AC-07.3.3 / Single, common household, employee contributes more (spec)
- ✅ AC-07.3.3 / Calculator run A0N, single, common household, other parent contributes more (zh_source_tax_calculator/F-zh_source_tax_calculator-5686d7) (spec)
- ✅ AC-07.3.3 / Calculator run H1N, single, no common household, no alternating custody (zh_source_tax_calculator/F-zh_source_tax_calculator-dc0ae9) (spec)
- ✅ AC-07.3.3 / Single, alternating custody, employee contributes more (spec)
- ✅ AC-07.3.3 / Single, alternating custody, other parent contributes more (inferred, go-live check) (spec)
- ✅ AC-07.3.4 / Registered partner, sole custody (spec)
- ✅ AC-07.3.4 / Separated, sole custody (spec)
- ✅ AC-07.4.1 / Married: shared custody asked (spec)
- ✅ AC-07.4.1 / Separated: parental care asked (spec)
- ✅ AC-07.4.1 / Married, no shared custody: block ends (spec)
- ✅ AC-07.4.1 / Single, parental care and alternating custody (spec)
- ✅ AC-07.4.2 / Calculator run B1N, married, shared custody, alternating, employee contributes more (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.2 / Married, alternating, other parent contributes more (inferred, go-live check) (spec)
- ✅ AC-07.4.2 / Married, shared custody, no alternating custody (inferred, go-live check) (spec)
- ✅ AC-07.4.2 / Calculator run B0N, married, no shared custody (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.2 / Calculator run H1N, single, parental care, alternating, employee contributes more (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.2 / Single, alternating, other parent contributes more (inferred, go-live check) (spec)
- ✅ AC-07.4.2 / Divorced, parental care, no alternating custody (inferred, go-live check) (spec)
- ✅ AC-07.4.2 / Calculator run A0N, single, no parental care (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.5.1 / Married, child in household with common household (spec)
- ✅ AC-07.5.1 / Single, child in household with common household (spec)
- ✅ AC-07.5.1 / Child in household without common household (spec)
- ✅ AC-07.5.1 / Child outside the household (spec)
- ✅ AC-07.5.2 / Calculator run B1N, married, child in household with common household (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.2 / Married, in household, no common household, more than 50% (inferred, go-live check) (spec)
- ✅ AC-07.5.2 / Married, in household, no common household, not more than 50% (inferred, go-live check) (spec)
- ✅ AC-07.5.2 / Registered partner, child outside household, more than 50% (inferred, go-live check) (spec)
- ✅ AC-07.5.2 / Calculator run B0N, married, child outside household, not more than 50% (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.3 / Single, common household, employee contributes more (spec)
- ✅ AC-07.5.3 / Single, common household, other parent contributes more (inferred, go-live check) (spec)
- ✅ AC-07.5.3 / Calculator run H1N, single, in household, no common household, more than 50% (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.3 / Separated, in household, no common household, not more than 50% (inferred, go-live check) (spec)
- ✅ AC-07.5.3 / Calculator run A1N, single, child outside household, more than 50% (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.3 / Divorced, child outside household, not more than 50% (inferred, go-live check) (spec)
- ✅ AC-07.6.1 / Counted child adds one (married, sole custody) (spec)
- ✅ AC-07.6.1 / Child counted with H adds one (single, sole custody) (spec)
- ✅ AC-07.6.1 / Child neither minor nor in first education adds nothing (spec)
- ✅ AC-07.6.1 / Child not counted adds nothing (married, no shared custody) (spec)

## Open questions (need your decision)

- **OQ-calculator-coverage**: Does Lonio's computed tariff code match the Zurich calculator on the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N, and the per-child rows marked inferred)? → recommended: Domain expert check before go-live (go-live condition, not blocking the spec).
- **OQ-fund-divorced-widowed**: Does the pension fund form show any extra field (e.g. a former spouse's date of birth) when civil status is Divorced or Widowed? → recommended: Ask the fund or HR to check the portal; proceed with D-004.

## Inferred items to confirm

- item.spouse_nationality
- rule.church_tax_suffix
- rule.child_result
- rule.base_tariff_letter
- story.US-01.8
- story.US-02.1
- story.US-03.3
- story.US-05.2
- story.US-06.2
- story.US-06.3
- story.US-06.7
- story.US-06.4
- story.US-07.3
- story.US-07.4
- story.US-07.5
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

## Dev refinement questions (7)

- [major] `stories/US-06.6-compute-and-record-the-full-source-tax-tariff-code.md` Every example in AC-06.6.1, AC-06.6.2 and AC-06.6.3 is marked ❌ under 'Checked', while all other stories show ✅. Are these expected tariff codes (N1Y, C1Y, L0Y, A0N, B0N, 'no tariff code', C1Y with the double taxation agreement note) known to be wrong, or just not checked yet? They are the main acceptance tests for the computed code.
- [major] `stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md` AC-01.6.2 contradicts AC-01.6.3. In the example, after HR records that Tomás's wife no longer lives in Switzerland, the expected result for Denomination is 'asked'. But the employee can no longer answer anything after submission (AC-01.6.1), and AC-01.6.3 / D-048 say the tariff code should then show 'incomplete - HR must complete'. Which is the expected outcome for this example: is the employee asked again (the questionnaire reopens for them), or does HR complete it while the result shows 'incomplete'?
- [minor] `stories/US-06.7-ask-employees-subject-to-source-tax-whether-they-have.md` In AC-06.7.3 the example 'Employee answers no' (France, Single, None or other, no children → A0N) is marked ❌, while the 'yes' example is ✅. Is A0N the wrong expected code for this case, or has it simply not been checked yet?
- [minor] `stories/US-03.1-employee-confirms-the-first-working-day.md` The first working day 'must lie within one year after the questionnaire is sent'. Can it also be before the send date or in the past, for example when the employee has already started or fills in the questionnaire late? Sending the questionnaire is part of the later HR-side spec, so which date counts as 'sent' for this check? Is there also any plausibility check on the spouse's date of birth?
- [minor] `stories/US-01.8-review-a-summary-and-submit-with-one-confirmation.md` The stories disagree on when a missing required answer blocks the employee. US-02.1 and US-02.2 say the employee 'cannot continue' to the next step. US-04.1 and AC-01.8.3 say the employee only cannot submit, and is then shown what is missing. Should a missing required answer stop the employee from moving to the next step, or only from submitting (so a partly filled step can be saved and left, as US-01.7 allows)?
- [minor] `stories/US-08.2-germany-daily-return-and-certificate-of-residence.md` The item is called 'Certificate of residence handed in', and the calculator asks whether it has been provided ('beigebracht'). The story instead asks whether the employee 'has a certificate of residence for HR'. Does 'yes' mean the certificate has already been given to HR, or only that the employee has one? Should HR expect a certificate later for 'no' as well as for 'not yet', or only for 'not yet'?
- [minor] `stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md` Expected results for the same question differ between stories. US-01.2 marks spouse's nationality, spouse lives in Switzerland and nationality as 'asked' (AC-01.2.4, AC-01.2.5). US-05.1 and US-05.2 mark the same cases as 'required'. Several rows also show '–' for questions that always apply, for example civil status for the married C-permit holder in AC-01.2.5, or postcode and town for Stefan in AC-01.2.3. Is there a real difference between 'asked' and 'required' (can any of these answers be left empty?), and does '–' mean 'not checked in this example'?

## Technical vocabulary found in the spec (6)

- `item.address_country` implementation vocabulary ['iso 3166']: Country chosen from the ISO 3166 country list, by English name (e.g. Switzerland, Germany, Liechtenstein).
- `item.nationality` implementation vocabulary ['iso 3166']: Country chosen from the ISO 3166 country list, plus 'stateless'.
- `item.spouse_nationality` implementation vocabulary ['iso 3166']: Country chosen from the ISO 3166 country list, plus 'stateless'.
- `ac.AC-02.3.1` implementation vocabulary ['iso 3166']: the country is required and is chosen from the ISO 3166 country list, shown by English name (e.g. Switzerland, Germany, Liechtenstein). This
- `feature.md` "(The expression gives, per child, whether that child is counted; the digit is the number of children for which it is true.)" - Refers to an internal formula ('expression') rather than business language. D-045 forbids this.
- `information.md` "(The expression gives, per child, whether that child is counted; the digit is the number of children for which it is true.)" - Refers to an internal formula ('expression') rather than business language. D-045 forbids this.

## Coverage

156/342 source units cited; 139/177 facts used.

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
- hr_transcript/T-051: Okay, that's fine, the calculator will tell us. I think I have what I need. Is there anything you were hoping to cover that we didn't?
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
- zh_source_tax_calculator/C-Q01: Für welche Einkünfte möchten Sie den Quellensteuertarif ermitteln? Options: Erwerbseinkommen | Ersatzeinkünfte Help: Calculator heading: 'Quellensteuertarif bes
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

## Other warnings (40)

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
- [coverage] `F-hr_transcript-8595fb` fact not used anywhere in the spec: For employees living abroad, the calculator asks more questions, and Germany has its own forms. Anna cannot remember what they are called. Leo deferred to the calculator, so the exact questions are unresolved in this transcript.
- [coverage] `F-pension_portal-3a97ab` fact not used anywhere in the spec: The portal requires an insurance start date on the 1st of a month but does not show how it relates to the employee's first working day (e.g. which 1st of a month to choose when work starts mid-month); the derivation rule is unknown.
- [coverage] `F-pension_portal-e45e5b` fact not used anywhere in the spec: No screenshot shows the validation error for an insurance start date that is not the 1st of a month or for a malformed date; its behaviour and wording are unknown.
- [trace_judge] `item.first_working_day` partial: No cited fact says the first working day is the reference date for children's age (only the insurance start date and the address are backed by D-039/D-041/D-047).
- [trace_judge] `item.spouse_nationality` partial: The form 'ISO 3166 country list plus stateless' is cited only for the employee's nationality in D-050, not for the spouse's nationality.
- [trace_judge] `item.residence_certificate` partial: The HR purpose ('knows a certificate is still expected') is not stated in the cited facts; the rest, including 'not yet', is backed.
- [trace_judge] `item.daily_return_reasonable` partial: Question, options and condition are backed, but no cited fact says this answer decides the cross-border tariff.
- [trace_judge] `item.non_return_days_60` partial: No cited fact backs the purpose 'more than 60 days gives the normal tariff, otherwise cross-border'; the question, options, condition and expectation framing are backed.
- [trace_judge] `item.spouse_gainful_employment` partial: The cited facts back the question, Yes/No values, married/registered-partner condition and B/C tariff, but not the 'address_country != Liechtenstein or non_return_days_45 == yes' part of the condition.
- [trace_judge] `item.has_children` partial: The question and values are backed, but the cited facts do not support the Liechtenstein/non_return_days_45 part of the asked_when and required_when conditions.
- [trace_judge] `item.child_main_financial_contributor` partial: The purpose 'H tariff for single parents' is not backed by any cited fact.
- [trace_judge] `rule.questionnaire_flow` partial: The step list, ordering, saving/resume, back-and-change and single confirmation are backed, but the row details (German certificate of residence, permit reminder only for non-Swiss or living abroad, C permit only if not Swiss, spouse questions) rely on facts and decisions that are not among the cited ones.
- [trace_judge] `rule.pension_fund_civil_status` partial: D-003 gives the partner's date of birth only for registered partnership, but the statement attaches it to Separated (and Married) too, which no cited fact backs.
- [trace_judge] `rule.cross_border_tariff` partial: The 'not Germany' row cites F-zh_source_tax_calculator-cc19c7, which is not among the cited facts, and the cited facts do not show that Liechtenstein never gets the cross-border tariff (only Switzerland and 'Anderes Land' are covered).
- [trace_judge] `rule.tariff_code` partial: The expression gives no 'subject to the double taxation agreement' note or flag for the more-than-45-days case, and no 'incomplete' result, although the statement and table say so; rows also cite fb87f1 and cc19c7, which are not among the cited facts.
- [trace_judge] `story.US-01.2` partial: AC-01.2.7 limits 'spouse gainfully employed' to married and registered partners, which no cited fact states, and the non-illustrative Maria example in AC-01.2.4 rests on F-hr_transcript-845204, which is not cited.
- [trace_judge] `story.US-01.4` partial: The non-illustrative Maria example cites F-hr_transcript-845204, which is not among the cited facts, so her C-permit and Portugal details are unbacked.
- [trace_judge] `story.US-03.1` partial: AC-03.1.4 says HR 'plans the start and keeps the fund registration up to date', which no cited fact states (the facts only say the pension fund needs the first working day).
- [trace_judge] `story.US-08.1` partial: AC-08.1.2 lists 'reasonableness of daily return' and 'non-return days' questions, which no cited fact backs.
- [trace_judge] `story.US-08.2` partial: AC-08.2.4 says the cross-border tariff never applies to any non-Germany resident, but the cited facts only back this for Switzerland, other countries and Liechtenstein with over 45 non-return days, not for a Liechtenstein resident who returns daily.
- [trace_judge] `story.US-06.2` partial: The non-illustrative Maria and Tomás examples cite F-hr_transcript-845204 and -b90bd9, which are not among the cited facts. The claim that the denomination is not part of the pension fund registration is also not backed.
- [trace_judge] `story.US-06.3` partial: The non-illustrative Tomás example (spouse exemption) cites F-hr_transcript-b90bd9, which is not among the cited facts. Everything else is backed.
- [trace_judge] `story.US-06.7` partial: The non-illustrative Maria example cites F-hr_transcript-845204, which is not among the cited facts. Everything else is backed.
- [trace_judge] `story.US-06.5` partial: The claim that Liechtenstein residents never get a cross-border letter is not backed by the cited facts (the Liechtenstein fact is not cited), and the priority reason relies on F-hr_transcript-3f2c2a, which is not among the cited facts.
- [trace_judge] `story.US-06.6` partial: AC-06.6.2 names Swiss nationals as exempt, but no cited fact says so (only C-permit holders and Swiss/C-permit spouses are covered), and several example source_refs (d75286, 300c72, 97139a) are not among the cited facts.
- [dev_refinement] `stories/US-06.6-compute-and-record-the-full-source-tax-tariff-code.md` Every example in AC-06.6.1, AC-06.6.2 and AC-06.6.3 is marked ❌ under 'Checked', while all other stories show ✅. Are these expected tariff codes (N1Y, C1Y, L0Y, A0N, B0N, 'no tariff code', C1Y with the double taxation agreement note) known to be wrong, or just not checked yet? They are the main acceptance tests for the computed code.
- [dev_refinement] `stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md` AC-01.6.2 contradicts AC-01.6.3. In the example, after HR records that Tomás's wife no longer lives in Switzerland, the expected result for Denomination is 'asked'. But the employee can no longer answer anything after submission (AC-01.6.1), and AC-01.6.3 / D-048 say the tariff code should then show 'incomplete - HR must complete'. Which is the expected outcome for this example: is the employee asked again (the questionnaire reopens for them), or does HR complete it while the result shows 'incomplete'?

## Run

Stages run: knowledge.raw, feature.plan, sections/SEC-03-employment-start, sections/SEC-04-civil-status-spouse, sections/SEC-02-personal-details-address, sections/SEC-08-cross-border-residence, sections/SEC-05-source-tax-liability, sections/SEC-01-questionnaire-flow, sections/SEC-07-source-tax-children, sections/SEC-06-source-tax-tariff-basics, feature.flow, judge_trace, dev_refinement, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator, judge_facts

LLM cost this run: $9.8

Tokens this run: 1,146,463 in 30 agent calls (60 input, 52,108 cache read, 894,249 cache write, 200,046 output)
