# Review: employee-onboarding

**Verdict: READY WITH CAVEATS**

Buildable: no errors, all spec examples pass, no blocking open questions. Before the build is final, the PO must decide four major refinement questions: post-submission edits, the late certificate of residence, how non-return days are counted, and the permit reminder for Swiss people living abroad. Six technical or UI leaks should be removed from feature.md. Some rule rows and ACs (AC-07.2.1, AC-08.1.2) rely on fact ids missing from their own citations or say more than the sources do. Fund-dependent questions and the inferred tariff rows remain go-live conditions.

## Reviewer findings

1. **No rule for changing answers after submission** – Only the first working day (AC-02.1.4) is covered. A move, marriage or new child could leave the source-tax status, tariff code, canton and fund civil status wrong, and engineering cannot design editing or recalculation without this.  
   Evidence: dev_refinement (major): post-submission edits; AC-02.1.4, AC-02.2.4  
   Action: Add a decision to decisions.yaml: which answers stay editable after submission and by whom (employee or HR), and whether derived results are recalculated the way AC-02.2.4 does for the insurance start date.
2. **A certificate handed in later leaves the recorded tariff wrong** – Answering 'not yet' records C1Y. Nobody updates it to N1Y when the certificate arrives, because the HR side is out of scope.  
   Evidence: dev_refinement (major); US-07.2, AC-07.2.4 'Certificate not yet provided'  
   Action: Decide who updates the answer later and whether the tariff code is recalculated, or accept the risk explicitly and add it to the exclusions.
3. **Non-return day limits are unclear for mid-year starters** – The 60-day (Germany) and 45-day (Liechtenstein) limits are 'per calendar year'. Whether the year is full, remaining or pro-rated changes the tariff and the Liechtenstein result.  
   Evidence: dev_refinement (major); US-07.2, US-07.3; calculator questions C-Q26/C-Q28  
   Action: Ask a domain expert or the Zurich tax office, then record the counting rule in decisions.yaml.
4. **Permit reminder also goes to Swiss citizens living abroad** – Nationality is not asked of people living abroad, so Swiss commuters like Stefan get a reminder that does not apply to them. This interacts with OQ-nationality-scope.  
   Evidence: dev_refinement (major); AC-08.1.1; OQ-nationality-scope; F-hr_transcript-1a20bb  
   Action: Decide together with OQ-nationality-scope: either accept the generic reminder or ask everyone 'Swiss citizen yes/no'.
5. **Technical and UI choices in the spec text** – Internal ids and UI patterns tie engineering to choices no source requires. 'English country names' has no source at all.  
   Evidence: tech_leak x6: 'Kept id permit_type for stability', rule ids pension_fund_civil_status / source_tax_civil_status / source_tax_residence in the text, date entry as DD.MM.YYYY, 'add and remove children', 'country given by its English name'; trace_judge on US-04.1, US-04.2, spouse_nationality, spouse_residence_country  
   Action: Replace rule ids with rule names and delete the permit_type note. State the business need instead of the UI: every child is described, and the fund receives the start date as DD.MM.YYYY. Drop 'English name' or move it into a decision with an owner (see the country-list question).
6. **Acceptance criteria say more than their sources** – Testers will check behaviour that no source supports.  
   Evidence: trace_judge: US-07.2 (AC-07.2.1 'Germany always makes them subject', liability fact not cited); US-08.1 (AC-08.1.2 'handed in person, nothing uploaded' beyond D-010); item.address_country (D-010 not cited)  
   Action: Cite F-hr_transcript-b6d9b3 and D-010 where they apply, or reduce AC-08.1.2 to what the sources say. If upload is out of scope, record that in decisions.yaml.
7. **Rule rows rely on fact ids missing from their own citations** – Traceability is broken for the Germany/Liechtenstein, 'not subject' and H-tariff branches. The core residence rule also adds the assumption that 'home address country' is the test for living abroad.  
   Evidence: trace_judge: source_tax_residence (31d762, e22d17), single_parent_h_tariff (c78e0c), cross_border_tariff_applies (52b67a), liechtenstein_no_source_tax_in_principle (e22d17), source_tax_result (b6d9b3); H-tariff purposes on has_children, child_parental_custody, child_main_financial_contributor; fact_judge F-hr_transcript-b6d9b3  
   Action: Add the missing facts to each rule's citations and back the H-tariff purposes with a calculator fact. Confirm with HR that 'home address country' is the test for living abroad and record it as a decision.
8. **Inferred tariff paths still need checking against the calculator** – Lonio now produces the tariff code itself (D-001). The inferred child rows, more than 3 children, H3N/P3N and the residence block for A/B/H are unverified. The single child digit also has no rule for 10 or more children.  
   Evidence: OQ-calculator-coverage; inferred rows in AC-06.2.3–AC-06.5.3; dev_refinement on child count; fact_judge partial on 3058a4 (garbled statement), 38dd4a, c2faa7, 56e79b, 50f74a  
   Action: Keep the go-live condition: a domain expert compares the computed codes with the calculator. Fix the garbled F-zh_source_tax_calculator-3058a4 and decide on a maximum or display rule for the child digit.
