# Review: employee-onboarding

**Verdict: NOT READY**

All 206 example simulations pass, and coverage of the facts is good (155 of 188 used). It is not ready yet for three reasons. First, four decisions are now out of date: the fund email added new facts about the canton and the insurance start date, and the check reports these as errors. Second, the fund email says the insurance start can fall on any day from 2027, but the portal says it must be the 1st of a month. Third, six dev-refinement questions are rated major and still unanswered. The technical leaks are small wording fixes. Several 'why we need it' notes and examples cite facts that are not in their citation lists. Once the decisions are re-confirmed and the major questions are decided, this should move to ready_with_caveats, with the remaining non-blocking open questions as the caveats.

## Reviewer findings

1. **Four decisions are out of date after the fund email** – The canton and insurance start date stories (US-01.4, US-01.5, US-02.2, US-08.3) depend on decisions written before the new evidence arrived. Engineering cannot rely on them until they are re-confirmed.  
   Evidence: decisions errors on D-002, D-012, D-033 and D-037; new facts F-fund_email-90df7e, -a03d8c, -be1403, -0abca9, -0b09ba, -0f18b5  
   Action: Update each decision against the fund email. D-002: ask Swiss residents for their canton of residence; for employees abroad, set the canton to Zurich (the place of work). D-012/D-033/D-037: from 01.01.2027 the insurance starts on the first working day itself. Then run `pipeline reconfirm` for each.
2. **OQ-canton-abroad is still open although the fund has answered it** – The open question contradicts US-01.5, which is marked 'confirmed', and it makes the package look less settled than it is.  
   Evidence: impact guard_reverted on open.OQ-canton-abroad; dev_refinement on open-questions.md; F-fund_email-90df7e and -a03d8c  
   Action: Close OQ-canton-abroad and cite the fund email facts. Mark D-002 as confirmed instead of provisional, so the removal is backed by evidence and is not reverted again.
3. **The 2027 insurance start date conflicts with the portal rule** – From 2027, Lonio would work out start dates that are not the 1st of a month, but the portal field says 'Must be the 1st of a month'. Registrations could be rejected.  
   Evidence: dev_refinement US-02.2 (major); F-pension_portal-dd8126 vs F-fund_email-0f18b5  
   Action: Ask Pensionskasse Muster to confirm that the portal will accept any day from 2027. Record the answer as a decision, or add a blocking open question until they reply.
4. **Unclear which home address applies when someone moves for the job** – The address country drives source tax liability, the canton, the nationality and permit questions, the cross-border questions and the permit reminder. Without this rule the results are ambiguous.  
   Evidence: dev_refinement information.md (major)  
   Action: Decide in decisions.yaml whether employees enter their current address or their address from the first working day, and add the matching guidance to information.md.
5. **Other major refinement questions have no decision yet** – Each one changes what gets built: the step order, the Finish step and read-only view, how the date is entered, and address validation.  
   Evidence: dev_refinement (major): US-07.3 order of the Liechtenstein questions (G-01); feature.md whether the employee sees derived results; US-02.1 first working day pre-filled or typed in, and date limits; US-01.2 addresses without a house number  
   Action: Add one decision for each to decisions.yaml. Suggested: ask the Liechtenstein daily-return and 45-day questions before the tariff questions; show derived results to HR only; HR pre-fills the first working day and the employee confirms or corrects it; allow a 'no house number' option.
6. **Tariff results that may be wrong in edge cases** – Lonio now owns the tariff code, so a wrong letter (H vs A) or a missing double-taxation-agreement (DBA) reservation would go straight into payroll.  
   Evidence: dev_refinement feature.md child row 22 (C-V20 H1N vs F-zh_source_tax_calculator-96658b); US-07.3 DBA reservation; fact_judge F-zh_source_tax_calculator-ab4e1e  
   Action: Decide which source wins for row 22; the calculator run is the stronger evidence. Decide whether to record 'Unter Vorbehalt DBA' plus an HR flag for Liechtenstein residents with more than 45 non-return days. Add both to the go-live check in OQ-calculator-coverage.
