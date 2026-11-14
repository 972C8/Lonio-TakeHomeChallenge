# Review: employee-onboarding

**Verdict: NOT READY**

Not ready. All 190 example simulations pass, but there are two blocking problems. First, 10 decisions are out of date: the HR follow-up of 14 Nov 2026 added new nationality facts that they don't reflect, and the check reports this as an error. Second, the same follow-up has a direct HR rule for Liechtenstein commuters that the spec doesn't use and goes against. On top of that, dev refinement raised 7 major questions (address timing, start date, reminder text, saving drafts, what the employee sees), and internal IDs still appear in the prose. The 5 open questions are all non-blocking. After the decisions are re-confirmed, the Liechtenstein rule is settled and the major dev questions are answered, this should reach ready_with_caveats.

## Reviewer findings

1. **10 decisions are out of date after HR's nationality follow-up** – The decisions behind the nationality, spouse-exemption, permit and source-tax-liability logic were made before HR said only 'Swiss: yes/no' is needed. 13 stories changed because of this, but nobody has re-confirmed the decisions, so the traceability can't be trusted.  
   Evidence: decisions errors on D-003, D-005, D-007, D-008, D-010, D-011, D-013, D-030, D-031, D-038; new facts F-hr_followup-8d9f77, -e8164e, -ee7d68, -32873d. Impact report: US-01.3, US-04.x, US-05.x, US-06.1/06.2, US-08.1/08.2/08.4 changed  
   Action: Review each decision against the new facts. Re-confirm, update or drop it in decisions.yaml, then run `pipeline reconfirm D-xxx` for each.
2. **HR's rule for Liechtenstein commuters is not in the spec, and the spec contradicts it** – HR said Liechtenstein commuters are not subject to source tax and should be asked no source tax questions at all. The spec instead asks them denomination, spouse employment, children and cross-border questions, still records them as 'subject', and only reaches 'no liability' in some cases. That collects data with no purpose, which goes against G-01 (data minimisation).  
   Evidence: coverage: F-hr_followup-664bcb, -edd03f, -ed14dd not used; dev_refinement US-07.3 (major) and feature.md (subject=yes next to 'no liability'); source hr_followup/T-004  
   Action: Decide in decisions.yaml whether HR's rule replaces the calculator's Liechtenstein path. If it does: residents of Liechtenstein are not subject, all source tax questions are skipped, address_country is asked first, and US-07.3, the Liechtenstein row of source_tax_result and the D-007 'shows' wording are removed or reworked. If it doesn't: record why HR is overruled and get HR to confirm.
3. **Unclear which home address counts: current or the one on the first working day** – The address country decides source tax liability, the canton, the nationality and permit questions and the cross-border questions. Many new hires move for the job, so the wrong address gives the wrong questions and the wrong result.  
   Evidence: dev_refinement major on US-01.2  
   Action: Ask HR and record the answer as a decision (most likely: the address on the first working day). Adjust the wording of the question.
4. **Unclear how to count non-return days when someone starts mid-year** – The 60-day (Germany) and 45-day (Liechtenstein) limits decide the tariff or whether source tax applies at all. If 'calendar year' is read differently, the result changes.  
   Evidence: dev_refinement major on US-07.2 and US-07.3  
   Action: Get a domain expert to say whether the count is for the rest of this year or a full-year figure. Put the answer into the question wording and record it as a decision.
5. **Unclear whether the employee ever sees the derived results** – D-007 says Lonio 'shows' the Liechtenstein statement, while the rest of the spec says results are only 'recorded for HR'. Without an answer, the user interface and the acceptance tests can't be defined.  
   Evidence: dev_refinement major on US-05.7; D-007  
   Action: Decide whether the employee sees anything (tariff code, liability, insurance start date) before or after submitting, and align D-007 with that.
