# Review: employee-onboarding

**Verdict: READY WITH CAVEATS**

Ready with caveats. Nothing blocks the build: there are no errors, all spec examples pass, and none of the 4 open questions or dev-refinement questions is marked blocking. Before refinement, the product owner should: (1) decide the Liechtenstein 'no liability' flow and what is recorded for it; (2) fix the Separated civil-status contradiction; (3) repair the rule rows that cite facts outside their cited set; (4) remove 4 small technical leaks from the spec text; (5) answer 7 major refinement questions (scope across customers, date rules, prefill of the first working day, saving and resuming, thresholds for mid-year starters, ownership of the reminder text). The child-tariff paths marked inferred and the questions for the pension fund stay as conditions before go-live.

## Reviewer findings

1. **Liechtenstein 'no source tax liability' flow is undefined** – These employees may be asked tariff questions no one needs (against G-01), and it is unclear whether 'Subject to source tax' is recorded as yes or no. That changes what HR sees.  
   Evidence: dev_refinement (major) on US-05.7; AC-05.7.3 examples show '–' for denomination and children, but step 6 asks those questions before the Liechtenstein daily-return question.  
   Action: Add a decision to decisions.yaml: ask the Liechtenstein daily-return and 45-day questions first, skip the tariff questions when the result is 'no liability', and state the value recorded for 'Subject to source tax'.
2. **Separated civil status contradicts itself on the spouse's date of birth** – The fund registration for separated employees would be wrong either way.  
   Evidence: trace_judge rule.pension_fund_civil_status: D-003 says Married without the spouse's date of birth, but the Separated row asks for it. OQ-civil-status-partnership says 'both as Married with spouse/partner date of birth'.  
   Action: Make D-003, D-004, the rule row and the open-question text say the same thing. Keep the mapping as provisional until the fund confirms it.
3. **Rule rows cite facts outside their cited set** – These are traceability gaps: some outcome rows have no backing in the facts they cite.  
   Evidence: trace_judge rule.source_tax_result (b6d9b3), rule.cross_border_tariff_applies (bc1639, 52b67a), rule.single_parent_h_tariff (c78e0c), rule.source_tax_residence (Germany/Liechtenstein questions); US-04.2, US-05.4, US-06.1 and US-08.1 do not cite d7431e/b6d9b3; US-08.3 names the Julia incident without citing it.  
   Action: Add the missing fact references to the rules and stories, then rerun trace_judge.
4. **Child-tariff paths are inferred and the 'H tariff' purpose has no source** – Lonio now owns the tariff result, so an unverified path can produce a wrong tariff code.  
   Evidence: inferred_items: rule.child_tariff_result and US-06.2, 06.3, 06.5, 06.6; examples marked '(inferred, to verify)'; trace_judge on 8 child items (H tariff purpose); OQ-calculator-coverage; several partial fact_judge results on calculator facts (Q10, Q11, Q14 and Q15 labels).  
   Action: Keep D-009 as a go-live gate. A domain expert compares the computed codes with the calculator for every inferred row. Add a fact or decision that backs the H tariff purpose.
5. **Scope: Muster AG only, or every Lonio customer?** – This decides whether the fund field list, canton or calculator, and reminder text are hard-coded or set per customer.  
   Evidence: dev_refinement (major) on feature.md.  
   Action: State the scope in feature.md, or record it as a decision. If the questionnaire serves every customer, list which parts each customer can set up.
6. **Technical decisions leak into the spec** – UI and modelling choices belong to engineering.  
   Evidence: tech_leak: information.md 'Country by English name…' and 'Expression describes one child'; US-02.1 'DD.MM.YYYY'; US-06.1 'add/remove a child, the child questions repeat'.  
   Action: Rewrite these as business needs: a country of residence, a date, facts collected per child. Keep DD.MM.YYYY only as the fund's output format.
7. **No date rules, and the first-working-day field is unclear** – The insurance start date is derived from unchecked dates, and it is unknown whether the first working day is prefilled by HR.  
   Evidence: dev_refinement (major) on information.md and US-02.1; coverage: F-pension_portal-3a97ab (how the insurance start date relates to the first working day) is not used anywhere in the spec.  
   Action: Decide the allowed ranges for the first working day and the dates of birth, and whether the first working day is prefilled and from where. Cite 3a97ab where the insurance start date is derived.
8. **Cross-border day thresholds for mid-year starters** – Using the full 60 or 45 days, or a pro-rated number, changes both the question wording and the tariff.  
   Evidence: dev_refinement (major) on US-07.2; there is also a minor question about 'not yet' versus 'no' for the certificate of residence.  
   Action: Get the rule from a domain expert and record it as a decision. Decide whether 'not yet' creates a follow-up for HR.
