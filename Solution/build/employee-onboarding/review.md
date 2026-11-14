# Review: employee-onboarding

**Verdict: NOT READY**

Not ready, but close. All examples pass and the open questions are non-blocking. Three things block release. Decision D-036 has new evidence from the email-copy update and must be re-confirmed (error). Five dev-refinement questions are rated major; one shows a contradiction between D-007 and the AC-05.7.3 examples, and another shows a gap in D-037 when HR edits after submission. Several rules and stories cite facts outside their cited set; one row (separated → spouse date of birth) disagrees with D-003. After that, the main open items are the inferred child-tariff paths and four places where implementation wording leaks into the spec.

## Reviewer findings

1. **D-036 has new evidence and must be re-confirmed** – This is the only error-level check. Five new email-copy facts touch D-036 (answers kept while the employee goes back and forth, and what gets submitted). Release can't happen while a decision is out of date against its evidence.  
   Evidence: decisions error on D-036: new facts F-hr_email_copy-029105, -37cede, -ab2538 and 2 more  
   Action: Re-check D-036 against the copy-email facts. Update the decision if it should also cover the copy, then run `pipeline reconfirm D-036`.
2. **Liechtenstein daily commuters: D-007 contradicts the AC-05.7.3 examples** – D-007 asks Liechtenstein residents every source tax question. But the examples show '–' for denomination and children in the 'in principle no source tax' rows. Under G-01, asking them would collect data that feeds no tariff code. This also decides the order of the source tax questions.  
   Evidence: dev_refinement (major) on US-05.7; AC-05.7.3; D-007  
   Action: Add a decision: ask the Liechtenstein daily-return and 45-day questions first, and close the source tax section early when there is in principle no liability. Then align D-007 and the AC-05.7.3 examples.
3. **HR edits after submission can open questions that were never answered** – D-037 says results are 're-derived from the latest answers'. But if HR changes residence, nationality or civil status, answers the result depends on (denomination, children, cross-border) were never collected. The tariff result is then undefined.  
   Evidence: dev_refinement (major) on US-08.3; D-037  
   Action: Decide who supplies the missing answers: the questionnaire reopens for just those questions, or HR enters them. Also decide what HR sees in the meantime (an 'incomplete' status vs no tariff code). Record it in decisions.yaml.