6. **Questionnaire lifecycle and start date are not defined** – Engineering can't build drafts, deadlines or date checks. It's not specified whether the employee can save and come back, what happens to a questionnaire that is never submitted (a data minimisation question), or whether HR pre-fills the start date and which dates are allowed.  
   Evidence: dev_refinement major on US-08.2 and US-02.1  
   Action: Add decisions on save/resume, a submission deadline and how long unsubmitted answers are kept, and on whether HR pre-fills the start date and which dates are valid.
7. **No text yet for the permit reminder** – US-08.1 can't be finished or accepted without the reminder wording. It's also unclear whether HR edits the text themselves or it is fixed once before go-live.  
   Evidence: dev_refinement major on US-08.1  
   Action: Get the text from HR (Anna) with a due date, and decide whether it is fixed or editable by HR.
8. **Internal IDs appear in the spec text** – Rule IDs, the child_* field pattern, 'formal expression' and snake_case stakeholder IDs are model internals, not business language.  
   Evidence: tech_leak: US-06.1 (subject_to_source_tax), feature.md (permit_reminder, child_*, formal expression), information.md (pension_fund/source_tax/hr in the 'Who needs it?' column)  
   Action: Add a guidance rule to use business names only, then regenerate the affected text.
9. **Some claims are not backed by the facts they cite** – Several items and stories state things their cited facts don't support. Reviewers can't check them, and some may be wrong.  
   Evidence: trace_judge: 'H tariff' purpose on 8 child_* items; tariff letters in US-03.4; the 'often moves' claim in US-08.3; the nine-step order in US-08.4; missing citations F-hr_transcript-d7431e / -b6d9b3 / F-zh_source_tax_calculator-52b67a in US-01.2, US-05.3, US-05.4, US-05.7 and in the rules cross_border_tariff_applies, liechtenstein_no_source_tax_in_principle and source_tax_result  
   Action: Add the missing citations (the H-tariff fact F-96658b and d7431e/b6d9b3/52b67a). Drop or cite the claims about the step order and dates that 'often move'.
10. **Some items and stories are inferred, and some child results still need checking** – 8 items and stories and several child-result rows (marked 'to be verified', including row 22: H1N or A) rest on inference. The tariff results Lonio computes have to match the Zurich calculator.  
   Evidence: inferred_items (spouse_residence_country, spouse_nationality, child_tariff_result, US-04.2, US-06.3–06.5, US-08.4); OQ-calculator-coverage; dev_refinement info on row 22; OQ-nationality-wording  
   Action: Keep the D-009 go-live gate. Have a domain expert confirm row 22 and the inferred rows against the calculator, and confirm that the spouse is also asked only Swiss yes/no and that D-008 applies to the spouse.

## Numbers

347 source units → 188 facts → 35 information items, 17 business rules → one feature with 8 sections, 30 stories, 100 acceptance criteria; 5 open questions, 12 exclusions.

## Impact of this run

Stories added: -; changed: US-01.3, US-04.1, US-04.2, US-04.3, US-05.3, US-05.4, US-05.6, US-05.7, US-06.1, US-06.2, US-08.1, US-08.2, US-08.4; removed: -; unchanged: 17.

Knowledge elements changed: OQ-nationality-wording, nationality, permit_reminder, permit_type, spouse_exempts_source_tax, spouse_nationality, spouse_permit_type, spouse_residence_country, subject_to_source_tax

## Errors (10)