9. **Saving and resuming, and who owns the reminder text** – Both decide whether more features are in scope: saving answers, reminders, HR editing of text.  
   Evidence: dev_refinement (major) on feature.md (resume, deadline, reminders) and US-08.1 (HR wording of the permit reminder).  
   Action: Decide whether a saved draft and a deadline or reminder are in scope. Get one fixed reminder text from HR, or mark HR editing as excluded.
10. **Questions for the pension fund are still open** – The fund's required 'Canton' field, and any hidden field for divorced or widowed employees, could block a registration.  
   Evidence: OQ-canton-abroad (D-002), OQ-spouse-dob-other-status (D-004); fact_judge partial F-pension_portal-6d3630 and 39bab1.  
   Action: Ask Pensionskasse Muster to confirm what 'Canton' means and what to enter for employees abroad, and get screenshots for Divorced and Widowed. Close both before go-live.

## Numbers

341 source units → 179 facts → 35 information items, 17 business rules → one feature with 8 sections, 29 stories, 84 acceptance criteria; 4 open questions, 9 exclusions.

## Impact of this run

Stories added: -; changed: -; removed: -; unchanged: 29.

Knowledge elements changed: -

## Errors (0)


## Examples executed against the knowledge model (215/215 pass)

- ✅ AC-01.1.1 / Any employee, whatever their residence (illustrative) (spec)
- ✅ AC-01.1.2 / Employee living in Switzerland (illustrative) (spec)
- ✅ AC-01.2.1 / Employee living in Switzerland (illustrative) (spec)
- ✅ AC-01.2.1 / Employee living in Germany (illustrative) (spec)
- ✅ AC-01.3.2 / Employee living in Konstanz, Germany (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-01.3.2 / Employee living in Liechtenstein (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-01.3.2 / Employee living in another country, e.g. France (illustrative) (spec)
- ✅ AC-01.3.2 / Employee living in Switzerland (illustrative) (spec)
- ✅ AC-01.4.1 / Employee living in Winterthur, Switzerland (illustrative) (spec)
- ✅ AC-01.4.1 / Employee living in Konstanz, Germany (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-01.4.1 / Employee living in Liechtenstein (illustrative) (spec)
- ✅ AC-02.1.1 / Employee living in Switzerland (spec)
- ✅ AC-02.1.1 / Employee living abroad (spec)
- ✅ AC-02.2.1 / Start on the 1st of May (spec)
- ✅ AC-02.2.1 / Start on the 1st of January (spec)
- ✅ AC-02.2.2 / Julia (hr_transcript/F-hr_transcript-30d25c) - 15 March; year assumed (spec)
- ✅ AC-02.2.2 / Start on the 2nd of a month (spec)
- ✅ AC-02.2.2 / Start in late December (year end) (spec)
- ✅ AC-02.2.3 / Julia (hr_transcript/F-hr_transcript-d7a23b) - date moved to 15 March; year assumed (spec)
- ✅ AC-03.1.1 / Single employee (spec)
- ✅ AC-03.1.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-03.2.1 / Married employee (spec)
- ✅ AC-03.2.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-03.2.1 / Separated employee (spec)
- ✅ AC-03.2.1 / Single employee (spec)
- ✅ AC-03.2.1 / Divorced employee (spec)
- ✅ AC-03.2.1 / Widowed employee (spec)
- ✅ AC-03.2.3 / Changed from Married to Divorced (spec)
- ✅ AC-03.3.1 / Single (spec)
- ✅ AC-03.3.1 / Married (spec)
- ✅ AC-03.3.1 / Divorced (spec)
- ✅ AC-03.3.1 / Widowed (spec)
- ✅ AC-03.3.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-03.3.1 / Separated (spec)
- ✅ AC-03.4.1 / Married (spec)
- ✅ AC-03.4.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-03.4.1 / Single (spec)
- ✅ AC-03.4.1 / Divorced (spec)
- ✅ AC-03.4.1 / Widowed (spec)
- ✅ AC-03.4.1 / Separated (spec)
- ✅ AC-03.4.2 / Separated employee (spec)
- ✅ AC-04.1.1 / Employee living in Switzerland (spec)
- ✅ AC-04.1.1 / Employee living in Konstanz, Germany (F-hr_transcript-1a20bb) (spec)
- ✅ AC-04.1.1 / Employee living in Liechtenstein (F-hr_transcript-1a20bb) (spec)
- ✅ AC-04.1.3 / Non-Swiss employee living in Switzerland (spec)
- ✅ AC-04.1.3 / Swiss employee living in Switzerland (spec)
- ✅ AC-04.1.3 / Employee living in Konstanz, Germany (F-hr_transcript-1a20bb) (spec)
- ✅ AC-04.2.1 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.2.1 / Registered partnership, non-Swiss without C permit (spec)
- ✅ AC-04.2.1 / Separated, non-Swiss without C permit (spec)
- ✅ AC-04.2.1 / Divorced, non-Swiss without C permit (spec)
- ✅ AC-04.2.1 / Married, non-Swiss with C permit (spec)
- ✅ AC-04.2.1 / Married Swiss citizen living in Switzerland (spec)
- ✅ AC-04.2.1 / Married employee living in Germany (spec)
- ✅ AC-04.2.2 / Non-Swiss spouse (spec)
- ✅ AC-04.2.2 / Tomás - Swiss wife (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.2.3 / Tomás - Swiss wife (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.2.3 / Non-Swiss spouse with C permit (spec)
- ✅ AC-04.2.3 / Non-Swiss spouse without C permit (spec)
- ✅ AC-04.2.4 / Tomás - Swiss wife living in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.2.4 / Registered partner is Swiss and lives in Switzerland (spec)
- ✅ AC-04.2.4 / Spouse with C permit living in Switzerland (spec)
- ✅ AC-04.2.4 / Swiss spouse living in another country (spec)
- ✅ AC-04.2.4 / C-permit spouse living in another country (spec)
- ✅ AC-04.2.4 / Non-Swiss spouse without C permit (spec)
- ✅ AC-04.2.4 / Single employee (spec)
- ✅ AC-04.2.4 / Separated employee (counts as single) (spec)
- ✅ AC-04.3.1 / Employee living in Konstanz, Germany (F-hr_transcript-1a20bb) (spec)
- ✅ AC-04.3.1 / Employee living in Liechtenstein (F-hr_transcript-1a20bb) (spec)
- ✅ AC-04.3.1 / Employee living in another country (spec)
- ✅ AC-04.3.2 / Swiss citizen (including dual citizens) living in Switzerland (spec)
- ✅ AC-04.3.2 / Non-Swiss with C permit living in Switzerland (spec)
- ✅ AC-04.3.2 / Tomás - Brazilian, B permit, Swiss wife, Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.3.2 / Single non-Swiss without C permit (spec)
- ✅ AC-04.3.2 / Married, Swiss spouse living in another country (spec)
- ✅ AC-04.3.2 / Separated non-Swiss without C permit (counts as single) (spec)
- ✅ AC-04.3.3 / Employee living in Konstanz, Germany (F-hr_transcript-1a20bb) (spec)
- ✅ AC-04.3.3 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.3.3 / Single non-Swiss without C permit living in Switzerland (spec)
- ✅ AC-05.3.1 / Tomás - Brazilian, B permit, Swiss wife, living in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-05.3.1 / Employee living in Germany (spec)
- ✅ AC-05.3.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-05.3.1 / Non-Swiss with C permit living in Switzerland (spec)
- ✅ AC-05.3.1 / Non-Swiss without C permit, single, living in Switzerland (spec)
- ✅ AC-05.3.3 / Recognised church member living in Germany (spec)
- ✅ AC-05.3.3 / No or other denomination, living in Germany (spec)
- ✅ AC-05.4.1 / Tomás - exempt through his Swiss wife living in Switzerland (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-05.4.1 / Married employee living in Germany (spec)
- ✅ AC-05.4.1 / Registered partner living in Germany (spec)
- ✅ AC-05.4.1 / Separated employee living in Germany (spec)
- ✅ AC-05.4.1 / Divorced employee living in Germany (spec)
- ✅ AC-05.4.1 / Married non-Swiss without C permit in Switzerland, spouse also non-Swiss without C permit (spec)
- ✅ AC-05.4.3 / Married, spouse works, living in Germany (spec)
- ✅ AC-05.4.3 / Registered partner, partner does not work, living in Germany (spec)
- ✅ AC-05.6.1 / Married non-Swiss without C permit in Switzerland, spouse works (spec)
- ✅ AC-05.6.1 / Registered partner in Switzerland, partner does not work (spec)
- ✅ AC-05.6.1 / Married, living in Germany, daily return not reasonable (normal tariff) (spec)
- ✅ AC-05.6.2 / Single without children in Switzerland (spec)
- ✅ AC-05.6.2 / Separated without children in Switzerland (spec)
- ✅ AC-05.6.2 / Divorced with a minor child in the household under sole custody (spec)
- ✅ AC-05.6.3 / Calculator example L0Y: single, Germany, daily return, certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.6.3 / Calculator example M0N: married, spouse not employed, Germany, daily return, certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.6.3 / Calculator example N1Y: married, spouse employed, Germany, daily return, certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.6.3 / Calculator example P1Y: single parent, Germany, daily return, certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.6.3 / Married, Germany, no daily return, return reasonable, not more than 60 non-return days (spec)
- ✅ AC-05.6.3 / Married, Germany, no daily return, more than 60 non-return days (normal tariff) (spec)
- ✅ AC-05.6.3 / Single, Germany, daily return, certificate not yet handed in (normal tariff) (spec)
- ✅ AC-05.6.4 / Swiss citizen living in Switzerland (spec)
- ✅ AC-05.7.1 / Calculator example L0Y (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.7.1 / Calculator example M0N (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.7.1 / Calculator example N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.7.1 / Calculator example A0Y: single, resident in Switzerland, no children (zh_source_tax_calculator/F-zh_source_tax_calculator-c78e0c) (spec)
- ✅ AC-05.7.2 / Tomás - Brazilian, B permit, Swiss wife, living in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-05.7.2 / Swiss citizen living in Switzerland (spec)
- ✅ AC-05.7.3 / Liechtenstein, daily return (spec)
- ✅ AC-05.7.3 / Liechtenstein, no daily return, not more than 45 non-return days (spec)
- ✅ AC-05.7.3 / Calculator example C1Y subject to the double taxation agreement: Liechtenstein, more than 45 non-return days (zh_source_tax_calculator/F-zh_source_tax_calculator-ab4e1e) (spec)
- ✅ AC-06.1.1 / Non-Swiss single employee in Switzerland without C permit (spec)
- ✅ AC-06.1.1 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-06.1.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-06.1.1 / Employee living in Germany (spec)
- ✅ AC-06.1.2 / Has children (spec)
- ✅ AC-06.1.2 / No children (spec)
- ✅ AC-06.1.3 / Calculator run 'weder noch' gives B0N (zh_source_tax_calculator/F-zh_source_tax_calculator-987091) (spec)
- ✅ AC-06.1.4 / Minor child (spec)
- ✅ AC-06.1.4 / Child of age in first education (spec)
- ✅ AC-06.2.1 / Minor child in household (spec)
- ✅ AC-06.2.1 / Minor child outside household (spec)
- ✅ AC-06.2.2 / Calculator run C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.2.2 / Calculator run H1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.2.2 / Separated employee with sole custody (counts as single, D-003) (spec)
- ✅ AC-06.2.3 / Shared custody, asks common household (spec)
- ✅ AC-06.2.3 / No common household, asks alternating care (spec)
- ✅ AC-06.2.3 / Common household, no alternating care question (spec)
- ✅ AC-06.2.4 / Calculator run C1Y, common household (zh_source_tax_calculator/F-zh_source_tax_calculator-3058a4) (spec)
- ✅ AC-06.2.4 / Calculator run C0Y, no alternating care (zh_source_tax_calculator/F-zh_source_tax_calculator-3058a4) (spec)
- ✅ AC-06.2.4 / Calculator run C0Y, other parent main contributor (zh_source_tax_calculator/F-zh_source_tax_calculator-3058a4) (spec)
- ✅ AC-06.2.4 / Alternating care, employee main contributor (inferred, to verify) (spec)
- ✅ AC-06.2.5 / Common household, employee main contributor (zh_source_tax_calculator/F-zh_source_tax_calculator-96658b) (spec)
- ✅ AC-06.2.5 / Calculator run A0N, common household, other parent contributes more (zh_source_tax_calculator/F-zh_source_tax_calculator-38dd4a) (spec)
- ✅ AC-06.2.5 / Calculator run H1N, no common household, no alternating care (zh_source_tax_calculator/F-zh_source_tax_calculator-38dd4a) (spec)
- ✅ AC-06.2.5 / Alternating care, employee main contributor (zh_source_tax_calculator/F-zh_source_tax_calculator-96658b) (spec)
- ✅ AC-06.2.5 / Alternating care, other parent main contributor (inferred, to verify) (spec)
- ✅ AC-06.3.1 / Married employee, child outside household (spec)
- ✅ AC-06.3.1 / Separated employee, child outside household (counts as single, D-003) (spec)
- ✅ AC-06.3.2 / Calculator run B0N, no shared custody (zh_source_tax_calculator/F-zh_source_tax_calculator-56e79b) (spec)
- ✅ AC-06.3.2 / Calculator run A0N, no parental custody (zh_source_tax_calculator/F-zh_source_tax_calculator-c2faa7) (spec)
- ✅ AC-06.3.2 / Single employee with parental custody (spec)
- ✅ AC-06.3.3 / Calculator run B1N (zh_source_tax_calculator/F-zh_source_tax_calculator-56e79b) (spec)
- ✅ AC-06.3.3 / Calculator run H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-c2faa7) (spec)
- ✅ AC-06.3.3 / Married, other parent contributes more (inferred, to verify) (spec)
- ✅ AC-06.3.3 / Married, no alternating care (inferred, to verify) (spec)
- ✅ AC-06.3.3 / Single, other parent contributes more (inferred, to verify) (spec)
- ✅ AC-06.3.3 / Single, no alternating care (inferred, to verify) (spec)
- ✅ AC-06.4.1 / Married, child in household, alternating care (spec)
- ✅ AC-06.4.1 / Single, child outside household, alternating care (spec)
- ✅ AC-06.4.1 / No alternating care (spec)
- ✅ AC-06.4.2 / Single, minor child, common household (spec)
- ✅ AC-06.4.2 / Single, child of age in first education, common household (spec)
- ✅ AC-06.4.2 / Married, common household (spec)
- ✅ AC-06.5.1 / Child in household (spec)
- ✅ AC-06.5.1 / Child in household, no common household (spec)
- ✅ AC-06.5.1 / Child outside household (spec)
- ✅ AC-06.5.2 / Calculator run B1N, common household (zh_source_tax_calculator/F-zh_source_tax_calculator-50f74a) (spec)
- ✅ AC-06.5.2 / Calculator run B0N, outside household, not mainly maintained (zh_source_tax_calculator/F-zh_source_tax_calculator-50f74a) (spec)
- ✅ AC-06.5.2 / Outside household, mainly maintained (inferred, to verify) (spec)
- ✅ AC-06.5.2 / In household, no common household, mainly maintained (inferred, to verify) (spec)
- ✅ AC-06.5.2 / In household, no common household, not mainly maintained (inferred, to verify) (spec)
- ✅ AC-06.5.3 / Calculator run H1N, in household, mainly maintained (zh_source_tax_calculator/F-zh_source_tax_calculator-562299) (spec)
- ✅ AC-06.5.3 / Calculator run A1N, outside household, mainly maintained (zh_source_tax_calculator/F-zh_source_tax_calculator-562299) (spec)
- ✅ AC-06.5.3 / Common household, employee contributes more (inferred, to verify) (spec)
- ✅ AC-06.5.3 / Common household, other parent contributes more (inferred, to verify) (spec)
- ✅ AC-06.5.3 / In household, not mainly maintained (inferred, to verify) (spec)
- ✅ AC-06.5.3 / Outside household, not mainly maintained (inferred, to verify) (spec)
- ✅ AC-06.6.1 / One child counting (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.6.1 / One child counting with H (zh_source_tax_calculator/F-zh_source_tax_calculator-38dd4a) (spec)
- ✅ AC-06.6.1 / Child does not count (zh_source_tax_calculator/F-zh_source_tax_calculator-56e79b) (spec)
- ✅ AC-06.6.1 / No children (spec)
- ✅ AC-06.6.2 / Calculator run H1Y, sole custody (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.6.2 / Calculator run A1N, child counts without H (zh_source_tax_calculator/F-zh_source_tax_calculator-562299) (spec)
- ✅ AC-06.6.2 / Married employee with sole custody child (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.6.2 / Single employee without children (spec)
- ✅ AC-07.1.1 / Tomás, living in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-07.1.1 / Employee living in Germany (spec)
- ✅ AC-07.1.1 / Employee living in Liechtenstein (spec)
- ✅ AC-07.1.1 / Employee living in another country (spec)
- ✅ AC-07.1.2 / Employee living in another country (spec)
- ✅ AC-07.1.2 / Employee living in Switzerland (spec)
- ✅ AC-07.2.1 / Employee living in Germany (spec)
- ✅ AC-07.2.1 / Employee living in Liechtenstein (spec)
- ✅ AC-07.2.2 / Daily return (spec)
- ✅ AC-07.2.2 / No daily return (spec)
- ✅ AC-07.2.3 / Return reasonable (spec)
- ✅ AC-07.2.3 / Return not reasonable (spec)
- ✅ AC-07.2.4 / Daily return with certificate (spec)
- ✅ AC-07.2.4 / Daily return without certificate (spec)
- ✅ AC-07.2.4 / Daily return, certificate not yet provided (spec)
- ✅ AC-07.2.4 / Calculator run: no daily return, reasonable, not more than 60 days → N1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-b948fd) (spec)
- ✅ AC-07.2.4 / Calculator run: more than 60 non-return days → C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-b948fd) (spec)
- ✅ AC-07.2.4 / Calculator run: return not reasonable → C1Y (zh_source_tax_calculator/F-zh_source_tax_calculator-bc1639) (spec)
- ✅ AC-07.2.4 / Not living in Germany (spec)
- ✅ AC-07.3.1 / Daily return to Liechtenstein (spec)
- ✅ AC-07.3.1 / No daily return to Liechtenstein (spec)
- ✅ AC-07.3.1 / Living in Germany (spec)
- ✅ AC-07.3.2 / Calculator run: daily return to Liechtenstein (zh_source_tax_calculator/F-zh_source_tax_calculator-e80d8f) (spec)
- ✅ AC-07.3.2 / No daily return, at most 45 non-return days (spec)
- ✅ AC-07.3.2 / Calculator run: more than 45 non-return days → C1Y subject to the agreement (zh_source_tax_calculator/F-zh_source_tax_calculator-ab4e1e) (spec)
- ✅ AC-07.3.2 / Not living in Liechtenstein (spec)
- ✅ AC-08.1.1 / Tomás - Brazilian, B permit, lives in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-08.1.1 / Stefan - Swiss citizen living abroad (hr_transcript/F-hr_transcript-1a20bb); country of residence assumed Germany (spec)
- ✅ AC-08.1.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-08.1.1 / Employee living in Liechtenstein (spec)
- ✅ AC-08.2.2 / Employee changed civil status from Married to Single - spouse's date of birth is discarded (spec)
- ✅ AC-08.2.2 / Employee changed home country from Switzerland to Germany - canton and citizenship answers are discarded (spec)
- ✅ AC-08.2.2 / Employee living in Switzerland changed Swiss citizenship from no to yes - C permit and source tax answers are discarded (spec)

## Open questions (need your decision)

- **OQ-canton-abroad**: What does Pensionskasse Muster expect in 'Canton' for employees living abroad, and does 'Canton' mean canton of residence or of work? → recommended: Provisionally ask only residents of Switzerland (D-002); verify with a domain expert and the fund.
- **OQ-civil-status-partnership**: How does the pension fund want registered partnerships and separated employees registered (the list has only Single, Married, Divorced, Widowed), and does it want partner details? → recommended: Use the provisional mapping (D-003) until a domain expert verifies it.
- **OQ-spouse-dob-other-status**: Does the fund's screen ask for a spouse's date of birth (or other data) for Divorced or Widowed? → recommended: Do not ask divorced/widowed employees (D-004); verify with a screenshot of the fund's screen.
- **OQ-calculator-coverage**: Does Lonio's computed tariff code match the calculator on paths not explored: residence block for A/B/H tariffs, more than 3 children, H3N/P3N, and the child paths marked 'inferred' in the child result table? → recommended: Go-live condition: domain expert verification (D-009).

## Inferred items to confirm

- item.spouse_residence_country
- rule.child_tariff_result
- story.US-04.2
- story.US-06.2
- story.US-06.3
- story.US-06.5
- story.US-06.6
- fact F-pension_portal-39bab1: The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected).
- fact F-pension_portal-6d3630: Screenshots do not show whether the spouse's date of birth (or other fields) appears for 'Divorced' or 'Widowed'; only Single (no) and Married (yes) are shown.
- fact F-pension_portal-9b24c5: The civil status list has no option for registered partnership or separated; it is unclear how such employees are to be registered.
- fact F-pension_portal-b359c3: The label 'Canton' does not state whether it is the canton of residence or of work, and the list only contains Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. a cross-border commuter).
- fact F-pension_portal-3a97ab: The portal requires an insurance start date on the 1st of a month but does not say how it relates to the employee's first working day (e.g. which 1st of a month to use when work starts mid-month).

## Dev refinement questions (14)

- [major] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` Liechtenstein residents: if the result is 'in principle no source tax liability' (daily return, or at most 45 non-return days), no tariff code is produced. Do they still have to answer the denomination, spouse employment and children questions? The flow in step 6 asks these first and the Liechtenstein daily-return question last. But the AC-05.7.3 examples show '–' for denomination and children, and G-01 says not to collect data no party needs. Should the Liechtenstein questions come first in step 6 and skip the tariff questions when the result is 'no liability'? And what is recorded as 'Subject to source tax' for these employees: yes or no?
- [major] `feature.md` Is this questionnaire built only for Muster AG (Pensionskasse Muster, the Zurich calculator for everyone, HR wording), or for every Lonio customer? If it is for every customer, which parts can each customer set up differently: the pension fund field list, the canton or calculator used, and the reminder text? The answer decides whether we hard-code the rules or make them per-customer settings.
- [major] `stories/US-08.1-remind-employees-to-bring-their-permit-on-the-first-working.md` The spec says HR words the permit reminder. Do we get one fixed text from HR before the build, or must HR be able to write and change the text themselves (per company)? If HR edits it, that is an HR-side feature, and the HR side is out of scope.
- [major] `stories/US-02.1-employee-enters-the-first-working-day.md` The employee 'enters and confirms' the first working day. Is the field empty, or filled in beforehand with the date HR agreed so the employee only confirms or corrects it? If filled in, where does that date come from, given that who starts the onboarding is out of scope?
- [major] `information.md` No date rules are given. Can the first working day be in the past, or far in the future? Must the date of birth (and the spouse's date of birth) be plausible, for example not in the future, or a minimum age? Today any date would be accepted, and the insurance start date would be derived from it.
- [major] `feature.md` Can the employee stop part-way and come back later (in another session or on another device) with the answers kept? Is there a deadline, or a reminder for unfinished questionnaires? D-036 only covers moving back and forth before submitting.
- [major] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` The 60-day (Germany) and 45-day (Liechtenstein) thresholds count non-return days 'in the calendar year'. An employee who starts mid-year works only part of that year. Should they use the same 60 and 45, a pro-rated threshold, or be guided to count only their working days at Muster AG? This changes both the question wording and the result.
- [minor] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` For the certificate of residence, what is the difference in meaning between 'no' and 'not yet'? Both count as 'no' for the tariff. Should 'not yet' be recorded for HR as a pending follow-up, unlike 'no'? Also, 'has provided' to whom, and by when, since the questionnaire is filled in before the first working day?
- [minor] `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` On which date is 'minor' or 'of age and in first education' judged: the day the questionnaire is filled in, the first working day, or the start of the year? Does the employee need guidance on what 'first education' covers? A child who turns 18 soon may count differently.
- [minor] `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` For married employees and registered partners, the children include the spouse's or partner's children. For such a stepchild, who is 'the other parent' in the questions about a common household, custody and the larger financial contribution? Should those questions be worded differently for stepchildren?
- [minor] `stories/US-01.2-complete-home-address-for-posting-documents.md` Every address part is required. What should an employee enter whose address has no house number (rural addresses, some foreign addresses)? Should a PO box or an extra address line (c/o, apartment) be allowed? HR says nothing beyond an envelope address is needed.
- [minor] `stories/US-01.2-complete-home-address-for-posting-documents.md` In the AC-01.2.1 example table, the Switzerland row shows '–' for the country, but the text says the country is always required. Is the country required for every employee? I assume yes.
- [minor] `information.md` The rules depend on whether the country is exactly Switzerland, Germany or Liechtenstein. Can the employee pick any country in the world? Do special cases need handling, such as Büsingen or Campione (enclaves), or a country typed in another language (for example 'Deutschland')?
- [minor] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` The child digit 'equals the number of children that count'. Is there a maximum number of children an employee can add? What is the tariff code if 10 or more children count (a two-digit number)?

## Technical vocabulary found in the spec (4)

- `information.md` "Form: Country by English name (e.g. Switzerland, Germany, Liechtenstein); part of a complete postal address" - G-10 covers the wording of values in the spec and its examples. Here it becomes a rule for how the employee must enter the country, which is an input and design choice for engineering.
- `stories/US-02.1-employee-enters-the-first-working-day.md` "the employee is asked for their first working day at Muster AG as a date (DD.MM.YYYY)" - The fund requires DD.MM.YYYY for the insurance start date and the dates of birth, not for the first working day. How the employee enters a date is a UI choice for engineering.
- `information.md` "Expression describes one child." - Refers to an internal rule 'expression' from the pipeline or engine, not business language. It implies how the rule is modelled per child.
- `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` "the employee can add further children and remove a child, and the child questions repeat per child" - Describes the UI interaction (add or remove a child, a repeating block) rather than the business need: collect the per-child facts for every child.

## Coverage

167/341 source units cited; 143/179 facts used.

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

## Other warnings (43)

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
- [coverage] `F-pension_portal-3a97ab` fact not used anywhere in the spec: The portal requires an insurance start date on the 1st of a month but does not say how it relates to the employee's first working day (e.g. which 1st of a month to use when work starts mid-month).
- [trace_judge] `item.address_country` partial: The claim that the country decides whether the canton question is asked rests on D-002, which is not cited here, and no cited fact states it.
- [trace_judge] `item.has_children` partial: No cited fact mentions the H tariff or that the children answer opens the child questions that determine it.
- [trace_judge] `item.child_same_household` partial: The 'H tariff' purpose is not backed by any cited fact.
- [trace_judge] `item.child_parental_custody` partial: The purpose 'sole custody counts the child (H for single employees)' is not backed by any cited fact.
- [trace_judge] `item.child_common_household_other_parent` partial: The 'H tariff' purpose is not backed by any cited fact.
- [trace_judge] `item.child_parental_care_not_in_household` partial: Question, options and condition are backed (separated counts as single per D-003), but no cited fact mentions the 'H tariff' purpose.
- [trace_judge] `item.child_alternating_custody` partial: Options and the combined asked_when are backed, but no cited fact supports the 'H tariff' purpose.
- [trace_judge] `item.child_main_financial_contributor` partial: Options and asked_when match the calculator facts, but no cited fact supports the 'H tariff' purpose.
- [trace_judge] `item.child_main_maintenance` partial: Question, options and condition are backed, but no cited fact supports the 'H tariff' purpose.
- [trace_judge] `rule.pension_fund_civil_status` partial: D-003 says separated is entered as Married without a spouse's date of birth, so the 'with the spouse's date of birth' part of the Separated row is not backed (D-004 is cited but not shown).
- [trace_judge] `rule.source_tax_residence` partial: The cited facts give only the residence options and the base tariff for Switzerland and other countries; the cross-border questions for Germany and Liechtenstein are not backed.
- [trace_judge] `rule.single_parent_h_tariff` partial: The 'No H tariff (A)' row cites F-zh_source_tax_calculator-c78e0c, which is not among the cited facts, so that row is not backed.
- [trace_judge] `rule.cross_border_tariff_applies` partial: The 'no return reasonable = no' row cites bc1639 and the non-Germany row cites 52b67a, and neither fact is in the cited set, so those rows are not backed.
- [trace_judge] `rule.source_tax_result` partial: The 'not subject to source tax' row cites F-hr_transcript-b6d9b3, which is not among the cited facts, so that row has no backing.
- [trace_judge] `story.US-01.2` partial: AC-01.2.1 says the address step follows the personal details, and no cited fact supports that ordering.
- [trace_judge] `story.US-05.4` partial: The 'only if subject to source tax' condition and the exemption example (Tomás) rely on the subject-to-source-tax rule (F-hr_transcript-b6d9b3/d7431e), which this story does not cite.
- [trace_judge] `story.US-06.1` partial: The Tomás example (subject_to_source_tax = no) depends on the subject-to-source-tax rule and the transcript fact, neither of which is cited; the rest is backed.
- [trace_judge] `story.US-06.2` partial: The cases not observed in the calculator are not backed by the cited facts: married alternating care with the employee as larger contributor counts, and single alternating care with the other parent as larger contributor does not count.
- [trace_judge] `story.US-06.3` partial: Only the B1N and H1N counting cases and the no-custody cases are observed; the other-parent-contributes and no-alternating-care outcomes are inferred and not in the cited facts.
- [trace_judge] `story.US-06.4` partial: AC-06.4.2 extends the question to divorced and widowed employees, but the cited facts only say 'single persons' (plus D-003 for separated), so that grouping is not backed.
- [trace_judge] `story.US-08.1` partial: The non-illustrative Tomás example (Brazilian, B permit, Winterthur) cites F-hr_transcript-d7431e, which is not among the cited facts, so it is not backed; the rest is supported by D-010, D-038 and F-c53552.
- [trace_judge] `story.US-08.3` partial: The read-only behaviour and the derived-again results are backed by D-037, D-033 and D-034, but the Julia changed-start-date incident named in the value and priority reason appears in none of the cited facts.
- [dev_refinement] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` Liechtenstein residents: if the result is 'in principle no source tax liability' (daily return, or at most 45 non-return days), no tariff code is produced. Do they still have to answer the denomination, spouse employment and children questions? The flow in step 6 asks these first and the Liechtenstein daily-return question last. But the AC-05.7.3 examples show '–' for denomination and children, and G-01 says not to collect data no party needs. Should the Liechtenstein questions come first in step 6 and skip the tariff questions when the result is 'no liability'? And what is recorded as 'Subject to source tax' for these employees: yes or no?
- [dev_refinement] `feature.md` Is this questionnaire built only for Muster AG (Pensionskasse Muster, the Zurich calculator for everyone, HR wording), or for every Lonio customer? If it is for every customer, which parts can each customer set up differently: the pension fund field list, the canton or calculator used, and the reminder text? The answer decides whether we hard-code the rules or make them per-customer settings.
- [dev_refinement] `stories/US-08.1-remind-employees-to-bring-their-permit-on-the-first-working.md` The spec says HR words the permit reminder. Do we get one fixed text from HR before the build, or must HR be able to write and change the text themselves (per company)? If HR edits it, that is an HR-side feature, and the HR side is out of scope.
- [dev_refinement] `stories/US-02.1-employee-enters-the-first-working-day.md` The employee 'enters and confirms' the first working day. Is the field empty, or filled in beforehand with the date HR agreed so the employee only confirms or corrects it? If filled in, where does that date come from, given that who starts the onboarding is out of scope?
- [dev_refinement] `information.md` No date rules are given. Can the first working day be in the past, or far in the future? Must the date of birth (and the spouse's date of birth) be plausible, for example not in the future, or a minimum age? Today any date would be accepted, and the insurance start date would be derived from it.
- [dev_refinement] `feature.md` Can the employee stop part-way and come back later (in another session or on another device) with the answers kept? Is there a deadline, or a reminder for unfinished questionnaires? D-036 only covers moving back and forth before submitting.
- [dev_refinement] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` The 60-day (Germany) and 45-day (Liechtenstein) thresholds count non-return days 'in the calendar year'. An employee who starts mid-year works only part of that year. Should they use the same 60 and 45, a pro-rated threshold, or be guided to count only their working days at Muster AG? This changes both the question wording and the result.

## Run

Stages run: dev_refinement, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator, judge_facts, knowledge.raw, feature.plan, feature.flow, judge_trace

LLM cost this run: $2.29