7. **Technical details leak into the spec** – Internal rule IDs, field naming patterns, a storage format and UI controls are design choices that belong to engineering, not to the spec.  
   Evidence: tech_leak: feature.md (pension_fund_canton, child_*, permit_reminder); US-06.1 (subject_to_source_tax; add/remove child controls); US-01.1 ('recorded as DD.MM.YYYY')  
   Action: Replace the rule IDs with business names. State 'one set of answers per child' instead of add/remove controls. Keep DD.MM.YYYY as the fund's format only, without saying how the date is stored.
8. **Traceability gaps** – Some 'why we need it' notes and examples are not backed by the facts they cite, so reviewers cannot check them.  
   Evidence: trace_judge: 'H tariff' purpose missing on 8 child_* items; F-hr_transcript-d7431e not cited in US-01.2, US-01.4 and US-05.4; F-zh_source_tax_calculator-52b67a not cited in the cross-border and Liechtenstein rules; F-hr_transcript-b6d9b3 not cited in source_tax_result; US-08.3 priority reason ('the first working day often moves') has no supporting quote; US-08.4 step order unbacked  
   Action: Add the missing facts to the citation lists. Cite the calculator H-tariff facts or D-001 for the child items. Either cite the transcript passage where HR says the first working day moves or drop that claim. Record the nine-step order as a decision.
9. **Non-blocking open questions and inferred items need human confirmation** – Each one could change the fund registration or the tariff code; how the fund wants partnerships recorded is the most visible.  
   Evidence: OQ-civil-status-partnership, OQ-spouse-dob-other-status, OQ-calculator-coverage (go-live per D-009), OQ-nationality-wording; inferred: spouse_residence_country, spouse_nationality, child_tariff_result, US-04.2, US-06.3–06.5, US-08.4  
   Action: Have a domain expert confirm with the fund (partnership mapping, screenshots for Divorced and Widowed). The product owner confirms or rejects the inferred stories. Keep the calculator comparison as a go-live check.
10. **Minor gaps in the behaviour rules** – Small rules engineering will otherwise guess.  
   Evidence: dev_refinement minor: US-08.2 'may be kept' vs 'are kept'; US-06.1 minimum and maximum number of children; US-04.1 stateless employees; US-08.3 answers missing after HR changes; plausibility checks on dates  
   Action: Make one guidance decision covering these: earlier input is kept and restored only within a session; at least 1 child if 'yes'; stateless counts as non-Swiss; date checks such as 'not in the future'; leave changes after submission to the HR spec.

## Numbers

346 source units → 188 facts → 35 information items, 18 business rules → one feature with 8 sections, 31 stories, 103 acceptance criteria; 5 open questions, 12 exclusions.

## Impact of this run

Stories added: US-01.5; changed: US-01.4, US-02.2, US-08.3; removed: -; unchanged: 27.

Knowledge elements changed: insurance_start_date, pension_fund_canton, residence_canton

Changes the update guard reverted (force with `--force knowledge.raw` if they are wanted):

- open.OQ-canton-abroad: removal reverted - it cites no removed fact

## Errors (4)

- [decisions] `D-002` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-002`: F-fund_email-90df7e: The pension fund registration field "Canton" means the employee's canton of residence.; F-fund_email-a03d8c: For employees living abroad, the employee does not have to provide anything for the pension fund's "Canton" field (the employer fills in the; F-fund_email-be1403: Inferred: the canton of residence only needs to be collected for the pension fund when the employee lives in Switzerland; for employees livi ...
- [decisions] `D-012` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-012`: F-fund_email-0abca9: Consolidated insurance start date rule (derived from first_working_day): if the first working day is on or after 01.01.2027, insurance start; F-fund_email-0b09ba: Inferred: the employee's first working day is needed to determine the pension fund insurance start date.; F-fund_email-0f18b5: For employees whose first working day is on or after 1 January 2027, the insurance starts on the first working day itself, even if that is n ...
- [decisions] `D-033` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-033`: F-fund_email-0abca9: Consolidated insurance start date rule (derived from first_working_day): if the first working day is on or after 01.01.2027, insurance start; F-fund_email-0b09ba: Inferred: the employee's first working day is needed to determine the pension fund insurance start date.; F-fund_email-0f18b5: For employees whose first working day is on or after 1 January 2027, the insurance starts on the first working day itself, even if that is n ...
- [decisions] `D-037` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-037`: F-fund_email-0abca9: Consolidated insurance start date rule (derived from first_working_day): if the first working day is on or after 01.01.2027, insurance start; F-fund_email-0b09ba: Inferred: the employee's first working day is needed to determine the pension fund insurance start date.; F-fund_email-0f18b5: For employees whose first working day is on or after 1 January 2027, the insurance starts on the first working day itself, even if that is n ...