4. **Scope: is the Zurich calculator logic used for residents of other cantons?** – Most staff are in Zurich, but residents of Aargau, St. Gallen and other cantons may need their own canton's church-tax rules or tariff rules. That would change the tariff computation and possibly the denomination question.  
   Evidence: dev_refinement (major) on feature.md  
   Action: Confirm with HR or a domain expert. Either record that the Zurich logic applies to all (Muster AG's tax office is Zurich), or exclude other cantons and add that to the exclusions.
5. **Some rules and stories cite facts outside their cited set; one row disagrees with D-003** – Some rows have no backing. One is a real content conflict: the Separated row in pension_fund_civil_status includes the spouse's date of birth, but D-003 says separated employees are entered as Married without it.  
   Evidence: trace_judge: rule.pension_fund_civil_status; rule.single_parent_h_tariff (c78e0c); rule.cross_border_tariff_applies (bc1639, 52b67a); rule.source_tax_result (b6d9b3); US-04.3/05.4/06.1/08.1 (d7431e, b6d9b3); US-08.3 (Julia incident); 'H tariff' purpose on 8 child items  
   Action: Fix the Separated row to match D-003/D-004, or update D-003. Add the missing fact refs to the cited sets. Add a cited fact or decision behind the 'H tariff' purpose of the child items.
6. **Inferred child-tariff paths have not been checked against the calculator** – Lonio now owns the tariff result. About 15 example rows in US-06.2–06.5 are marked 'inferred, to verify', and US-06.4 extends a rule to divorced and widowed employees without a source. A wrong path gives HR a wrong tariff code.  
   Evidence: OQ-calculator-coverage (D-009); inferred stories US-06.2, US-06.3, US-06.5, US-06.6; trace_judge US-06.2/06.3/06.4  
   Action: Keep domain-expert verification as a stated go-live condition. Ideally run the inferred paths through the calculator now and replace 'inferred' with observed facts.
7. **Non-return days 'in the calendar year' are unclear for employees who start mid-year** – The answer, and possibly the question text, depends on which period counts. Without a rule, employees starting in, say, November will answer inconsistently, and the cross-border tariff may be wrong.  
   Evidence: dev_refinement (major) on US-07.2  
   Action: Clarify with a domain expert which period applies: rest of the year, projected full year, or next year. Record a decision and adjust the question wording.
8. **Saving an unfinished questionnaire and finishing deadline not defined** – This affects how D-036 retention works, reminders, and what happens before the first working day. Engineering can't size the flow without it.  
   Evidence: dev_refinement (major) on US-08.2; D-036  
   Action: Decide whether the employee can save and come back later, whether there is a deadline (e.g. before the first working day), and what happens to an unsubmitted questionnaire. Fold this into the D-036 re-confirmation.
9. **Implementation wording in the spec** – Phrases like 'repeating child block', 'add/remove', 'Expressions' and storing 'source tax questions apply' as its own value prescribe UI or storage design instead of the business need.  
   Evidence: tech_leak: US-06.1, feature.md notes, US-04.3, information.md  
   Action: Rephrase as needs: 'each child is assessed separately'. Drop the 'Expression' wording and drop recording the intermediate 'questions apply' value.
10. **Smaller gaps to tidy up** – These cause rework during refinement if left open.  
   Evidence: dev_refinement: AC-01.2.1 table shows '–' for country in the Switzerland row; US-08.4 has no check on the copy address and the copy holds sensitive data; US-08.1 has no owner for the permit-reminder wording; coverage: F-pension_portal-3a97ab unused  
   Action: Correct the AC-01.2.1 table. Decide on confirming the copy address and whether the copy includes question texts. Name who supplies the reminder text. Cite F-pension_portal-3a97ab in US-02.2 as the reason for the mid-month rule.

## Numbers

343 source units → 189 facts → 37 information items, 18 business rules → one feature with 8 sections, 30 stories, 88 acceptance criteria; 5 open questions, 10 exclusions.

## Impact of this run

Stories added: US-08.4; changed: -; removed: -; unchanged: 29.

Knowledge elements changed: OQ-copy-email-retention, copy_recipient_email, submission_copy_email, wants_copy_email

## Errors (1)

- [decisions] `D-036` new evidence since this decision (5 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-036`: F-hr_email_copy-029105: If the employee wants a copy, they type in the email address the copy should be sent to (asked at the end of the questionnaire, at submissio; F-hr_email_copy-37cede: At the end of the questionnaire, on submission, the employee should be able to send themselves an email with a copy of their form data.; F-hr_email_copy-ab2538: The emailed copy should show the answers exactly as they were submitted, nothing more. ...

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
- ✅ AC-08.4.1 / Employee is offered the copy at submission (spec)
- ✅ AC-08.4.2 / Employee wants a copy (spec)
- ✅ AC-08.4.2 / Employee does not want a copy (spec)
- ✅ AC-08.4.3 / Employee asks for a copy and gives an address (spec)
- ✅ AC-08.4.3 / Employee declines the copy (spec)
- ✅ AC-08.4.3 / Employee leaves the copy question unanswered (spec)

## Open questions (need your decision)

- **OQ-canton-abroad**: What does Pensionskasse Muster expect in 'Canton' for employees living abroad, and does 'Canton' mean canton of residence or of work? → recommended: Provisionally ask only residents of Switzerland (D-002); verify with a domain expert and the fund.
- **OQ-civil-status-partnership**: How does the pension fund want registered partnerships and separated employees registered (the list has only Single, Married, Divorced, Widowed), and does it want partner details? → recommended: Use the provisional mapping (D-003) until a domain expert verifies it.
- **OQ-spouse-dob-other-status**: Does the fund's screen ask for a spouse's date of birth (or other data) for Divorced or Widowed? → recommended: Do not ask divorced/widowed employees (D-004); verify with a screenshot of the fund's screen.
- **OQ-calculator-coverage**: Does Lonio's computed tariff code match the calculator on paths not explored: residence block for A/B/H tariffs, more than 3 children, H3N/P3N, and the child paths marked 'inferred' in the child result table? → recommended: Go-live condition: domain expert verification (D-009).
- **OQ-copy-email-retention**: Is the email address for the copy kept after the copy has been sent, and is it recorded for HR, or used only for sending? → recommended: Use it only to send the copy and do not record it for any receiving party.

## Inferred items to confirm

- item.spouse_residence_country
- item.copy_recipient_email
- rule.child_tariff_result
- rule.submission_copy_email
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
- fact F-hr_email_copy-b67d2f: The copy email address is only needed when the employee chooses to receive a copy of their form data.
- fact F-hr_email_copy-daa6b1: The emailed copy must not contain anything beyond the submitted answers (e.g. no derived values or additional information).
- fact F-hr_email_copy-fd28be: The copy email address serves only to send the employee their own copy; it is requested by HR for the employee's benefit, not as data a receiving party (pension fund, source tax) needs.

## Dev refinement questions (12)

- [major] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` Do employees living in Liechtenstein who return home daily (or expect 45 or fewer non-return days) still have to answer denomination, spouse employment and all the child questions? D-007 says Liechtenstein residents get all the source tax questions. But the AC-05.7.3 examples show '–' for denomination and children in the 'in principle no source tax' rows, and for those people the answers feed no tariff code. Under G-01 we should not ask them. This decides whether the Liechtenstein daily-return questions come before the rest of the source tax block and close it early.
- [major] `stories/US-08.3-questionnaire-is-read-only-for-the-employee-after-submission.md` After submission HR may change an answer so that new questions apply. Examples: a move from Switzerland to Germany, a corrected nationality, a marriage. The employee was never asked denomination, children or the cross-border questions, so the tariff code cannot be 're-derived from the latest answers' (D-037). Who supplies the missing answers? Does the employee's questionnaire reopen for just those questions, or is it all HR-side? And what is recorded for HR in the meantime: no tariff code, or an 'incomplete' state?
- [major] `feature.md` Should the Zurich calculator's logic (tariff letters, church-tax Y/N) be used for every employee subject to source tax, including those living in other Swiss cantons (for example Aargau or St. Gallen)? Or only for Zurich residents and cross-border commuters? If other cantons' residents need their own canton's rules or church-tax rules, the tariff computation and possibly the denomination question change.
- [major] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` The Germany and Liechtenstein non-return-day questions say 'in the calendar year'. For someone who starts in, say, November, is that the rest of the current year, the projected full year, or the next year? The answer changes what the question text says and when a later change (by HR) is needed.
- [major] `stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md` Can the employee leave the questionnaire and come back later to finish it (a saved draft)? Or must it be completed in one session? D-036 only says answers are kept 'while the employee goes back and forth'. Is there a deadline (for example before the first working day), and what happens to an unsubmitted draft?
- [minor] `stories/US-02.1-employee-enters-the-first-working-day.md` Are there limits on the dates an employee can enter? For example: a first working day in the past or far in the future, a date of birth that makes the employee under age or implausibly old, or a spouse's date of birth in the future. Should the questionnaire reject these or just accept them?
- [minor] `stories/US-08.1-remind-employees-to-bring-their-permit-on-the-first-working.md` HR 'provides the wording' for the permit reminder. Who delivers the final text before the build, and is it one fixed English text for Muster AG? Or must each customer company be able to set its own wording?
- [minor] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` D-007 says Lonio 'shows' the Liechtenstein result. Does the employee see any derived result (tariff code, 'in principle no source tax liability', insurance start date) at the end of the questionnaire? Or is it only recorded for HR? The email copy explicitly excludes derived results, which suggests the employee does not see them.
- [minor] `stories/US-08.4-send-myself-an-email-copy-of-my-submitted-answers.md` The copy contains sensitive data (religion, children, custody) and goes to any address the employee types in. Is that acceptable without checking the address (for example typing it twice or confirming it)? Does 'answers exactly as submitted, nothing more' still allow the question texts and section headings, so the copy can be read?
- [minor] `stories/US-01.2-complete-home-address-for-posting-documents.md` AC-01.2.1 says every address part, including the country, is required. But in its example table the Switzerland row shows '–' for country where the Germany row shows 'required'. Is this just a mistake in the table, or is the country meant to default to Switzerland?
- [minor] `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` Should the questionnaire explain 'of age and in first education' and 'replacement income' (for example age limits, what counts as first education, which benefits count)? Or does the employee judge these alone, as in the calculator? Wrong self-assessment changes the tariff code.
- [minor] `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` For married employees and registered partners the children question also covers the spouse's or partner's children. For a stepchild, how should the employee answer the custody and 'common household with the other parent' questions, given that the 'other parent' is not the spouse? Is the calculator's wording reused as it is?

## Technical vocabulary found in the spec (4)

- `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` "the employee can add further children and remove a child, and the child questions repeat per child" - Prescribes the UI interaction (add/remove repeating blocks). The business need is only that every child is assessed; how the employee enters several children is an engineering/UX choice.
- `feature.md` "Notes | Flow step 6, child block repeated per child (employee can add further children). Expressions describe one child." - 'Child block repeated' and 'Expressions' describe a form or rule-engine implementation rather than a business need.
- `stories/US-04.3-decide-whether-the-employee-is-subject-to-source-tax.md` "It is recorded for HR, together with the decision whether the source tax questions apply." - Says what intermediate derived state to store. Whether 'source tax questions apply' is kept as its own recorded value is a design choice; HR's stated need is the liability result and the tariff code.
- `information.md` "Rows marked inferred were not observed in the calculator and must be checked (OQ-calculator-coverage). Expression describes one child." - 'Expression' is rule-engine wording that slips implementation thinking into the business rule description.

## Coverage

168/343 source units cited; 151/189 facts used.

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

## Other warnings (45)

- [fact_judge] `F-hr_transcript-5518ad` partial: Address is needed, but 'home' is not stated explicitly. | HR needs the employee's home address.
- [fact_judge] `F-hr_transcript-550840` partial: Leo's summary and Anna's 'I think so' are supported, but 'later added further cases' is not in these units (T-044 in the neighbouring context does add the spouse case, so the gist holds). | Leo summarised 'non-Swiss, but not with a C permit'; Anna only hedged ('I think so') and later added further cases.
- [fact_judge] `F-hr_transcript-a45422` partial: Anna says she checks the spouse case by hand and asks for spouse details by email (takes forever), but 'HR' generalizes and 'asks for spouse details' is slightly loose (she asks them by email, presumably employees). | Today HR checks the spouse case by hand and asks for spouse details by email, which takes forever.
- [fact_judge] `F-hr_transcript-e505f8` partial: Address with country is collected and abroad residence matters, but the units never say that abroad status is derived from the address country; it's a reasonable inference. | Whether the employee lives abroad can be derived from the country of the home address, which is relevant for source tax liability.
- [fact_judge] `F-pension_portal-c8bc73` partial: Portal, page and Muster AG are supported, but 'insured person' is only implied by the breadcrumb 'Insured persons'; employer role inferred from header. | The source is the 'Register new employee' page in the Pensionskasse Muster employer portal, used by employer Muster AG to register a new employee as an insured person.
- [fact_judge] `F-pension_portal-3cfe89` partial: Footnote supports the asterisk rule, but these units don't show that all visible fields carry the marker. | Fields marked with an asterisk are required; all visible fields on the form carry the marker.
- [fact_judge] `F-pension_portal-6d3630` partial: Units show Divorced/Widowed options but cannot establish that no screenshot covers them; reasonable but unverifiable here. | Screenshots do not show whether the spouse's date of birth (or other fields) appears for 'Divorced' or 'Widowed'; only Single (no) and Married (yes) are shown.
- [fact_judge] `F-zh_source_tax_calculator-351289` partial: Skipping to Q16 is stated, but the units never say Q16 is the main-residence question. | If the income type is 'Ersatzeinkünfte', all personal and child questions are skipped and the calculator goes straight to the main-residence question (Q16).
- [fact_judge] `F-zh_source_tax_calculator-c78e0c` partial: Test vectors show A0Y/A0N for single persons without children, but 'resident in Switzerland' is not stated in these units (Q16 = Ja is unexplained). | A person with civil status 'Ledig, Geschieden, Getrennt, Verwitwet' and no counting children, resident in Switzerland, gets tariff letter A (e.g. A0Y / A0N).
- [fact_judge] `F-zh_source_tax_calculator-7dcce6` partial: Condition is Q08 = Nein; the units never state that Q08 means 'child not in same household'. | Q13 is shown only when civil status is married/registered partnership AND the child is 'Minderjährig' AND the child does not live in the same household.
- [fact_judge] `F-zh_source_tax_calculator-fb4a56` partial: Condition is Q08 = Nein; the units never state that Q08 means 'child not in same household'. | Q14 is shown only when civil status is 'Ledig, Geschieden, Getrennt, Verwitwet' AND the child is 'Minderjährig' AND the child does not live in the same household.
- [fact_judge] `F-zh_source_tax_calculator-cd1015` partial: The meanings of Q08 and Q10 (same household, common household with other parent) are not defined in these units. | Q15 is shown only when the child is 'Volljährig und in Erstausbildung' AND (child not in same household OR (same household AND no common household with the other parent)).
- [fact_judge] `F-zh_source_tax_calculator-3058a4` partial: Test vectors give C1Y for Q10=Ja and C0Y for the Q10=Nein cases, but the question labels (common household, alternating care) aren't shown in the units, and the statement contains an unfinished 'only if...' fragment. | Married person, minor child in same household, shared custody: common household with the other parent counts the child (C1Y); no common household counts the child only if... observed: alternating care with other parent as main contributor -> 0 (C0Y), no alternating care -> 0 (C0Y).
- [fact_judge] `F-zh_source_tax_calculator-56e79b` partial: Vectors V12/V13 show B1N vs B0N, but labelling Q13 as 'shared custody' and Q11/Q12 as alternating care/main contributor is a guess, since question texts aren't in these units. | Married person, minor child not in household: shared custody + alternating care + person is main contributor counts the child (B1N); no shared custody does not count it (B0N).
- [fact_judge] `F-zh_source_tax_calculator-c2faa7` partial: V20/V21 show H1N vs A0N, but the label 'parental care' for Q14 is not stated in the units. | Single person, minor child not in household: parental care Ja + alternating care + person main contributor -> H1N; parental care Nein -> A0N.
- [fact_judge] `F-hr_email_copy-fd28be` partial: The address is for sending the employee their own copy, but the email says nothing about pension fund or source tax recipients, so that contrast is not stated. | The copy email address serves only to send the employee their own copy; it is requested by HR for the employee's benefit, not as data a receiving party (pension fund, source tax) needs.
- [coverage] `F-pension_portal-3a97ab` fact not used anywhere in the spec: The portal requires an insurance start date on the 1st of a month but does not say how it relates to the employee's first working day (e.g. which 1st of a month to use when work starts mid-month).
- [coverage] `F-hr_email_copy-607694` fact not used anywhere in the spec: Apart from the copy-email feature, everything else stays as discussed in the earlier HR meeting.
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
- [dev_refinement] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` Do employees living in Liechtenstein who return home daily (or expect 45 or fewer non-return days) still have to answer denomination, spouse employment and all the child questions? D-007 says Liechtenstein residents get all the source tax questions. But the AC-05.7.3 examples show '–' for denomination and children in the 'in principle no source tax' rows, and for those people the answers feed no tariff code. Under G-01 we should not ask them. This decides whether the Liechtenstein daily-return questions come before the rest of the source tax block and close it early.
- [dev_refinement] `stories/US-08.3-questionnaire-is-read-only-for-the-employee-after-submission.md` After submission HR may change an answer so that new questions apply. Examples: a move from Switzerland to Germany, a corrected nationality, a marriage. The employee was never asked denomination, children or the cross-border questions, so the tariff code cannot be 're-derived from the latest answers' (D-037). Who supplies the missing answers? Does the employee's questionnaire reopen for just those questions, or is it all HR-side? And what is recorded for HR in the meantime: no tariff code, or an 'incomplete' state?
- [dev_refinement] `feature.md` Should the Zurich calculator's logic (tariff letters, church-tax Y/N) be used for every employee subject to source tax, including those living in other Swiss cantons (for example Aargau or St. Gallen)? Or only for Zurich residents and cross-border commuters? If other cantons' residents need their own canton's rules or church-tax rules, the tariff computation and possibly the denomination question change.
- [dev_refinement] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` The Germany and Liechtenstein non-return-day questions say 'in the calendar year'. For someone who starts in, say, November, is that the rest of the current year, the projected full year, or the next year? The answer changes what the question text says and when a later change (by HR) is needed.
- [dev_refinement] `stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md` Can the employee leave the questionnaire and come back later to finish it (a saved draft)? Or must it be completed in one session? D-036 only says answers are kept 'while the employee goes back and forth'. Is there a deadline (for example before the first working day), and what happens to an unsubmitted draft?

## Run

Stages run: normalize/hr_email_copy, extract/hr_email_copy, judge_facts, knowledge.raw, feature.plan, sections/SEC-01-identity-and-address, sections/SEC-08-completion-and-submission, judge_trace, dev_refinement, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator

LLM cost this run: $4.54
