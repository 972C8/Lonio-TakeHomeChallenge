# Review: employee-onboarding

**Verdict: NOT READY**

Two examples in AC-06.6.5 fail, and dev refinement raised two major questions about the 'incomplete - HR must complete' state. Technical wording also leaks into the spec (D-045). Several rules and items are only partly traced to cited sources. The calculator-coverage open question is non-blocking, but it needs sign-off before go-live.

## Reviewer findings

1. **AC-06.6.5 examples fail: the 'incomplete' case has no passing test** – After an HR change, the tariff code is specified as 'incomplete - HR must complete' (D-053). The computed code instead returns a partial value (A0 / N). The first example expects Denomination 'required', which contradicts D-053. The second never shows the unasked spouse-employment question. The incomplete-state behaviour is therefore untested and ambiguous.  
   Evidence: examples: AC-06.6.5 (both cases pass=false); dev_refinement US-06.6 (major)  
   Action: Decide in decisions.yaml that the tariff code is 'incomplete - HR must complete' whenever a required input was never asked. Then fix both example tables: show the unasked question as 'not asked' and expect 'incomplete'. Fix the rule expression so it returns 'incomplete' rather than a partial code.
2. **Scope of the 'incomplete' state is undefined for pension fund results** – The spec covers only the tariff code and 'subject to source tax'. It does not say what the fund canton, or the fund civil status Married without a spouse date of birth, show after an HR change that makes an unasked answer applicable. Engineering would have to guess.  
   Evidence: dev_refinement US-01.6 (major); items pension_fund_canton, pension_fund_civil_status  
   Action: Decide which derived results go 'incomplete' (for example canton and the spouse date of birth for the fund). Or decide that HR must enter the missing value, and state that in US-01.6.
3. **tariff_code rule contradicts its own statement** – The expression uses if_else(child_count,1,0), which yields only 0 or 1. The statement and the calculator facts require the number of counted children (for example C3Y). Codes for two or more children would be wrong.  
   Evidence: trace_judge rule.tariff_code; OQ-calculator-coverage (H3N/P3N, more than 3 children)  
   Action: Correct the expression to use the child count (or its capped value). Add examples for 2 and 3 children. Confirm the behaviour for more than 3 children with the domain expert.
4. **Technical wording leaks into the spec** – D-045 forbids internal-formula language in business text. ISO 3166 is implementation vocabulary, and 'free text is not accepted' dictates how the input behaves.  
   Evidence: tech_leak: feature.md and information.md ('internal expression'); US-02.3; item.address_country, nationality, spouse_nationality; AC-02.3.1, AC-05.1.2, AC-05.2.3  
   Action: Remove the 'internal expression' sentence. Say 'a list of countries (English names) plus stateless'. Drop the free-text prohibition and keep only 'the country is required'.
5. **Rules rely on facts and gating that no cited source backs** – Liechtenstein/non_return_days_45 gating, the tariff purposes, the 'cannot occur for onboarding' claim and several table rows are not backed by the cited facts. Some rows cite facts that are not in the rule's citation list. That weakens traceability and risks wrong rules.  
   Evidence: trace_judge: rule.questionnaire_flow, base_tariff_letter, cross_border_tariff, tariff_letter, calculator_residence, pension_fund_canton, liechtenstein_no_source_tax; items has_children, child_*, spouse_gainful_employment  
   Action: Add the missing citations (D-002, D-047, F-...3432a9, e22d17, f86c6b, 5af8d0). Where no source exists, mark the claim as inferred in decisions.yaml or remove it.
6. **Unconfirmed rule: at least one child block is required** – AC-07.2.1 requires at least one child block and every child question to be required. No source backs either. The behaviour when the last block is removed is undefined.  
   Evidence: trace_judge story.US-07.2; dev_refinement US-07.2  
   Action: Confirm with HR. Decide whether removing the last child block is blocked or sets 'has children' to no.
7. **Inconsistent expected values across example tables** – The same question is marked 'asked' in some stories and 'required' in others. '–' is used for inputs and for results with mismatched values, and Married/Single spouse date of birth differs from Divorced/Widowed. Testers cannot tell what to assert.  
   Evidence: dev_refinement US-01.2, US-01.1, US-04.4  
   Action: Define a single vocabulary (required / optional / not asked) and what '–' means. Align the tables to it and fix the US-04.4 rows.
8. **Conflicting rules on when a missing answer blocks the employee** – Some stories block leaving the step and others block only submission. US-01.7 allows saving a partly filled step.  
   Evidence: dev_refinement US-01.8 (US-02.1, US-02.2, US-03.1, US-04.1, AC-01.8.2)  
   Action: Decide that missing answers block only submission, not navigation. Align the stories and say how an incomplete step is shown.
9. **Tariff calculator coverage is unverified (non-blocking)** – Unexplored paths (A/B/H residence block, inferred per-child rows, more than 3 children, H3N/P3N) could produce wrong source tax codes. Some calculator facts are only partly verified (Q16 residence meaning, Q14, Q19, Q to the cross-border tariff).  
   Evidence: open_questions OQ-calculator-coverage; fact_judge F-zh_source_tax_calculator-037b1c, 64ac33, dc0ae9, c8aa5e, 2754e8; inferred_items  
   Action: Schedule the domain expert comparison against the Zurich calculator before go-live. Confirm the meaning of Q14, Q16 and Q19.
