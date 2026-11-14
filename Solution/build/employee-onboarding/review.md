# Review: employee-onboarding

**Verdict: NOT READY**

All example simulations pass, and none of the 5 open questions is blocking. The package is still not ready for four reasons. Decision D-036 has new evidence and must be re-confirmed (the check report lists this as an error). The written H-child rule and the decision table give different answers. The Liechtenstein status is inconsistent and its question order is unclear. Four technical or unsourced behaviours have leaked into the stories. Fix these and the package should reach ready_with_caveats. The caveats would be the open questions for the pension fund and D-009: before go-live, a domain expert compares Lonio's tariff codes with the calculator.

## Reviewer findings

1. **D-036 has new evidence and needs re-confirming** – The decision on the emailed copy was made before Anna's email arrived. The email says the copy holds only the submitted answers, exactly as submitted, with no derived values. Until D-036 is re-confirmed, US-08.4 rests on an outdated decision.  
   Evidence: decisions error D-036; F-hr_email_copy-37cede, -9e81ef, -daa6b1  
   Action: Check D-036 against the email, then confirm, update or drop it, and run `pipeline reconfirm D-036`. Resolve this together with finding 6.
2. **H-child rule text contradicts the decision table** – The written rule says an H child must live in the employee's household. Row 21 and AC-06.3.3 count a child outside the household as an H child (H1N). This changes the tariff letter (H/P vs A/L), so the computed code would be wrong in one of the two readings.  
   Evidence: dev_refinement major (feature.md H rule vs row 21 / AC-06.3.3); trace_judge rule.single_parent_h_tariff, item.has_children, item.child_main_financial_contributor  
   Action: Add a decision to decisions.yaml saying which is right. The calculator run in F-c2faa7 supports the table. Then align the rule text and cite the facts behind it (c78e0c, 562299, 97139a).
3. **Liechtenstein residents: status and question order undefined** – The US-01.3 example records 'subject to source tax: yes' with no source tax questions. D-007 instead asks the questions and can give 'in principle no liability'. Denomination, spouse and children answers are asked before the cross-border questions but are not needed for these employees, which goes against data minimisation (G-01).  
   Evidence: trace_judge story.US-01.3; dev_refinement major (feature.md steps 6/6a vs 7); info US-01.3, US-05.7 (>45 days double-taxation-agreement flag)  
   Action: Decide what is recorded as 'subject to source tax' for Liechtenstein residents (yes, no, or a separate status). Decide whether the Liechtenstein questions come first and the later ones are skipped. Decide whether the >45-days case is flagged for HR.
4. **US-05.7 adds 'cannot be computed yet' behaviour that no source asked for** – The spec chooses one fallback for unexplored child combinations, but OQ-child-paths-undetermined still lists 'HR determines the code' as an option. Engineering would build an outcome nobody has agreed to.  
   Evidence: tech_leak US-05.7; trace_judge story.US-05.6 (AC-05.6.4), story.US-05.7 (AC-05.7.5), rule.source_tax_result  
   Action: Pick the interim behaviour for OQ-child-paths-undetermined in decisions.yaml and cite it in AC-05.6.4 and AC-05.7.5, or remove the behaviour from the stories.
5. **US-08.3 widens 'no history kept' to every derived value** – This is a data-retention decision. D-033 covers only the first working day. The story also cites a 'Julia changed start date' incident that no source backs.  
   Evidence: tech_leak US-08.3; trace_judge story.US-08.3  
   Action: Either narrow the wording to what D-033 says, or add a decision that covers all derived results. Remove the unbacked incident or cite a source for it.
6. **Emailed copy: retention of the email address and scope of 'answers' unclear** – Nothing says whether the email address typed in for the copy is stored or shown to HR. Nothing says whether the 'send me a copy' answer and the address count as answers that appear in the copy. AC-08.4.3 lists excluded derived values that no source names.  
   Evidence: dev_refinement major US-08.4; trace_judge rule.employee_copy_content, story.US-08.4; inferred item.copy_email_address  
   Action: While re-confirming D-036, decide how long the address is kept and what exactly the copy contains. Write AC-08.4.3 as 'no derived values' rather than an unsourced list.
7. **No date checks for the first working day or dates of birth** – A wrong first working day leads straight to a wrong insurance start date for the pension fund. Engineering cannot write validation without rules.  
   Evidence: dev_refinement major US-02.1  
   Action: Ask HR and decide: can the first working day be in the past, and how far ahead can it be? Are there age limits for the employee's date of birth, and any check on the spouse's date of birth?
