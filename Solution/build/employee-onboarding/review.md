# Review: employee-onboarding

**Verdict: READY WITH CAVEATS**

All 300+ examples pass. There are no errors, no blocking open questions and no blocker-level dev questions. The package is buildable. Five major dev-refinement questions, five non-blocking open questions, several partly unbacked claims and some internal rule ids in the prose need a product owner decision or cleanup. The tariff logic rests on inferred per-child rows, which D-009 makes a go-live verification gate.

## Reviewer findings

1. **Insurance start rule: contract start vs actual first working day** – If the contract starts on the 1st but the first working day is later (weekend or holiday), the rule moves insurance start to the next month. This gives wrong fund registrations. The fund's link between start date and first working day is also unknown.  
   Evidence: dev_refinement (feature.md, major); coverage: F-pension_portal-3a97ab unused; US-03.2  
   Action: Decide in decisions.yaml whether the rule uses the contractual start date or the actual first working day. Confirm with the fund how mid-month starts are handled.
2. **Child per-child result is inferred and internally inconsistent** – Lonio now computes the tariff itself. The rule expression disagrees with its table in at least two cases, and many rows rest only on D-009, which is a verification decision and not a source. Wrong tariff codes are possible.  
   Evidence: trace_judge rule.child_result; inferred_items; OQ-calculator-coverage; US-07.3 to 07.6  
   Action: Have the domain expert reconcile the expression and the table. Run the inferred rows against the Zurich calculator before go-live, as D-009 requires. Keep this as an explicit release gate.
3. **Liechtenstein question order and the reservation under the double taxation agreement** – Liechtenstein residents who return daily get no tariff code, yet they are still asked about denomination, spouse employment and children. This breaks data minimisation. The 'subject to double taxation agreement' reservation for more than 45 non-return days is not recorded in AC-08.4.3.  
   Evidence: dev_refinement (feature.md; US-08.4, major); F-zh_source_tax_calculator-cc19c7  
   Action: Decide whether the Liechtenstein questions come first or answers are discarded. Decide whether the reservation is recorded and flagged for HR.
4. **Residence country timing** – The home-address country decides source-tax liability, the canton and the cross-border questions. Movers' current address may differ from the one that applies from the first working day.  
   Evidence: dev_refinement US-02.3 (major)  
   Action: Decide whether to ask for the address applying at the first working day. Add this to the story.
5. **House number required without a source** – Employees whose address has no house number could not submit.  
   Evidence: trace_judge item.address_house_number; dev_refinement US-02.2 (major); AC-02.2.2  
   Action: Decide whether the house number is optional or allows an explicit 'no house number'.
6. **Fund registration gaps (canton abroad, partnership and separated mapping, divorced and widowed)** – The fund's canton field is required, but employees abroad have no valid value. The Married mapping for registered partners and separated employees is provisional. Divorced and widowed screens are unseen. Registration could be blocked.  
   Evidence: OQ-canton-abroad; OQ-civil-status-partnership; OQ-spouse-dob-other-status; fact_judge F-pension_portal-b359c3, 6d3630, 39bab1; trace_judge rule.pension_fund_civil_status (Separated not backed)  
   Action: Get the fund's answers and a screenshot for Divorced and Widowed. Record the decisions in decisions.yaml.
7. **Source tax liability rule is hedged by HR** – Anna said 'I think so' and added conditions over time. 'Here' is read as Switzerland. This rule gates all the source tax questions.  
   Evidence: OQ-source-tax-rule-confirmation; fact_judge F-hr_transcript-550840 and 5af8d0; trace_judge AC-08.3.1  
   Action: Have HR confirm the decision table in writing, including 'lives here' = Switzerland and that everyone living abroad is subject.
8. **Stories include behaviour that no cited fact backs** – Several claims are untraceable. Examples: the confession, children and spouse-works questions; the fixed step order; the Liechtenstein base-letter handling; the 'no maximum number of children' statement; and the date format and permit reminder purposes. Some cite facts that are not in the cited set.  
   Evidence: trace_judge story.US-01.1, US-01.2, US-01.4, US-03.1, US-06.5, US-07.2; rule.questionnaire_flow, cross_border_tariff, liechtenstein_no_source_tax  
   Action: Fix the citations where facts exist. Otherwise mark these items inferred or add decisions. Decide the maximum number of children.
9. **Internal rule ids written into business prose** – Snake_case rule ids and 'expression' wording appear in the feature, stories and open-questions files. This is a minor technical leak.  
   Evidence: tech_leak: feature.md, US-02.3, US-06.4, US-06.5, US-07.1, open-questions.md  
   Action: Replace the ids with business terms such as 'source tax liability rule' and 'per-child result'.
10. **Untestable and ambiguous acceptance criteria wording** – Some wording cannot be tested as written. AC-03.1.2 is untestable. 'Required' and 'asked' are used inconsistently in the example tables. The permit reminder text is missing. The date on which a child's age is judged is not set.  
   Evidence: dev_refinement info: US-03.1, US-05.1, US-05.2, US-01.4, US-07.2  
   Action: Agree the question wording and the permit reminder text with HR. Standardise 'required' in the examples. Fix the child age reference date.