## Examples executed against the knowledge model (227/227 pass)

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
- ✅ AC-01.5.1 / Employee living in Switzerland, canton Bern (spec)
- ✅ AC-01.5.2 / Employee living in Germany (e.g. Konstanz) (spec)
- ✅ AC-01.5.2 / Employee living in Liechtenstein (spec)
- ✅ AC-02.1.1 / Employee living in Switzerland (spec)
- ✅ AC-02.1.1 / Employee living abroad (spec)
- ✅ AC-02.2.2 / Start on the 1st of a month (spec)
- ✅ AC-02.2.2 / Start on 1st January (spec)
- ✅ AC-02.2.3 / Julia (hr_transcript/F-hr_transcript-d7a23b), first working day 15 March (year illustrative) (spec)
- ✅ AC-02.2.3 / Start on the last day of a month (spec)
- ✅ AC-02.2.3 / Start in mid-December (spec)
- ✅ AC-02.2.3 / Start on the last day of 2026 (spec)
- ✅ AC-02.2.4 / Julia (hr_transcript/F-hr_transcript-d7a23b), moved to 15 March (year illustrative) (spec)
- ✅ AC-02.2.4 / Earlier exit agreed, start moved to the 1st (spec)
- ✅ AC-02.2.5 / Start in mid-March 2027 (spec)
- ✅ AC-02.2.5 / Start on the 1st of a month in 2027 (spec)
- ✅ AC-02.2.5 / Start on 2nd January 2027 (spec)
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
- ✅ AC-08.3.2 / First working day moved into 2027, in the middle of a month (spec)
- ✅ AC-08.4.2 / Swiss employee living in Switzerland, single (spec)
- ✅ AC-08.4.2 / Employee living in Germany, single (spec)

## Open questions (need your decision)