8. **Implementation and UI wording in the business rules** – The text refers to 'the expression', and US-06.1 describes add/remove child controls. These are design and implementation choices, not requirements.  
   Evidence: tech_leak feature.md ('The expression evaluates one child…'); tech_leak US-06.1  
   Action: Rewrite as business rules: 'each child is assessed separately; the counted children are added up' and 'answers are collected for each child'. Leave the UI to design.
9. **Some rule rows cite facts that are not in their cited set** – Several rows (for example 'other country → base tariff' and 'not subject → no result') rest on facts the rule does not cite. That breaks the link from rule to source.  
   Evidence: trace_judge rule.source_tax_residence, rule.cross_border_tariff_applies, rule.liechtenstein_no_source_tax_in_principle, rule.source_tax_result (F-52b67a, 332e2a, b6d9b3, 2eab9a not cited); item.daily_return_germany, item.child_parental_custody; story.US-04.1 (F-b84498)  
   Action: Add the missing fact citations, or mark these rows as inferred and confirm them.
10. **Example tables and question wording need cleanup before they can serve as tests** – The example tables mix '–', 'asked' and 'required'. The certificate question is phrased both as 'has' and 'have provided', and the two readings give different tariffs. 'Calendar year' is not defined for employees who start late in the year. The permit reminder text has no owner.  
   Evidence: dev_refinement info US-01.2, US-03.3, US-07.2 (×2), US-08.1, US-06.1 (more than 9 children), US-06.2 (stepchildren)  
   Action: Correct the example tables. Decide whether the certificate question means 'has' or 'has provided', and which year is meant. Name who writes the permit reminder text and by when. Set a maximum number of children and how a code is formed above 9. Decide how the questions apply to stepchildren.

## Numbers

343 source units → 188 facts → 37 information items, 18 business rules → one feature with 8 sections, 30 stories, 89 acceptance criteria; 5 open questions, 12 exclusions.

## Errors (1)