9. **Example tables contradict their own criteria** – The examples pass the simulation, but engineering cannot use them as reliable test cases.  
   Evidence: dev_refinement: AC-01.1.1 (names shown as 'asked' instead of 'required'), AC-05.7.2 (M0N/P1Y rows show '–'), AC-01.3.2 (Italy canton '–'), AC-02.2.4 (Julia example has no change)  
   Action: Correct the tables. Add a second row to the Julia example that shows the start date being moved.
10. **Fund-side registration questions are still open** – These do not block the build, but cross-border employees, registered partners and separated, divorced or widowed employees may be registered wrongly. Dissolved partnerships are also missing from the civil-status list.  
   Evidence: OQ-canton-abroad, OQ-civil-status-partnership, OQ-spouse-dob-other-status; dev_refinement on civil statuses; fact_judge F-pension_portal-6d3630  
   Action: Ask Pensionskasse Muster to confirm the canton for employees abroad and the civil-status mapping, and to send screenshots for Divorced and Widowed. Decide how dissolved partnerships and a deceased partner are mapped.

## Numbers

341 source units → 179 facts → 35 information items, 17 business rules → one feature with 8 sections, 28 stories, 86 acceptance criteria; 5 open questions, 10 exclusions.

## Errors (0)


## Examples executed against the knowledge model (197/197 pass)