- **OQ-canton-abroad**: What should be entered in the pension fund's 'Canton' field for employees living abroad, and does 'Canton' mean canton of residence or of work? → recommended: Keep D-002 (ask only residents of Switzerland); a domain expert verifies with Pensionskasse Muster.
- **OQ-civil-status-partnership**: How does Pensionskasse Muster want registered partnerships and separated employees registered (its list has only Single, Married, Divorced, Widowed), and does it want the partner's details? → recommended: Keep the provisional mapping of D-003; verify with a domain expert and the fund.
- **OQ-spouse-dob-other-status**: Does the fund's screen require the spouse's (or former spouse's) date of birth or other fields for Divorced or Widowed? → recommended: Domain expert obtains a screenshot of the fund screen for Divorced and Widowed.
- **OQ-calculator-coverage**: Does Lonio's computed tariff code match the Zurich calculator on the paths not explored: the residence block for A/B/H tariffs, more than 3 children, H3N/P3N, and the child rows marked inferred? → recommended: Go-live condition per D-009; non-blocking for the spec.
- **OQ-nationality-wording**: Should the questionnaire ask for the nationality as a country, or only whether the employee (and the spouse) holds Swiss citizenship? And does the dual-citizenship rule (D-008) also apply to the spouse? → recommended: Keep the current model and confirm with the product owner; apply D-008 to the spouse unless a domain expert says otherwise.

## Inferred items to confirm

- item.spouse_residence_country
- item.spouse_nationality
- rule.child_tariff_result
- story.US-04.2
- story.US-06.3
- story.US-06.4
- story.US-06.5
- story.US-08.4
- fact F-pension_portal-39bab1: The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected).
- fact F-pension_portal-6d3630: Screenshots do not show whether the spouse's date of birth (or other fields) appears for 'Divorced' or 'Widowed'; only Single (no) and Married (yes) are shown.
- fact F-pension_portal-9b24c5: The civil status list has no option for registered partnership or separated; it is unclear how such employees are to be registered.
- fact F-pension_portal-b359c3: The label 'Canton' does not state whether it is the canton of residence or of work, and the list only contains Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. a cross-border commuter).
- fact F-pension_portal-3a97ab: The portal requires an insurance start date on the 1st of a month but does not say how it relates to the employee's first working day (e.g. which 1st of a month to use when work starts mid-month).
- fact F-fund_email-be1403: Inferred: the canton of residence only needs to be collected for the pension fund when the employee lives in Switzerland; for employees living abroad it is not asked but set to Zurich (Muster AG's place of work). Whether the fund's sentence about the employee providing nothing applies only to the abroad case or to the canton field in general is not fully explicit.
- fact F-fund_email-0abca9: Consolidated insurance start date rule (derived from first_working_day): if the first working day is on or after 01.01.2027, insurance starts on the first working day; if it is on or before 31.12.2026, insurance starts on the first working day when it is the 1st of a month, otherwise on the 1st of the following month.
- fact F-fund_email-0b09ba: Inferred: the employee's first working day is needed to determine the pension fund insurance start date.

## Dev refinement questions (14)

- [major] `information.md` The home address country decides almost everything: source tax liability, canton, nationality and permit questions, cross-border questions and the permit reminder. Which address should a new employee enter if they move for the job, for example from abroad to Zurich around the first working day: the current address or the address they will have from the first working day? The source tax result and the pension fund canton change completely depending on the answer.
- [major] `stories/US-07.3-determine-the-source-tax-outcome-for-employees-living-in.md` A Liechtenstein resident who returns daily (or expects at most 45 non-return days) ends up with 'in principle no source tax liability' and no tariff code. But the cross-border step comes after the children, so they have already answered denomination, spouse employment and every child question. Under data minimisation (G-01), should the Liechtenstein daily-return and 45-day questions come first, so the tariff questions are asked only when a tariff code will actually be computed? Or does HR need those answers anyway?
- [major] `stories/US-02.2-insurance-start-date-derived-from-the-first-working-day.md` From 01.01.2027 the insurance start date can fall on any day (fund email), but the pension portal field says 'Must be the 1st of a month' (F-pension_portal-dd8126). Has the fund confirmed that its portal will accept dates that are not the 1st of a month from 2027? If not, what should Lonio record for those employees?
- [major] `stories/US-01.2-complete-home-address-for-posting-documents.md` The house number is required for every employee, and the spec itself notes that 'the sources do not say what applies to an address without a house number'. Some valid addresses have no house number (rural addresses, named buildings, some foreign formats). Can those employees submit without one? Is there an alternative (e.g. 'no number', or the number written into the street line)?
- [major] `stories/US-02.1-employee-enters-the-first-working-day.md` The employee 'enters and thereby confirms' the first working day. Does the employee see a date HR already planned and confirm or correct it, or do they type it into an empty field? Are there limits on the date (e.g. not in the past, not before the questionnaire was started)?
- [major] `feature.md` Should the employee see any derived results before or after submission: subject to source tax, the tariff code, the Liechtenstein 'no liability' statement, the insurance start date? The spec says these are 'recorded for HR' but never says whether the employee sees them. This changes the Finish step and the read-only view.
- [minor] `stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md` D-036 and AC-01.4.3 say inapplicable answers 'may be kept' until submission, but AC-08.2.1 says they 'are kept' and 'the earlier input reappears'. Is restoring earlier input a firm acceptance criterion or optional? Also, are answers kept if the employee leaves and comes back later (save and resume before submission)?
- [minor] `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` If the employee answers 'yes' to having children, must they add at least one child block before submitting? Can they remove the last block? Is there a maximum number of children? The calculator's upper limit is unknown and codes for more than 3 children are unverified.
- [minor] `feature.md` Child result row 22 (not married, minor child not in the household, parental custody, alternating care, employee contributes more) gives 'Counted with H'. That matches calculator run C-V20 (H1N), but it contradicts the calculator note F-zh_source_tax_calculator-96658b ('counted with H when it lives in the household'). Which applies? It changes the tariff letter (H vs A).
- [minor] `stories/US-07.3-determine-the-source-tax-outcome-for-employees-living-in.md` For Liechtenstein residents with more than 45 non-return days, the calculator returns the normal tariff plus 'Unter Vorbehalt des Doppelbesteuerungsabkommens' (e.g. 'C1Y / Unter Vorbehalt…'). The spec records only the normal tariff code. Should the double-taxation-agreement reservation (and the HR flag) also be recorded in this case?
- [minor] `open-questions.md` OQ-canton-abroad is still listed as open and D-002 is still called provisional. Yet the fund's email answers both parts ('Canton' means canton of residence; Zurich, the place of work, for employees living abroad), and US-01.5 has status 'confirmed'. Can OQ-canton-abroad be closed, or is anything still outstanding that could change what gets built?
- [minor] `stories/US-04.1-ask-swiss-citizenship-and-c-permit-only-of-employees-living.md` How do stateless employees (or those with an unclear nationality) living in Switzerland answer the nationality question, which expects a country? Should they simply be treated as non-Swiss and get the C permit question?
- [minor] `stories/US-08.3-questionnaire-is-read-only-for-the-employee-after-submission.md` After submission HR may record a change that makes questions apply that were never asked: a move from abroad to Switzerland (nationality, C permit, canton missing), a marriage (spouse's date of birth and spouse details missing), a new child. Derived results are 'always derived again from the latest answers'. What should Lonio derive or show while those answers are missing? Is that fully left to the later HR spec?
- [minor] `information.md` Are there plausibility rules for the dates the employee enters? For example: a minimum age for the employee's date of birth, the spouse's date of birth not in the future, a first working day not too far in the past or future.

## Technical vocabulary found in the spec (6)

- `feature.md` "For employees living abroad the canton entered at the fund is derived (rule pension_fund_canton), not asked." - Uses an internal rule identifier in business prose. The rule should be named in business terms ('Canton for the pension fund').
- `feature.md` "Step 7 'Children' – one block per child, repeated for each child the employee adds; all child_* conditions refer to the same child." - 'child_*' is a field-id naming pattern from the data model and leaks into the spec text.
- `feature.md` "Afterwards Step 9 'Finish': permit reminder (rule permit_reminder), then submission" - Internal rule identifier in prose instead of a business name.
- `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` "When Lonio has decided whether the employee is subject to source tax (rule subject_to_source_tax)" - Internal rule identifier inside an acceptance criterion.
- `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` "the employee goes through one block of questions per child and can add another child or remove one" - Prescribes add/remove-child interaction controls copied from the calculator UI ('Ein weiteres Kind erfassen' / 'Kind löschen'). How the employee enters several children is a UI design choice. The business need is only one set of answers per child.
- `stories/US-01.1-personal-details-for-the-pension-fund-registration.md` "the date of birth is a full calendar date, shown and recorded as DD.MM.YYYY" - The fund's entry format is a business constraint, but 'recorded as DD.MM.YYYY' prescribes how the date is stored, which is an engineering choice.

## Coverage

169/346 source units cited; 155/188 facts used.

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
- fund_email/T-000: Subject: Registration of new employees - two clarifications From: Pensionskasse Muster, employer service To: Leo (Lonio) Date: 14 November 2026
- fund_email/T-001: Dear Leo, thank you for your questions about the registration screen in our employer portal. Here are our two answers.
- fund_email/T-004: Kind regards, Pensionskasse Muster, employer service

## Other warnings (44)

- [fact_judge] `F-hr_transcript-5518ad` partial: Address is needed, but 'home' is not stated explicitly (reasonable inference since it's postal to employees). | HR needs the employee's home address.
- [fact_judge] `F-hr_transcript-872bd7` partial: First working day is 'number one thing' Anna needs, but the units don't explicitly tie it to the pension fund only; context (answer to fund question) makes it reasonable. | The employee's first working day is needed for the pension fund; it is the most important item.
- [fact_judge] `F-hr_transcript-550840` partial: Leo's summary and Anna's 'I think so' are supported, but 'later added further cases' is only shown by T-044 (spouse case), which appears in a neighbouring unit. | Leo summarised 'non-Swiss, but not with a C permit'; Anna only hedged ('I think so') and later added further cases.
- [fact_judge] `F-hr_transcript-a45422` partial: Anna says she checks the spouse case by hand and asks by email which takes forever, but 'HR' as actor is fine; minor: 'by hand' refers to the exemption check, and email is for spouse details — essentially supported, slight conflation. | Today HR checks the spouse case by hand and asks for spouse details by email, which takes forever.
- [fact_judge] `F-hr_transcript-e505f8` partial: Address includes country and abroad residents are subject, so the derivation is reasonable, but nobody states that country of address determines it. | Whether the employee lives abroad can be derived from the country of the home address, which is relevant for source tax liability.
- [fact_judge] `F-pension_portal-c8bc73` partial: Portal, Muster AG and register-new-employee page are supported; 'insured person' is only implied by breadcrumb. | The source is the 'Register new employee' page in the Pensionskasse Muster employer portal, used by employer Muster AG to register a new employee as an insured person.
- [fact_judge] `F-pension_portal-3432a9` partial: The 26 cantons are listed, but 'exactly' and 'no option for living outside Switzerland' are inferred from the list; the list is complete in the units though. | The Canton dropdown offers exactly the 26 Swiss cantons: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for living outside Switzerland.
- [fact_judge] `F-pension_portal-39bab1` partial: Units show the field in 05 and 07 and absence in 04 (Single), but absence in 01, 02, 03, 06 is not evidenced here, and 'only when Married' is not shown for Divorced/Widowed. | The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected).
- [fact_judge] `F-pension_portal-3cfe89` partial: Footnote 'Fields marked * are required' is supported, but 'all visible fields carry the marker' is not established (e.g. first/last name markers not shown, though several fields do have them). | Fields marked with an asterisk are required; all visible fields on the form carry the marker.
- [fact_judge] `F-zh_source_tax_calculator-351289` partial: Q16 is described only as Q16; 'main-residence' meaning is not in these units. | If the income type is 'Ersatzeinkünfte', all personal and child questions are skipped and the calculator goes straight to the main-residence question (Q16).
- [fact_judge] `F-zh_source_tax_calculator-64ac33` partial: Q14 branch is described as 'single AND ... Q14 = Ja' but the unit covers Ledig, Geschieden, Getrennt, Verwitwet; also Q14 is not labelled as shared custody, though the meaning is close. | Alternating care is asked when (child minor AND same household AND shared custody AND no common household with the other parent) OR (married AND child minor AND not same household AND Q13 shared custody = Ja) OR (single AND child minor AND not same household AND Q14 = Ja).
- [fact_judge] `F-zh_source_tax_calculator-cd1015` partial: Condition matches, but the units never define Q10 as 'common household with the other parent'; that reading is an unverified assumption. | Q15 is shown only when the child is 'Volljährig und in Erstausbildung' AND (child not in same household OR (same household AND no common household with the other parent)).
- [fact_judge] `F-zh_source_tax_calculator-5f6820` partial: Condition Q18=Ja OR Q24=Ja is shown, but the units never say Q24 concerns replacement income or daily return to Germany. | The certificate of residence question is asked only when the person returns daily to Germany (Q18 = Ja for earned income, or Q24 = Ja for replacement income).
- [fact_judge] `F-zh_source_tax_calculator-ab4e1e` partial: Ja outcome is supported, but the Nein vector V41 also shows 'Unter Vorbehalt des DBA', which the statement omits for the Nein case; the Q23 help only lists the no-liability text. | More than 45 non-return days (Ja) gives the normal tariff plus 'Unter Vorbehalt des Doppelbesteuerungsabkommens'; otherwise (Nein) 'Grundsätzlich keine Quellensteuerpflicht'.
- [fact_judge] `F-zh_source_tax_calculator-3058a4` partial: The vectors support C1Y/C0Y outcomes, but the statement contains an unfinished clause ('counts the child only if...') and the 'Q10 = Nein' no-common-household condition isn't stated cleanly. | Married person, minor child in same household, shared custody: common household with the other parent counts the child (C1Y); no common household counts the child only if... observed: alternating care with other parent as main contributor -> 0 (C0Y), no alternating care -> 0 (C0Y).
- [fact_judge] `F-zh_source_tax_calculator-56e79b` partial: Vectors V12/V13 give B1N/B0N, but the meaning of Q13 (shared custody) and Q11 (alternating care) is not labelled in these units and is only inferred. | Married person, minor child not in household: shared custody + alternating care + person is main contributor counts the child (B1N); no shared custody does not count it (B0N).
- [fact_judge] `F-fund_email-be1403` partial: Reasonable reading, but the statement that residence canton is 'only needed' for Swiss residents and 'not asked' abroad is an extrapolation; it also flags its own ambiguity. | Inferred: the canton of residence only needs to be collected for the pension fund when the employee lives in Switzerland; for employees living abroad it is not asked but set to Zurich (Muster AG's place of work). Whether the fund's sentence about the employee providing nothing applies only to the abroad case or to the canton field in general is not fully explicit.
- [impact] `open.OQ-canton-abroad` removal reverted - it cites no removed fact
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
- [trace_judge] `story.US-01.4` partial: The non-illustrative Tomás/Winterthur example in AC-01.4.1 cites F-hr_transcript-d7431e, which is not among the cited facts, so nothing backs it.
- [trace_judge] `story.US-03.4` partial: The priority reason's tariff letters (A/B/C/H) are not backed by any cited fact; the criteria themselves are supported.
- [trace_judge] `story.US-05.4` partial: The non-illustrative Tomás example cites F-hr_transcript-d7431e and the 'not subject to source tax' condition rests on a rule (F-hr_transcript-b6d9b3), and neither is among the cited facts.
- [trace_judge] `story.US-08.3` partial: The ACs, examples and derived-result list are backed by D-033/D-034/D-037 and the fund/HR facts, but the priority_reason claim that "HR reports that the first working day often moves" is not in any cited fact or quote.
- [trace_judge] `story.US-08.4` partial: No cited fact sets the nine-step order in AC-08.4.1; only English (G-09), canton for Swiss residents (D-002) and the reminder at the end (D-010) are backed.
- [dev_refinement] `information.md` The home address country decides almost everything: source tax liability, canton, nationality and permit questions, cross-border questions and the permit reminder. Which address should a new employee enter if they move for the job, for example from abroad to Zurich around the first working day: the current address or the address they will have from the first working day? The source tax result and the pension fund canton change completely depending on the answer.
- [dev_refinement] `stories/US-07.3-determine-the-source-tax-outcome-for-employees-living-in.md` A Liechtenstein resident who returns daily (or expects at most 45 non-return days) ends up with 'in principle no source tax liability' and no tariff code. But the cross-border step comes after the children, so they have already answered denomination, spouse employment and every child question. Under data minimisation (G-01), should the Liechtenstein daily-return and 45-day questions come first, so the tariff questions are asked only when a tariff code will actually be computed? Or does HR need those answers anyway?
- [dev_refinement] `stories/US-02.2-insurance-start-date-derived-from-the-first-working-day.md` From 01.01.2027 the insurance start date can fall on any day (fund email), but the pension portal field says 'Must be the 1st of a month' (F-pension_portal-dd8126). Has the fund confirmed that its portal will accept dates that are not the 1st of a month from 2027? If not, what should Lonio record for those employees?
- [dev_refinement] `stories/US-01.2-complete-home-address-for-posting-documents.md` The house number is required for every employee, and the spec itself notes that 'the sources do not say what applies to an address without a house number'. Some valid addresses have no house number (rural addresses, named buildings, some foreign formats). Can those employees submit without one? Is there an alternative (e.g. 'no number', or the number written into the street line)?
- [dev_refinement] `stories/US-02.1-employee-enters-the-first-working-day.md` The employee 'enters and thereby confirms' the first working day. Does the employee see a date HR already planned and confirm or correct it, or do they type it into an empty field? Are there limits on the date (e.g. not in the past, not before the questionnaire was started)?
- [dev_refinement] `feature.md` Should the employee see any derived results before or after submission: subject to source tax, the tariff code, the Liechtenstein 'no liability' statement, the insurance start date? The spec says these are 'recorded for HR' but never says whether the employee sees them. This changes the Finish step and the read-only view.

## Run

Stages run: normalize/fund_email, extract/fund_email, judge_facts, knowledge.raw, feature.plan, sections/SEC-02-start-date-insurance, sections/SEC-08-completion-and-submission, sections/SEC-01-identity-and-address, feature.flow, judge_trace, dev_refinement, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator

LLM cost this run: $4.97

Tokens this run: 1,875,015 in 24 agent calls (69 input, 1,340,187 cache read, 477,515 cache write, 57,244 output)