- [decisions] `D-003` new evidence since this decision (3 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-003`: F-hr_followup-8d9f77: The nationality question can be answered as Swiss yes or no (allowed values: yes / no).; F-hr_followup-e8164e: For nationality, HR (Muster AG) only needs to know whether the employee is Swiss or not; the actual country of nationality is not needed.; F-hr_followup-ee7d68: The exact country of nationality should not be collected, since only Swiss yes/no is needed (data minimisation).
- [decisions] `D-005` new evidence since this decision (3 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-005`: F-hr_followup-32873d: Nationality (Swiss or not) is needed only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be answered as Swiss yes or no (allowed values: yes / no).; F-hr_followup-e8164e: For nationality, HR (Muster AG) only needs to know whether the employee is Swiss or not; the actual country of nationality is not needed.
- [decisions] `D-007` new evidence since this decision (2 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-007`: F-hr_followup-32873d: Nationality (Swiss or not) is needed only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be answered as Swiss yes or no (allowed values: yes / no).
- [decisions] `D-008` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-008`: F-hr_followup-32873d: Nationality (Swiss or not) is needed only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be answered as Swiss yes or no (allowed values: yes / no).; F-hr_followup-e8164e: For nationality, HR (Muster AG) only needs to know whether the employee is Swiss or not; the actual country of nationality is not needed. ...
- [decisions] `D-010` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-010`: F-hr_followup-32873d: Nationality (Swiss or not) is needed only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be answered as Swiss yes or no (allowed values: yes / no).; F-hr_followup-e8164e: For nationality, HR (Muster AG) only needs to know whether the employee is Swiss or not; the actual country of nationality is not needed. ...
- [decisions] `D-011` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-011`: F-hr_followup-32873d: Nationality (Swiss or not) is needed only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be answered as Swiss yes or no (allowed values: yes / no).; F-hr_followup-e8164e: For nationality, HR (Muster AG) only needs to know whether the employee is Swiss or not; the actual country of nationality is not needed. ...
- [decisions] `D-013` new evidence since this decision (2 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-013`: F-hr_followup-32873d: Nationality (Swiss or not) is needed only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be answered as Swiss yes or no (allowed values: yes / no).
- [decisions] `D-030` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-030`: F-hr_followup-32873d: Nationality (Swiss or not) is needed only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be answered as Swiss yes or no (allowed values: yes / no).; F-hr_followup-e8164e: For nationality, HR (Muster AG) only needs to know whether the employee is Swiss or not; the actual country of nationality is not needed. ...
- [decisions] `D-031` new evidence since this decision (1 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-031`: F-hr_followup-8d9f77: The nationality question can be answered as Swiss yes or no (allowed values: yes / no).
- [decisions] `D-038` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-038`: F-hr_followup-32873d: Nationality (Swiss or not) is needed only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be answered as Swiss yes or no (allowed values: yes / no).; F-hr_followup-e8164e: For nationality, HR (Muster AG) only needs to know whether the employee is Swiss or not; the actual country of nationality is not needed. ...

## Examples executed against the knowledge model (219/219 pass)

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
- ✅ AC-04.2.3 / Non-Swiss spouse living in Switzerland (spec)
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
- ✅ AC-08.2.2 / Changed the Swiss citizenship answer to yes after answering the C permit question and the source tax questions (spec)
- ✅ AC-08.3.2 / First working day moved from the 15th to the 1st of a month (spec)
- ✅ AC-08.3.2 / First working day in the middle of a month (spec)
- ✅ AC-08.4.2 / Swiss employee living in Switzerland, single (spec)
- ✅ AC-08.4.2 / Employee living in Germany, single (spec)

## Open questions (need your decision)

- **OQ-canton-abroad**: What should be entered in the pension fund's 'Canton' field for employees living abroad, and does 'Canton' mean canton of residence or of work? → recommended: Keep D-002 (ask only residents of Switzerland); a domain expert verifies with Pensionskasse Muster.
- **OQ-civil-status-partnership**: How does Pensionskasse Muster want registered partnerships and separated employees registered (its list has only Single, Married, Divorced, Widowed), and does it want the partner's details? → recommended: Keep the provisional mapping of D-003; verify with a domain expert and the fund.
- **OQ-spouse-dob-other-status**: Does the fund's screen require the spouse's (or former spouse's) date of birth or other fields for Divorced or Widowed? → recommended: Domain expert obtains a screenshot of the fund screen for Divorced and Widowed.
- **OQ-calculator-coverage**: Does Lonio's computed tariff code match the Zurich calculator on the paths not explored: the residence block for A/B/H tariffs, more than 3 children, H3N/P3N, and the child rows marked inferred? → recommended: Go-live condition per D-009; non-blocking for the spec.
- **OQ-nationality-wording**: HR confirmed that only 'Swiss: yes or no' is needed for the employee. Is the same enough for the spouse or registered partner? And does the dual-citizenship rule (D-008) also apply to the spouse? → recommended: Keep yes/no for the spouse (data minimisation, G-01) and apply D-008 to the spouse unless a domain expert says otherwise.

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
- fact F-hr_followup-ee7d68: The exact country of nationality should not be collected, since only Swiss yes/no is needed (data minimisation).
- fact F-hr_followup-32873d-2: Being Swiss or not affects source tax eligibility; the stakeholder implies that source tax may not apply at all depending on Swiss nationality, but did not state explicitly that Swiss nationals are never subject to source tax.
- fact F-hr_followup-ed14dd: Since Liechtenstein residence decides whether source tax questions are skipped, the country of residence (address_country) must be known before the source tax questions are asked.

## Dev refinement questions (14)

- [major] `stories/US-01.2-complete-home-address-for-posting-documents.md` Which home address should a new employee give: the one they live at when they fill in the questionnaire, or the one they will live at on their first working day? Many new hires move for the job. The address country decides source tax liability, the canton, the nationality and permit questions and the cross-border questions, so the answer changes what Lonio asks and what it records.
- [major] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` The non-return-day questions ask about 'more than 60' (Germany) and 'more than 45' (Liechtenstein) days 'in the calendar year'. For an employee who starts mid-year, are these the days expected for the rest of this year, or a full-year (pro-rata) figure? Should the question wording say which year it means? The same applies to US-07.3.
- [major] `stories/US-07.3-determine-the-source-tax-outcome-for-employees-living-in.md` Liechtenstein residents answer denomination, spouse employment and every child block (steps 6–7) before the cross-border step 8. If they then return daily or expect at most 45 non-return days, the result is 'in principle no source tax liability' and none of those answers is used. Under G-01 (data minimisation), should the Liechtenstein questions come first so the tariff questions are skipped for them? Or should the answers be collected anyway (for example in case HR changes something later) or discarded?
- [major] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` Does the employee see any derived result (tariff code, the Liechtenstein statement, insurance start date, subject or not subject), before or after submitting? Or is it only recorded for HR? D-007 says Lonio 'shows' the Liechtenstein statement, while the rest of the spec says results are 'recorded for HR'.
- [major] `stories/US-02.1-employee-enters-the-first-working-day.md` HR already knows the agreed start date from the contract. Is the first working day empty for the employee to fill in, or pre-filled by HR for the employee to confirm or correct? Which dates are acceptable: is a date in the past or before the submission date allowed, and is there a limit on how far in the future it can be?
- [major] `stories/US-08.1-remind-employees-to-bring-their-permit-on-the-first-working.md` 'HR words the reminder': is the text supplied once before go-live, or must HR be able to change it themselves? No wording exists yet, so the story cannot be finished or accepted. Who provides the text, and by when?
- [major] `stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md` Can the employee stop part-way and come back later, keeping the answers they already gave (including answers that are hidden but kept, per D-036)? Is there a deadline for submitting, for example before the first working day? What happens to a questionnaire that is never submitted, given data minimisation?
- [minor] `feature.md` For a Liechtenstein resident with the 'in principle no source tax liability' result, 'Subject to source tax' is still recorded as yes. HR would then see 'subject' next to 'no liability'. Which value should HR get? And for more than 45 non-return days, the calculator gives the tariff code together with 'subject to the double taxation agreement' (F-ab4e1e). Should that note or a flag also be recorded with the normal tariff code?
- [minor] `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` Can an employee answer 'yes' to having children and then submit with no child block, for example after removing them all? Is there a maximum number of children? The calculator's limit is unknown.
- [minor] `feature.md` The source fact F-96658b says a child counts with H only 'when it lives in the household'. Child-result row 22 (not married, child outside the household, parental custody, alternating care, employee contributes more) gives 'Counted with H' (calculator run C-V20, H1N). Please confirm that row 22 is H and not just 'Counted' (A), so the code follows the observed run and not the summary.
- [minor] `stories/US-01.2-complete-home-address-for-posting-documents.md` The house number is always required. What should an employee enter whose address has no house number (rural addresses, building names, PO-box-style addresses abroad)? The section notes say the sources don't cover this.
- [minor] `stories/US-01.1-personal-details-for-the-pension-fund-registration.md` Are there plausibility rules for the employee's and the spouse's dates of birth, for example not in the future or a minimum working age? Or is any full calendar date accepted?
- [minor] `stories/US-08.3-questionnaire-is-read-only-for-the-employee-after-submission.md` Derived results are always worked out again from the latest answers. What should Lonio record when an HR change after submission makes questions apply that were never answered? Examples: a move to Germany leaves the cross-border answers missing; a marriage leaves the spouse's date of birth and spouse employment missing. Should the result show as 'incomplete', or should the employee be asked again?
- [minor] `feature.md` Flow overview item 4 says employees living in Switzerland 'give their nationality', but the flow table, US-04.1 and the HR follow-up say only 'Swiss: yes or no' is asked. Please confirm that the overview is just loose wording and no nationality country is collected.

## Technical vocabulary found in the spec (5)

- `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` "When Lonio has decided whether the employee is subject to source tax (rule subject_to_source_tax)" - Uses an internal rule identifier in an acceptance criterion. That is implementation naming, not business language.
- `feature.md` "Afterwards Step 9 'Finish': permit reminder (rule permit_reminder), then submission" - Uses an internal snake_case rule id in prose.
- `feature.md` "one block per child, repeated for each child the employee adds; all child_* conditions refer to the same child" - Refers to a field-id naming pattern (child_*) and to 'conditions', which are internal model details and not a business statement.
- `feature.md` "(The formal expression covers one child block; the digit is the sum over all children.)" - Talks about how the rule's formal expression is implemented. The business rule only needs to say that the digit is the number of counting children. The same sentence appears in information.md.
- `information.md` "| Always | Always |  | pension_fund | [Personal details and home address]" - The 'Who needs it?' column uses snake_case stakeholder ids (pension_fund, source_tax, hr) instead of business names. These are data-model identifiers leaking into the prose table.

## Coverage

169/347 source units cited; 151/188 facts used.

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
- hr_followup/T-000: Subject: Notes from our follow-up call From: Leo (Lonio) To: Anna (HR, Muster AG) Date: 14 November 2026
- hr_followup/T-003: And people who live in Liechtenstein and commute to Zurich?
- hr_followup/T-004: Honestly, we never ask them anything about source tax. For us Liechtenstein commuters are not subject to source tax, so skip all the source tax questions for th
- hr_followup/T-005: Thanks, I will note both points.

## Other warnings (54)

- [fact_judge] `F-hr_transcript-9eeab6` partial: 'Muster AG' company name is not in these units, and 'about 150 employees mostly in Zurich' is supported, but the company name is added. | Muster AG hires around twenty people a year (more in summer) and has about 150 employees, mostly in Zurich.
- [fact_judge] `F-hr_transcript-b84498` partial: Reasonable reading, but the units say non-Swiss employees must answer, which is stated as a heuristic rather than 'subject to source tax' in general; mostly fine. | Source tax questions should only be asked to employees who are subject to source tax, not to everybody.
- [fact_judge] `F-hr_transcript-5518ad` partial: Address is needed, but 'home' is not stated explicitly (reasonable since posted to people). | HR needs the employee's home address.
- [fact_judge] `F-hr_transcript-30ead4` partial: Pension fund name, old portal and screenshots are supported, but 'Muster AG' as company name is not in these units (only implied by fund name). | Muster AG's pension fund is Pensionskasse Muster, which has an old portal; Anna will send screenshots of it.
- [fact_judge] `F-hr_transcript-550840` partial: Leo's summary and Anna's 'I think so' are supported, but 'later added further cases' is only visible in T-044 which is within context, so mostly fine; the added-cases claim is supported only via the spouse rule. | Leo summarised 'non-Swiss, but not with a C permit'; Anna only hedged ('I think so') and later added further cases.
- [fact_judge] `F-hr_transcript-a45422` partial: Anna says she checks the spouse case by hand and asks by email which takes forever, but 'HR' as a whole is her inference, fine; the 'takes forever' applies to the email asking, which is stated; mostly supported but slightly generalised. | Today HR checks the spouse case by hand and asks for spouse details by email, which takes forever.
- [fact_judge] `F-hr_transcript-e505f8` partial: Address includes country and living abroad matters, but deriving abroad status from the address country is a reasonable inference not stated explicitly. | Whether the employee lives abroad can be derived from the country of the home address, which is relevant for source tax liability.
- [fact_judge] `F-hr_transcript-d5c04b` partial: Leo will respond this week once they've gone through Anna's screenshots; 'after reviewing the screenshots' is close, but Anna says she'll send them after lunch—fine; minor paraphrase. | Anna asked about timing; Leo will respond this week after reviewing the screenshots.
- [fact_judge] `F-pension_portal-39bab1` partial: Shown for Married (05, 07) and absent for Single (04) is visible in units; absence in 01, 02, 03, 06 isn't evidenced by the given units, and 'only when Married' is overstated given Divorced/Widowed are untested. | The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected).
- [fact_judge] `F-pension_portal-3cfe89` partial: Footnote 'Fields marked * are required.' is supported, and the visible fields shown carry required_marker true, but the claim that all visible fields carry the marker isn't fully shown (no marker on e.g. every field in these units, e.g. First/Last name only in S06). | Fields marked with an asterisk are required; all visible fields on the form carry the marker.
- [fact_judge] `F-zh_source_tax_calculator-351289` partial: Skipping to Q16 is stated, but 'main-residence question' for Q16 is not shown in the units. | If the income type is 'Ersatzeinkünfte', all personal and child questions are skipped and the calculator goes straight to the main-residence question (Q16).
- [fact_judge] `F-zh_source_tax_calculator-64ac33` partial: Q14 = Ja for single persons is described only as 'Q14 = Ja' (parental care), and the 'Q13 shared custody' labelling is fine, but the statement mixes wording; essentially matches the condition, though Q14 is not named as shared custody here. | Alternating care is asked when (child minor AND same household AND shared custody AND no common household with the other parent) OR (married AND child minor AND not same household AND Q13 shared custody = Ja) OR (single AND child minor AND not same household AND Q14 = Ja).
- [fact_judge] `F-zh_source_tax_calculator-ad867a` partial: Omits nothing major, but the Q10 = Ja condition for singles also requires Q08 = Ja; stated. The 'ends the child block' note is supported; however the statement's single-person condition is accurate, so only minor paraphrase risk. | The larger-contributor question is asked when alternating care = Ja, OR for single persons when the child lives in the same household and there is a common household with the other parent; for married persons a common household with the other parent ends the child block without this question.
- [fact_judge] `F-zh_source_tax_calculator-cd1015` partial: Condition matches, but the meaning of Q10 as 'no common household with the other parent' is not stated in the units. | Q15 is shown only when the child is 'Volljährig und in Erstausbildung' AND (child not in same household OR (same household AND no common household with the other parent)).
- [fact_judge] `F-zh_source_tax_calculator-5f6820` partial: Condition Q18=Ja OR Q24=Ja is stated, but the units don't define Q24 so 'replacement income' is an unsupported gloss. | The certificate of residence question is asked only when the person returns daily to Germany (Q18 = Ja for earned income, or Q24 = Ja for replacement income).
- [fact_judge] `F-zh_source_tax_calculator-ab4e1e` partial: Nein gives 'keine Quellensteuerpflicht' per help, but test vector V41 also shows the DBA reservation on Nein, so 'Nein' stated without it is only partly consistent; Ja rule is fine. | More than 45 non-return days (Ja) gives the normal tariff plus 'Unter Vorbehalt des Doppelbesteuerungsabkommens'; otherwise (Nein) 'Grundsätzlich keine Quellensteuerpflicht'.
- [fact_judge] `F-zh_source_tax_calculator-3058a4` partial: Vectors show Q10=Ja gives C1Y and Q10=Nein gives C0Y, but the meaning of Q10/Q11 (common household, alternating care) isn't in the units, and the statement has an unfinished 'only if...' fragment. | Married person, minor child in same household, shared custody: common household with the other parent counts the child (C1Y); no common household counts the child only if... observed: alternating care with other parent as main contributor -> 0 (C0Y), no alternating care -> 0 (C0Y).
- [fact_judge] `F-zh_source_tax_calculator-56e79b` partial: Outcomes B1N/B0N match V12/V13, but vectors only show Q13 Ja/Nein without a label, so reading Q13 as 'shared custody' and Q11 as 'alternating care' is an inference. | Married person, minor child not in household: shared custody + alternating care + person is main contributor counts the child (B1N); no shared custody does not count it (B0N).
- [fact_judge] `F-hr_followup-ed14dd` partial: Reasonable inference that residence must be known first, but the field name address_country is not in the units. | Since Liechtenstein residence decides whether source tax questions are skipped, the country of residence (address_country) must be known before the source tax questions are asked.
- [coverage] `F-hr_followup-32873d-2` fact not used anywhere in the spec: Being Swiss or not affects source tax eligibility; the stakeholder implies that source tax may not apply at all depending on Swiss nationality, but did not state explicitly that Swiss nationals are never subject to source tax.
- [coverage] `F-hr_followup-664bcb` fact not used anywhere in the spec: Employees who live in Liechtenstein and commute to Zurich are not subject to source tax (per Muster AG HR).
- [coverage] `F-hr_followup-edd03f` fact not used anywhere in the spec: All source tax questions must be skipped for employees who live in Liechtenstein and commute to Zurich.
- [coverage] `F-hr_followup-ed14dd` fact not used anywhere in the spec: Since Liechtenstein residence decides whether source tax questions are skipped, the country of residence (address_country) must be known before the source tax questions are asked.
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
- [trace_judge] `rule.permit_reminder` partial: The claim that the reminder 'collects no data' is not stated in D-010, D-038 or the other cited facts.
- [trace_judge] `story.US-01.2` partial: The non-illustrative Tomás/Winterthur example (country Switzerland) relies on F-hr_transcript-d7431e, which is not among the cited facts and has no source_refs on the example.
- [trace_judge] `story.US-03.4` partial: The priority reason's tariff letters (A/B/C/H) are not backed by any cited fact; the criteria themselves are supported.
- [trace_judge] `story.US-04.2` partial: Asking the spouse's residence first, asking the spouse's Swiss yes/no and applying the dual-citizenship rule to the spouse are self-declared inferences, not backed by the cited facts.
- [trace_judge] `story.US-05.3` partial: Who is subject to source tax is relied on (e.g. the Tomás example, F-hr_transcript-d7431e) but neither that fact nor the subject rule F-hr_transcript-b6d9b3 is cited.
- [trace_judge] `story.US-05.4` partial: The non-illustrative Tomás example (not subject) depends on F-hr_transcript-d7431e and the subject rule, which are not among the cited facts.
- [trace_judge] `story.US-05.6` partial: The base-letter scope excludes Liechtenstein residents, and no cited fact covers Liechtenstein; the cited facts mention only CH, other countries and Germany.
- [trace_judge] `story.US-05.7` partial: AC-05.7.5 lists 'child results marked inferred' as unexplored paths, but D-009 does not list that path; the Tomás example also cites F-hr_transcript-d7431e, which is not provided.
- [trace_judge] `story.US-08.3` partial: The priority reason's claim that HR reports the first working day often moves is not in any cited fact; the rest is backed by D-033, D-037 and F-1d5c07.
- [trace_judge] `story.US-08.4` partial: No cited fact gives the nine-step order in AC-08.4.1, and the 'submission only with all required answers' rule in AC-08.4.3 is not stated in the cited facts; the rest (English, skipping, read-only after submission) is backed.
- [dev_refinement] `stories/US-01.2-complete-home-address-for-posting-documents.md` Which home address should a new employee give: the one they live at when they fill in the questionnaire, or the one they will live at on their first working day? Many new hires move for the job. The address country decides source tax liability, the canton, the nationality and permit questions and the cross-border questions, so the answer changes what Lonio asks and what it records.
- [dev_refinement] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` The non-return-day questions ask about 'more than 60' (Germany) and 'more than 45' (Liechtenstein) days 'in the calendar year'. For an employee who starts mid-year, are these the days expected for the rest of this year, or a full-year (pro-rata) figure? Should the question wording say which year it means? The same applies to US-07.3.
- [dev_refinement] `stories/US-07.3-determine-the-source-tax-outcome-for-employees-living-in.md` Liechtenstein residents answer denomination, spouse employment and every child block (steps 6–7) before the cross-border step 8. If they then return daily or expect at most 45 non-return days, the result is 'in principle no source tax liability' and none of those answers is used. Under G-01 (data minimisation), should the Liechtenstein questions come first so the tariff questions are skipped for them? Or should the answers be collected anyway (for example in case HR changes something later) or discarded?
- [dev_refinement] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` Does the employee see any derived result (tariff code, the Liechtenstein statement, insurance start date, subject or not subject), before or after submitting? Or is it only recorded for HR? D-007 says Lonio 'shows' the Liechtenstein statement, while the rest of the spec says results are 'recorded for HR'.
- [dev_refinement] `stories/US-02.1-employee-enters-the-first-working-day.md` HR already knows the agreed start date from the contract. Is the first working day empty for the employee to fill in, or pre-filled by HR for the employee to confirm or correct? Which dates are acceptable: is a date in the past or before the submission date allowed, and is there a limit on how far in the future it can be?
- [dev_refinement] `stories/US-08.1-remind-employees-to-bring-their-permit-on-the-first-working.md` 'HR words the reminder': is the text supplied once before go-live, or must HR be able to change it themselves? No wording exists yet, so the story cannot be finished or accepted. Who provides the text, and by when?
- [dev_refinement] `stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md` Can the employee stop part-way and come back later, keeping the answers they already gave (including answers that are hidden but kept, per D-036)? Is there a deadline for submitting, for example before the first working day? What happens to a questionnaire that is never submitted, given data minimisation?

## Run

Stages run: normalize/hr_followup, extract/hr_followup, judge_facts, knowledge.raw, feature.plan, sections/SEC-01-identity-and-address, sections/SEC-08-completion-and-submission, sections/SEC-07-living-abroad, sections/SEC-04-source-tax-liability, sections/SEC-05-tariff-basics, sections/SEC-06-children, feature.flow, judge_trace, dev_refinement, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator

LLM cost this run: $9.35

Tokens this run: 2,293,896 in 28 agent calls (79 input, 1,195,072 cache read, 981,233 cache write, 117,512 output)