- ✅ AC-01.1.1 / Employee living in Switzerland (spec)
- ✅ AC-01.1.1 / Employee living abroad (spec)
- ✅ AC-01.2.1 / Address in Switzerland (spec)
- ✅ AC-01.2.1 / Address in Liechtenstein (spec)
- ✅ AC-01.3.1 / Lives in Switzerland (spec)
- ✅ AC-01.3.1 / Lives in Germany (spec)
- ✅ AC-01.3.1 / Lives in Liechtenstein (spec)
- ✅ AC-01.3.1 / Lives in France (spec)
- ✅ AC-01.3.2 / Lives in Germany (spec)
- ✅ AC-01.3.2 / Lives in another country (Italy) (spec)
- ✅ AC-01.3.2 / Lives in Switzerland (spec)
- ✅ AC-01.4.1 / Lives in Switzerland (spec)
- ✅ AC-01.4.1 / Cross-border commuter living in Germany (spec)
- ✅ AC-01.4.1 / Lives in Liechtenstein (spec)
- ✅ AC-02.1.1 / Any employee - first working day asked and required (spec)
- ✅ AC-02.1.1 / Employee living abroad - first working day still asked and required (spec)
- ✅ AC-02.2.2 / Start on the 1st of a month (spec)
- ✅ AC-02.2.2 / Start on 1 January (spec)
- ✅ AC-02.2.3 / Julia (hr_transcript/F-hr_transcript-30d25c) - 15 March gives 1 April (spec)
- ✅ AC-02.2.3 / Start on the 2nd of a month (spec)
- ✅ AC-02.2.3 / Start at the end of the year (spec)
- ✅ AC-02.2.4 / Julia (hr_transcript/F-hr_transcript-d7a23b) - start moved to 15 March (spec)
- ✅ AC-03.1.1 / Employee living in Switzerland (spec)
- ✅ AC-03.1.1 / Employee living abroad (spec)
- ✅ AC-03.2.1 / Married employee (spec)
- ✅ AC-03.2.1 / Daniel (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-03.2.1 / Separated employee (spec)
- ✅ AC-03.2.2 / Single employee (spec)
- ✅ AC-03.2.2 / Divorced employee (spec)
- ✅ AC-03.2.2 / Widowed employee (spec)
- ✅ AC-03.2.4 / Changed from Married to Divorced (spec)
- ✅ AC-03.3.1 / Single (spec)
- ✅ AC-03.3.1 / Married (spec)
- ✅ AC-03.3.1 / Divorced (spec)
- ✅ AC-03.3.1 / Widowed (spec)
- ✅ AC-03.3.2 / Daniel (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-03.3.2 / Separated employee (spec)
- ✅ AC-03.4.1 / Married employee (spec)
- ✅ AC-03.4.1 / Daniel (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-03.4.2 / Single (spec)
- ✅ AC-03.4.2 / Divorced (spec)
- ✅ AC-03.4.2 / Separated (spec)
- ✅ AC-03.4.2 / Widowed (spec)
- ✅ AC-04.1.1 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.1.1 / Stefan, Swiss living abroad (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-04.1.1 / Employee living in Liechtenstein (spec)
- ✅ AC-04.1.2 / Swiss (or dual Swiss) employee living in Switzerland (spec)
- ✅ AC-04.1.3 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.1.3 / Non-Swiss employee living abroad (spec)
- ✅ AC-04.2.1 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.2.1 / Registered partner without C permit (spec)
- ✅ AC-04.2.1 / Separated employee without C permit (spec)
- ✅ AC-04.2.1 / Divorced employee without C permit (spec)
- ✅ AC-04.2.1 / Married employee with C permit (spec)
- ✅ AC-04.2.1 / Married Swiss employee (spec)
- ✅ AC-04.2.1 / Married employee living abroad (spec)
- ✅ AC-04.2.2 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.2.2 / Spouse living abroad (spec)
- ✅ AC-04.2.3 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.2.3 / Non-Swiss spouse living in Switzerland (spec)
- ✅ AC-04.2.4 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.2.4 / Registered partner with C permit living in Switzerland (spec)
- ✅ AC-04.2.4 / Non-Swiss spouse without C permit (spec)
- ✅ AC-04.2.4 / Spouse living abroad (spec)
- ✅ AC-04.2.4 / Separated employee (spec)
- ✅ AC-04.2.4 / Single employee (spec)
- ✅ AC-04.3.1 / Stefan, Swiss living abroad (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-04.3.1 / Employee living in Liechtenstein (spec)
- ✅ AC-04.3.2 / Swiss employee living in Switzerland (spec)
- ✅ AC-04.3.2 / Non-Swiss employee with C permit (spec)
- ✅ AC-04.3.2 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.3.2 / Single non-Swiss employee without C permit (spec)
- ✅ AC-04.3.2 / Separated non-Swiss employee without C permit (spec)
- ✅ AC-04.3.2 / Married, non-Swiss spouse without C permit (spec)
- ✅ AC-04.3.2 / Married, spouse living abroad (spec)
- ✅ AC-04.3.3 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.3.3 / Stefan, Swiss living abroad (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-05.3.1 / Lives abroad (other country) - subject (spec)
- ✅ AC-05.3.1 / Non-Swiss without C permit living in Switzerland - subject (spec)
- ✅ AC-05.3.1 / Swiss citizen living in Switzerland - not subject (spec)
- ✅ AC-05.3.1 / C permit holder living in Switzerland - not subject (spec)
- ✅ AC-05.3.3 / A0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-2eab9a) (spec)
- ✅ AC-05.3.3 / A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-2eab9a) (spec)
- ✅ AC-05.4.1 / Married, lives abroad (spec)
- ✅ AC-05.4.1 / Registered partnership, lives abroad (spec)
- ✅ AC-05.4.1 / Separated counts as single (spec)
- ✅ AC-05.4.1 / Single (spec)
- ✅ AC-05.4.1 / Married, living in Switzerland, spouse abroad - subject (spec)
- ✅ AC-05.4.1 / Married to a Swiss spouse living in Switzerland - not subject (spec)
- ✅ AC-05.4.2 / C0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-05.4.2 / B0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-05.4.2 / Registered partner, partner works (spec)
- ✅ AC-05.6.1 / Married, spouse works (spec)
- ✅ AC-05.6.1 / Married, spouse does not work (spec)
- ✅ AC-05.6.1 / A0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c78e0c) (spec)
- ✅ AC-05.6.1 / Separated, no children (counts as single) (spec)
- ✅ AC-05.6.1 / Single with minor child in household, sole custody (spec)
- ✅ AC-05.6.2 / L0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.6.2 / M0N (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.6.2 / N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.6.2 / P1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.6.2 / C1Y without certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-4d3ac0) (spec)
- ✅ AC-05.6.2 / No daily return, reasonable, at most 60 non-return days (spec)
- ✅ AC-05.7.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-05.7.1 / Liechtenstein, daily return (zh_source_tax_calculator/F-zh_source_tax_calculator-e80d8f) (spec)
- ✅ AC-05.7.1 / Liechtenstein, no daily return, at most 45 days (zh_source_tax_calculator/F-zh_source_tax_calculator-ab4e1e) (spec)
- ✅ AC-05.7.1 / C1Y / subject to DTA (zh_source_tax_calculator/F-zh_source_tax_calculator-ab4e1e) (spec)
- ✅ AC-05.7.1 / Lives in Germany (spec)
- ✅ AC-05.7.1 / Non-Swiss without C permit living in Switzerland (spec)
- ✅ AC-05.7.2 / N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.7.2 / M0N (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.7.2 / P1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.7.2 / A0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c78e0c) (spec)
- ✅ AC-05.7.2 / C1Y / subject to DTA (zh_source_tax_calculator/F-zh_source_tax_calculator-ab4e1e) (spec)
- ✅ AC-06.1.1 / Single employee living in Germany (spec)
- ✅ AC-06.1.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-06.1.1 / Employee subject to source tax without children (spec)
- ✅ AC-06.1.2 / Employee with children (spec)
- ✅ AC-06.1.3 / Married, child 'weder noch' -> B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-987091) (spec)
- ✅ AC-06.1.4 / Minor child (spec)
- ✅ AC-06.1.4 / Child of age in first education (spec)
- ✅ AC-06.2.1 / Minor child in household (spec)
- ✅ AC-06.2.1 / Minor child outside household (spec)
- ✅ AC-06.2.2 / Married, sole custody -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.2.2 / Single, sole custody -> H1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.2.2 / Separated employee counts as single, sole custody (spec)
- ✅ AC-06.2.3 / Married, shared custody, common household -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-3058a4) (spec)
- ✅ AC-06.2.3 / Single, common household, other parent contributes more -> A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-38dd4a) (spec)
- ✅ AC-06.2.3 / Single, common household, employee contributes more (inferred) (spec)
- ✅ AC-06.2.4 / Married, no common household, no alternating care -> C0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-3058a4) (spec)
- ✅ AC-06.2.4 / Married, alternating care, other parent contributes more -> C0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-3058a4) (spec)
- ✅ AC-06.2.4 / Single, no common household, no alternating care -> H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-38dd4a) (spec)
- ✅ AC-06.2.4 / Married, alternating care, employee contributes more (inferred) (spec)
- ✅ AC-06.2.4 / Single, alternating care, employee contributes more (inferred) (spec)
- ✅ AC-06.2.4 / Single, alternating care, other parent contributes more (inferred) (spec)
- ✅ AC-06.3.1 / Registered partner, child outside household (spec)
- ✅ AC-06.3.1 / Widowed employee, child outside household (spec)
- ✅ AC-06.3.2 / Married, no shared custody -> B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-56e79b) (spec)
- ✅ AC-06.3.2 / Single, no parental custody -> A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-c2faa7) (spec)
- ✅ AC-06.3.3 / Married, shared custody, alternating care, employee contributes more -> B1N (zh_source_tax_calculator/F-zh_source_tax_calculator-56e79b) (spec)
- ✅ AC-06.3.3 / Single, parental custody, alternating care, employee contributes more -> H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-c2faa7) (spec)
- ✅ AC-06.3.3 / Single, parental custody, no alternating care (inferred) (spec)
- ✅ AC-06.3.3 / Married, shared custody, alternating care, other parent contributes more (inferred) (spec)
- ✅ AC-06.4.1 / Married, common household with other parent (spec)
- ✅ AC-06.4.1 / Single, common household with other parent (spec)
- ✅ AC-06.4.1 / Alternating care for a child in the household (spec)
- ✅ AC-06.4.1 / No alternating care (spec)
- ✅ AC-06.4.1 / Single, child of age in first education living with both parents (spec)
- ✅ AC-06.5.1 / Married, child in first education, common household -> B1N (zh_source_tax_calculator/F-zh_source_tax_calculator-50f74a) (spec)
- ✅ AC-06.5.1 / Single, common household, employee contributes more (inferred) (spec)
- ✅ AC-06.5.1 / Single, common household, other parent contributes more (inferred) (spec)
- ✅ AC-06.5.2 / Single, in household, no common household, >50% maintenance -> H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-562299) (spec)
- ✅ AC-06.5.2 / Married, in household, no common household, >50% maintenance (inferred) (spec)
- ✅ AC-06.5.2 / In household, no common household, not mainly maintained (inferred) (spec)
- ✅ AC-06.5.3 / Single, outside household, >50% maintenance -> A1N (zh_source_tax_calculator/F-zh_source_tax_calculator-562299) (spec)
- ✅ AC-06.5.3 / Married, outside household, not mainly maintained -> B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-50f74a) (spec)
- ✅ AC-06.5.3 / Married, outside household, >50% maintenance (inferred) (spec)
- ✅ AC-06.6.1 / Married, sole custody child counts (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.6.1 / Single, H child adds one (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.6.1 / Child neither minor nor in education adds nothing (zh_source_tax_calculator/F-zh_source_tax_calculator-987091) (spec)
- ✅ AC-06.6.2 / Single, sole custody -> H1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.6.2 / Single, adult child outside household -> A1N (zh_source_tax_calculator/F-zh_source_tax_calculator-562299) (spec)
- ✅ AC-06.6.2 / Married, sole custody -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-07.1.1 / Lives in Switzerland (spec)
- ✅ AC-07.1.1 / Lives in Germany (spec)
- ✅ AC-07.1.1 / Lives in Liechtenstein (spec)
- ✅ AC-07.1.1 / Lives in France (spec)
- ✅ AC-07.1.2 / Calculator run 'Anderes Land' -> A0N (zh_source_tax_calculator/F-zh_source_tax_calculator-52b67a) (spec)
- ✅ AC-07.1.2 / Non-Swiss employee without C permit living in Switzerland (spec)
- ✅ AC-07.1.3 / Lives in Germany (spec)
- ✅ AC-07.1.3 / Lives in Liechtenstein (spec)
- ✅ AC-07.2.1 / Lives in Germany (spec)
- ✅ AC-07.2.1 / Lives in Austria (spec)
- ✅ AC-07.2.2 / Returns daily (spec)
- ✅ AC-07.2.3 / No daily return, return reasonable (spec)
- ✅ AC-07.2.3 / No daily return, return not reasonable (spec)
- ✅ AC-07.2.4 / Certificate provided -> N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-4d3ac0) (spec)
- ✅ AC-07.2.4 / No certificate -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-4d3ac0) (spec)
- ✅ AC-07.2.4 / Certificate not yet provided (spec)
- ✅ AC-07.2.4 / Return not reasonable -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-bc1639) (spec)
- ✅ AC-07.2.4 / More than 60 non-return days -> C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-b948fd) (spec)
- ✅ AC-07.2.4 / At most 60 non-return days -> N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-b948fd) (spec)
- ✅ AC-07.2.4 / Lives in Liechtenstein (spec)
- ✅ AC-07.3.1 / Returns daily (spec)
- ✅ AC-07.3.1 / Does not return daily (spec)
- ✅ AC-07.3.1 / Lives in Germany (spec)
- ✅ AC-07.3.2 / Daily return -> in principle no liability (zh_source_tax_calculator/F-zh_source_tax_calculator-e80d8f) (spec)
- ✅ AC-07.3.2 / At most 45 non-return days (zh_source_tax_calculator/F-zh_source_tax_calculator-ab4e1e) (spec)
- ✅ AC-07.3.2 / More than 45 non-return days -> C1Y subject to the agreement (zh_source_tax_calculator/F-zh_source_tax_calculator-ab4e1e) (spec)
- ✅ AC-07.3.2 / Lives in Germany (spec)
- ✅ AC-08.1.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-08.1.1 / Non-Swiss employee living in Switzerland (spec)
- ✅ AC-08.1.1 / Employee living in Germany (nationality not asked) (spec)
- ✅ AC-08.1.1 / Employee living in Liechtenstein (spec)
- ✅ AC-08.2.2 / Employee first said Married, then changed to Single (spec)
- ✅ AC-08.2.2 / Employee first entered a Swiss address, then changed to Germany (spec)
- ✅ AC-08.2.2 / Employee first entered another nationality, then changed to Switzerland (spec)