10. **Certificate-of-residence and start-date semantics unclear (minor)** – 'Provided' versus 'has' a certificate changes what HR expects. The first-working-day check has no defined 'sent' date, and past dates are not addressed. The insurance start date validation (the 1st of a month) has no source for its error behaviour.  
   Evidence: dev_refinement US-08.2, US-03.1; coverage F-pension_portal-e45e5b unused  
   Action: Decide: 'yes' means already given to HR. Define the reference date for the one-year window and whether past dates are allowed. State the start-date error wording as a product decision.

## Numbers

342 source units → 177 facts → 35 information items, 19 business rules → one feature with 8 sections, 40 stories, 120 acceptance criteria; 1 open questions, 11 exclusions.

## Impact of this run

Stories added: US-08.5; changed: US-01.1, US-01.2, US-01.3, US-01.4, US-01.5, US-01.6, US-01.7, US-01.8, US-02.1, US-02.2, US-02.3, US-02.4, US-03.1, US-03.2, US-03.3, US-04.1, US-04.2, US-04.3, US-04.4, US-05.1, US-05.2, US-05.3, US-05.4, US-06.2, US-06.3, US-06.4, US-06.5, US-06.6, US-06.7, US-07.1, US-07.2, US-07.3, US-07.4, US-07.5, US-07.6, US-08.1, US-08.2, US-08.3, US-08.4; removed: -; unchanged: 0.

Knowledge elements changed: OQ-calculator-coverage, OQ-fund-divorced-widowed, address_country, address_house_number, address_postcode, address_street, address_town, base_tariff_letter, calculator_civil_status, calculator_residence, child_age_status, child_alternating_custody, child_common_household_other_parent, child_count, child_custody, child_main_financial_contributor, child_maintenance_over_50, child_parental_care, child_result, child_same_household, child_shared_custody, church_tax_suffix, civil_status, confession, cross_border_tariff, daily_return_germany, daily_return_liechtenstein, daily_return_reasonable, date_of_birth, discard_inapplicable_answers, dta_reservation_note, first_name, first_working_day, has_children, holds_c_permit, insurance_start_date, last_name, liechtenstein_no_source_tax, nationality, non_return_days_45, non_return_days_60, pension_fund_canton, pension_fund_civil_status, permit_reminder, questionnaire_flow, read_only_after_submission, residence_canton, residence_certificate, spouse_date_of_birth, spouse_gainful_employment, spouse_holds_c_permit, spouse_nationality, spouse_residence_country, subject_to_source_tax, tariff_code, tariff_letter

## Errors (2)

- [examples] `AC-06.6.5 / HR changed the address to France; denomination never asked` tariff_code = ['A', 0, None], expected 'incomplete - HR must complete'
- [examples] `AC-06.6.5 / HR changed the civil status to Married; spouse employment never asked` tariff_code = [None, 0, 'N'], expected 'incomplete - HR must complete'

## Examples executed against the knowledge model (266/268 pass)