- [decisions] `D-036` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-036`: F-hr_email_copy-37cede: At the end of the questionnaire, when submitting, the employee should be able to send themselves an email with a copy of their form data.; F-hr_email_copy-9e81ef: The emailed copy must show the answers exactly as they were submitted, nothing more.; F-hr_email_copy-daa6b1: The emailed copy must not contain derived values or any other information beyond the submitted answers. ...

## Examples executed against the knowledge model (221/221 pass)

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
- ✅ AC-05.7.5 / Married, minor child in the household, shared custody, alternating care, employee is the larger contributor (spec)
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
- ✅ AC-06.2.4 / Alternating care, employee main contributor (not shown by the calculator) (spec)
- ✅ AC-06.2.5 / Common household, employee main contributor (zh_source_tax_calculator/F-zh_source_tax_calculator-96658b) (spec)
- ✅ AC-06.2.5 / Calculator run A0N, common household, other parent contributes more (zh_source_tax_calculator/F-zh_source_tax_calculator-38dd4a) (spec)
- ✅ AC-06.2.5 / Calculator run H1N, no common household, no alternating care (zh_source_tax_calculator/F-zh_source_tax_calculator-38dd4a) (spec)
- ✅ AC-06.2.5 / Alternating care, employee main contributor (zh_source_tax_calculator/F-zh_source_tax_calculator-96658b) (spec)
- ✅ AC-06.2.5 / Alternating care, other parent main contributor (not shown by the calculator) (spec)
- ✅ AC-06.3.1 / Married employee, child outside household (spec)
- ✅ AC-06.3.1 / Separated employee, child outside household (counts as single, D-003) (spec)
- ✅ AC-06.3.2 / Calculator run B0N, no shared custody (zh_source_tax_calculator/F-zh_source_tax_calculator-56e79b) (spec)
- ✅ AC-06.3.2 / Calculator run A0N, no parental custody (zh_source_tax_calculator/F-zh_source_tax_calculator-c2faa7) (spec)
- ✅ AC-06.3.2 / Single employee with parental custody (spec)
- ✅ AC-06.3.3 / Calculator run B1N (zh_source_tax_calculator/F-zh_source_tax_calculator-56e79b) (spec)
- ✅ AC-06.3.3 / Calculator run H1N (zh_source_tax_calculator/F-zh_source_tax_calculator-c2faa7) (spec)
- ✅ AC-06.3.3 / Married, other parent contributes more (not shown by the calculator) (spec)
- ✅ AC-06.3.3 / Married, no alternating care (not shown by the calculator) (spec)
- ✅ AC-06.3.3 / Single, other parent contributes more (not shown by the calculator) (spec)
- ✅ AC-06.3.3 / Single, no alternating care (not shown by the calculator) (spec)
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
- ✅ AC-06.5.2 / Outside household, mainly maintained (not shown by the calculator) (spec)
- ✅ AC-06.5.2 / In household, no common household, mainly maintained (not shown by the calculator) (spec)
- ✅ AC-06.5.2 / In household, no common household, not mainly maintained (not shown by the calculator) (spec)
- ✅ AC-06.5.3 / Calculator run H1N, in household, mainly maintained (zh_source_tax_calculator/F-zh_source_tax_calculator-562299) (spec)
- ✅ AC-06.5.3 / Calculator run A1N, outside household, mainly maintained (zh_source_tax_calculator/F-zh_source_tax_calculator-562299) (spec)
- ✅ AC-06.5.3 / Common household, employee contributes more (zh_source_tax_calculator/F-zh_source_tax_calculator-96658b) (spec)
- ✅ AC-06.5.3 / Common household, other parent contributes more (not shown by the calculator) (spec)
- ✅ AC-06.5.3 / In household, not mainly maintained (not shown by the calculator) (spec)
- ✅ AC-06.5.3 / Outside household, not mainly maintained (not shown by the calculator) (spec)
- ✅ AC-06.6.1 / One child counting (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.6.1 / One H child (zh_source_tax_calculator/F-zh_source_tax_calculator-38dd4a) (spec)
- ✅ AC-06.6.1 / Child does not count (zh_source_tax_calculator/F-zh_source_tax_calculator-56e79b) (spec)
- ✅ AC-06.6.1 / No children (spec)
- ✅ AC-06.6.2 / Calculator run H1Y, sole custody (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.6.2 / Calculator run A1N, child counts without H (zh_source_tax_calculator/F-zh_source_tax_calculator-562299) (spec)
- ✅ AC-06.6.2 / Married employee with sole custody child (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-06.6.2 / Single employee without children (spec)
- ✅ AC-06.6.3 / Single, adult child in first education outside household, not mainly maintained (not shown by the calculator) (spec)
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
- ✅ AC-08.2.2 / Employee living in Switzerland changed Swiss citizenship from Not Swiss to Swiss - C permit and source tax answers are discarded (spec)
- ✅ AC-08.4.1 / Any employee at submission (spec)
- ✅ AC-08.4.2 / Employee wants a copy (spec)
- ✅ AC-08.4.2 / Employee does not want a copy (spec)
- ✅ AC-08.4.2 / Employee leaves the copy question empty (spec)

## Open questions (need your decision)

- **OQ-canton-abroad**: What should be entered in the pension fund's required 'Canton' field for employees living abroad, and does 'Canton' mean canton of residence or of work? → recommended: Domain expert and Pensionskasse Muster to confirm; keep the provisional rule until then.
- **OQ-civil-status-partnership**: How does Pensionskasse Muster want registered partnerships and separated employees registered, and does it want the partner's details? → recommended: Domain expert to verify with the fund.
- **OQ-spouse-dob-other-status**: Does the fund's form ask for a spouse's date of birth (or other fields) for Divorced or Widowed? → recommended: Domain expert to provide a screenshot of the fund screen for these statuses.
- **OQ-calculator-coverage**: Does Lonio's computed tariff code match the calculator for the paths not explored: the residence block for A/B/H tariffs, more than 3 children, H3N/P3N and the full cross-product of paths? → recommended: Run the comparison before release.
- **OQ-child-paths-undetermined**: How does a child count in the child-answer combinations that the calculator exploration did not show (rows marked 'Not determined', e.g. married with alternating care where the employee is main contributor; single with an adult child in first education not mainly maintained)? → recommended: Include these paths in the pre-go-live comparison of D-009.

## Inferred items to confirm

- item.spouse_residence_country
- item.copy_email_address
- rule.source_tax_residence
- rule.child_tariff_result
- story.US-04.2
- story.US-06.2
- story.US-06.3
- story.US-06.5
- story.US-06.6
- story.US-08.4
- fact F-pension_portal-39bab1: The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected).
- fact F-pension_portal-6d3630: Screenshots do not show whether the spouse's date of birth (or other fields) appears for 'Divorced' or 'Widowed'; only Single (no) and Married (yes) are shown.
- fact F-pension_portal-9b24c5: The civil status list has no option for registered partnership or separated; it is unclear how such employees are to be registered.
- fact F-pension_portal-b359c3: The label 'Canton' does not state whether it is the canton of residence or of work, and the list only contains Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. a cross-border commuter).
- fact F-pension_portal-3a97ab: The portal requires an insurance start date on the 1st of a month but does not say how it relates to the employee's first working day (e.g. which 1st of a month to use when work starts mid-month).
- fact F-hr_email_copy-b67d2f: The copy email address is only needed when the employee chooses to receive a copy (asked only then, not required otherwise).
- fact F-hr_email_copy-daa6b1: The emailed copy must not contain derived values or any other information beyond the submitted answers.

## Dev refinement questions (14)

- [major] `feature.md` The step notes put the source tax details (denomination, spouse works, children: steps 6/6a) before the cross-border questions (step 7). A Liechtenstein resident who returns daily, or expects at most 45 non-return days, gets 'in principle no source tax liability' and no tariff code. So their denomination, spouse employment and children answers are not needed (AC-05.7.3 shows them as '–'). Should these employees be asked the Liechtenstein questions first and then skip denomination, spouse employment and children? Or are those answers asked and then discarded on submission? Either way the order of the flow changes, and so does what is collected (G-01 data minimisation).
- [major] `stories/US-08.4-employee-can-get-an-emailed-copy-of-their-submitted-answers.md` Is the email address typed in for the copy recorded for HR or kept after the email is sent, or only used to send it? Does the copy itself list the 'send me a copy' answer and the email address as submitted answers? The spec says 'nothing more' but does not say whether these two closing items count as answers.
- [major] `stories/US-02.1-employee-enters-the-first-working-day.md` What date checks apply? Can the first working day be in the past, or how far in the future? Is there a minimum or maximum age for the employee's date of birth, and any check on the spouse's date of birth? The ACs only say 'required, DD.MM.YYYY'. A wrong first working day directly gives a wrong insurance start date.
- [major] `feature.md` The rule 'How a child counts for the tariff' and the Single-parent H rule say a child counts as an H child when it 'lives in the household and the employee has sole custody or is the main contributor'. Yet row 21 (and AC-06.3.3) count a minor child NOT in the household as an H child (single parent with custody, alternating care, employee is the main contributor → H1N). Which is right: the plain-language rule or the decision table? The H/P letter depends on it.
- [minor] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` The certificate of residence question is phrased two ways. information.md asks whether the employee 'has' a certificate; AC-07.2.2 asks whether they 'have provided' it (to HR). Which one is meant? An employee who has the certificate but has not handed it in yet would answer differently, and the answer switches between the cross-border and normal tariff.
- [minor] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` The cross-border answers are 'what they expect for the year' / 'in the calendar year'. Which year is meant for an employee who starts late in the year (e.g. in December): the current calendar year, the first full year, or the next 12 months? Without this the question wording cannot be finalised.
- [minor] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` For Liechtenstein residents with more than 45 non-return days, the normal code is 'marked subject to the double taxation agreement'. Is this case also flagged for HR, like the 'in principle no liability' case? Or is it only a note on the code? Two different outcomes have to be recorded.
- [minor] `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` Is there a maximum number of children an employee can enter? The calculator limit is unknown, and the tariff code holds a single digit. What should the result be when 10 or more children count?
- [minor] `stories/US-06.2-ask-custody-and-common-household-for-a-minor-child-living.md` For married employees, 'Has children' includes the spouse's/partner's children. For a stepchild, whose custody, maintenance contribution and 'other parent' do the custody and contribution questions refer to? The question wording has to make this clear, or answers will be inconsistent.
- [minor] `stories/US-08.1-remind-employees-to-bring-their-permit-on-the-first-working.md` HR words the permit reminder. Who supplies the final text, and by when? It also has to work for Swiss citizens living abroad. Without the text the story cannot be finished or accepted.
- [minor] `stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md` Before submission, can the employee leave the questionnaire and come back later with their answers kept? Is there a deadline, or a point at which an unsubmitted questionnaire's answers are deleted? 'Kept while going back and forth' does not say whether answers survive across sessions, which matters for data minimisation.
- [minor] `stories/US-02.2-insurance-start-date-derived-from-the-first-working-day.md` Should the employee see the derived insurance start date (or the source tax result) anywhere in the questionnaire before or after submitting? Or is it only recorded for HR/the fund? The copy explicitly excludes these values, but nothing is said about showing them on screen.
- [minor] `stories/US-01.2-complete-home-address-for-posting-documents.md` The AC-01.2.1 example shows the country as '–' for the Switzerland row but 'required' for the Germany row, although the country is always required. Similarly, US-03.3 shows the spouse's date of birth as '–' for Married but 'required' for Registered partnership. Examples elsewhere also mix 'asked' and 'required'. Please correct the example tables so they can be used as test cases.
- [minor] `stories/US-01.3-home-address-country-is-the-country-of-residence-for-later.md` The trace check notes that the Liechtenstein example treats the employee as 'subject to source tax: yes', while D-007 gives them 'in principle no source tax liability'. What should be recorded for HR as 'subject to source tax' for these employees: yes, no, or a separate status?

