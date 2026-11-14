# Review: employee-onboarding

**Verdict: NOT READY**

All 220 examples pass and no open question is marked blocking. One error stops release: decision D-036 is out of date because of new evidence from the HR email-copy message. The same topic, keeping answers while going back and forth, also shows up as a technical leak and a major refinement question in US-08.2. Refinement also raised 7 major questions that the product owner needs to decide. The most important are which address counts for new hires who are moving, the partial-year non-return-day limits, the question order for Liechtenstein residents, and protecting the email copy. Once D-036 is fixed and the major questions are answered, this becomes ready_with_caveats. What remains after that is the 6 non-blocking open questions, 12 inferred items and some citation gaps.

## Reviewer findings

1. **D-036 is out of date: 4 new facts from the HR email-copy source** – Error-level traceability break. The decision was made before the email-copy facts existed, so stories that depend on it (US-08.2, US-08.5) rest on an unconfirmed basis.  
   Evidence: decisions error D-036; F-hr_email_copy-029105, -37cede, -ab2538 (+1)  
   Action: Read D-036 again against the email-copy facts. Confirm it, update it or drop it in decisions.yaml, then run `pipeline reconfirm D-036`.
2. **US-08.2 turns 'may keep answers' into a hard rule about how drafts are stored** – This is a technical leak and the spec contradicts itself. D-036 says answers 'may be kept', but AC-08.2.1 says they 'are kept' and must reappear. Engineering can't tell what is required, including whether drafts must survive across sessions.  
   Evidence: tech_leak US-08.2; dev_refinement major US-08.2  
   Action: Decide in D-036: are drafts kept within one sitting only, or across sessions, and is restoring earlier answers required? Rewrite AC-08.2.1 as a need, not as a way of storing data.
3. **No rule for which home address counts when a new hire is moving** – The country decides source tax liability, canton, nationality questions and the cross-border tariff. A hire moving to Switzerland could get the wrong path.  
   Evidence: dev_refinement major feature.md  
   Action: Add a decision: current address or address on the first working day, and whether both are recorded.
4. **Non-return-day limits (60 for Germany, 45 for Liechtenstein) are unclear for hires who start mid-year** – The answer changes the question wording and the tariff result for cross-border employees.  
   Evidence: dev_refinement major US-07.2; rule.cross_border_tariff_applies  
   Action: Ask a domain expert or the Zurich tax office to clarify. Record the answer (count the remaining year, or scale the limit) as a decision.
5. **Liechtenstein residents are asked tariff and child questions that may never be used (data minimisation, G-01)** – Denomination and children's data are collected for no purpose when the result is 'in principle no source tax'. There is also a conflict about what to record as 'Subject to source tax' (yes or no).  
   Evidence: dev_refinement major US-07.3; info feature.md (Liechtenstein subject flag); D-007  
   Action: Decide the step order (cross-border questions for Liechtenstein first) and what value HR records for 'Subject to source tax'. Add both to decisions.yaml.
6. **The email copy sends sensitive data to an address that is never checked** – Denomination, nationality, custody and spouse data could go to the wrong address. This is a data-protection risk in the new story US-08.5, which is inferred.  
   Evidence: dev_refinement major US-08.5; OQ-copy-email-retention; inferred story.US-08.5, rule.employee_copy  
   Action: HR or the data-protection contact decides: confirm the address, limit the copy to an address HR already has, or accept the risk. Also settle whether the address is kept and what the copy contains (question wording, permit reminder).
7. **The first working day and the read-only view are not fully specified** – It's unclear whether the employee confirms a date HR already has or types it in, and which dates are valid. It's also unclear whether derived results (tariff code, insurance start) appear in the read-only view.  
   Evidence: dev_refinement major US-02.1, US-08.3  
   Action: Add decisions on how the date is entered and checked, and on what the employee sees after submission.
8. **The H tariff for a child outside the household contradicts the calculator note, and some example rows contradict their own labels** – This risks a wrong tariff code (H or A), and tests can't rely on example rows that contradict their own labels.  
   Evidence: dev_refinement US-06.4 (F-…-96658b vs AC-06.4.3 row 22); US-05.6 (C1Y rows with Has children=no; AC-05.4.3 input/output); many '(to be verified)' cases in US-06.4/06.5  
   Action: Have a domain expert check these against the Zurich calculator (as part of OQ-calculator-coverage). Fix the example rows.
9. **Claims that rest on uncited facts (traceability gaps)** – The 'H tariff' purpose on 8 child items, rows citing facts that aren't in their cited set, and claims in story priority reasons can't be traced to a source.  
   Evidence: trace_judge partial: item.child_* (8), rule.cross_border_tariff_applies, rule.liechtenstein_no_source_tax_in_principle, rule.source_tax_result (F-…-52b67a, F-hr_transcript-b6d9b3), US-01.2, US-05.4, US-08.3, US-08.4, US-08.5  
   Action: Add the missing citations (F-…-52b67a, F-hr_transcript-b6d9b3, -d7431e, D-010/D-038). Cite or remove the 'H tariff' purpose and the unsupported priority reasons.
10. **Internal ids and UI mechanics in business text** – Rule ids and the child_* field prefix appear in prose, and the add/remove child interaction is prescribed, which is a design decision for engineering.  
   Evidence: tech_leak US-06.1 (×2), feature.md (×2)  
   Action: Use business names instead (for example 'Subject to source tax', 'permit reminder'). State the need: any number of children, each assessed separately.

## Numbers

343 source units → 187 facts → 37 information items, 18 business rules → one feature with 8 sections, 31 stories, 105 acceptance criteria; 6 open questions, 12 exclusions.

## Impact of this run

Stories added: US-08.5; changed: -; removed: -; unchanged: 30.