## Open questions (need your decision)

- **OQ-canton-abroad**: What must be entered in the pension fund's 'Canton' field for employees living abroad, and does 'Canton' mean canton of residence or of work? → recommended: Keep asking the canton only from residents (D-002) until a domain expert and Pensionskasse Muster confirm.
- **OQ-civil-status-partnership**: How does Pensionskasse Muster want registered partnerships and separated employees registered (the list has only Single, Married, Divorced, Widowed), and does it want the partner's details? → recommended: Verify with a domain expert / the fund; keep D-003 mapping meanwhile.
- **OQ-spouse-dob-other-status**: Does the fund's screen ask for a spouse's date of birth (or other fields) for Divorced or Widowed? → recommended: Domain expert obtains a screenshot of the fund's screen for Divorced and Widowed.
- **OQ-calculator-coverage**: Does Lonio's computed tariff code match the calculator for the paths not explored: residence block for A/B/H tariffs, more than 3 children, H3N/P3N, and the child-result rows marked inferred? → recommended: Go-live condition: compare all inferred rows and unexplored paths with the calculator.
- **OQ-nationality-scope**: Is the specific nationality (and the spouse's nationality and country of residence) needed by any party, or only whether the person is Swiss / lives in Switzerland? → recommended: Ask only the yes/no facts unless HR confirms it needs the full nationality.

## Inferred items to confirm

- item.residence_canton
- item.nationality
- item.permit_type
- item.spouse_date_of_birth
- item.spouse_residence_country
- item.spouse_nationality
- item.spouse_permit_type
- rule.source_tax_residence
- rule.child_tariff_result
- story.US-03.2
- story.US-04.1
- story.US-04.2
- story.US-06.2
- story.US-06.3
- story.US-06.5
- story.US-07.1
- fact F-pension_portal-39bab1: The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected).
- fact F-pension_portal-6d3630: Screenshots do not show whether the spouse's date of birth (or other fields) appears for 'Divorced' or 'Widowed'; only Single (no) and Married (yes) are shown.
- fact F-pension_portal-9b24c5: The civil status list has no option for registered partnership or separated; it is unclear how such employees are to be registered.
- fact F-pension_portal-b359c3: The label 'Canton' does not state whether it is the canton of residence or of work, and the list only contains Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. a cross-border commuter).
- fact F-pension_portal-3a97ab: The portal requires an insurance start date on the 1st of a month but does not say how it relates to the employee's first working day (e.g. which 1st of a month to use when work starts mid-month).