## Technical vocabulary found in the spec (4)

- `stories/US-08.3-questionnaire-is-read-only-for-the-employee-after-submission.md` "are derived again from the latest answers; no history of earlier values is kept" - This makes a storage/retention decision for all derived results. The source (D-033) only says no history is kept of earlier first working days; the spec's own trace check notes this extension is not backed.
- `feature.md` "The expression evaluates one child; the rule applies to each child." - It refers to an implementation artifact (an 'expression') instead of the business rule. The same applies to 'The expression covers a single child; with several children the counts are added up.'
- `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` "Lonio records that the tariff code cannot be computed yet instead of a possibly wrong code, so the case stays visible for HR" - This prescribes system behaviour that no stakeholder or decision asked for; the trace check says the cited facts do not require it. The open question still offers 'HR determines the code' as an alternative.
- `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` "the employee can add further children and remove a child, and the child questions repeat per child" - This describes interaction mechanics (add/remove child blocks, copied from the calculator UI). The business need is only that each child's answers are collected; how the employee enters several children is a UI choice.

## Coverage

168/343 source units cited; 155/188 facts used.

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
- hr_email_copy/T-000: Subject: Onboarding questionnaire - copy for the employee From: Anna (HR, Muster AG) To: Leo (Lonio) Date: 14 November 2026