Knowledge elements changed: OQ-copy-email-retention, copy_email_address, employee_copy, send_copy_requested

## Errors (1)

- [decisions] `D-036` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-036`: F-hr_email_copy-029105: The employee types in the email address the copy of their form data should be sent to.; F-hr_email_copy-37cede: At the end of the questionnaire, when submitting, the employee should be able to send themselves an email with a copy of their form data.; F-hr_email_copy-ab2538: The copy must show the answers exactly as they were submitted, nothing more. ...

## Examples executed against the knowledge model (225/225 pass)

- ✅ AC-01.1.1 / Any employee, regardless of later answers (spec)
- ✅ AC-01.2.1 / Tomás, living in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-01.2.1 / Employee living in Germany (e.g. Konstanz) (spec)
- ✅ AC-01.3.2 / Tomás, living in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-01.3.2 / Employee living in Germany (e.g. Konstanz) (spec)
- ✅ AC-01.3.2 / Employee living in Liechtenstein (spec)
- ✅ AC-01.3.2 / Employee living in another country (spec)
- ✅ AC-01.3.3 / Employee living in Germany, e.g. a Swiss citizen like Stefan (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-01.3.3 / Tomás, living in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-01.4.1 / Tomás, living in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-01.4.1 / Employee living in Germany (e.g. Konstanz) (spec)
- ✅ AC-01.4.1 / Employee living in Liechtenstein (spec)
- ✅ AC-01.4.3 / Employee who first entered Switzerland, then corrected to Germany (spec)
- ✅ AC-02.1.1 / Employee living in Switzerland (spec)
- ✅ AC-02.1.1 / Employee living abroad (spec)
- ✅ AC-02.2.2 / Start on the 1st of a month (spec)
- ✅ AC-02.2.2 / Start on 1st January (spec)
- ✅ AC-02.2.3 / Julia (hr_transcript/F-hr_transcript-d7a23b), first working day 15 March (year illustrative) (spec)
- ✅ AC-02.2.3 / Start on the last day of a month (spec)
- ✅ AC-02.2.3 / Start in mid-December (spec)
- ✅ AC-02.2.4 / Julia (hr_transcript/F-hr_transcript-d7a23b), moved to 15 March (year illustrative) (spec)
- ✅ AC-02.2.4 / Earlier exit agreed, start moved to the 1st (spec)
- ✅ AC-03.1.1 / Employee living in Switzerland, Single (spec)
- ✅ AC-03.1.1 / Employee living in Germany, Married (spec)
- ✅ AC-03.1.2 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-03.2.1 / Married employee (spec)
- ✅ AC-03.2.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-03.2.1 / Separated employee (spec)
- ✅ AC-03.2.2 / Single employee (spec)
- ✅ AC-03.2.2 / Divorced employee (spec)
- ✅ AC-03.2.2 / Widowed employee (spec)
- ✅ AC-03.3.1 / Single (spec)
- ✅ AC-03.3.1 / Married (spec)
- ✅ AC-03.3.1 / Divorced (spec)
- ✅ AC-03.3.1 / Widowed (spec)
- ✅ AC-03.3.2 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-03.3.2 / Separated (spec)
- ✅ AC-03.4.1 / Married (spec)
- ✅ AC-03.4.1 / Daniel, registered partnership (hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-03.4.2 / Single (spec)
- ✅ AC-03.4.2 / Divorced (spec)
- ✅ AC-03.4.2 / Widowed (spec)
- ✅ AC-03.4.2 / Separated (spec)
- ✅ AC-04.1.1 / Swiss citizen living abroad, like Stefan (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-04.1.1 / Employee living in Liechtenstein (spec)
- ✅ AC-04.1.1 / Tomás, Brazilian living in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.1.3 / Tomás, Brazilian living in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.1.3 / Swiss citizen (also dual citizen) living in Switzerland (spec)
- ✅ AC-04.1.3 / Employee living in Germany (spec)
- ✅ AC-04.2.1 / Tomás, Brazilian, B permit, married (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.2.1 / Registered partner without C permit (spec)
- ✅ AC-04.2.1 / Separated employee without C permit (spec)
- ✅ AC-04.2.1 / Married employee with C permit (spec)
- ✅ AC-04.2.1 / Married employee living abroad (spec)
- ✅ AC-04.2.2 / Tomás, wife lives in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.2.2 / Spouse lives in Germany (spec)
- ✅ AC-04.2.3 / Tomás, Swiss wife (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.2.3 / Italian spouse living in Switzerland (spec)
- ✅ AC-04.2.4 / Tomás, Swiss wife in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.2.4 / Registered partner with Swiss partner (spec)
- ✅ AC-04.2.4 / Spouse with C permit living in Switzerland (spec)
- ✅ AC-04.2.4 / Spouse without C permit living in Switzerland (spec)
- ✅ AC-04.2.4 / Spouse living abroad (spec)
- ✅ AC-04.2.4 / Separated employee (counts as not married) (spec)
- ✅ AC-04.2.4 / Single employee (spec)
- ✅ AC-04.3.1 / Living in Konstanz, Germany (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-04.3.1 / Living in Liechtenstein (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-04.3.1 / Living in another country (spec)
- ✅ AC-04.3.2 / Swiss citizen living in Switzerland (incl. dual citizen) (spec)
- ✅ AC-04.3.2 / Non-Swiss with C permit (spec)
- ✅ AC-04.3.2 / Tomás, Brazilian, B permit, Swiss wife in Winterthur (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.3.2 / Single non-Swiss without C permit (spec)
- ✅ AC-04.3.2 / Married non-Swiss without C permit, spouse living abroad (spec)
- ✅ AC-04.3.2 / Married non-Swiss without C permit, non-Swiss spouse without C permit (spec)
- ✅ AC-04.3.3 / Swiss citizen living in Switzerland (spec)
- ✅ AC-04.3.3 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-04.3.3 / Living in Germany (spec)
- ✅ AC-05.3.1 / Tomás (hr_transcript/F-hr_transcript-d7431e) - Brazilian, B permit, Swiss wife living in Switzerland, not subject (spec)
- ✅ AC-05.3.1 / Employee living in Germany - subject whatever the nationality (spec)
- ✅ AC-05.3.1 / Non-Swiss resident of Switzerland without C permit, single - subject (spec)
- ✅ AC-05.3.1 / Swiss citizen living in Switzerland - not subject (spec)
- ✅ AC-05.3.1 / Non-Swiss resident of Switzerland with C permit - not subject (spec)
- ✅ AC-05.3.3 / Calculator run A0Y - single, no children, church member (zh_source_tax_calculator/F-zh_source_tax_calculator-c78e0c) (spec)
- ✅ AC-05.3.3 / Calculator run A0N - single, no children, none or other (zh_source_tax_calculator/F-zh_source_tax_calculator-2eab9a) (spec)
- ✅ AC-05.4.1 / Married employee living in Germany (spec)
- ✅ AC-05.4.1 / Registered partner living in Germany - counts as married for source tax (like Daniel's civil status, hr_transcript/F-hr_transcript-3907fe) (spec)
- ✅ AC-05.4.1 / Separated employee living in Germany - counts as single for source tax (spec)
- ✅ AC-05.4.1 / Single employee living in Germany (spec)
- ✅ AC-05.4.1 / Divorced employee living in Germany (spec)
- ✅ AC-05.4.1 / Widowed employee living in Germany (spec)
- ✅ AC-05.4.1 / Tomás (hr_transcript/F-hr_transcript-d7431e) - married but not subject, Swiss wife in Switzerland (spec)
- ✅ AC-05.4.3 / Calculator run C0Y - spouse employed (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-05.4.3 / Calculator run B0Y - spouse not employed (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-05.6.1 / Calculator run C0Y - married, spouse employed (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-05.6.1 / Calculator run B0Y - married, spouse not employed (zh_source_tax_calculator/F-zh_source_tax_calculator-97139a) (spec)
- ✅ AC-05.6.1 / Calculator run A0Y - single, no children (zh_source_tax_calculator/F-zh_source_tax_calculator-c78e0c) (spec)
- ✅ AC-05.6.1 / Calculator run H1Y - single, minor child in household with sole custody (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-05.6.1 / Separated employee counts as not married - letter A (spec)
- ✅ AC-05.6.1 / Registered partner counts as married - partner employed gives C (spec)
- ✅ AC-05.6.1 / Calculator run A0N - single living in another country keeps the base letter (zh_source_tax_calculator/F-zh_source_tax_calculator-52b67a) (spec)
- ✅ AC-05.6.2 / Calculator run L0Y - single, daily return with certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.6.2 / Calculator run M0N - married, spouse not employed, daily return with certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.6.2 / Calculator run N1Y - married, spouse employed, no daily return, return reasonable, not more than 60 non-return days (zh_source_tax_calculator/F-zh_source_tax_calculator-b948fd) (spec)
- ✅ AC-05.6.2 / Calculator run P1Y - single with an H child, daily return with certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.6.2 / Calculator run C1Y - more than 60 non-return days gives the normal letter (zh_source_tax_calculator/F-zh_source_tax_calculator-b948fd) (spec)
- ✅ AC-05.6.2 / Calculator run C1Y - daily return not reasonable gives the normal letter (zh_source_tax_calculator/F-zh_source_tax_calculator-bc1639) (spec)
- ✅ AC-05.6.2 / Daily return, certificate 'not yet' - normal letter A (spec)
- ✅ AC-05.6.2 / Calculator run - daily return without certificate gives the normal letter (zh_source_tax_calculator/F-zh_source_tax_calculator-4d3ac0) (spec)
- ✅ AC-05.7.1 / Tomás (hr_transcript/F-hr_transcript-d7431e) - Swiss wife living in Switzerland (spec)
- ✅ AC-05.7.1 / Swiss citizen living in Switzerland (spec)
- ✅ AC-05.7.2 / Calculator run A0Y - single, no children, church member (zh_source_tax_calculator/F-zh_source_tax_calculator-c78e0c) (spec)
- ✅ AC-05.7.2 / Calculator run L0Y - single living in Germany, daily return with certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.7.2 / Calculator run M0N - married living in Germany, spouse not employed, daily return with certificate (zh_source_tax_calculator/F-zh_source_tax_calculator-b7154e) (spec)
- ✅ AC-05.7.2 / Calculator run C1Y - married resident, spouse employed, one minor child with sole custody (zh_source_tax_calculator/F-zh_source_tax_calculator-c53a22) (spec)
- ✅ AC-05.7.3 / Calculator run - daily return to Liechtenstein (zh_source_tax_calculator/F-zh_source_tax_calculator-e80d8f) (spec)
- ✅ AC-05.7.3 / Calculator run - no daily return, at most 45 non-return days (zh_source_tax_calculator/F-zh_source_tax_calculator-ab4e1e) (spec)
- ✅ AC-05.7.3 / Calculator run C1Y - more than 45 non-return days gives the normal tariff code (zh_source_tax_calculator/F-zh_source_tax_calculator-ab4e1e) (spec)
- ✅ AC-06.1.1 / Employee living in Germany is asked (spec)
- ✅ AC-06.1.1 / Non-Swiss employee without C permit living in Switzerland is asked (spec)
- ✅ AC-06.1.1 / Swiss employee living in Switzerland is not asked (spec)
- ✅ AC-06.1.1 / C permit holder living in Switzerland is not asked (spec)
- ✅ AC-06.1.2 / Employee with children gets the age status question (spec)
- ✅ AC-06.1.2 / Employee without children gets no child block (spec)
- ✅ AC-06.1.3 / Adult child no longer in first education (spec)
- ✅ AC-06.1.3 / Single employee, child neither minor nor in first education (spec)
- ✅ AC-06.1.4 / Minor child (spec)
- ✅ AC-06.1.4 / Child of age in first education (spec)
- ✅ AC-06.2.1 / Minor in household - custody asked (spec)
- ✅ AC-06.2.1 / Minor not in household - custody (shared/sole) not asked (spec)
- ✅ AC-06.2.1 / Sole custody ends the block (spec)
- ✅ AC-06.2.2 / Shared custody - common household asked (spec)
- ✅ AC-06.2.2 / No common household - alternating care asked (spec)
- ✅ AC-06.2.2 / Common household - alternating care not asked (spec)
- ✅ AC-06.2.3 / Married, sole custody (spec)
- ✅ AC-06.2.3 / Registered partnership, shared custody, common household with other parent (spec)
- ✅ AC-06.2.3 / Married, shared custody, no common household, no alternating care (spec)
- ✅ AC-06.2.4 / Single, sole custody (spec)
- ✅ AC-06.2.4 / Divorced, shared custody, no common household, no alternating care (spec)
- ✅ AC-06.3.1 / Married employee (spec)
- ✅ AC-06.3.1 / Separated employee counts as not married (spec)
- ✅ AC-06.3.2 / Married, shared custody - alternating care asked (spec)
- ✅ AC-06.3.2 / Married, no shared custody (spec)
- ✅ AC-06.3.2 / Single, no parental custody (spec)
- ✅ AC-06.3.3 / Married, shared custody, no alternating care (spec)
- ✅ AC-06.3.3 / Widowed, parental custody, no alternating care (spec)
- ✅ AC-06.4.1 / Alternating care, child in household (spec)
- ✅ AC-06.4.1 / Single, common household with other parent (spec)
- ✅ AC-06.4.1 / Married, common household with other parent - not asked (spec)
- ✅ AC-06.4.1 / Married, child of age in common household - not asked (spec)
- ✅ AC-06.4.2 / In household, employee contributes more (to be verified) (spec)
- ✅ AC-06.4.2 / In household, other parent contributes more (spec)
- ✅ AC-06.4.2 / Outside household, employee contributes more (spec)
- ✅ AC-06.4.2 / Outside household, other parent contributes more (to be verified) (spec)
- ✅ AC-06.4.3 / Minor, common household, employee contributes more (spec)
- ✅ AC-06.4.3 / Minor, common household, other parent contributes more (spec)
- ✅ AC-06.4.3 / Minor in household, alternating care, employee contributes more (spec)
- ✅ AC-06.4.3 / Minor in household, alternating care, other parent contributes more (to be verified) (spec)
- ✅ AC-06.4.3 / Minor outside household, parental custody, alternating care, employee contributes more (spec)
- ✅ AC-06.4.3 / Minor outside household, other parent contributes more (to be verified) (spec)
- ✅ AC-06.4.3 / Child of age, common household, employee contributes more (to be verified) (spec)
- ✅ AC-06.4.3 / Child of age, common household, other parent contributes more (to be verified) (spec)
- ✅ AC-06.5.1 / Child of age in household - common household asked (spec)
- ✅ AC-06.5.1 / Child of age outside household - maintenance asked (spec)
- ✅ AC-06.5.1 / Common household with other parent - maintenance not asked (spec)
- ✅ AC-06.5.2 / In household, common household with other parent (spec)
- ✅ AC-06.5.2 / In household, no common household, mainly maintained (to be verified) (spec)
- ✅ AC-06.5.2 / In household, no common household, not mainly maintained (to be verified) (spec)
- ✅ AC-06.5.2 / Outside household, mainly maintained (to be verified) (spec)
- ✅ AC-06.5.2 / Outside household, not mainly maintained (spec)
- ✅ AC-06.5.3 / In household, mainly maintained (spec)
- ✅ AC-06.5.3 / In household, not mainly maintained (to be verified) (spec)
- ✅ AC-06.5.3 / Outside household, mainly maintained (spec)
- ✅ AC-06.5.3 / Outside household, not mainly maintained (to be verified) (spec)
- ✅ AC-06.6.1 / No children (spec)
- ✅ AC-06.6.1 / One child counted (married, sole custody) (spec)
- ✅ AC-06.6.1 / One child counted with H (spec)
- ✅ AC-06.6.1 / Only child does not count (spec)
- ✅ AC-06.6.2 / Single, child with sole custody in household (spec)
- ✅ AC-06.6.2 / Single, child of age outside household counted without H (spec)
- ✅ AC-06.6.2 / Single, no children (spec)
- ✅ AC-06.6.2 / Married, child with sole custody (spec)
- ✅ AC-07.1.1 / Employee living in Konstanz (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-07.1.1 / Employee living in Liechtenstein (spec)
- ✅ AC-07.1.1 / Employee living in Switzerland (spec)
- ✅ AC-07.1.1 / Employee living in France (spec)
- ✅ AC-07.1.2 / Employee living in France (spec)
- ✅ AC-07.1.2 / Employee living in Switzerland (spec)
- ✅ AC-07.2.1 / Employee living in Konstanz (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-07.2.1 / Employee living in Liechtenstein (spec)
- ✅ AC-07.2.2 / Daily returner (spec)
- ✅ AC-07.2.2 / No daily return (spec)
- ✅ AC-07.2.3 / Return reasonable (spec)
- ✅ AC-07.2.3 / Return not reasonable (spec)
- ✅ AC-07.2.4 / Daily return with certificate (spec)
- ✅ AC-07.2.4 / Daily return without certificate (spec)
- ✅ AC-07.2.4 / Daily return, certificate not yet provided (spec)
- ✅ AC-07.2.4 / No daily return, return not reasonable (spec)
- ✅ AC-07.2.4 / No daily return, reasonable, more than 60 non-return days (spec)
- ✅ AC-07.2.4 / No daily return, reasonable, at most 60 non-return days (spec)
- ✅ AC-07.2.4 / Employee living in Liechtenstein (spec)
- ✅ AC-07.3.1 / Employee living in Liechtenstein (spec)
- ✅ AC-07.3.1 / Employee living in Germany (spec)
- ✅ AC-07.3.2 / No daily return (spec)
- ✅ AC-07.3.2 / Daily return (spec)
- ✅ AC-07.3.3 / Daily return (spec)
- ✅ AC-07.3.3 / No daily return, at most 45 non-return days (spec)
- ✅ AC-07.3.3 / No daily return, more than 45 non-return days (spec)
- ✅ AC-07.3.3 / Employee living in Germany (spec)
- ✅ AC-08.1.1 / Tomás (hr_transcript/F-hr_transcript-d7431e) (spec)
- ✅ AC-08.1.2 / Swiss citizen living in Germany, like Stefan (hr_transcript/F-hr_transcript-1a20bb) (spec)
- ✅ AC-08.1.2 / Employee living in Liechtenstein (spec)
- ✅ AC-08.1.3 / Swiss employee living in Switzerland (spec)
- ✅ AC-08.2.2 / Moved the home address from Switzerland to Germany after answering nationality and canton (spec)
- ✅ AC-08.2.2 / Changed civil status from Married to Single after entering the spouse's date of birth (spec)
- ✅ AC-08.2.2 / Changed nationality to Switzerland after answering the C permit question and the source tax questions (spec)
- ✅ AC-08.3.2 / First working day moved from the 15th to the 1st of a month (spec)
- ✅ AC-08.3.2 / First working day in the middle of a month (spec)
- ✅ AC-08.4.2 / Swiss employee living in Switzerland, single (spec)
- ✅ AC-08.4.2 / Employee living in Germany, single (spec)
- ✅ AC-08.5.1 / Any employee at submission (spec)
- ✅ AC-08.5.2 / Wants a copy (spec)
- ✅ AC-08.5.2 / Declines the copy (spec)
- ✅ AC-08.5.3 / Copy requested with an address (spec)
- ✅ AC-08.5.4 / Declines the copy (spec)
- ✅ AC-08.5.4 / Leaves the copy question unanswered (spec)

## Open questions (need your decision)

- **OQ-canton-abroad**: What should be entered in the pension fund's 'Canton' field for employees living abroad, and does 'Canton' mean canton of residence or of work? → recommended: Keep D-002 (ask only residents of Switzerland); a domain expert verifies with Pensionskasse Muster.
- **OQ-civil-status-partnership**: How does Pensionskasse Muster want registered partnerships and separated employees registered (its list has only Single, Married, Divorced, Widowed), and does it want the partner's details? → recommended: Keep the provisional mapping of D-003; verify with a domain expert and the fund.
- **OQ-spouse-dob-other-status**: Does the fund's screen require the spouse's (or former spouse's) date of birth or other fields for Divorced or Widowed? → recommended: Domain expert obtains a screenshot of the fund screen for Divorced and Widowed.
- **OQ-calculator-coverage**: Does Lonio's computed tariff code match the Zurich calculator on the paths not explored: the residence block for A/B/H tariffs, more than 3 children, H3N/P3N, and the child rows marked inferred? → recommended: Go-live condition per D-009; non-blocking for the spec.
- **OQ-nationality-wording**: Should the questionnaire ask for the nationality as a country, or only whether the employee (and the spouse) holds Swiss citizenship? And does the dual-citizenship rule (D-008) also apply to the spouse? → recommended: Keep the current model and confirm with the product owner; apply D-008 to the spouse unless a domain expert says otherwise.
- **OQ-copy-email-retention**: Is the email address for the copy kept after the copy is sent, and is it recorded for HR? Or is it used only to send the copy? → recommended: Use it only to send the copy; HR confirms.

## Inferred items to confirm

- item.spouse_residence_country
- item.spouse_nationality
- item.send_copy_requested
- item.copy_email_address
- rule.child_tariff_result
- rule.employee_copy
- story.US-04.2
- story.US-06.3
- story.US-06.4
- story.US-06.5
- story.US-08.4
- story.US-08.5
- fact F-pension_portal-39bab1: The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected).
- fact F-pension_portal-6d3630: Screenshots do not show whether the spouse's date of birth (or other fields) appears for 'Divorced' or 'Widowed'; only Single (no) and Married (yes) are shown.
- fact F-pension_portal-9b24c5: The civil status list has no option for registered partnership or separated; it is unclear how such employees are to be registered.
- fact F-pension_portal-b359c3: The label 'Canton' does not state whether it is the canton of residence or of work, and the list only contains Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. a cross-border commuter).
- fact F-pension_portal-3a97ab: The portal requires an insurance start date on the 1st of a month but does not say how it relates to the employee's first working day (e.g. which 1st of a month to use when work starts mid-month).
- fact F-hr_email_copy-b67d2f: The copy email address is only needed when the employee chooses to receive a copy (it is not required otherwise).
- fact F-hr_email_copy-07f744: The email copy request comes from the employer's HR (Anna, Muster AG) as an addition forgotten in the meeting; the copy's recipient is the employee themselves, not one of the receiving parties.

## Dev refinement questions (16)

- [major] `feature.md` Which home address counts when a new hire is moving for the job, for example someone living abroad today who will live in Switzerland by the first working day? The country decides source tax liability, the canton, the nationality questions and the cross-border tariff, so we need to know whether to ask for the current address or the address on the first working day, and whether one form can record both.
- [major] `stories/US-02.1-employee-enters-the-first-working-day.md` HR says it asks employees to 'confirm' the first working day. Does that mean Lonio shows the planned date HR already knows so the employee confirms or corrects it, or does the employee type it in from scratch? Also, which dates are valid: can the date be in the past, on a weekend, or more than X months ahead?
- [major] `stories/US-08.3-questionnaire-is-read-only-for-the-employee-after-submission.md` After submission the employee 'can see their answers'. Should the employee also see the derived results (insurance start date, civil status for the fund, tariff code, the Liechtenstein statement)? The email copy explicitly leaves them out, so the read-only view needs its own decision.
- [major] `stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md` Can the employee stop part-way and come back later (a saved draft across sessions), or does the questionnaire only have to keep answers during one sitting? D-036 says answers 'may be kept' while going back and forth, but AC-08.2.1 says they 'are kept' and must reappear. Which one is the requirement?
- [major] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` The 60 (Germany) and 45 (Liechtenstein) non-return-day limits apply to 'the calendar year'. For a new hire who starts mid-year, should the employee count only the remaining months, or should the limit be scaled down for a partial year? The answer changes the wording of the question and the tariff result.
- [major] `stories/US-07.3-determine-the-source-tax-outcome-for-employees-living-in.md` For Liechtenstein residents who return daily, the result is 'in principle no source tax liability', so the denomination, spouse-employment and children answers they gave are never used. The cross-border step comes after the children, so we collect religion and child data with no purpose (G-01). Should the Liechtenstein daily-return and 45-day questions come first, so the tariff questions are only asked when a tariff code results? D-007 says Liechtenstein residents get the source tax questions, but it does not settle the order.
- [major] `stories/US-08.5-optional-email-copy-of-the-submitted-answers.md` The copy holds sensitive answers (denomination, nationality, custody and children details, spouse data) and goes to an address the employee types in without any check. Is that acceptable to the business and for data protection, or must the address be confirmed first, or limited to an address HR already holds?
- [minor] `stories/US-08.5-optional-email-copy-of-the-submitted-answers.md` Should the copy include the questions as they were worded, or only the answer values? Should it also include the permit reminder text the employee saw? 'Exactly as submitted, nothing more' leaves this open.
- [minor] `feature.md` For a Liechtenstein resident with the 'in principle no source tax liability' result, what does Lonio record as 'Subject to source tax' for HR: yes (as the liability rule says) or no? The two records point in different directions.
- [minor] `stories/US-06.4-ask-who-contributes-more-to-the-child-s-maintenance.md` The calculator note (F-...-96658b) says a child counts with H only when it lives in the employee's household. Child-result row 22 and AC-06.4.3, however, count a minor child outside the household (parental custody, alternating care, employee pays more) 'with H'. Which one is right for a non-married employee: H or A?
- [minor] `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` On what date is a child judged a 'Minor', for example a child turning 18 during the year: the first working day or the day the questionnaire is filled in? Is there a maximum number of children an employee can add? The calculator was only checked up to 3.
- [minor] `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` Married employees are asked about children 'of the employee or of either spouse'. For a stepchild, how should the custody questions (sole or shared custody, the other parent) be answered? Do they apply as worded?
- [minor] `stories/US-01.2-complete-home-address-for-posting-documents.md` The house number is always required, but some addresses have none (rural addresses, named buildings). Should a missing house number be allowed, and if so how? information.md already notes that the sources don't settle this.
- [minor] `stories/US-04.1-ask-swiss-citizenship-and-c-permit-only-of-employees-living.md` How should a stateless employee, or one whose nationality is unclear, answer the nationality question? Should they then go straight to the C-permit question?
- [minor] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` For the certificate of residence, 'no' and 'not yet' both count as no for the tariff. Does HR need to treat them differently (e.g. 'no' means no certificate will ever come)? If not, are three options really needed?
- [minor] `stories/US-05.6-determine-the-tariff-letter-including-the-cross-border.md` Some example rows contradict their own labels. In AC-05.6.2, 'Calculator run C1Y' rows have Has children = no. In AC-05.4.3, the spouse-employment answer is listed both as an input and as an output ('asked'). Which values are correct, so the tests can rely on them?

## Technical vocabulary found in the spec (5)

- `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` "When Lonio has decided whether the employee is subject to source tax (rule subject_to_source_tax)" - An internal rule id in acceptance-criteria prose; the business name 'Subject to source tax' is enough.
- `feature.md` "Afterwards Step 9 'Finish': permit reminder (rule permit_reminder), then submission" - An internal rule id appears in the business notes.
- `feature.md` "one block per child, repeated for each child the employee adds; all child_* conditions refer to the same child." - Refers to field-id naming (child_* prefix) from the data model instead of business terms.
- `stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md` "the questions that no longer apply are no longer asked, but their answers are kept, so that if the employee changes the earlier answer back, the earlier input reappears" - Prescribes how drafts are held in the system. The decision (D-036) only says answers 'may be kept'; turning that into a hard rule for draft storage is an engineering choice.
- `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` "the employee goes through one block of questions per child and can add another child or remove one" - Prescribes the add/remove interaction rather than the need (any number of children, each assessed separately).

## Coverage

168/343 source units cited; 154/187 facts used.

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

- [fact_judge] `F-hr_transcript-9eeab6` partial: 'Muster AG' company name is not stated in these units; hiring and headcount details are supported. | Muster AG hires around twenty people a year (more in summer) and has about 150 employees, mostly in Zurich.
- [fact_judge] `F-hr_transcript-5518ad` partial: Address is needed, but 'home' is not stated explicitly. | HR needs the employee's home address.
- [fact_judge] `F-hr_transcript-30ead4` partial: Pension fund and portal supported, but 'Muster AG' as company name is not stated in these units. | Muster AG's pension fund is Pensionskasse Muster, which has an old portal; Anna will send screenshots of it.
- [fact_judge] `F-hr_transcript-550840` partial: Leo's summary and Anna's 'I think so' are supported, but 'later added further cases' is only evidenced by T-044 (the spouse exception), which is in the neighbouring context. | Leo summarised 'non-Swiss, but not with a C permit'; Anna only hedged ('I think so') and later added further cases.
- [fact_judge] `F-hr_transcript-a45422` partial: Anna says she checks the spouse case by hand and asks by email which takes forever, but 'HR' generalizes slightly; essentially fine. | Today HR checks the spouse case by hand and asks for spouse details by email, which takes forever.
- [fact_judge] `F-hr_transcript-e505f8` partial: Address country and living abroad are both mentioned, but the units never explicitly link deriving residence from the address country; it is a reasonable inference. | Whether the employee lives abroad can be derived from the country of the home address, which is relevant for source tax liability.
- [fact_judge] `F-hr_transcript-d5c04b` partial: Anna asked about timing and Leo will reply this week after going through the screenshots; 'will respond' is supported but it's a reply on timing, not a delivery date. | Anna asked about timing; Leo will respond this week after reviewing the screenshots.
- [fact_judge] `F-pension_portal-c8bc73` partial: Page, portal and Muster AG are supported, but 'employer Muster AG registers as an insured person' is a mild inference from the breadcrumb. | The source is the 'Register new employee' page in the Pensionskasse Muster employer portal, used by employer Muster AG to register a new employee as an insured person.
- [fact_judge] `F-pension_portal-39bab1` partial: Units show the field in Married screens (05, 07) and absence in Single (04) only by omission of its elements; screenshots 01, 02, 03, 06 are not in the provided units, and 'only when Married' is not shown for Divorced/Widowed. | The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected).
- [fact_judge] `F-pension_portal-3cfe89` partial: Footnote says * means required, but 'all visible fields carry the marker' is not shown (e.g., placeholder/hint units; units don't cover First/Last name in screen 01). | Fields marked with an asterisk are required; all visible fields on the form carry the marker.
- [fact_judge] `F-zh_source_tax_calculator-d5a6fe` partial: 'shown_when: always' is supported and it's labelled Q01, but 'first question' is only implied by numbering. | The income type question is always shown and is the first question.
- [fact_judge] `F-zh_source_tax_calculator-351289` partial: Skipping to Q16 is stated, but 'main-residence question' is not described in the units. | If the income type is 'Ersatzeinkünfte', all personal and child questions are skipped and the calculator goes straight to the main-residence question (Q16).
- [fact_judge] `F-zh_source_tax_calculator-64ac33` partial: Third clause says 'Q14 = Ja' (fine) but statement omits that Q14 is the single-person parental care question; also Q13/Q14 labels are loosely rendered, though the logic matches. | Alternating care is asked when (child minor AND same household AND shared custody AND no common household with the other parent) OR (married AND child minor AND not same household AND Q13 shared custody = Ja) OR (single AND child minor AND not same household AND Q14 = Ja).
- [fact_judge] `F-zh_source_tax_calculator-cd1015` partial: Q08=Nein is plausibly 'not in same household', but the meaning of Q10 ('no common household with the other parent') is not defined in these units. | Q15 is shown only when the child is 'Volljährig und in Erstausbildung' AND (child not in same household OR (same household AND no common household with the other parent)).
- [fact_judge] `F-zh_source_tax_calculator-5f6820` partial: The shown_when (Q18 = Ja OR Q24 = Ja) is supported, but the units never show that Q24 is the replacement-income daily-return question. | The certificate of residence question is asked only when the person returns daily to Germany (Q18 = Ja for earned income, or Q24 = Ja for replacement income).
- [fact_judge] `F-zh_source_tax_calculator-ab4e1e` partial: Ja case is supported, but V41 shows the Nein result also carries the DBA reservation, which the help text omits. | More than 45 non-return days (Ja) gives the normal tariff plus 'Unter Vorbehalt des Doppelbesteuerungsabkommens'; otherwise (Nein) 'Grundsätzlich keine Quellensteuerpflicht'.
- [fact_judge] `F-zh_source_tax_calculator-3058a4` partial: Observed outcomes (C1Y with common household, C0Y otherwise) match V09-V11, but the statement is garbled with an unfinished 'only if...' clause, and the Q11 'alternating care' label is inferred. | Married person, minor child in same household, shared custody: common household with the other parent counts the child (C1Y); no common household counts the child only if... observed: alternating care with other parent as main contributor -> 0 (C0Y), no alternating care -> 0 (C0Y).
- [coverage] `F-hr_email_copy-607694` fact not used anywhere in the spec: Apart from the email copy feature, everything else remains as discussed in the earlier HR meeting.
- [trace_judge] `item.address_country` partial: The claim that the country decides whether the permit reminder is shown is not backed by the cited facts (D-010 and D-038 are not cited).
- [trace_judge] `item.first_working_day` partial: The claim that HR 'runs the onboarding around the start date' is not backed, since D-034 leaves who starts the onboarding to a later spec.
- [trace_judge] `item.has_children` partial: The 'H tariff' purpose is not backed by any cited fact; the rest (question, options, wording, condition) is backed.
- [trace_judge] `item.child_same_household` partial: Question, options and condition are backed, but the 'H tariff' purpose is not in the cited facts.
- [trace_judge] `item.child_parental_custody` partial: Options and condition are backed, but 'sole custody counts the child (H for non-married employees)' is not supported by the cited facts.
- [trace_judge] `item.child_common_household_other_parent` partial: Question, options and condition are backed, but the 'H tariff' purpose is not in the cited facts.
- [trace_judge] `item.child_parental_care_not_in_household` partial: The purpose 'H tariff' is not mentioned in any cited fact (D-001 covers only the child digit).
- [trace_judge] `item.child_alternating_custody` partial: The purpose 'H tariff' is not backed by the cited facts, although the question, values and conditions are.
- [trace_judge] `item.child_main_financial_contributor` partial: The purpose 'H tariff' is not backed by the cited facts, although the values and conditions are.
- [trace_judge] `item.child_main_maintenance` partial: The purpose 'H tariff' is not backed by the cited facts, although the question, values and condition are.
- [trace_judge] `item.non_return_days_45` partial: The question, condition and outcomes are backed, but the note about Step 9 and the permit reminder rule has no cited support; only the read-only point (D-037) is backed.
- [trace_judge] `rule.cross_border_tariff_applies` partial: The 'Not Germany → no' row cites F-zh_source_tax_calculator-52b67a, which is not among the cited facts, so that row is not backed.
- [trace_judge] `rule.liechtenstein_no_source_tax_in_principle` partial: The 'Not Liechtenstein → no' row cites F-zh_source_tax_calculator-52b67a, which is not among the cited facts, so that row is not backed.
- [trace_judge] `rule.source_tax_result` partial: The 'not subject → no tariff code' row cites F-hr_transcript-b6d9b3, which is not among the cited facts, and the Liechtenstein row's F-zh_source_tax_calculator-e80d8f and -ab4e1e are also not provided (though D-007 covers the Liechtenstein row).
- [trace_judge] `story.US-01.2` partial: The non-illustrative Tomás/Winterthur example (country Switzerland) relies on F-hr_transcript-d7431e, which is not among the cited facts and has no source_refs on the example.
- [trace_judge] `story.US-03.4` partial: The priority reason's tariff letters (A/B/C/H) are not backed by any cited fact; the criteria themselves are supported.
- [trace_judge] `story.US-05.4` partial: The non-illustrative Tomás example cites F-hr_transcript-d7431e and the 'not subject to source tax' condition rests on a rule (F-hr_transcript-b6d9b3), and neither is among the cited facts.
- [trace_judge] `story.US-08.3` partial: The priority reason's claim that HR reports the first working day often moves is not in any cited fact; the rest is backed by D-033, D-037 and F-1d5c07.
- [trace_judge] `story.US-08.4` partial: No cited fact sets the nine-step order in AC-08.4.1; only English (G-09), canton for Swiss residents (D-002) and the reminder at the end (D-010) are backed.
- [trace_judge] `story.US-08.5` partial: AC-08.5.3 names 'the civil status for the pension fund' as a derived result, and the P2 priority is stated, but no cited fact backs either; the rest is supported.
- [dev_refinement] `feature.md` Which home address counts when a new hire is moving for the job, for example someone living abroad today who will live in Switzerland by the first working day? The country decides source tax liability, the canton, the nationality questions and the cross-border tariff, so we need to know whether to ask for the current address or the address on the first working day, and whether one form can record both.
- [dev_refinement] `stories/US-02.1-employee-enters-the-first-working-day.md` HR says it asks employees to 'confirm' the first working day. Does that mean Lonio shows the planned date HR already knows so the employee confirms or corrects it, or does the employee type it in from scratch? Also, which dates are valid: can the date be in the past, on a weekend, or more than X months ahead?
- [dev_refinement] `stories/US-08.3-questionnaire-is-read-only-for-the-employee-after-submission.md` After submission the employee 'can see their answers'. Should the employee also see the derived results (insurance start date, civil status for the fund, tariff code, the Liechtenstein statement)? The email copy explicitly leaves them out, so the read-only view needs its own decision.
- [dev_refinement] `stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md` Can the employee stop part-way and come back later (a saved draft across sessions), or does the questionnaire only have to keep answers during one sitting? D-036 says answers 'may be kept' while going back and forth, but AC-08.2.1 says they 'are kept' and must reappear. Which one is the requirement?
- [dev_refinement] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` The 60 (Germany) and 45 (Liechtenstein) non-return-day limits apply to 'the calendar year'. For a new hire who starts mid-year, should the employee count only the remaining months, or should the limit be scaled down for a partial year? The answer changes the wording of the question and the tariff result.
- [dev_refinement] `stories/US-07.3-determine-the-source-tax-outcome-for-employees-living-in.md` For Liechtenstein residents who return daily, the result is 'in principle no source tax liability', so the denomination, spouse-employment and children answers they gave are never used. The cross-border step comes after the children, so we collect religion and child data with no purpose (G-01). Should the Liechtenstein daily-return and 45-day questions come first, so the tariff questions are only asked when a tariff code results? D-007 says Liechtenstein residents get the source tax questions, but it does not settle the order.
- [dev_refinement] `stories/US-08.5-optional-email-copy-of-the-submitted-answers.md` The copy holds sensitive answers (denomination, nationality, custody and children details, spouse data) and goes to an address the employee types in without any check. Is that acceptable to the business and for data protection, or must the address be confirmed first, or limited to an address HR already holds?

## Run

Stages run: normalize/hr_email_copy, extract/hr_email_copy, judge_facts, knowledge.raw, feature.plan, sections/SEC-08-completion-and-submission, feature.flow, judge_trace, dev_refinement, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator

LLM cost this run: $3.66

Tokens this run: 1,685,896 in 21 agent calls (67 input, 1,296,470 cache read, 347,757 cache write, 41,602 output)