## Dev refinement questions (12)

- [major] `feature.md` Apart from the first working day (AC-02.1.4), what happens to all other answers after submission? Can the employee reopen or correct the questionnaire, for example after a move, a marriage, a new child or a corrected nationality? Or are the answers frozen and only HR can change them, and if so, which answers? Should the derived results (subject to source tax, tariff code, canton, civil status for the fund) be recalculated after a change, as AC-02.2.4 requires for the insurance start date?
- [major] `feature.md` Certificate of residence (US-07.2): 'not yet' is a valid answer and produces the normal tariff instead of the cross-border tariff. When the employee hands in the certificate later, who updates the answer, and does the recorded tariff code then change (C1Y → N1Y)? The employee cannot edit after submission, and the HR side is out of scope, so the recorded code could stay wrong. Is that acceptable?
- [major] `feature.md` Non-return days for Germany (more than 60) and Liechtenstein (more than 45) are asked 'in the calendar year'. Most new employees start mid-year. Is the threshold for the remaining part of the year, the full calendar year, or pro-rated (for start date and/or part-time work)? The answer changes whether the cross-border tariff or the Liechtenstein result applies.
- [major] `feature.md` Permit reminder (AC-08.1.1): every employee living abroad gets the reminder. That includes Swiss citizens living in Germany or Liechtenstein, such as Stefan, who have no Swiss permit. Nationality is not asked of people living abroad, so we cannot exclude them. Is a reminder that does not apply to Swiss cross-border commuters acceptable, or should nationality (or 'Swiss citizen yes/no') also be asked of employees living abroad?
- [minor] `feature.md` Does the employee see any computed result: the insurance start date, the tariff code, the Liechtenstein result, or 'not subject to source tax'? Or is everything only recorded for HR? Is there a review or summary of all answers before submission, and a confirmation after it?
- [minor] `feature.md` Children (US-06.1): if the employee answers 'yes' to having children, must they add at least one child? Is there a maximum number of children? The tariff code has a single child digit, and more than 3 children was never tested in the calculator. What should the code look like with 10 or more counting children?
- [minor] `feature.md` Are there plausibility rules for dates? For example: date of birth not in the future and a minimum age (apprentices or minors), spouse's date of birth plausible, first working day not in the past or not more than X months ahead. If the first working day is already in the past at submission, which insurance start date applies?
- [minor] `feature.md` House number is always required (AC-01.2.1). What should employees enter whose address has no house number (rural addresses abroad, named houses, PO-box-only addresses)? Are extra address lines needed for 'c/o' or apartment names, given that HR posts documents to these addresses?
- [minor] `feature.md` The civil status list (AC-03.1.2) has no 'dissolved registered partnership' and no 'partner deceased', which are official Swiss civil statuses. How should employees in those situations answer, and how are they mapped for the fund and for source tax?
- [minor] `feature.md` The example table in AC-01.1.1 shows first and last name as 'asked' (not 'required') for an employee living abroad, but the criterion says all three fields are always required. Which is correct?
- [minor] `feature.md` Several example tables contradict their own criteria or each other. In AC-05.7.2, the M0N and P1Y rows show the source tax result as '–' while the other rows show 'tariff code'. In AC-01.3.2, the Italy row shows Canton '–' instead of 'not asked'. In AC-02.2.4, the Julia example has a single row that does not actually show a change of the first working day. Can these be corrected so they can be used as test cases?
- [minor] `feature.md` The country list must cover everyone (countries by English name). Which official list should we use, for example the one the fund or HR uses? Should the list also cover nationalities such as stateless persons or refugees, whose nationality is not a country?