## Other warnings (36)

- [fact_judge] `F-hr_transcript-5518ad` partial: Address is needed, but 'home' is not stated explicitly (though implied). | HR needs the employee's home address.
- [fact_judge] `F-hr_transcript-550840` partial: Leo's summary and Anna's 'I think so' are supported, but 'later added further cases' is not visible in the units, although T-044 in the neighbouring context does add the spouse case. | Leo summarised 'non-Swiss, but not with a C permit'; Anna only hedged ('I think so') and later added further cases.
- [fact_judge] `F-hr_transcript-51bed3` partial: Anna offered numbers on 'how long this takes' from the payroll person; that this refers to source tax processing is only implied. | Anna offered to get numbers from the payroll person on how long source tax processing takes.
- [fact_judge] `F-hr_transcript-a45422` partial: Anna says she checks the spouse case by hand and asks for spouse details by email which takes forever, but 'by hand' and email are separate remarks; reasonably fine though 'today HR' is mildly interpretive. | Today HR checks the spouse case by hand and asks for spouse details by email, which takes forever.
- [fact_judge] `F-hr_transcript-ab8886` partial: Leo's remark 'the calculator will tell us' is about the forms/questions, but 'tell which questions apply' overstates what he said. | For employees living abroad the source tax calculator has many more questions; Germany has its own forms whose names Anna cannot recall. Leo noted the calculator will tell which questions apply.
- [fact_judge] `F-hr_transcript-e505f8` partial: Address includes country and living abroad matters, but the units don't state that country of home address is used to derive it; it's a reasonable inference. | Whether the employee lives abroad can be derived from the country of the home address, which is relevant for source tax liability.
- [fact_judge] `F-pension_portal-c8bc73` partial: Portal, page and employer Muster AG are supported, but 'to register a new employee as an insured person' is only loosely supported via the breadcrumb 'Insured persons'. | The source is the 'Register new employee' page in the Pensionskasse Muster employer portal, used by employer Muster AG to register a new employee as an insured person.
- [fact_judge] `F-pension_portal-39bab1` partial: Field shown for Married and absent for Single, but the units don't show screenshots 01/02/03 and 'only when Married' overstates since Divorced/Widowed are not shown. | The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected).
- [fact_judge] `F-pension_portal-3cfe89` partial: Footnote supports that * marks required fields, but the units shown don't establish that all visible fields carry the marker. | Fields marked with an asterisk are required; all visible fields on the form carry the marker.
- [fact_judge] `F-zh_source_tax_calculator-351289` partial: The skip to Q16 is stated, but nothing in the units says Q16 is the main-residence question. | If the income type is 'Ersatzeinkünfte', all personal and child questions are skipped and the calculator goes straight to the main-residence question (Q16).
- [fact_judge] `F-zh_source_tax_calculator-c78e0c` partial: Single with no children giving A0Y/A0N is shown in the test vectors, but the units don't explicitly tie this to Swiss residence (Q16 = Ja is not defined as such). | A person with civil status 'Ledig, Geschieden, Getrennt, Verwitwet' and no counting children, resident in Switzerland, gets tariff letter A (e.g. A0Y / A0N).
- [fact_judge] `F-zh_source_tax_calculator-956f07` partial: Q14 is shown for Ledig/Geschieden/Getrennt/Verwitwet, not just single, and 'whether the person has parental custody' is an interpretation of 'Elterliche Sorge'. | For single persons with a minor child not in the household, the calculator asks 'Elterliche Sorge' with Ja/Nein (whether the person has parental custody).
- [fact_judge] `F-zh_source_tax_calculator-cd1015` partial: Q08 = Nein is not shown to mean 'not in same household' and Q10 = Nein 'no common household with other parent' in these units; the mapping is plausible but not stated. | Q15 is shown only when the child is 'Volljährig und in Erstausbildung' AND (child not in same household OR (same household AND no common household with the other parent)).
- [fact_judge] `F-zh_source_tax_calculator-5f6820` partial: Q19's shown_when matches, but the units never say Q24 concerns replacement income, and the 'only when' framing as daily return to Germany for Q24 is unverified. | The certificate of residence question is asked only when the person returns daily to Germany (Q18 = Ja for earned income, or Q24 = Ja for replacement income).
- [fact_judge] `F-zh_source_tax_calculator-3058a4` partial: The vector outcomes (C1Y with Q10=Ja, C0Y otherwise) match, but the statement is garbled and unfinished. The units never say Q10 means 'common household' or Q11 means 'alternating care'. | Married person, minor child in same household, shared custody: common household with the other parent counts the child (C1Y); no common household counts the child only if... observed: alternating care with other parent as main contributor -> 0 (C0Y), no alternating care -> 0 (C0Y).
- [fact_judge] `F-zh_source_tax_calculator-56e79b` partial: Outcomes match V12/V13, but the vectors only show Q13/Q11/Q12 answers; the labels 'shared custody' and 'alternating care' are inferred, not stated. | Married person, minor child not in household: shared custody + alternating care + person is main contributor counts the child (B1N); no shared custody does not count it (B0N).
- [trace_judge] `item.has_children` partial: The purpose claim that children change the tariff letter to H is not backed by any cited fact.
- [trace_judge] `item.child_parental_custody` partial: The purpose 'sole custody counts the child (H for single employees)' is not backed by the cited facts, which only cover the question, options and display condition.
- [trace_judge] `item.child_main_financial_contributor` partial: The purpose 'H when the employee is the main contributor' (tariff code H) is not backed by any cited fact.
- [trace_judge] `item.daily_return_germany` partial: No cited fact states that the answer decides whether the cross-border tariff applies, and the 'subject_to_source_tax' condition is not stated in the facts.
- [trace_judge] `rule.source_tax_residence` partial: The cited facts do not support the claim that 'other country' leaves the base tariff unchanged (its source 52b67a is not cited), and mapping the home-address country to the residence answers is only loosely backed by e505f8.
- [trace_judge] `rule.single_parent_h_tariff` partial: The 'no H child gives A' and 'married not applicable' rows rest on facts (c78e0c, 562299, 97139a) that are not among the cited facts.
- [trace_judge] `rule.cross_border_tariff_applies` partial: The 'Switzerland, Liechtenstein or Other country -> No' row cites F-zh_source_tax_calculator-52b67a, which is not among the cited facts, and the cited facts only say that other Germany combinations give the base tariff.
- [trace_judge] `rule.liechtenstein_no_source_tax_in_principle` partial: The 'Switzerland, Germany or Other country -> No' row relies on F-zh_source_tax_calculator-52b67a, which is not among the cited facts; the Liechtenstein rows are supported by e80d8f, ab4e1e and D-007.
- [trace_judge] `rule.source_tax_result` partial: The 'cannot be computed yet (OQ-child-paths-undetermined)' row and the 'not subject -> no result' row cite facts that are not in the cited set (332e2a, b6d9b3, 2eab9a), so those rows are unbacked.
- [trace_judge] `rule.employee_copy_content` partial: No cited fact says the copy goes to an email address the employee typed in; the facts only say the employee can email a copy to themselves.
- [trace_judge] `story.US-01.3` partial: The Liechtenstein example expects subject_to_source_tax 'yes' and no source tax questions, but D-007 says Liechtenstein residents are asked the source tax questions and may get 'in principle no source tax liability' instead.
- [trace_judge] `story.US-04.1` partial: The priority reason says HR works source tax liability out by hand and cannot know in advance who must answer, and cites F-hr_transcript-b84498, which is not among the cited facts and is not backed by the ones that are.
- [trace_judge] `story.US-05.6` partial: AC-05.6.4's claim that unknown child-answer combinations 'stay undetermined until verified' is not backed by the cited facts, which only say the cross-product was not enumerated and that an expert compares paths before go-live.
- [trace_judge] `story.US-05.7` partial: AC-05.7.5 has Lonio record 'cannot be computed yet' for unexplored child combinations, but the cited facts only say these paths were not enumerated and need expert comparison, not that this behaviour is required.
- [trace_judge] `story.US-08.3` partial: The 'Julia's changed start date' incident in the value and priority reason is not backed by any cited fact, and 'no history of earlier values' for all derived results is only stated for the first working day (D-033).
- [trace_judge] `story.US-08.4` partial: AC-08.4.3 names specific excluded derived values (insurance start date, civil status for fund/source tax, source-tax subject, tariff code) that the cited facts never mention, since they only say "nothing more".
- [dev_refinement] `feature.md` The step notes put the source tax details (denomination, spouse works, children: steps 6/6a) before the cross-border questions (step 7). A Liechtenstein resident who returns daily, or expects at most 45 non-return days, gets 'in principle no source tax liability' and no tariff code. So their denomination, spouse employment and children answers are not needed (AC-05.7.3 shows them as '–'). Should these employees be asked the Liechtenstein questions first and then skip denomination, spouse employment and children? Or are those answers asked and then discarded on submission? Either way the order of the flow changes, and so does what is collected (G-01 data minimisation).
- [dev_refinement] `stories/US-08.4-employee-can-get-an-emailed-copy-of-their-submitted-answers.md` Is the email address typed in for the copy recorded for HR or kept after the email is sent, or only used to send it? Does the copy itself list the 'send me a copy' answer and the email address as submitted answers? The spec says 'nothing more' but does not say whether these two closing items count as answers.
- [dev_refinement] `stories/US-02.1-employee-enters-the-first-working-day.md` What date checks apply? Can the first working day be in the past, or how far in the future? Is there a minimum or maximum age for the employee's date of birth, and any check on the spouse's date of birth? The ACs only say 'required, DD.MM.YYYY'. A wrong first working day directly gives a wrong insurance start date.
- [dev_refinement] `feature.md` The rule 'How a child counts for the tariff' and the Single-parent H rule say a child counts as an H child when it 'lives in the household and the employee has sole custody or is the main contributor'. Yet row 21 (and AC-06.3.3) count a minor child NOT in the household as an H child (single parent with custody, alternating care, employee is the main contributor → H1N). Which is right: the plain-language rule or the decision table? The H/P letter depends on it.

## Run

Stages run: normalize/hr_email_copy, extract/hr_email_copy, judge_facts, knowledge.raw, feature.plan, sections/SEC-02-start-date-insurance, sections/SEC-01-identity-and-address, sections/SEC-03-civil-status-spouse, sections/SEC-04-source-tax-liability, sections/SEC-08-completion-and-submission, sections/SEC-07-living-abroad, sections/SEC-05-tariff-basics, sections/SEC-06-children, judge_trace, dev_refinement, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator

LLM cost this run: $12.93