- ✅ AC-01.1.1 / Maria, Portuguese with a C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.1.1 / Tomás, Brazilian with a B permit, Swiss wife, living in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.1.1 / Swiss citizen living abroad like Stefan (hr_transcript/F-hr_transcript-3f2c2a); country of residence assumed to be Germany (spec)
- ✅ AC-01.1.1 / Non-Swiss single employee without C permit living in Switzerland (spec)
- ✅ AC-01.1.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-01.1.2 / Liechtenstein resident who returns daily (spec)
- ✅ AC-01.1.2 / Liechtenstein resident, no daily return, at most 45 non-return days (spec)
- ✅ AC-01.1.2 / Liechtenstein resident, more than 45 non-return days (spec)
- ✅ AC-01.2.2 / Employee living in Switzerland (spec)
- ✅ AC-01.2.2 / Employee living in Germany (spec)
- ✅ AC-01.2.3 / Maria, Portuguese with a C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.2.3 / Swiss citizen living in Switzerland (spec)
- ✅ AC-01.2.3 / Employee living in Liechtenstein (spec)
- ✅ AC-01.2.4 / Tomás, Brazilian with a B permit, Swiss wife (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.2.4 / Married employee living in Germany (spec)
- ✅ AC-01.2.4 / Separated non-Swiss employee without C permit in Switzerland (spec)
- ✅ AC-01.2.4 / Widowed employee (spec)
- ✅ AC-01.2.5 / Liechtenstein resident without daily return (spec)
- ✅ AC-01.2.5 / Germany resident (spec)
- ✅ AC-01.2.5 / Switzerland resident (spec)
- ✅ AC-01.2.6 / Married employee living in Germany (spec)
- ✅ AC-01.2.6 / Single employee living in Germany (spec)
- ✅ AC-01.2.6 / Swiss citizen living in Switzerland (spec)
- ✅ AC-01.3.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-01.3.2 / Swiss citizen living abroad like Stefan (hr_transcript/F-hr_transcript-3f2c2a); country of residence assumed to be Germany (spec)
- ✅ AC-01.4.1 / Maria, Portuguese with a C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.4.1 / Tomás, Brazilian with a B permit (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.4.1 / Swiss citizen living abroad like Stefan (hr_transcript/F-hr_transcript-3f2c2a); country of residence assumed to be Germany (spec)
- ✅ AC-01.4.1 / Employee living in Liechtenstein (spec)
- ✅ AC-01.4.1 / Stateless employee living in Switzerland (spec)
- ✅ AC-01.4.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-01.5.2 / Employee first answered Married, then changed to Single (spec)
- ✅ AC-01.5.2 / Employee first entered Germany, then changed the home address to Switzerland (spec)
- ✅ AC-02.1.1 / Employee living in Switzerland (spec)
- ✅ AC-02.1.1 / Employee living abroad (spec)
- ✅ AC-02.2.1 / Address in Switzerland (spec)
- ✅ AC-02.2.1 / Address in Germany (cross-border commuter) (spec)
- ✅ AC-02.2.2 / Farmhouse without house number (spec)
- ✅ AC-02.3.3 / Lives in Switzerland (spec)
- ✅ AC-02.3.3 / Lives in Germany (spec)
- ✅ AC-02.3.3 / Lives in Liechtenstein (spec)
- ✅ AC-02.3.4 / Living abroad is enough for source tax (spec)
- ✅ AC-02.4.1 / Lives in Switzerland (spec)
- ✅ AC-02.4.1 / Lives in Germany (spec)
- ✅ AC-02.4.3 / Lives in canton Bern (spec)
- ✅ AC-02.4.3 / Lives in canton Zurich (spec)
- ✅ AC-02.4.3 / Lives in Germany (spec)
- ✅ AC-02.4.3 / Lives in Liechtenstein (spec)
- ✅ AC-03.1.1 / Employee starting mid-month (spec)
- ✅ AC-03.1.1 / Employee starting on the 1st of a month (spec)
- ✅ AC-03.2.1 / Starts on the 1st of a month (spec)
- ✅ AC-03.2.1 / Contract starts on a Saturday and public holiday (1 August) (spec)
- ✅ AC-03.2.2 / Julia (hr_transcript/F-hr_transcript-30d25c), year assumed (spec)
- ✅ AC-03.2.2 / Starts on the 2nd of a month (spec)
- ✅ AC-03.2.2 / Starts on the last day of the year (spec)
- ✅ AC-03.3.1 / Julia (hr_transcript/F-hr_transcript-e18e66): start moved to 15 March, year assumed (spec)
- ✅ AC-03.3.1 / Start moved earlier to the 1st of a month (latest date shown) (spec)
- ✅ AC-03.3.2 / HR moves the start from 01.03 to 15.03 (latest date shown) (spec)
- ✅ AC-03.3.2 / HR moves the start from 20.04 to 01.04 (latest date shown) (spec)
- ✅ AC-04.1.1 / Daniel, registered partnership, living in Switzerland (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-04.1.1 / Employee living in Germany (spec)
- ✅ AC-04.1.1 / Employee living in Liechtenstein (spec)
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
- ✅ AC-04.4.1 / Married (spec)
- ✅ AC-04.4.1 / Single (spec)
- ✅ AC-04.4.1 / Divorced (spec)
- ✅ AC-04.4.1 / Widowed (spec)
- ✅ AC-05.1.1 / Maria, Portuguese living in Switzerland (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.1.1 / Employee living in Konstanz (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.1.1 / Employee living in Liechtenstein (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.1.1 / Employee living in France (spec)
- ✅ AC-05.1.3 / Maria, Portuguese, C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.1.3 / Tomás, Brazilian living in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.1.3 / Swiss citizen living in Switzerland (spec)
- ✅ AC-05.1.3 / Stateless employee living in Switzerland (spec)
- ✅ AC-05.1.3 / Employee living in Konstanz (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.1.5 / Employee changes the home address from Switzerland to Germany (spec)
- ✅ AC-05.2.1 / Tomás, Brazilian, B permit, married, Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.1 / Non-Swiss employee in a registered partnership (spec)
- ✅ AC-05.2.1 / Separated non-Swiss employee without C permit (spec)
- ✅ AC-05.2.1 / Divorced non-Swiss employee without C permit (spec)
- ✅ AC-05.2.1 / Married C-permit holder (spec)
- ✅ AC-05.2.1 / Married Swiss employee living in Switzerland (spec)
- ✅ AC-05.2.1 / Married employee living in Germany (spec)
- ✅ AC-05.2.2 / Tomás, wife is Swiss (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.2 / Married employee with an Italian spouse (spec)
- ✅ AC-05.2.2 / Registered partner who is stateless (spec)
- ✅ AC-05.3.1 / Stefan, Swiss citizen living abroad (hr_transcript/F-hr_transcript-3f2c2a; country assumed Germany) (spec)
- ✅ AC-05.3.1 / Employee living in Liechtenstein (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.3.1 / Employee living in France (spec)
- ✅ AC-05.3.2 / Maria, Portuguese, C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.3.2 / Swiss citizen living in Switzerland (spec)
- ✅ AC-05.3.3 / Single non-Swiss employee without C permit (spec)
- ✅ AC-05.3.3 / Separated non-Swiss employee without C permit (spec)
- ✅ AC-05.3.3 / Widowed stateless employee without C permit (spec)
- ✅ AC-05.3.4 / Tomás, Brazilian, B permit, Swiss wife, Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.3.4 / Spouse with C permit living in Switzerland (spec)
- ✅ AC-05.3.4 / Swiss registered partner living in Switzerland (spec)
- ✅ AC-05.3.4 / Spouse living in Switzerland, neither Swiss nor C permit (spec)
- ✅ AC-05.3.4 / Swiss spouse living outside Switzerland (spec)
- ✅ AC-05.3.4 / C-permit spouse living outside Switzerland (spec)
- ✅ AC-05.4.1 / Employee living in Switzerland (spec)
- ✅ AC-05.4.1 / Employee living in Konstanz (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.4.1 / Employee living in Liechtenstein (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.4.1 / Employee living in France (spec)
- ✅ AC-08.1.1 / Lives in Switzerland (spec)
- ✅ AC-08.1.1 / Lives in Germany (Konstanz, hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.1.1 / Lives in Liechtenstein (spec)
- ✅ AC-08.1.1 / Lives in France (spec)
- ✅ AC-08.1.2 / Lives in Germany (spec)
- ✅ AC-08.1.2 / Lives in Liechtenstein (spec)
- ✅ AC-08.1.2 / Lives in Switzerland (spec)
- ✅ AC-08.1.2 / Lives in France (spec)
- ✅ AC-08.2.1 / Lives in Germany (spec)
- ✅ AC-08.2.1 / Lives in Liechtenstein (spec)
- ✅ AC-08.2.2 / Germany, daily return (spec)
- ✅ AC-08.2.2 / Germany, no daily return (spec)
- ✅ AC-08.2.3 / Calculator example daily return + certificate -> N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-08.2.3 / Calculator example daily return, no certificate -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-08.2.3 / Certificate not yet available (spec)
- ✅ AC-08.3.1 / Germany, no daily return (spec)
- ✅ AC-08.3.1 / Germany, daily return (spec)
- ✅ AC-08.3.2 / Reasonable (spec)
- ✅ AC-08.3.2 / Not reasonable (spec)
- ✅ AC-08.3.3 / Calculator example reasonable, no >60 days -> N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-08.3.3 / Calculator example reasonable, >60 days -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-08.3.3 / Calculator example not reasonable -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-08.3.3 / Lives in France (spec)
- ✅ AC-08.4.1 / Liechtenstein, daily return (spec)
- ✅ AC-08.4.1 / Liechtenstein, no daily return (spec)
- ✅ AC-08.4.1 / Lives in Germany (spec)
- ✅ AC-08.4.2 / Calculator example daily return (zh_source_tax_calculator/F-zh_source_tax_calculator-fb87f1) (spec)
- ✅ AC-08.4.2 / Calculator example at most 45 days (zh_source_tax_calculator/F-zh_source_tax_calculator-fb87f1) (spec)
- ✅ AC-08.4.2 / Calculator example more than 45 days (zh_source_tax_calculator/F-zh_source_tax_calculator-cc19c7) (spec)
- ✅ AC-08.4.2 / Lives in Germany (spec)
- ✅ AC-08.5.1 / Calculator example more than 45 days -> C1Y / DTA reservation (zh_source_tax_calculator/F-zh_source_tax_calculator-cc19c7) (spec)
- ✅ AC-08.5.1 / Liechtenstein, daily return (spec)
- ✅ AC-08.5.1 / Liechtenstein, at most 45 days (spec)
- ✅ AC-08.5.1 / Lives in Germany (spec)
- ✅ AC-06.2.1 / Non-Swiss employee in Switzerland without a C permit (spec)
- ✅ AC-06.2.1 / Maria, Portuguese with a C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-06.2.1 / Tomás, Brazilian, Swiss wife, living in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-06.2.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-06.2.1 / Employee living in France (spec)
- ✅ AC-06.2.1 / Liechtenstein resident who returns daily (spec)
- ✅ AC-06.2.1 / Liechtenstein resident with at most 45 non-return days (spec)
- ✅ AC-06.2.1 / Liechtenstein resident with more than 45 non-return days (spec)
- ✅ AC-06.2.3 / Calculator A0Y case (zh_source_tax_calculator/F-zh_source_tax_calculator-2eab9a) (spec)
- ✅ AC-06.2.3 / Calculator A0N case (zh_source_tax_calculator/F-zh_source_tax_calculator-2eab9a) (spec)
- ✅ AC-06.3.1 / Married employee living in France (spec)
- ✅ AC-06.3.1 / Registered partner living in France (spec)
- ✅ AC-06.3.1 / Separated employee living in France (spec)
- ✅ AC-06.3.1 / Single employee in Switzerland without a C permit (spec)
- ✅ AC-06.3.1 / Married non-Swiss employee whose non-Swiss spouse without C permit lives in Switzerland (spec)
- ✅ AC-06.3.1 / Tomás, Brazilian, Swiss wife, living in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-06.3.1 / Married Liechtenstein resident who returns daily (spec)
- ✅ AC-06.7.1 / Single employee living in France (spec)
- ✅ AC-06.7.1 / Married employee living in France (spec)
- ✅ AC-06.7.1 / Germany resident who returns daily (spec)
- ✅ AC-06.7.1 / Maria, Portuguese with a C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-06.7.1 / Liechtenstein resident with at most 45 non-return days (spec)
- ✅ AC-06.7.1 / Liechtenstein resident with more than 45 non-return days (spec)
- ✅ AC-06.4.1 / Calculator C0Y case (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-06.4.1 / Calculator B0Y case (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-06.4.1 / Registered partner whose partner works (spec)
- ✅ AC-06.4.1 / Married, spouse not working, minor child in household with sole custody (spec)
- ✅ AC-06.4.2 / Calculator A0Y case (zh_source_tax_calculator/F-zh_source_tax_calculator-037b1c) (spec)
- ✅ AC-06.4.2 / Separated employee without children (spec)
- ✅ AC-06.4.2 / Widowed employee without children (spec)
- ✅ AC-06.4.2 / Calculator H1Y case: single with minor child in household, sole custody (zh_source_tax_calculator/F-zh_source_tax_calculator-300c72) (spec)
- ✅ AC-06.4.2 / Divorced with a child who is neither minor nor in first education (spec)
- ✅ AC-06.5.1 / Calculator N1Y case: daily return with certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-06.5.1 / Single, daily return with certificate (spec)
- ✅ AC-06.5.1 / Married, spouse not working, daily return with certificate (spec)
- ✅ AC-06.5.1 / Single with minor child in household, sole custody, daily return with certificate (spec)
- ✅ AC-06.5.1 / Calculator N1Y case: no daily return, reasonable, at most 60 days (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-06.5.2 / Calculator C1Y case: daily return without certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-06.5.2 / Daily return, certificate not yet available (spec)
- ✅ AC-06.5.2 / Calculator C1Y case: daily return not reasonable (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-06.5.2 / Calculator C1Y case: more than 60 non-return days (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-06.5.2 / Employee living in France (spec)
- ✅ AC-06.5.2 / Liechtenstein resident with more than 45 non-return days (spec)
- ✅ AC-06.6.1 / Calculator A0Y case (zh_source_tax_calculator/F-zh_source_tax_calculator-037b1c) (spec)
- ✅ AC-06.6.1 / Separated employee, no denomination, no children (spec)
- ✅ AC-06.6.1 / Calculator B0Y case: married, spouse not Swiss, no C permit (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-06.6.1 / Calculator B0N case: child neither minor nor in first education (zh_source_tax_calculator/F-zh_source_tax_calculator-abe889) (spec)
- ✅ AC-06.6.1 / Registered partner living in France, partner works (spec)
- ✅ AC-06.6.1 / Calculator C1Y case: Germany, daily return without certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-06.6.1 / Calculator N1Y case: Germany, daily return with certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-06.6.1 / Calculator H1N case: single, minor child not in household, parental care, alternating custody, main contributor (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-06.6.2 / Maria, Portuguese with a C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-06.6.2 / Tomás, Brazilian, Swiss wife, living in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-06.6.2 / Swiss citizen living in Switzerland (spec)
- ✅ AC-06.6.3 / Liechtenstein resident who returns daily (spec)
- ✅ AC-06.6.3 / Liechtenstein resident with at most 45 non-return days (spec)
- ✅ AC-06.6.4 / Calculator C1Y with treaty reservation (zh_source_tax_calculator/F-zh_source_tax_calculator-cc19c7) (spec)
- ❌ AC-06.6.5 / HR changed the address to France; denomination never asked (spec): tariff_code = ['A', 0, None], expected 'incomplete - HR must complete'
- ❌ AC-06.6.5 / HR changed the civil status to Married; spouse employment never asked (spec): tariff_code = [None, 0, 'N'], expected 'incomplete - HR must complete'
- ✅ AC-07.1.1 / Married cross-border commuter from Germany with children (spec)
- ✅ AC-07.1.1 / Single resident of Germany without children (spec)
- ✅ AC-07.1.1 / Non-Swiss without C permit living in Switzerland, with children (spec)
- ✅ AC-07.1.2 / Swiss citizen living in Switzerland (spec)
- ✅ AC-07.1.2 / Maria: Portuguese with a C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-07.1.3 / Liechtenstein, daily return (zh_source_tax_calculator/F-zh_source_tax_calculator-fb87f1) (spec)
- ✅ AC-07.1.3 / Liechtenstein, no daily return, at most 45 days (zh_source_tax_calculator/F-zh_source_tax_calculator-fb87f1) (spec)
- ✅ AC-07.1.3 / Liechtenstein, more than 45 non-return days, with children (spec)
- ✅ AC-07.2.2 / Married, child neither minor nor in first education -> B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-abe889) (spec)
- ✅ AC-07.2.3 / Minor child (spec)
- ✅ AC-07.2.3 / Adult child in first education (spec)
- ✅ AC-07.3.1 / Married, sole custody (spec)
- ✅ AC-07.3.1 / Married, shared custody, common household: no contributor question (spec)
- ✅ AC-07.3.1 / Single, shared custody, common household: contributor asked (spec)
- ✅ AC-07.3.1 / Shared custody, no common household: alternating custody asked (spec)
- ✅ AC-07.3.2 / Married, sole custody -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-d75286) (spec)
- ✅ AC-07.3.2 / Single, sole custody -> H1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-300c72) (spec)
- ✅ AC-07.3.2 / Married, shared custody, common household -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-5d8fb0) (spec)
- ✅ AC-07.3.2 / Registered partnership, shared custody, common household (counts as married) (spec)
- ✅ AC-07.3.2 / Single, shared custody, common household, other parent main contributor -> A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-5686d7) (spec)
- ✅ AC-07.3.2 / Single, shared custody, common household, employee main contributor (inferred, D-009) (spec)
- ✅ AC-07.3.2 / Married, no common household, alternating custody, other parent main contributor -> C0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-a4d358) (spec)
- ✅ AC-07.3.2 / Married, no common household, alternating custody, employee main contributor (inferred, D-009) (spec)
- ✅ AC-07.3.2 / Widowed, no common household, alternating custody, other parent main contributor (inferred, D-009) (spec)
- ✅ AC-07.3.2 / Divorced, no common household, alternating custody, employee main contributor (inferred, D-009) (spec)
- ✅ AC-07.3.2 / Married, no common household, no alternating custody -> C0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-a4d358) (spec)
- ✅ AC-07.3.2 / Separated (counts as single), no common household, no alternating custody -> H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc0ae9) (spec)
- ✅ AC-07.4.1 / Married, child outside household (spec)
- ✅ AC-07.4.1 / Divorced, child outside household (spec)
- ✅ AC-07.4.1 / Married, shared custody, alternating custody: contributor asked (spec)
- ✅ AC-07.4.1 / Single, no parental care: block ends (spec)
- ✅ AC-07.4.2 / Married, no shared custody -> B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.2 / Married, shared custody, alternating, employee main contributor -> B1N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.2 / Married, shared custody, alternating, other parent main contributor (inferred, D-009) (spec)
- ✅ AC-07.4.2 / Registered partnership, shared custody, no alternating custody (inferred, D-009) (spec)
- ✅ AC-07.4.2 / Single, no parental care -> A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.2 / Single, parental care, alternating, employee main contributor -> H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.2 / Separated, parental care, alternating, other parent main contributor (inferred, D-009) (spec)
- ✅ AC-07.4.2 / Widowed, parental care, no alternating custody (inferred, D-009) (spec)
- ✅ AC-07.5.1 / Married, in household, common household: nothing more asked (spec)
- ✅ AC-07.5.1 / Single, in household, common household: contributor asked (spec)
- ✅ AC-07.5.1 / In household, no common household: maintenance asked (spec)
- ✅ AC-07.5.1 / Not in household: maintenance asked, common household not asked (spec)
- ✅ AC-07.5.2 / Married, in household, common household -> B1N (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.2 / Single, common household, employee main contributor (inferred, D-009) (spec)
- ✅ AC-07.5.2 / Divorced, common household, other parent main contributor (inferred, D-009) (spec)
- ✅ AC-07.5.2 / Married, in household, no common household, more than 50% maintenance (inferred, D-009) (spec)
- ✅ AC-07.5.2 / Registered partnership, in household, no common household, not more than 50% (inferred, D-009) (spec)
- ✅ AC-07.5.2 / Single, in household, no common household, more than 50% -> H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.2 / Widowed, in household, no common household, not more than 50% (inferred, D-009) (spec)
- ✅ AC-07.5.2 / Single, not in household, more than 50% -> A1N (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.2 / Married, not in household, more than 50% (spec)
- ✅ AC-07.5.2 / Married, not in household, not more than 50% -> B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.6.1 / No children (spec)
- ✅ AC-07.6.1 / One counted child (married, sole custody) (spec)
- ✅ AC-07.6.1 / One child counted with H (single, sole custody) (spec)
- ✅ AC-07.6.1 / Child not counted (neither minor nor in first education) (spec)

## Open questions (need your decision)

- **OQ-calculator-coverage**: Does Lonio's computed tariff code match the Zurich calculator for the unexplored paths: the residence block for tariffs A/B/H, the inferred per-child rows, more than 3 children, and the H3N/P3N examples? → recommended: Domain expert check before go-live (D-009); observed rows win over derived ones (D-046).

## Inferred items to confirm

- item.spouse_nationality
- item.spouse_holds_c_permit
- item.spouse_residence_country
- rule.calculator_residence
- rule.child_result
- story.US-03.3
- story.US-05.2
- story.US-05.4
- story.US-08.1
- story.US-06.4
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

## Dev refinement questions (9)

- [minor] `stories/US-03.1-employee-confirms-the-first-working-day.md` The first working day 'must lie within one year after the questionnaire is sent'. Can it also be before the send date or in the past, for example when the employee has already started or fills in the questionnaire late? Sending the questionnaire is part of the later HR-side spec, so which date counts as 'sent' for this check? Is there also any plausibility check on the spouse's date of birth?
- [minor] `stories/US-01.8-review-a-summary-and-submit-with-one-confirmation.md` The stories disagree on when a missing required answer blocks the employee. US-02.1 says the employee 'cannot leave step 1 complete' without the name or date of birth. US-02.2 says the address 'step cannot be completed'. US-03.1, US-04.1 and AC-01.8.2 say the employee only cannot submit. Should a missing required answer stop the employee from moving to the next step, or only from submitting (so a partly filled step can be saved and left, as US-01.7 allows)? And if the employee can go on, how is a step that is not complete shown?
- [minor] `stories/US-08.2-germany-daily-return-and-certificate-of-residence.md` The calculator asks whether the certificate of residence has been provided ('beigebracht'). The story asks whether the employee 'has a certificate of residence for HR'. Does 'yes' mean the certificate has already been given to HR, or only that the employee has one? Should HR expect a certificate later for 'no' as well as for 'not yet', or only for 'not yet'?
- [minor] `stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md` Expected results for the same question still differ between stories. AC-01.2.2 marks the canton as 'asked', but US-02.4 marks it 'required'. AC-01.2.4 marks the spouse's date of birth and the spouse's nationality as 'asked', but US-04.2 and US-05.2 mark them 'required'. US-06.3 has 'required' for a married employee and 'asked' for a registered partner. Several rows also show '–' for questions that always apply, for example First name for the Germany resident in AC-01.2.2. Is there a real difference between 'asked' and 'required' (can any of these answers be left empty?), and does '–' mean 'not checked in this example'?
- [major] `stories/US-06.6-compute-and-record-the-full-source-tax-tariff-code.md` Both examples in AC-06.6.5 are marked as failed (❌). The first expects Denomination 'required' after an HR change. D-053 says that examples after an HR change should expect 'HR must complete', not that the question is asked. The second example (civil status changed to Married) does not show the never-asked spouse employment question at all. What exactly should these examples expect, so we have a passing acceptance test for the 'incomplete' case?
- [major] `stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md` After an HR change, 'incomplete - HR must complete' is specified for the tariff code and for 'subject to source tax'. What happens to the pension fund results when an HR change makes an answer apply that was never asked? Two examples: a move from abroad to Switzerland, where the canton was never asked; and a change from Single to Married, where the spouse's date of birth was never asked. Should the canton for the fund, and the fund registration with civil status Married, also show 'incomplete - HR must complete'? Or should the canton keep showing Zurich until HR enters it? Which derived results does the 'incomplete' state apply to?
- [minor] `stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md` Several example tables use the same item as both an input and an expected result, with values that do not match. In AC-01.1.1, Nationality is '–' as an input but 'not asked' as a result for Stefan. In AC-01.1.2, 'More than 45 non-return days' is 'yes' or 'no' as an input but '–' or 'not asked' as a result. The same happens in US-07.3 and US-07.5. Which of the two values is the expected outcome a tester should check?
- [minor] `stories/US-04.4-enter-the-civil-status-on-the-pension-fund-s-list.md` In the AC-04.4.1 example table, the spouse's date of birth is '–' for Married, but 'required' for Registered partnership and Separated. It is also '–' for Single, but 'not asked' for Divorced and Widowed. Should Married expect 'required' and Single expect 'not asked', as US-04.2 says?
- [minor] `stories/US-07.2-one-block-per-child-age-status-and-household.md` AC-07.2.1 says 'At least one child block is filled in' when the employee answered 'yes' to having children. The trace check notes that no cited source backs this. Is it a confirmed rule, and if so what happens when the employee removes the last child block? Is that blocked, or is 'has children' then treated as 'no'?

## Technical vocabulary found in the spec (9)

- `item.address_country` implementation vocabulary ['iso 3166']: Chosen from the ISO 3166 country list (English names, e.g. Switzerland, Germany, Liechtenstein)
- `item.nationality` implementation vocabulary ['iso 3166']: Chosen from the ISO 3166 country list, plus 'stateless'
- `item.spouse_nationality` implementation vocabulary ['iso 3166']: Chosen from the ISO 3166 country list, plus 'stateless'
- `ac.AC-02.3.1` implementation vocabulary ['iso 3166']: they choose it from the ISO 3166 country list with English country names (for example Switzerland, Germany, Liechtenstein); free text is not
- `ac.AC-05.1.2` implementation vocabulary ['iso 3166']: the employee chooses one country from the ISO 3166 country list (English names) or 'stateless'. Anyone with Swiss citizenship chooses Switze
- `ac.AC-05.2.3` implementation vocabulary ['iso 3166']: the spouse's nationality is chosen from the ISO 3166 country list or 'stateless'; a spouse with Swiss citizenship counts as Swiss, even with
- `feature.md` "(The internal expression evaluates one child block; it is summed over all blocks.)" - Refers to an internal formula ('internal expression') rather than business language. D-045 forbids this.
- `information.md` "(The internal expression evaluates one child block; it is summed over all blocks.)" - Refers to an internal formula ('internal expression') rather than business language. D-045 forbids this.
- `stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md` "free text is not accepted and the country is required" - Prescribes how the input field behaves (no free text). Choosing from the list is already the business rule; how input is restricted is up to engineering.

## Coverage

167/342 source units cited; 150/177 facts used.

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
- zh_source_tax_calculator/C-V51: Answers {"Q01": "Ersatzeinkünfte", "Q16": "Nein", "Q17": "Liechtenstein", "Q27": "Nein", "Q28": "Nein"} -> result Grundsätzlich keine Quellensteuerpflicht / Unt
- zh_source_tax_calculator/C-N01: The calculator is an Angular app (app-root, ng 11, assets from www.services.zh.ch/app/quest/tarifbestimmung/prod/) rendered inline in the section 'Tarifrechner 
- zh_source_tax_calculator/C-N08: The answer value in V25–V29 summarises repeated per-child answers (Kind 1/2/3) because the schema allows one value per question id.

## Other warnings (36)

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
- [trace_judge] `item.address_country` partial: The pension fund purpose (canton of residence vs place of work) and the 'cross-border questions' use are not backed by the cited facts, since D-002 and D-047 are not cited.
- [trace_judge] `item.civil_status` partial: The purpose 'tariff A/H vs B/C' is not in the cited facts, which only describe two groups (married/partnership vs single/divorced/separated/widowed) without tariff letters.
- [trace_judge] `item.spouse_nationality` partial: The ISO 3166 list plus 'stateless' is only cited for the employee's nationality (D-050), not the spouse's, and the narrowing to employees who are non-Swiss without a C permit is only a 'presumably' inference.
- [trace_judge] `item.spouse_gainful_employment` partial: The Liechtenstein/non_return_days_45 and subject_to_source_tax part of the asked/required condition is not backed by any cited fact, though the question, Ja/Nein values, married/registered-partnership scope, C/B tariff and step 6 are.
- [trace_judge] `item.has_children` partial: The cited facts back the question, Ja/Nein values and step 6, but not the Liechtenstein/non_return_days_45 gating, nor 'tariff H' as the purpose.
- [trace_judge] `item.child_age_status` partial: Options, per-child blocks, 'neither' not counting, no maximum and step 7 are backed, but the Liechtenstein/non_return_days_45 source-tax gating in the expression is not cited.
- [trace_judge] `item.child_same_household` partial: Question, values and the minor/adult-in-first-education condition are backed, but the Liechtenstein/non_return_days_45 gating and the has_children precondition are not cited.
- [trace_judge] `item.child_custody` partial: Options and the minor-in-household condition are backed, but the Liechtenstein gating and the purpose 'sole custody counts the child (H for single persons)' are not in the cited facts.
- [trace_judge] `item.child_common_household_other_parent` partial: Question and display condition are backed, but the Liechtenstein/non_return_days_45 gating is not cited, and the cited condition for an adult in first education doesn't explicitly cover the same-household requirement beyond the fact statement.
- [trace_judge] `rule.questionnaire_flow` partial: The eight steps, their order, once-only asking, save/resume and single confirmation are backed, but many row details are not in the supplied facts: address fields, commuting days and the German certificate, spouse conditions, the Liechtenstein exception, 'no maximum' children, and who gets the permit reminder.
- [trace_judge] `rule.pension_fund_canton` partial: Table row 1 cites F-pension_portal-3432a9, which is not among the cited facts; the other claims are backed by D-002.
- [trace_judge] `rule.liechtenstein_no_source_tax` partial: The 'does not apply' row for non-Liechtenstein countries cites F-zh_source_tax_calculator-e22d17, which is not among the cited facts.
- [trace_judge] `rule.calculator_residence` partial: The cited facts only list Germany and Liechtenstein as options and never mention 'cross-border questions' for them, so those two table rows are not backed.
- [trace_judge] `rule.base_tariff_letter` partial: The expression gates the letter on subject_to_source_tax and on Liechtenstein/non_return_days_45, which neither the statement nor the cited facts support; the C/B/H/A logic itself is backed.
- [trace_judge] `rule.cross_border_tariff` partial: The 'any country other than Germany → normal tariff' row relies on F-zh_source_tax_calculator-f86c6b, which is not among the cited facts, so that row is unbacked.
- [trace_judge] `rule.tariff_letter` partial: The claim that G→Q 'cannot occur for onboarding' is not supported by any cited fact; D-051 only says the mapping includes G to Q.
- [trace_judge] `rule.tariff_code` partial: The expression uses if_else(child_count, 1, 0), giving only 0 or 1, which contradicts the statement and F-4c53e3 (number of counted children, e.g. C3Y); the 'no tariff code' row also cites F-hr_transcript-5af8d0, which is not among the cited facts.
- [trace_judge] `story.US-05.4` partial: The claim that Germany and Liechtenstein lead to the cross-border questions is not backed by the cited facts; the cited calculator facts cover only the CH and 'Anderes Land' base-tariff path.
- [trace_judge] `story.US-06.7` partial: The rule for who is subject to source tax (the C-permit and Swiss cases behind the non-illustrative Maria 'not asked' example) is not backed by the cited facts, which omit F-hr_transcript-5af8d0 and F-hr_transcript-845204.
- [trace_judge] `story.US-07.2` partial: AC-07.2.1 says at least one child block must be filled in and that every child question is required whenever asked, but no cited fact or decision backs either.
- [dev_refinement] `stories/US-06.6-compute-and-record-the-full-source-tax-tariff-code.md` Both examples in AC-06.6.5 are marked as failed (❌). The first expects Denomination 'required' after an HR change. D-053 says that examples after an HR change should expect 'HR must complete', not that the question is asked. The second example (civil status changed to Married) does not show the never-asked spouse employment question at all. What exactly should these examples expect, so we have a passing acceptance test for the 'incomplete' case?
- [dev_refinement] `stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md` After an HR change, 'incomplete - HR must complete' is specified for the tariff code and for 'subject to source tax'. What happens to the pension fund results when an HR change makes an answer apply that was never asked? Two examples: a move from abroad to Switzerland, where the canton was never asked; and a change from Single to Married, where the spouse's date of birth was never asked. Should the canton for the fund, and the fund registration with civil status Married, also show 'incomplete - HR must complete'? Or should the canton keep showing Zurich until HR enters it? Which derived results does the 'incomplete' state apply to?

## Run

Stages run: knowledge.raw, feature.plan, sections/SEC-03-employment-start, sections/SEC-04-civil-status-spouse, sections/SEC-02-personal-details-address, sections/SEC-08-cross-border-residence, sections/SEC-05-source-tax-liability, sections/SEC-01-questionnaire-flow, sections/SEC-07-source-tax-children, sections/SEC-06-source-tax-tariff-basics, feature.flow, judge_trace, dev_refinement, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator, judge_facts

LLM cost this run: $9.81

Tokens this run: 1,148,464 in 29 agent calls (58 input, 51,294 cache read, 899,001 cache write, 198,111 output)