## Technical vocabulary found in the spec (6)

- `feature.md` "Kept id permit_type for stability; content reduced to 'C permit yes/no' (D-005)." - Names an internal field id and a stability concern about it in the spec text; field ids and their stability are engineering concerns.
- `feature.md` "Required field 'Civil status' (mapped to the fund's list, see rule pension_fund_civil_status)<br>source tax office: Decides married vs single tariff and the spouse exemption (see rule source_tax_civil_status)" - Refers to internal rule identifiers (snake_case ids) in the business text instead of the rule names.
- `feature.md` "The calculator's questions 'main residence in Switzerland?' and 'state of residence' are derived from this answer, not asked again (see rule source_tax_residence)." - Another internal snake_case rule id in the prose.
- `feature.md` "they are asked for their first working day as a date (DD.MM.YYYY)" - Prescribes the format in which the employee enters the first working day. The fund's DD.MM.YYYY requirement applies to the insurance start date it receives, not to how the employee enters a date; the input format is a UI choice.
- `feature.md` "the employee can add and remove children, and for each child is asked" - Prescribes the interaction pattern (add/remove child blocks, copied from the calculator's buttons). The business need is only that every child is described; how the UI collects them is up to engineering.
- `feature.md` "with the country given by its English name (e.g. "Switzerland", "Germany")" - Prescribes how country values are represented, and the trace check notes no source backs it. It reads as a representation choice rather than a stakeholder requirement.

## Coverage

167/341 source units cited; 145/179 facts used.

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
- pension_portal/S01-E11: Please select
- pension_portal/S01-E16: Please select
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
- pension_portal/S07-E22: DD.MM.YYYY
- pension_portal/S07-E24: Cancel
- pension_portal/S07-E25: Register
- pension_portal/S07-E26: Fields marked * are required.
- zh_source_tax_calculator/C-Q24: Tägliche Rückkehr an den Hauptwohnsitz in Deutschland während oder vor Bezug der Ersatzeinkünfte? Options: Ja | Nein
- zh_source_tax_calculator/C-Q25: Tägliche Rückkehr grundsätzlich zumutbar während oder vor Bezug der Ersatzeinkünfte (weniger als 100km Fahrdistanz)? Options: Ja | Nein
- zh_source_tax_calculator/C-Q26: Nachweis von mehr als 60 beruflich bedingten Nichtrückkehrtagen im Kalenderjahr beigebracht während oder vor Bezug der Ersatzeinkünfte? Options: Ja | Nein
- zh_source_tax_calculator/C-Q27: Tägliche Rückkehr an den Hauptwohnsitz in Liechtenstein während oder vor Bezug der Ersatzeinkünfte? Options: Ja | Nein
- zh_source_tax_calculator/C-Q28: Mehr als 45 beruflich bedingte Nichtrückkehrtage im Kalenderjahr während oder vor Bezug der Ersatzeinkünfte? Options: Ja | Nein
- zh_source_tax_calculator/C-V04: Answers {"Q01": "Erwerbseinkommen", "Q02": "Verheiratet oder eingetragene Partnerschaft", "Q03": "Keine oder andere", "Q04": "Nein", "Q05": "Nein", "Q16": "Ja"}
- zh_source_tax_calculator/C-V06: Answers {"Q01": "Erwerbseinkommen", "Q02": "Verheiratet oder eingetragene Partnerschaft", "Q03": "Keine oder andere", "Q04": "Ja", "Q05": "Nein", "Q16": "Ja"} -
- zh_source_tax_calculator/C-V08: Answers {"Q01": "Erwerbseinkommen", "Q02": "Verheiratet oder eingetragene Partnerschaft", "Q03": "Keine oder andere", "Q04": "Nein", "Q05": "Ja", "Q07": "Minder
- zh_source_tax_calculator/C-V24: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "weder noch", "Q16": "Ja"} 
- zh_source_tax_calculator/C-V25: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "Minderjährig (Kind 1) + Mi
- zh_source_tax_calculator/C-V41: Answers {"Q01": "Erwerbseinkommen", "Q02": "Verheiratet oder eingetragene Partnerschaft", "Q03": "röm.-kath., christ.-kath., evang.-ref.", "Q04": "Ja", "Q05": "
- zh_source_tax_calculator/C-N01: The calculator is an Angular app (app-root, ng 11, assets from www.services.zh.ch/app/quest/tarifbestimmung/prod/) rendered inline in the section 'Tarifrechner 
- zh_source_tax_calculator/C-N08: The answer value in V25–V29 summarises repeated per-child answers (Kind 1/2/3) because the schema allows one value per question id.

## Other warnings (34)

- [fact_judge] `F-hr_transcript-a45422` partial: Anna says she checks the spouse case by hand and asks for spouse details by email (takes forever), but 'HR' generalization is fine; mostly supported, though 'by hand' and 'email' are two separate remarks. | Today HR checks the spouse case by hand and asks for spouse details by email, which takes forever.
- [fact_judge] `F-hr_transcript-b6d9b3` partial: Consolidated rule is a reasonable synthesis, but 'home address country' as the abroad test is an added assumption, and the spouse exception's interaction with C permit/abroad is inferred. | Consolidated final rule: an employee is subject to source tax if they live abroad (home address country not Switzerland), regardless of nationality. If they live in Switzerland, they are subject only if they are not Swiss and do not hold a C permit, unless they are married to a spouse who is Swiss or holds a C permit and lives in Switzerland (then not subject).
- [fact_judge] `F-hr_transcript-d5c04b` partial: Leo said he'd come back this week once screenshots are gone through; 'respond' is fine but it's a commitment on timing, not a stated answer — essentially supported. | Anna asked about timing; Leo will respond this week after reviewing the screenshots.
- [fact_judge] `F-pension_portal-39bab1` partial: Units support Single (absent) vs Married (present), but screenshots 01, 02, 03 and 06 are not among the units, so their absence of the field isn't verifiable. | The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected).
- [fact_judge] `F-pension_portal-3cfe89` partial: Footnote supports the asterisk rule, but the cited units don't show that all visible fields carry the marker. | Fields marked with an asterisk are required; all visible fields on the form carry the marker.
- [fact_judge] `F-pension_portal-6d3630` partial: Units show the Divorced/Widowed options but not which screenshots exist, so the absence claim is a plausible but unverified reading. | Screenshots do not show whether the spouse's date of birth (or other fields) appears for 'Divorced' or 'Widowed'; only Single (no) and Married (yes) are shown.
- [fact_judge] `F-zh_source_tax_calculator-351289` partial: The skip to Q16 is stated, but these units never say Q16 is the main-residence question. | If the income type is 'Ersatzeinkünfte', all personal and child questions are skipped and the calculator goes straight to the main-residence question (Q16).
- [fact_judge] `F-zh_source_tax_calculator-c78e0c` partial: Single, no children gives A0Y/A0N in test vectors, but the 'resident in Switzerland' condition is not shown in these units (Q16=Ja is not explained). | A person with civil status 'Ledig, Geschieden, Getrennt, Verwitwet' and no counting children, resident in Switzerland, gets tariff letter A (e.g. A0Y / A0N).
- [fact_judge] `F-zh_source_tax_calculator-3058a4` partial: The V09-V11 outcomes match, but the statement is garbled and unfinished ('counts the child only if...'). The units also don't label Q10 or Q11 as common household or alternating care. | Married person, minor child in same household, shared custody: common household with the other parent counts the child (C1Y); no common household counts the child only if... observed: alternating care with other parent as main contributor -> 0 (C0Y), no alternating care -> 0 (C0Y).
- [fact_judge] `F-zh_source_tax_calculator-56e79b` partial: Vectors V12/V13 show B1N vs B0N on Q13 Ja/Nein, but the question labels (shared custody, alternating care) are not given in these units. | Married person, minor child not in household: shared custody + alternating care + person is main contributor counts the child (B1N); no shared custody does not count it (B0N).
- [fact_judge] `F-zh_source_tax_calculator-50f74a` partial: Outcomes in V14/V15 match, but meanings of Q10 (common household) and Q15 are not stated in these units. | Married person, adult child in first education: in same household with common household with other parent counts (B1N); not in household and not mainly maintained (Q15 = Nein) does not count (B0N).
- [fact_judge] `F-zh_source_tax_calculator-38dd4a` partial: V18 and V19 give A0N and H1N, but the meaning of Q10/Q11 (common household, alternating care) is inferred, not labelled. | Single person, minor child in household with shared custody: common household with other parent and other parent main contributor -> A0N (not counted); no common household and no alternating care -> H1N.
- [fact_judge] `F-zh_source_tax_calculator-c2faa7` partial: V20 and V21 give H1N and A0N, but the meaning of Q14/Q11 (parental care, alternating care) is not labelled in these units. | Single person, minor child not in household: parental care Ja + alternating care + person main contributor -> H1N; parental care Nein -> A0N.
- [trace_judge] `item.address_country` partial: The claim that country decides whether the permit reminder is shown is not backed by any cited fact (D-010 is not cited here).
- [trace_judge] `item.spouse_residence_country` partial: The asking condition and the source-tax purpose are backed, but the form 'Countries by English name' is not supported by any cited fact.
- [trace_judge] `item.spouse_nationality` partial: The asking condition, the Swiss-citizenship rule (D-008) and the purpose are backed, but the form 'Countries by English name' is not supported by any cited fact.
- [trace_judge] `item.has_children` partial: The purpose mentions the 'H tariff', which none of the cited facts mention.
- [trace_judge] `item.child_parental_custody` partial: The purpose 'Sole custody counts the child (H for single employees)' is not backed by the cited facts; the question, options and condition are.
- [trace_judge] `item.child_shared_custody_not_in_household` partial: The needed_by purpose 'No shared custody: child does not count' is not stated in any cited fact; the question, options and conditions are backed.
- [trace_judge] `item.child_parental_care_not_in_household` partial: The needed_by purpose 'No parental custody: child does not count' is not backed by the cited facts; the question, options and conditions are backed.
- [trace_judge] `item.child_main_financial_contributor` partial: The purpose mentions 'H tariff', which no cited fact supports; the question, options, conditions and the married exclusion are backed.
- [trace_judge] `rule.source_tax_residence` partial: The Germany and Liechtenstein rows (the cross-border questions) cite F-zh_source_tax_calculator-31d762 and -e22d17, which are not among the cited facts supplied, so only the Switzerland and other-country rows are backed.
- [trace_judge] `rule.single_parent_h_tariff` partial: The 'single, no H child -> no H tariff' row cites F-...-c78e0c, which is not among the cited facts, and 97139a does not explicitly say married persons get no H tariff.
- [trace_judge] `rule.cross_border_tariff_applies` partial: The 'not Germany -> normal tariff' row cites F-...-52b67a, which is not among the cited facts, and 89a9f1 only covers German residence.
- [trace_judge] `rule.liechtenstein_no_source_tax_in_principle` partial: The 'not Liechtenstein -> not applicable' row cites F-...-e22d17, which is not among the cited facts; the other rows are backed by e80d8f, ab4e1e and D-007.
- [trace_judge] `rule.source_tax_result` partial: The 'not subject to source tax -> no result' row cites F-hr_transcript-b6d9b3, which is not among the cited facts, so that row and the matching statement sentence are not backed.
- [trace_judge] `story.US-04.1` partial: No cited fact says the nationality list is 'countries by English name'.
- [trace_judge] `story.US-04.2` partial: No cited fact says the spouse residence and nationality lists are 'countries by English name'; the rest is backed.
- [trace_judge] `story.US-07.2` partial: AC-07.2.1 says living in Germany 'always makes them subject to source tax', but none of the cited facts (the HR transcript fact on liability is not cited here) back that claim.
- [trace_judge] `story.US-08.1` partial: AC-08.1.2 claims the permit is handed to HR in person outside Lonio and that nothing must be answered, confirmed or uploaded, but D-010 and the HR quotes only say to remind people to bring the permit; D-008 is also scoped to source tax, not the reminder.
- [dev_refinement] `feature.md` Apart from the first working day (AC-02.1.4), what happens to all other answers after submission? Can the employee reopen or correct the questionnaire, for example after a move, a marriage, a new child or a corrected nationality? Or are the answers frozen and only HR can change them, and if so, which answers? Should the derived results (subject to source tax, tariff code, canton, civil status for the fund) be recalculated after a change, as AC-02.2.4 requires for the insurance start date?
- [dev_refinement] `feature.md` Certificate of residence (US-07.2): 'not yet' is a valid answer and produces the normal tariff instead of the cross-border tariff. When the employee hands in the certificate later, who updates the answer, and does the recorded tariff code then change (C1Y → N1Y)? The employee cannot edit after submission, and the HR side is out of scope, so the recorded code could stay wrong. Is that acceptable?
- [dev_refinement] `feature.md` Non-return days for Germany (more than 60) and Liechtenstein (more than 45) are asked 'in the calendar year'. Most new employees start mid-year. Is the threshold for the remaining part of the year, the full calendar year, or pro-rated (for start date and/or part-time work)? The answer changes whether the cross-border tariff or the Liechtenstein result applies.
- [dev_refinement] `feature.md` Permit reminder (AC-08.1.1): every employee living abroad gets the reminder. That includes Swiss citizens living in Germany or Liechtenstein, such as Stefan, who have no Swiss permit. Nationality is not asked of people living abroad, so we cannot exclude them. Is a reminder that does not apply to Swiss cross-border commuters acceptable, or should nationality (or 'Swiss citizen yes/no') also be asked of employees living abroad?

## Run

Stages run: knowledge.raw, feature.plan, sections/SEC-02-start-date-insurance, sections/SEC-03-civil-status-spouse, sections/SEC-01-identity-and-address, sections/SEC-08-completion-and-submission, sections/SEC-04-source-tax-liability, sections/SEC-05-tariff-basics, sections/SEC-07-living-abroad, sections/SEC-06-children, judge_trace, dev_refinement, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator, judge_facts

LLM cost this run: $8.6