## Numbers

342 source units → 177 facts → 35 information items, 17 business rules → one feature with 8 sections, 34 stories, 108 acceptance criteria; 5 open questions, 10 exclusions.

## Impact of this run

Stories added: US-01.4, US-01.5, US-01.6, US-06.5, US-06.6, US-07.6; changed: US-01.1, US-01.2, US-01.3, US-02.1, US-02.2, US-02.3, US-02.4, US-03.1, US-03.2, US-03.3, US-04.1, US-04.2, US-04.3, US-05.1, US-05.2, US-05.3, US-06.2, US-06.3, US-06.4, US-07.1, US-07.2, US-07.3, US-07.4, US-07.5, US-08.1, US-08.2, US-08.3, US-08.4; removed: US-06.1; unchanged: 0.

Knowledge elements changed: OQ-calculator-coverage, OQ-canton, OQ-canton-abroad, OQ-civil-status-partnership, OQ-divorced-widowed, OQ-dual-nationality, OQ-income-type, OQ-liechtenstein, OQ-permit-list, OQ-permit-reminder, OQ-proof-documents, OQ-registered-partnership, OQ-separated, OQ-source-tax-rule, OQ-source-tax-rule-confirmation, OQ-spouse-dob-other-status, OQ-spouse-residence-form, address_country, address_house_number, address_postcode, address_street, address_town, base_tariff_letter, calculator_civil_status, calculator_residence, child_age_status, child_alternating_custody, child_common_household_other_parent, child_count, child_custody, child_main_financial_contributor, child_maintenance_over_50, child_parental_care, child_result, child_same_household, child_shared_custody, church_tax_suffix, civil_status, confession, cross_border_tariff, daily_return_germany, daily_return_liechtenstein, daily_return_reasonable, date_of_birth, discard_inapplicable_answers, first_name, first_working_day, has_children, holds_c_permit, income_type, insurance_start_date, last_name, liechtenstein_no_source_tax, nationality, non_return_days_45, non_return_days_60, pension_fund_civil_status, permit_reminder, permit_type, questionnaire_flow, read_only_after_submission, residence_canton, residence_certificate, spouse_date_of_birth, spouse_gainful_employment, spouse_holds_c_permit, spouse_nationality, spouse_permit_type, spouse_residence_country, subject_to_source_tax, tariff_code, tariff_letter

## Errors (0)


## Examples executed against the knowledge model (240/240 pass)

- ✅ AC-01.1.1 / Non-Swiss single employee without C permit living in Switzerland (spec)
- ✅ AC-01.1.1 / Married employee living in Germany (spec)
- ✅ AC-01.1.1 / Non-Swiss married employee whose C-permit spouse lives abroad (spec)
- ✅ AC-01.1.1 / Separated non-Swiss employee without C permit (counts as single for source tax) (spec)
- ✅ AC-01.1.2 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.1.2 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.1.2 / Swiss citizen living in Switzerland (spec)
- ✅ AC-01.1.2 / Registered partner of a C-permit holder living in Switzerland (spec)
- ✅ AC-01.1.3 / Employee living in Germany (spec)
- ✅ AC-01.1.3 / Employee living in Liechtenstein (spec)
- ✅ AC-01.1.3 / Employee living in another country (spec)
- ✅ AC-01.1.3 / Non-Swiss employee without C permit living in Switzerland (spec)
- ✅ AC-01.2.2 / Employee living in Switzerland (spec)
- ✅ AC-01.2.2 / Employee living in Germany (spec)
- ✅ AC-01.2.3 / Daniel (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-01.2.3 / Married employee (spec)
- ✅ AC-01.2.3 / Separated employee (spec)
- ✅ AC-01.2.3 / Single employee (spec)
- ✅ AC-01.2.3 / Divorced employee (spec)
- ✅ AC-01.2.3 / Widowed employee (spec)
- ✅ AC-01.2.4 / Swiss citizen living in Germany (like Stefan, hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-01.2.4 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.2.4 / Swiss citizen living in Switzerland (spec)
- ✅ AC-01.2.5 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.2.5 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.2.5 / Married, spouse not Swiss and without C permit (spec)
- ✅ AC-01.2.5 / Separated employee without C permit (spec)
- ✅ AC-01.2.5 / Single employee without C permit (spec)
- ✅ AC-01.3.2 / Separated non-Swiss employee: one civil status answer, two uses (spec)
- ✅ AC-01.3.2 / Registered partner without C permit: one civil status answer, two uses (spec)
- ✅ AC-01.3.2 / Employee living in Germany: country answer used for canton and source tax (spec)
- ✅ AC-01.4.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.4.1 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.4.1 / Swiss citizen living in Germany (like Stefan, hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-01.4.1 / Employee living in Liechtenstein (spec)
- ✅ AC-01.4.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-01.5.2 / Employee first entered Switzerland and an Italian nationality, then changed the country to Germany (spec)
- ✅ AC-01.5.2 / Employee first chose Married and gave a spouse's date of birth, then changed to Single (spec)
- ✅ AC-01.5.2 / Non-Swiss employee first answered no C permit and the source tax details, then changed to yes (spec)
- ✅ AC-01.6.2 / Nationality corrected to Switzerland after submission (spec)
- ✅ AC-01.6.2 / Non-Swiss employee without C permit marries a Swiss citizen living in Switzerland after submission (spec)
- ✅ AC-01.6.2 / Swiss citizen moves from Switzerland to Germany after submission (spec)
- ✅ AC-02.3.2 / Employee living in Konstanz, Germany (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-02.3.2 / Employee living in Liechtenstein (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-02.3.2 / Employee living in another country (spec)
- ✅ AC-02.3.3 / Tomás, lives in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-02.3.4 / Employee living in Konstanz, Germany (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-02.3.4 / Employee living in Liechtenstein (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-02.3.4 / Employee living in another country (spec)
- ✅ AC-02.4.1 / Tomás, lives in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-02.4.1 / Employee living in Konstanz, Germany (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-02.4.1 / Employee living in Liechtenstein (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-02.4.3 / Employee corrects the country to Germany (spec)
- ✅ AC-03.1.1 / Julia (hr_transcript/F-hr_transcript-e18e66) (spec)
- ✅ AC-03.1.1 / Start on the 1st of a month (spec)
- ✅ AC-03.2.2 / Start on 1 March (spec)
- ✅ AC-03.2.2 / Start on 1 January (spec)
- ✅ AC-03.2.3 / Julia (hr_transcript/F-hr_transcript-e18e66) (spec)
- ✅ AC-03.2.3 / Start on the 2nd of a month (spec)
- ✅ AC-03.2.3 / Start in December, insurance starts next year (spec)
- ✅ AC-03.2.3 / Start on the last day of a month (spec)
- ✅ AC-03.3.1 / Julia moves her start to the 15th (hr_transcript/F-hr_transcript-e18e66) (spec)
- ✅ AC-03.3.1 / Start moved one week earlier onto the 1st (spec)
- ✅ AC-03.3.2 / Julia: latest date 15.03 (hr_transcript/F-hr_transcript-e18e66) (spec)
- ✅ AC-03.3.2 / Latest date moved to the 1st of the following month (spec)
- ✅ AC-04.1.1 / Employee living in Switzerland (spec)
- ✅ AC-04.1.1 / Employee living in Germany (spec)
- ✅ AC-04.1.3 / Daniel (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-04.1.3 / Single employee (spec)
- ✅ AC-04.1.3 / Married employee (spec)
- ✅ AC-04.1.3 / Divorced employee (spec)
- ✅ AC-04.1.3 / Widowed employee (spec)
- ✅ AC-04.1.3 / Separated employee (spec)
- ✅ AC-04.2.1 / Daniel (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-04.2.1 / Married employee (spec)
- ✅ AC-04.2.1 / Separated employee (spec)
- ✅ AC-04.2.2 / Single employee (spec)
- ✅ AC-04.2.2 / Divorced employee (spec)
- ✅ AC-04.2.2 / Widowed employee (spec)
- ✅ AC-04.3.1 / Daniel (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-04.3.1 / Married employee (spec)
- ✅ AC-04.3.1 / Single employee (spec)
- ✅ AC-04.3.1 / Divorced employee (spec)
- ✅ AC-04.3.1 / Widowed employee (spec)
- ✅ AC-04.3.1 / Separated employee (spec)
- ✅ AC-05.1.1 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.1.1 / Stefan, Swiss living abroad (hr_transcript/F-hr_transcript-3f2c2a), country assumed (spec)
- ✅ AC-05.1.1 / Employee living in Liechtenstein (spec)
- ✅ AC-05.1.2 / Swiss-Italian dual national living in Switzerland (spec)
- ✅ AC-05.1.3 / Maria, Portuguese (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.1.3 / Tomás, Brazilian (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.1.3 / Swiss citizen living in Switzerland (spec)
- ✅ AC-05.1.3 / Stefan, Swiss living abroad (hr_transcript/F-hr_transcript-3f2c2a), country assumed (spec)
- ✅ AC-05.2.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.1 / Non-Swiss employee in a registered partnership (spec)
- ✅ AC-05.2.1 / Married C-permit holder (spec)
- ✅ AC-05.2.1 / Married Swiss citizen (spec)
- ✅ AC-05.2.1 / Separated non-Swiss employee without C permit (spec)
- ✅ AC-05.2.1 / Single non-Swiss employee without C permit (spec)
- ✅ AC-05.2.1 / Married employee living abroad (spec)
- ✅ AC-05.2.2 / Tomás, Swiss wife (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.2 / Married employee with an Italian spouse (spec)
- ✅ AC-05.2.3 / Tomás, Swiss wife (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.3 / Spouse is Italian with a C permit (spec)
- ✅ AC-05.2.3 / Spouse is Italian without a C permit (spec)
- ✅ AC-05.3.1 / Stefan, Swiss living abroad (hr_transcript/F-hr_transcript-3f2c2a), country assumed (spec)
- ✅ AC-05.3.1 / Married employee living in Liechtenstein (spec)
- ✅ AC-05.3.2 / Maria, Portuguese with C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.3.2 / Swiss citizen living in Switzerland (spec)
- ✅ AC-05.3.3 / Single Italian with B permit (spec)
- ✅ AC-05.3.3 / Separated Italian without C permit (spec)
- ✅ AC-05.3.4 / Tomás, Swiss wife, living in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.3.4 / Registered partner of a C-permit holder living in Switzerland (spec)
- ✅ AC-05.3.4 / Swiss spouse living in Germany (spec)
- ✅ AC-05.3.4 / Spouse neither Swiss nor C-permit holder (spec)
- ✅ AC-05.3.5 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.3.5 / Single Italian without C permit (spec)
- ✅ AC-06.2.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-06.2.1 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-06.2.1 / Swiss citizen living abroad, like Stefan (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-06.2.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-06.2.1 / Non-Swiss employee in Switzerland without C permit (spec)
- ✅ AC-06.2.3 / Calculator path A0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-037b1c) (spec)
- ✅ AC-06.2.3 / Calculator path A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-2eab9a) (spec)
- ✅ AC-06.3.1 / Married, subject to source tax (spec)
- ✅ AC-06.3.1 / Registered partner, like Daniel (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-06.3.1 / Separated, subject to source tax (spec)
- ✅ AC-06.3.1 / Divorced, living abroad (spec)
- ✅ AC-06.3.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-06.4.1 / Calculator path C0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-06.4.1 / Calculator path B0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-06.4.1 / Calculator path B1N, child with sole custody (zh_source_tax_calculator/F-zh_source_tax_calculator-d75286) (spec)
- ✅ AC-06.4.1 / Registered partner whose partner works (spec)
- ✅ AC-06.4.2 / Calculator path A0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-037b1c) (spec)
- ✅ AC-06.4.2 / Calculator path H1Y, sole custody (zh_source_tax_calculator/F-zh_source_tax_calculator-300c72) (spec)
- ✅ AC-06.4.2 / Calculator path A0N, other parent main contributor (zh_source_tax_calculator/F-zh_source_tax_calculator-5686d7) (spec)
- ✅ AC-06.4.2 / Separated employee without children (spec)
- ✅ AC-06.5.1 / Calculator path L0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-66732c) (spec)
- ✅ AC-06.5.1 / Calculator path M0N (zh_source_tax_calculator/F-zh_source_tax_calculator-66732c) (spec)
- ✅ AC-06.5.1 / Calculator path N1Y, daily return with certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-06.5.1 / Calculator path P1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-66732c) (spec)
- ✅ AC-06.5.1 / Calculator path N1Y, no daily return, at most 60 days (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-06.5.2 / Calculator path C1Y, no certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-06.5.2 / Certificate of residence 'not yet' (spec)
- ✅ AC-06.5.2 / Calculator path C1Y, more than 60 days (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-06.5.2 / Calculator path C1Y, daily return not reasonable (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-06.5.2 / Calculator path A0N, other country (zh_source_tax_calculator/F-zh_source_tax_calculator-f86c6b) (spec)
- ✅ AC-06.5.2 / Living in Switzerland, married, spouse does not work (spec)
- ✅ AC-06.6.1 / Calculator path A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-2eab9a) (spec)
- ✅ AC-06.6.1 / Calculator path C1Y, sole custody (zh_source_tax_calculator/F-zh_source_tax_calculator-d75286) (spec)
- ✅ AC-06.6.1 / Calculator path B0N, child neither minor nor in first education (zh_source_tax_calculator/F-zh_source_tax_calculator-abe889) (spec)
- ✅ AC-06.6.1 / Calculator path N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-06.6.1 / Calculator path L0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-66732c) (spec)
- ✅ AC-06.6.1 / Calculator path C1Y, Liechtenstein more than 45 days (zh_source_tax_calculator/F-zh_source_tax_calculator-cc19c7) (spec)
- ✅ AC-06.6.2 / Calculator path Liechtenstein daily return (zh_source_tax_calculator/F-zh_source_tax_calculator-fb87f1) (spec)
- ✅ AC-06.6.2 / Calculator path Liechtenstein at most 45 days (zh_source_tax_calculator/F-zh_source_tax_calculator-fb87f1) (spec)
- ✅ AC-06.6.3 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-06.6.3 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-07.1.1 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-07.1.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-07.1.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-07.1.1 / Non-Swiss without C permit living in Switzerland (spec)
- ✅ AC-07.1.1 / Employee living in Germany (spec)
- ✅ AC-07.1.1 / Employee living in Liechtenstein (spec)
- ✅ AC-07.1.3 / No children (spec)
- ✅ AC-07.1.3 / Has children (spec)
- ✅ AC-07.2.2 / Calculator path 'weder noch' -> B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-abe889) (spec)
- ✅ AC-07.2.2 / Single employee, child neither minor nor in first education (spec)
- ✅ AC-07.2.3 / Minor child (spec)
- ✅ AC-07.2.3 / Adult child in first education (spec)
- ✅ AC-07.3.1 / Calculator path married, sole custody -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-d75286) (spec)
- ✅ AC-07.3.1 / Calculator path single, sole custody -> H1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-300c72) (spec)
- ✅ AC-07.3.1 / Minor child outside the household (spec)
- ✅ AC-07.3.2 / Calculator path married, shared custody, common household -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-5d8fb0) (spec)
- ✅ AC-07.3.2 / Calculator path single, common household, other parent main contributor -> A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-5686d7) (spec)
- ✅ AC-07.3.2 / Single, common household, employee main contributor (spec)
- ✅ AC-07.3.2 / Registered partner, common household (spec)
- ✅ AC-07.3.3 / Calculator path married, no alternating custody -> C0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-a4d358) (spec)
- ✅ AC-07.3.3 / Calculator path single, no alternating custody -> H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc0ae9) (spec)
- ✅ AC-07.3.3 / Separated employee, no alternating custody (spec)
- ✅ AC-07.3.4 / Calculator path married, alternating custody, other parent main contributor -> C0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-a4d358) (spec)
- ✅ AC-07.3.4 / Married, alternating custody, employee main contributor (inferred) (spec)
- ✅ AC-07.3.4 / Single, alternating custody, employee main contributor (spec)
- ✅ AC-07.3.4 / Divorced, alternating custody, other parent main contributor (inferred) (spec)
- ✅ AC-07.4.1 / Calculator path married, no shared custody -> B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.1 / Registered partner, child outside the household (spec)
- ✅ AC-07.4.2 / Calculator path single, no parental care -> A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.2 / Widowed employee, child outside the household (spec)
- ✅ AC-07.4.3 / Married, shared custody, no alternating custody (inferred) (spec)
- ✅ AC-07.4.3 / Single, parental care, no alternating custody (inferred) (spec)
- ✅ AC-07.4.4 / Calculator path married, alternating custody, employee main contributor -> B1N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.4 / Calculator path single, alternating custody, employee main contributor -> H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.4 / Married, other parent main contributor (inferred) (spec)
- ✅ AC-07.4.4 / Divorced, other parent main contributor (inferred) (spec)
- ✅ AC-07.5.1 / Calculator path married, adult child, common household -> B1N (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.1 / Single, adult child, common household, employee main contributor (inferred) (spec)
- ✅ AC-07.5.1 / Single, adult child, common household, other parent main contributor (inferred) (spec)
- ✅ AC-07.5.2 / Calculator path single, adult child in household, >50% maintenance -> H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.2 / Married, >50% maintenance (inferred) (spec)
- ✅ AC-07.5.2 / Married, not more than 50% maintenance (inferred) (spec)
- ✅ AC-07.5.2 / Separated, not more than 50% maintenance (inferred) (spec)
- ✅ AC-07.5.3 / Calculator path single, adult child outside household, >50% maintenance -> A1N (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.3 / Calculator path married, adult child outside household, not >50% -> B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.3 / Married, >50% maintenance (inferred) (spec)
- ✅ AC-07.5.3 / Widowed, not more than 50% maintenance (inferred) (spec)
- ✅ AC-07.6.1 / No children (spec)
- ✅ AC-07.6.1 / One child counting with H (spec)
- ✅ AC-07.6.1 / One child counting without H (spec)
- ✅ AC-07.6.1 / One child that does not count (spec)
- ✅ AC-08.1.1 / Tomás, lives in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-08.1.1 / Employee living in Konstanz (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.1.1 / Employee living in Liechtenstein (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.1.1 / Employee living in France (spec)
- ✅ AC-08.1.2 / Tomás, lives in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-08.1.2 / Employee living in France (spec)
- ✅ AC-08.1.3 / Employee moves the address from Germany to Switzerland before submitting (spec)
- ✅ AC-08.2.1 / Employee living in Konstanz (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.2.1 / Employee living in Liechtenstein (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.2.2 / Germany resident returning daily (spec)
- ✅ AC-08.2.2 / Germany resident not returning daily (spec)
- ✅ AC-08.2.3 / Calculator run: daily return, certificate handed in, result N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-08.2.3 / Calculator run: daily return, no certificate, result C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-993db3) (spec)
- ✅ AC-08.2.3 / New hire without a certificate yet (spec)
- ✅ AC-08.2.3 / Tomás, lives in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-08.2.4 / Certificate later recorded as handed in (spec)
- ✅ AC-08.3.1 / Germany resident not returning daily (spec)
- ✅ AC-08.3.1 / Germany resident returning daily (spec)
- ✅ AC-08.3.2 / Return reasonable (spec)
- ✅ AC-08.3.2 / Return not reasonable (spec)
- ✅ AC-08.3.3 / Calculator run: return not reasonable, result C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-08.3.3 / Calculator run: reasonable, more than 60 days, result C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-08.3.3 / Calculator run: reasonable, not more than 60 days, result N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c8aa5e) (spec)
- ✅ AC-08.4.1 / Employee living in Liechtenstein (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.4.1 / Employee living in Konstanz (hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.4.2 / Liechtenstein resident not returning daily (spec)
- ✅ AC-08.4.2 / Liechtenstein resident returning daily (spec)
- ✅ AC-08.4.3 / Calculator run: daily return to Liechtenstein (zh_source_tax_calculator/F-zh_source_tax_calculator-fb87f1) (spec)
- ✅ AC-08.4.3 / Calculator run: no daily return, not more than 45 days (zh_source_tax_calculator/F-zh_source_tax_calculator-fb87f1) (spec)
- ✅ AC-08.4.3 / Calculator run: more than 45 days, result C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-cc19c7) (spec)
- ✅ AC-08.4.3 / Employee living in Konstanz (hr_transcript/F-hr_transcript-3f2c2a) (spec)

## Open questions (need your decision)

- **OQ-canton-abroad**: What does Pensionskasse Muster expect in its required 'Canton' field for employees living abroad, and does 'Canton' mean canton of residence or canton of work? → recommended: Keep D-002 (ask residents only); a domain expert verifies with Pensionskasse Muster.
- **OQ-civil-status-partnership**: How does Pensionskasse Muster want registered partnerships and separated employees entered, given its list offers only Single, Married, Divorced, Widowed? → recommended: Keep D-003 provisional mapping; domain expert verifies with the fund.
- **OQ-spouse-dob-other-status**: Does the fund's screen ask for a spouse's date of birth (or other fields) when civil status is Divorced or Widowed? → recommended: Get a screenshot of the fund's screen for Divorced and Widowed.
- **OQ-calculator-coverage**: Does Lonio's computed tariff code match the calculator for the paths not explored: residence block for A/B/H tariffs, more than 3 children, H3N/P3N, and the per-child results marked as inferred? → recommended: Go-live condition per D-009: compare all inferred rows of child_result and the cross-border paths.
- **OQ-source-tax-rule-confirmation**: Is HR's final source tax liability rule complete, and does 'lives here' mean lives in Switzerland? → recommended: Confirm the decision table of subject_to_source_tax with HR.

## Inferred items to confirm

- item.first_name
- item.last_name
- item.spouse_nationality
- item.spouse_residence_country
- rule.church_tax_suffix
- rule.child_result
- story.US-02.1
- story.US-03.3
- story.US-05.2
- story.US-06.2
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

## Dev refinement questions (13)

- [major] `feature.md` The insurance start rule uses the 'first working day'. If the contract starts on the 1st but the first actual working day is later (weekend or holiday, e.g. contract from Sat 01.06, first day Mon 03.06), the rule gives 01.07 instead of 01.06. Should the rule use the contractual start date or the actual first working day?
- [major] `stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md` New hires often move to Switzerland when they start, or move away from it. Is the home address the current one or the one that applies from the first working day? The country decides source-tax liability, the canton and all the cross-border questions, so the answer changes which questions are asked.
- [major] `feature.md` In step 6 the Liechtenstein cross-border questions come after denomination, spouse employment and all the children questions. A Liechtenstein resident who returns daily (or expects at most 45 non-return days) gets 'in principle no source tax liability' and no tariff code, so their denomination, spouse-employment and children answers are not needed by any party (G-01). Should the Liechtenstein questions come first so those questions are skipped? Or, if the order stays, should those answers be discarded on submission like other answers that no longer apply? Or does HR need them anyway in case the case changes later?
- [major] `stories/US-08.4-liechtenstein-daily-return-and-more-than-45-non-return-days.md` For Liechtenstein residents with more than 45 non-return days, the calculator returns the normal tariff plus 'Unter Vorbehalt des Doppelbesteuerungsabkommens' (subject to the double taxation agreement), per F-zh_source_tax_calculator-cc19c7. AC-08.4.3 records only 'the normal tariff code'. Should this reservation also be recorded and flagged for HR in that case?
- [major] `stories/US-02.2-collect-a-complete-postal-home-address.md` AC-02.2.2 keeps the house number required even though the spec says no source confirms that every address has one. An employee whose address has no house number (rural address, named building, etc.) could not submit at all. Should the house number be required, optional, or allow an explicit 'no house number'?
- [minor] `stories/US-01.6-make-the-questionnaire-read-only-after-submission-and-derive.md` Before submission, can the employee save partway and come back later, and is there a review/summary of all answers before the final submit? After submission, does the employee get a confirmation? Submission is final (read-only), so these decide what the employee can check before locking it.
- [minor] `stories/US-03.1-employee-confirms-the-first-working-day.md` Are there business limits on the first working day, e.g. it must not be in the past or more than N months ahead? Is there a plausibility check on the employee's and spouse's dates of birth (minimum working age)? The pension fund only requires the DD.MM.YYYY format.
- [minor] `stories/US-03.1-employee-confirms-the-first-working-day.md` AC-03.1.2 ('the question makes clear the date must be the currently agreed one') cannot be tested as written. Is there agreed wording for the question, or a business requirement such as showing the date HR has on file?
- [minor] `stories/US-05.1-ask-nationality-and-c-permit-only-of-employees-living-in.md` Nationality (and the country of the home address and of the spouse's residence) is 'a country by English name'. Which list of countries/nationalities should be offered, and how do stateless employees or employees with unclear status answer the nationality question? Only 'Switzerland vs not' matters for the rule.
- [minor] `stories/US-05.2-ask-the-spouse-s-nationality-c-permit-and-residence-only.md` The example tables mix 'required' and 'asked' as expected results for questions the text says must be answered. Examples: spouse nationality 'required' for Tomás vs 'asked' for the registered partner; spouse residence 'required' vs 'asked'; in US-05.1, C permit 'required' for Maria vs 'asked' for Tomás. Is there a real difference (i.e. may some of these be left empty), or are they the same?
- [minor] `stories/US-05.2-ask-the-spouse-s-nationality-c-permit-and-residence-only.md` The spouse's country of residence matters only as 'lives in Switzerland or not'. Under data minimisation (G-01), should we ask the full country, or only 'Does your spouse/partner live in Switzerland? yes/no'?
- [minor] `stories/US-07.2-one-block-per-child-age-status-and-household.md` 'Minor' vs 'Adult in first education': on which date is the child's age judged? The submission date, the first working day, or the start of the tax year? A child who turns 18 around the start date would otherwise be classified differently.
- [minor] `stories/US-01.4-remind-non-swiss-employees-and-employees-living-abroad-to.md` The permit reminder is 'worded by HR', but no text is given. Who provides the final wording and when (before build or configurable later)? Is it shown only at the end, or also elsewhere (e.g. in a confirmation)?

## Technical vocabulary found in the spec (7)

- `feature.md` "Feeds the civil status entered at the fund (pension_fund_civil_status) and, for employees subject to source tax, the calculator's civil status group (calculator_civil_status)." - Internal snake_case rule ids are written into the business description of the Civil status item instead of business terms.
- `feature.md` "(The expression shows the contribution of one child; for several children the contributions are added up.)" - This refers to an internal formula/expression representation of the rule, not business language.
- `stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md` "(rule subject_to_source_tax, owned by the source tax section)" - A code-style rule identifier appears in acceptance-criterion prose.
- `stories/US-06.4-derive-the-base-source-tax-tariff-letter.md` "(per-child result, rule child_result)" - A code-style rule identifier appears in acceptance-criterion prose.
- `stories/US-06.5-replace-the-base-letter-with-the-cross-border-letter-where.md` "(rule cross_border_tariff: daily return with a certificate of residence handed in" - A code-style rule identifier appears in acceptance-criterion prose.
- `stories/US-07.1-ask-about-children-only-of-employees-who-need-a-source-tax.md` "(rule subject_to_source_tax: country of residence and, for residents of Switzerland, Swiss citizenship, C permit, civil status and spouse details)" - A code-style rule identifier appears in acceptance-criterion prose.
- `open-questions.md` "compare all inferred rows of child_result and the cross-border paths" - An internal rule identifier is used instead of the business term 'per-child result'.

## Coverage

159/342 source units cited; 146/177 facts used.

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

## Other warnings (38)

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
- [coverage] `F-pension_portal-3a97ab` fact not used anywhere in the spec: The portal requires an insurance start date on the 1st of a month but does not show how it relates to the employee's first working day (e.g. which 1st of a month to choose when work starts mid-month); the derivation rule is unknown.
- [trace_judge] `item.address_house_number` partial: The house number is listed in the full address, but 'required always' is not backed because no source says every address has a house number (as the item's own note admits).
- [trace_judge] `item.first_working_day` partial: The HR purpose 'reminder to bring the permit refers to it' is not backed by any cited fact.
- [trace_judge] `item.has_children` partial: The purpose claim that the answer possibly leads to tariff H is not backed by any cited fact.
- [trace_judge] `item.child_custody` partial: The purpose claim that sole custody counts the child, with H for single employees, is not backed by the cited facts.
- [trace_judge] `item.child_main_financial_contributor` partial: The purpose claim 'main contributor counts the child (with H for single employees)' is not backed by any cited fact; the question, options and conditions are backed.
- [trace_judge] `rule.questionnaire_flow` partial: The cited facts back the English language, canton only for Switzerland, civil status and spouse date of birth, C permit, the end reminder and the read-only and discard behaviour, and source-tax-only details. They do not back the personal details fields (names, date of birth), the address fields (street, house number, postcode, town), the confession, spouse-works and children questions, or the spouse's country of residence condition.
- [trace_judge] `rule.pension_fund_civil_status` partial: D-003 gives the partner's date of birth only for registered partnership, but the statement attaches it to Separated as well.
- [trace_judge] `rule.calculator_residence` partial: The claim that Germany and Liechtenstein have their own follow-up questions is not backed by the cited facts, which only list the residence options and the base-tariff cases.
- [trace_judge] `rule.child_result` partial: The expression disagrees with the table (e.g. single, minor not in household, no parental care, Employee contributor gives 'counts with H' in the expression but 'does not count' in the table; married, no parental care, >50% maintenance gives 'counts' in the expression), and the many 'inferred' rows rest only on D-009, which is a verification decision, not a backing fact.
- [trace_judge] `rule.cross_border_tariff` partial: The 'not Germany -> normal tariff' row cites F-zh_source_tax_calculator-f86c6b, which is not among the cited facts, and fb87f1 only covers Liechtenstein, so that row is not backed.
- [trace_judge] `rule.liechtenstein_no_source_tax` partial: The 'not Liechtenstein -> tariff code' row cites f86c6b, which is not among the cited facts; the Liechtenstein rows are backed by fb87f1, cc19c7 and D-007.
- [trace_judge] `story.US-01.1` partial: No cited fact backs asking the confession, children or spouse-works questions, or the German cross-border question details (certificate of residence, reasonable return, 60 days). The subject-to-source-tax conditions, Liechtenstein handling and country options are backed.
- [trace_judge] `story.US-01.2` partial: The fixed seven-step order in AC-01.2.1 is not stated in any cited fact; the individual conditional questions are backed, and the order of steps 5 and 6 is only implied.
- [trace_judge] `story.US-01.4` partial: The two non-illustrative examples (Tomás/Brazil, Maria/Portugal) cite transcript facts F-hr_transcript-b90bd9 and F-hr_transcript-845204 that are not among the cited facts, so they are not backed.
- [trace_judge] `story.US-02.1` partial: The cited facts don't say HR uses the name to identify the employee, and F-hr_transcript-3edf89 only weakly supports HR needing the name, since Anna elaborated only on the address.
- [trace_judge] `story.US-03.1` partial: AC-03.1.1's DD.MM.YYYY date format and the 'at Muster AG' wording are not backed by the cited facts, since the format comes from F-pension_portal-dd8126 and G-10, which are not cited here.
- [trace_judge] `story.US-06.5` partial: AC-06.5.2 says Liechtenstein residents keep the base letter, but the cited facts only cover Switzerland and 'Anderes Land' (F-f86c6b) and say nothing about Liechtenstein.
- [trace_judge] `story.US-07.2` partial: AC-07.2.1 says the questionnaire sets no maximum number of children, but the facts only say the calculator's upper limit is unknown and untested (F-4957f6, D-009), so no such product decision is cited.
- [trace_judge] `story.US-08.3` partial: AC-08.3.1's precondition that everyone living abroad is subject to source tax is not backed by any cited fact (F-hr_transcript-3f2c2a is not cited here); the rest is supported by the calculator facts, D-035 and D-001.
- [dev_refinement] `feature.md` The insurance start rule uses the 'first working day'. If the contract starts on the 1st but the first actual working day is later (weekend or holiday, e.g. contract from Sat 01.06, first day Mon 03.06), the rule gives 01.07 instead of 01.06. Should the rule use the contractual start date or the actual first working day?
- [dev_refinement] `stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md` New hires often move to Switzerland when they start, or move away from it. Is the home address the current one or the one that applies from the first working day? The country decides source-tax liability, the canton and all the cross-border questions, so the answer changes which questions are asked.
- [dev_refinement] `feature.md` In step 6 the Liechtenstein cross-border questions come after denomination, spouse employment and all the children questions. A Liechtenstein resident who returns daily (or expects at most 45 non-return days) gets 'in principle no source tax liability' and no tariff code, so their denomination, spouse-employment and children answers are not needed by any party (G-01). Should the Liechtenstein questions come first so those questions are skipped? Or, if the order stays, should those answers be discarded on submission like other answers that no longer apply? Or does HR need them anyway in case the case changes later?
- [dev_refinement] `stories/US-08.4-liechtenstein-daily-return-and-more-than-45-non-return-days.md` For Liechtenstein residents with more than 45 non-return days, the calculator returns the normal tariff plus 'Unter Vorbehalt des Doppelbesteuerungsabkommens' (subject to the double taxation agreement), per F-zh_source_tax_calculator-cc19c7. AC-08.4.3 records only 'the normal tariff code'. Should this reservation also be recorded and flagged for HR in that case?
- [dev_refinement] `stories/US-02.2-collect-a-complete-postal-home-address.md` AC-02.2.2 keeps the house number required even though the spec says no source confirms that every address has one. An employee whose address has no house number (rural address, named building, etc.) could not submit at all. Should the house number be required, optional, or allow an explicit 'no house number'?

## Run

Stages run: knowledge.raw, feature.plan, sections/SEC-03-employment-start, sections/SEC-04-civil-status-spouse, sections/SEC-02-personal-details-address, sections/SEC-05-source-tax-liability, sections/SEC-08-cross-border-residence, sections/SEC-01-questionnaire-flow, sections/SEC-06-source-tax-tariff-basics, sections/SEC-07-source-tax-children, feature.flow, judge_trace, dev_refinement, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator, judge_facts

LLM cost this run: $9.09

Tokens this run: 1,056,804 in 29 agent calls (58 input, 47,673 cache read, 824,484 cache write, 184,589 output)
