# Review: employee-onboarding

**Verdict: NOT READY**

All 250+ examples pass and no open question is blocking. But 10 decisions (D-003, 005, 007, 008, 010, 011, 013, 030, 031, 038) are stale after the HR follow-up on nationality, which is an error-level check. Several dev-refinement questions rated major could change tariff results or stop employees submitting. Technical leaks are present, and some trace claims are unbacked.

## Reviewer findings

1. **Decisions stale after HR follow-up on nationality** – The follow-up says HR needs only Swiss yes/no, and that Swiss employees and Liechtenstein commuters have no source tax. Ten decisions that depend on nationality were made before this evidence. Stories built on them (US-01.3, 04.x, 05.x, 06.x, 08.x) may be wrong.  
   Evidence: decisions check errors: D-003, D-005, D-007, D-008, D-010, D-011, D-013, D-030, D-031, D-038; new facts F-hr_followup-32873d, -8d9f77, -e8164e  
   Action: Review each decision against the new facts. Update or confirm it, then run `pipeline reconfirm <id>`. Resolve OQ-nationality-wording at the same time, including the spouse and dual citizenship.
2. **Liechtenstein / nationality eligibility facts unused in the spec** – HR said Liechtenstein commuters get no source tax questions. These facts are not cited anywhere. It is also unclear whether the rule covers all Liechtenstein residents or only those commuting to Zurich. The spec still asks Liechtenstein residents tariff questions, which conflicts with this and with G-01.  
   Evidence: coverage: F-hr_followup-664bcb, -297dfa, -446835, -b65e24, -32873d-2; dev_refinement: Liechtenstein data minimisation question  
   Action: Decide in decisions.yaml whether all Liechtenstein residents skip every source tax question. Then update the rules, and the flow if the cross-border questions need to come first.
3. **Child H-tariff conflict for a non-household child** – Child result row 22 and AC-06.4.3 say a minor child of a non-married employee who does not live in the household 'counts with H'. The calculator note says H applies only if the child lives in the household. The tariff letter would be wrong.  
   Evidence: dev_refinement (major); F-zh_source_tax_calculator-96658b; AC-06.4.3; rule.child_tariff_result (inferred); trace_judge: 'H tariff' purpose unbacked on child items  
   Action: Have a domain expert check this against the calculator. Record the answer as a decision, fix row 22 and AC-06.4.3, and cite the source for the H-tariff purpose.
4. **Liechtenstein >45 days: DBA reservation not recorded** – The calculator returns the tariff code together with 'Unter Vorbehalt des DBA'. The spec records only the code, so HR loses the reservation.  
   Evidence: dev_refinement major on US-07.3 and US-05.7; F-zh_source_tax_calculator-ab4e1e; AC-05.7.3  
   Action: Decide whether the reservation and an HR flag are recorded with the code. Update AC-05.7.3 and US-07.3.
5. **House number required with no way past it for addresses without one** – Employees with rural, building-name or some foreign addresses cannot submit.  
   Evidence: dev_refinement major, US-01.2  
   Action: Decide whether the house number is optional or has a 'no number' option.
6. **Address date and what the employee sees of derived results are undefined** – The home address country drives liability, canton and tariff. It is not specified whether the address is the current one or the one from the start date. It is also not specified whether the employee sees derived results such as the tariff or subject status.  
   Evidence: dev_refinement major: feature.md (address date), US-05.7 (employee visibility), US-02.1 (does the form start empty or prefilled with HR's date)  
   Action: Add decisions for each of the three points. Ask HR which address applies and whether HR prefills the first working day.
7. **Spouse data collected beyond need (nationality and residence)** – Only 'Swiss?' and 'lives in Switzerland?' drive rules. Asking for full countries conflicts with G-01. The form is not backed by facts and is inferred.  
   Evidence: OQ-nationality-wording; dev_refinement major on US-04.2; trace_judge item.spouse_nationality; inferred items spouse_residence_country and spouse_nationality  
   Action: Decide on yes/no questions for both the spouse's nationality and the spouse's residence. Extend OQ-nationality-wording to cover residence.
8. **Technical leaks in the spec** – Internal ids and implementation prescriptions appear in business text. US-08.2 turns D-036's 'may be kept' into a requirement.  
   Evidence: tech_leak: feature.md (child_*, permit_reminder, 'formal expression'), US-06.1 (subject_to_source_tax, add/remove blocks), US-08.2 (answer retention)  
   Action: Replace the ids with business names, drop the UI prescriptions, and align US-08.2 with D-036 or make retention an explicit decision.
9. **Unbacked trace claims** – Some rules and stories cite facts that are not in their source list, or state things no fact supports. Traceability is weak for engineering.  
   Evidence: trace_judge: rule.cross_border_tariff_applies and rule.liechtenstein_no_source_tax_in_principle (F-…-52b67a), rule.source_tax_result (F-hr_transcript-b6d9b3), US-01.2 and US-05.4 (F-hr_transcript-d7431e), US-08.4 nine-step order, US-08.3, item.first_working_day, item.address_country  
   Action: Fix the citations. Record the nine-step order as a decision, or mark it inferred and drop the unsupported claims.
10. **Non-blocking open questions and test gaps remain** – The fund's Canton field for residents abroad, partnership mapping, and the calculator paths not explored could cause wrong registrations or tariff codes. Date ranges, child count limits and the ambiguous example tables are also untestable as written.  
   Evidence: OQ-canton-abroad, OQ-civil-status-partnership, OQ-spouse-dob-other-status, OQ-calculator-coverage; dev_refinement minor items; US-08.4 and AC-05.4.3 examples use the same item as input and output  
   Action: Keep these as go-live conditions with a named owner. Add date range and child count rules, and fix the example tables.

## Numbers

347 source units → 189 facts → 35 information items, 17 business rules → one feature with 8 sections, 30 stories, 100 acceptance criteria; 5 open questions, 13 exclusions.

## Impact of this run

Stories added: -; changed: US-01.3, US-04.1, US-04.2, US-04.3, US-05.3, US-05.4, US-05.6, US-05.7, US-06.1, US-06.2, US-08.1, US-08.2, US-08.4; removed: -; unchanged: 17.

Knowledge elements changed: OQ-nationality-wording, nationality, permit_reminder, permit_type, spouse_nationality, spouse_permit_type, spouse_residence_country, subject_to_source_tax

## Errors (10)

- [decisions] `D-003` new evidence since this decision (1 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-003`: F-hr_followup-8d9f77: The nationality question can be captured as Swiss: yes / no.
- [decisions] `D-005` new evidence since this decision (2 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-005`: F-hr_followup-32873d: HR needs nationality only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be captured as Swiss: yes / no.
- [decisions] `D-007` new evidence since this decision (2 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-007`: F-hr_followup-32873d: HR needs nationality only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be captured as Swiss: yes / no.
- [decisions] `D-008` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-008`: F-hr_followup-32873d: HR needs nationality only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be captured as Swiss: yes / no.; F-hr_followup-e8164e: HR (Muster AG) does not need the employee's actual country of nationality; knowing whether the employee is Swiss (yes/no) is enough. ...
- [decisions] `D-010` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-010`: F-hr_followup-32873d: HR needs nationality only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be captured as Swiss: yes / no.; F-hr_followup-e8164e: HR (Muster AG) does not need the employee's actual country of nationality; knowing whether the employee is Swiss (yes/no) is enough. ...
- [decisions] `D-011` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-011`: F-hr_followup-32873d: HR needs nationality only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be captured as Swiss: yes / no.; F-hr_followup-e8164e: HR (Muster AG) does not need the employee's actual country of nationality; knowing whether the employee is Swiss (yes/no) is enough. ...
- [decisions] `D-013` new evidence since this decision (2 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-013`: F-hr_followup-32873d: HR needs nationality only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be captured as Swiss: yes / no.
- [decisions] `D-030` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-030`: F-hr_followup-32873d: HR needs nationality only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be captured as Swiss: yes / no.; F-hr_followup-e8164e: HR (Muster AG) does not need the employee's actual country of nationality; knowing whether the employee is Swiss (yes/no) is enough. ...
- [decisions] `D-031` new evidence since this decision (1 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-031`: F-hr_followup-8d9f77: The nationality question can be captured as Swiss: yes / no.
- [decisions] `D-038` new evidence since this decision (4 fact(s)) - re-confirm, update or drop it, then run `pipeline reconfirm D-038`: F-hr_followup-32873d: HR needs nationality only to determine whether source tax can apply to the employee at all.; F-hr_followup-8d9f77: The nationality question can be captured as Swiss: yes / no.; F-hr_followup-e8164e: HR (Muster AG) does not need the employee's actual country of nationality; knowing whether the employee is Swiss (yes/no) is enough. ...

## Examples executed against the knowledge model (220/220 pass)

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
- ✅ AC-04.1.2 / Swiss citizen (also dual citizen) living in Switzerland (spec)
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
- ✅ AC-08.2.2 / Changed the answer to 'Swiss' to yes after answering the C permit question and the source tax questions (spec)
- ✅ AC-08.3.2 / First working day moved from the 15th to the 1st of a month (spec)
- ✅ AC-08.3.2 / First working day in the middle of a month (spec)
- ✅ AC-08.4.2 / Swiss employee living in Switzerland, single (spec)
- ✅ AC-08.4.2 / Employee living in Germany, single (spec)

## Open questions (need your decision)

- **OQ-canton-abroad**: What should be entered in the pension fund's 'Canton' field for employees living abroad, and does 'Canton' mean canton of residence or of work? → recommended: Keep D-002 (ask only residents of Switzerland); a domain expert verifies with Pensionskasse Muster.
- **OQ-civil-status-partnership**: How does Pensionskasse Muster want registered partnerships and separated employees registered (its list has only Single, Married, Divorced, Widowed), and does it want the partner's details? → recommended: Keep the provisional mapping of D-003; verify with a domain expert and the fund.
- **OQ-spouse-dob-other-status**: Does the fund's screen require the spouse's (or former spouse's) date of birth or other fields for Divorced or Widowed? → recommended: Domain expert obtains a screenshot of the fund screen for Divorced and Widowed.
- **OQ-calculator-coverage**: Does Lonio's computed tariff code match the Zurich calculator on the paths not explored: the residence block for A/B/H tariffs, more than 3 children, H3N/P3N, and the child rows marked inferred? → recommended: Go-live condition per D-009; non-blocking for the spec.
- **OQ-nationality-wording**: Should the spouse's or registered partner's nationality also be asked only as 'Swiss: yes / no', as HR confirmed for the employee? And does the dual-citizenship rule (D-008) also apply to the spouse? → recommended: Use yes/no for the spouse as well, as for the employee. Apply D-008 to the spouse unless a domain expert says otherwise. Confirm with the product owner.

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
- fact F-hr_followup-32873d-2: Being Swiss is relevant to whether source tax can apply; the reading that Swiss employees cannot be subject to source tax is inferred and not stated explicitly.
- fact F-hr_followup-ee7d68: For HR's purposes, the specific nationality country is not needed. Whether other receiving parties, such as the pension fund, need it is not addressed here.
- fact F-hr_followup-446835: Taken together, the Liechtenstein rule and the nationality rule mean the source tax questions should be asked only if the employee is not Swiss and does not live in Liechtenstein. This is inferred from the two rules and is not a complete eligibility rule.
- fact F-hr_followup-b65e24: It is unclear whether the Liechtenstein exemption applies to every employee who lives in Liechtenstein, or only to those who commute to Zurich. The term 'commute to Zurich' was used by the interviewer, and the stakeholder said only 'Liechtenstein commuters'.

## Dev refinement questions (16)

- [major] `stories/US-02.1-employee-enters-the-first-working-day.md` Does the questionnaire start empty, or does it show the first working day HR already agreed, for the employee to confirm or correct? HR says 'I ask them to confirm it', which suggests HR already has a date. The spec only says the employee 'enters' it. This decides whether HR provides a value that is shown at the start.
- [major] `stories/US-07.3-determine-the-source-tax-outcome-for-employees-living-in.md` For Liechtenstein residents with more than 45 non-return days, the calculator gives the normal tariff code together with 'Unter Vorbehalt des Doppelbesteuerungsabkommens' (subject to the double taxation agreement) (F-zh_source_tax_calculator-ab4e1e, C1Y / Unter Vorbehalt…). The spec records only the normal tariff code and flags only the 'no liability' case. Should the 'subject to the double taxation agreement' note and the HR flag also go with the tariff code in this case?
- [major] `stories/US-01.2-complete-home-address-for-posting-documents.md` The house number is required for every employee, but the notes say the sources do not cover addresses without one (rural addresses, building names, some foreign addresses). Can the employee submit without a house number, and if so how? As written, these employees cannot submit at all.
- [minor] `stories/US-02.1-employee-enters-the-first-working-day.md` What are the valid ranges for dates? For example: can the first working day be in the past or far in the future, and must the date of birth (employee and spouse) be in the past or show a minimum age? Without this there are no rejection criteria to test.
- [minor] `stories/US-07.2-decide-the-cross-border-tariff-for-employees-living-in.md` The 60-day (Germany) and 45-day (Liechtenstein) questions refer to the calendar year. For someone who starts mid-year, does the employee estimate for the rest of the current year or for a full year?
- [major] `feature.md` Which home address should the employee give: the current one, or the one that applies from the first working day? A new hire who is moving from abroad to Switzerland, or the other way, gets a different source tax liability, canton, cross-border questions and tariff code depending on which address counts. The spec treats the home address country as the country of residence without saying for which date.
- [major] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` Should the employee ever see the derived results (insurance start date, civil status as the fund will receive it, whether they are subject to source tax, the tariff code or the Liechtenstein result), for example before submitting or in the read-only view? Or are these recorded only for HR? The spec says 'recorded for HR' but never says what the employee sees.
- [major] `feature.md` Liechtenstein residents who return daily, or expect at most 45 non-return days, get no tariff code. Yet they are asked the denomination, whether the spouse works, and all the children questions before the cross-border step, and none of those answers is used. Is that intended, given data minimisation (G-01)? Or should the cross-border questions come first for Liechtenstein residents so the tariff questions can be skipped, and should those answers be discarded on submission?
- [major] `feature.md` Child result row 22, and AC-06.4.3 with it: a minor child of a non-married employee who does NOT live in the household (parental custody, alternating care, employee pays more) 'counts with H'. The calculator note F-zh_source_tax_calculator-96658b says a child counts with H only when it lives in the household. Which is right: H or counted without H (A)? The answer changes the tariff letter.
- [minor] `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` If the employee answers 'yes' to having children, must they add at least one child block before they can submit? And is there a maximum number of children? Today an employee could say 'yes' and add no child at all.
- [minor] `stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md` D-036 says inapplicable answers 'may be kept' until submission. AC-08.2.1 says they are kept and reappear when the earlier answer is changed back. Is keeping them a requirement or only allowed? Does it also apply if the employee leaves and comes back later in a new session, before submitting?
- [minor] `stories/US-08.4-step-by-step-questionnaire-flow.md` Some example tables use the same item as both input and expected output (AC-08.4.2 lists 'Nationality' twice; AC-05.4.3 has 'Spouse / partner is gainfully employed…' as input and output 'asked'). Which value is the expected result, so the examples can be tested?
- [major] `stories/US-04.2-ask-spouse-details-only-when-the-spouse-could-exempt-the.md` The spouse's or partner's country of residence is asked as a full country, but the only thing that decides anything is whether the spouse lives in Switzerland. Under data minimisation (G-01), should it be asked only as 'Does your spouse/partner live in Switzerland? yes/no'? OQ-nationality-wording covers only the spouse's nationality, not the spouse's residence.
- [major] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` For Liechtenstein residents with more than 45 non-return days, the calculator gives the normal tariff code together with 'Unter Vorbehalt des Doppelbesteuerungsabkommens' (F-zh_source_tax_calculator-ab4e1e, e.g. 'C1Y / Unter Vorbehalt…'). AC-05.7.3 records only 'the normal tariff code'. Should this reservation (and a flag for HR) also be recorded with the code?
- [minor] `feature.md` Certificate of residence offers 'yes', 'no' and 'not yet', and both 'no' and 'not yet' count as no for the tariff code. What should an employee mean by 'no' compared with 'not yet' (for example, will never provide one)? Does HR treat the two answers differently, for example by following up only on 'not yet'?
- [minor] `stories/US-04.1-ask-swiss-citizenship-and-c-permit-only-of-employees-living.md` Which countries can be chosen for the home address and for the spouse's residence and nationality? Is there an option for a stateless spouse or one whose nationality is unknown? And which nationality should the employee enter for a spouse who holds several non-Swiss nationalities?

## Technical vocabulary found in the spec (6)

- `feature.md` "Step 7 'Children' – one block per child, repeated for each child the employee adds; all child_* conditions refer to the same child." - 'child_*' is an internal field-id prefix used in prose. Business readers should not see identifier naming.
- `feature.md` "Afterwards Step 9 'Finish': permit reminder (rule permit_reminder), then submission" - Uses an internal rule id ('permit_reminder') in prose instead of the business name of the rule.
- `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` "When Lonio has decided whether the employee is subject to source tax (rule subject_to_source_tax)" - Uses an internal rule identifier in an acceptance criterion. That is an implementation artifact, not business language.
- `feature.md` "(The formal expression covers one child block; the digit is the sum over all children.)" - Refers to how the rule is encoded (a 'formal expression' per child block). That is an implementation detail of the rule engine, not a business statement.
- `stories/US-06.1-ask-each-child-s-age-status-and-household-only-where-the.md` "the employee goes through one block of questions per child and can add another child or remove one" - Prescribes the interaction (repeatable blocks with add and remove controls, copied from the calculator UI). The need is only to capture each child's answers.
- `stories/US-08.2-discard-answers-that-no-longer-apply-on-submission.md` "their answers are kept, so that if the employee changes the earlier answer back, the earlier input reappears and need not be entered again" - Turns D-036's permissive 'may be kept' into required draft-retention and re-display behaviour, which is an implementation choice.

## Coverage

169/347 source units cited; 151/189 facts used.

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

## Other warnings (51)

- [fact_judge] `F-hr_transcript-5518ad` partial: Address is needed, but 'home' address is not explicitly stated, though it is implied. | HR needs the employee's home address.
- [fact_judge] `F-hr_transcript-872bd7` partial: First working day and 'number one thing' are stated, but T-024 doesn't tie it specifically to the pension fund, though context (T-023) implies it. | The employee's first working day is needed for the pension fund; it is the most important item.
- [fact_judge] `F-hr_transcript-550840` partial: Leo's summary and Anna's hedge are supported, but 'later added further cases' is only visible via T-044 (spouse case), which is in the neighbouring context, so it is weakly supported. | Leo summarised 'non-Swiss, but not with a C permit'; Anna only hedged ('I think so') and later added further cases.
- [fact_judge] `F-hr_transcript-a45422` partial: Anna says she checks the spouse case by hand and asks by email which takes forever; 'HR' is reasonable but the email slowness refers to asking for spouse details, which is fine; minor generalization. | Today HR checks the spouse case by hand and asks for spouse details by email, which takes forever.
- [fact_judge] `F-hr_transcript-d5c04b` partial: Leo said he'll come back on timing this week after going through the screenshots, but the units don't state that he'll review them or that he responds with a timing answer beyond that; mostly supported. | Anna asked about timing; Leo will respond this week after reviewing the screenshots.
- [fact_judge] `F-pension_portal-39bab1` partial: Units show the field present for Married (05, 07) and absent in Single (04, no spouse unit); absence in 01, 02, 03, 06 is not visible in the given units, and 'only when Married' is not established for Divorced/Widowed. | The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected).
- [fact_judge] `F-pension_portal-3cfe89` partial: Footnote says fields marked * are required, but 'all visible fields carry the marker' isn't shown; units show required_marker true only on some labels and the shown units don't establish all fields. | Fields marked with an asterisk are required; all visible fields on the form carry the marker.
- [fact_judge] `F-zh_source_tax_calculator-351289` partial: Q16 is stated as the target, but 'main-residence question' is not described in the units. | If the income type is 'Ersatzeinkünfte', all personal and child questions are skipped and the calculator goes straight to the main-residence question (Q16).
- [fact_judge] `F-zh_source_tax_calculator-64ac33` partial: Q14 = Ja is stated for the single branch only via 'Q14' (not described as shared custody/parental care) and Q13/Q14 are labelled loosely; the core condition matches but 'single' is a simplification of Ledig/Geschieden/Getrennt/Verwitwet. | Alternating care is asked when (child minor AND same household AND shared custody AND no common household with the other parent) OR (married AND child minor AND not same household AND Q13 shared custody = Ja) OR (single AND child minor AND not same household AND Q14 = Ja).
- [fact_judge] `F-zh_source_tax_calculator-ad867a` partial: 'Single' simplifies the non-married statuses, and the statement omits that Q10 = Ja is required in addition to Q08 = Ja; otherwise matches the shown_when and help note. | The larger-contributor question is asked when alternating care = Ja, OR for single persons when the child lives in the same household and there is a common household with the other parent; for married persons a common household with the other parent ends the child block without this question.
- [fact_judge] `F-zh_source_tax_calculator-cd1015` partial: Condition structure matches, but the meaning of Q10=Nein as 'no common household with other parent' is not shown in these units. | Q15 is shown only when the child is 'Volljährig und in Erstausbildung' AND (child not in same household OR (same household AND no common household with the other parent)).
- [fact_judge] `F-zh_source_tax_calculator-5f6820` partial: Condition Q18=Ja OR Q24=Ja is explicit, but the units never define Q24 as the replacement-income daily-return question, so that gloss is unsupported. | The certificate of residence question is asked only when the person returns daily to Germany (Q18 = Ja for earned income, or Q24 = Ja for replacement income).
- [fact_judge] `F-zh_source_tax_calculator-ab4e1e` partial: Q23 help says Nein gives only 'Grundsätzlich keine Quellensteuerpflicht', but vector V41 shows Nein also yields the DBA reservation text, so the 'otherwise' phrasing is mostly right but the Ja case is fine; the minor inconsistency is in the sources. | More than 45 non-return days (Ja) gives the normal tariff plus 'Unter Vorbehalt des Doppelbesteuerungsabkommens'; otherwise (Nein) 'Grundsätzlich keine Quellensteuerpflicht'.
- [fact_judge] `F-zh_source_tax_calculator-3058a4` partial: Vectors give C1Y for common household and C0Y for the no-household cases, but the statement is garbled (unfinished 'only if...') and the units never label Q11 as 'alternating care'. | Married person, minor child in same household, shared custody: common household with the other parent counts the child (C1Y); no common household counts the child only if... observed: alternating care with other parent as main contributor -> 0 (C0Y), no alternating care -> 0 (C0Y).
- [fact_judge] `F-zh_source_tax_calculator-56e79b` partial: Vectors V12/V13 show B1N vs B0N, but the units never label Q13 as shared custody or Q11 as alternating care, so those labels are assumed. | Married person, minor child not in household: shared custody + alternating care + person is main contributor counts the child (B1N); no shared custody does not count it (B0N).
- [fact_judge] `F-hr_followup-297dfa` partial: Skipping source tax questions for Liechtenstein commuters is stated, but the 'address_country' field mapping is an addition. | If the employee lives in Liechtenstein (country of residence/address_country = Liechtenstein) and commutes to Zurich, all source tax questions must be skipped.
- [coverage] `F-hr_followup-32873d-2` fact not used anywhere in the spec: Being Swiss is relevant to whether source tax can apply; the reading that Swiss employees cannot be subject to source tax is inferred and not stated explicitly.
- [coverage] `F-hr_followup-664bcb` fact not used anywhere in the spec: Employees who live in Liechtenstein and commute to Zurich are not subject to source tax.
- [coverage] `F-hr_followup-297dfa` fact not used anywhere in the spec: If the employee lives in Liechtenstein (country of residence/address_country = Liechtenstein) and commutes to Zurich, all source tax questions must be skipped.
- [coverage] `F-hr_followup-446835` fact not used anywhere in the spec: Taken together, the Liechtenstein rule and the nationality rule mean the source tax questions should be asked only if the employee is not Swiss and does not live in Liechtenstein. This is inferred from the two rules and is not a complete eligibility rule.
- [coverage] `F-hr_followup-b65e24` fact not used anywhere in the spec: It is unclear whether the Liechtenstein exemption applies to every employee who lives in Liechtenstein, or only to those who commute to Zurich. The term 'commute to Zurich' was used by the interviewer, and the stakeholder said only 'Liechtenstein commuters'.
- [trace_judge] `item.address_country` partial: The claim that the country decides whether the permit reminder is shown is not backed by the cited facts (D-010 and D-038 are not cited).
- [trace_judge] `item.first_working_day` partial: The claim that HR 'runs the onboarding around the start date' is not backed, since D-034 leaves who starts the onboarding to a later spec.
- [trace_judge] `item.spouse_nationality` partial: The form (spouse entered as a country, with Swiss citizens entered as "Switzerland") is not backed by the facts. F-hr_followup only says Swiss yes/no is enough, and applying D-008 to the spouse is an inference.
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
- [trace_judge] `story.US-05.4` partial: The non-illustrative Tomás example relies on F-hr_transcript-d7431e (and the subject-to-source-tax rule), which is not among the cited facts.
- [trace_judge] `story.US-05.7` partial: AC-05.7.5 includes 'child results marked inferred' as an unexplored path, but D-009 and the cited calculator disclaimer do not mention it.
- [trace_judge] `story.US-08.3` partial: The priority reason's claim that HR reports the first working day often moves is not in any cited fact; the rest is backed by D-033, D-037 and F-1d5c07.
- [trace_judge] `story.US-08.4` partial: The fixed nine-step order in AC-08.4.1 (including step names and sequence) is not stated in any cited fact; the facts back only English (G-09), canton for residents of Switzerland (D-002), the permit reminder (D-010) and the C-permit step (D-005). The skipping and submission criteria are backed by G-01, F-hr_transcript, D-036 and D-037.
- [dev_refinement] `stories/US-02.1-employee-enters-the-first-working-day.md` Does the questionnaire start empty, or does it show the first working day HR already agreed, for the employee to confirm or correct? HR says 'I ask them to confirm it', which suggests HR already has a date. The spec only says the employee 'enters' it. This decides whether HR provides a value that is shown at the start.
- [dev_refinement] `stories/US-07.3-determine-the-source-tax-outcome-for-employees-living-in.md` For Liechtenstein residents with more than 45 non-return days, the calculator gives the normal tariff code together with 'Unter Vorbehalt des Doppelbesteuerungsabkommens' (subject to the double taxation agreement) (F-zh_source_tax_calculator-ab4e1e, C1Y / Unter Vorbehalt…). The spec records only the normal tariff code and flags only the 'no liability' case. Should the 'subject to the double taxation agreement' note and the HR flag also go with the tariff code in this case?
- [dev_refinement] `stories/US-01.2-complete-home-address-for-posting-documents.md` The house number is required for every employee, but the notes say the sources do not cover addresses without one (rural addresses, building names, some foreign addresses). Can the employee submit without a house number, and if so how? As written, these employees cannot submit at all.
- [dev_refinement] `feature.md` Which home address should the employee give: the current one, or the one that applies from the first working day? A new hire who is moving from abroad to Switzerland, or the other way, gets a different source tax liability, canton, cross-border questions and tariff code depending on which address counts. The spec treats the home address country as the country of residence without saying for which date.
- [dev_refinement] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` Should the employee ever see the derived results (insurance start date, civil status as the fund will receive it, whether they are subject to source tax, the tariff code or the Liechtenstein result), for example before submitting or in the read-only view? Or are these recorded only for HR? The spec says 'recorded for HR' but never says what the employee sees.
- [dev_refinement] `feature.md` Liechtenstein residents who return daily, or expect at most 45 non-return days, get no tariff code. Yet they are asked the denomination, whether the spouse works, and all the children questions before the cross-border step, and none of those answers is used. Is that intended, given data minimisation (G-01)? Or should the cross-border questions come first for Liechtenstein residents so the tariff questions can be skipped, and should those answers be discarded on submission?
- [dev_refinement] `feature.md` Child result row 22, and AC-06.4.3 with it: a minor child of a non-married employee who does NOT live in the household (parental custody, alternating care, employee pays more) 'counts with H'. The calculator note F-zh_source_tax_calculator-96658b says a child counts with H only when it lives in the household. Which is right: H or counted without H (A)? The answer changes the tariff letter.
- [dev_refinement] `stories/US-04.2-ask-spouse-details-only-when-the-spouse-could-exempt-the.md` The spouse's or partner's country of residence is asked as a full country, but the only thing that decides anything is whether the spouse lives in Switzerland. Under data minimisation (G-01), should it be asked only as 'Does your spouse/partner live in Switzerland? yes/no'? OQ-nationality-wording covers only the spouse's nationality, not the spouse's residence.
- [dev_refinement] `stories/US-05.7-compute-and-record-the-source-tax-result-for-hr.md` For Liechtenstein residents with more than 45 non-return days, the calculator gives the normal tariff code together with 'Unter Vorbehalt des Doppelbesteuerungsabkommens' (F-zh_source_tax_calculator-ab4e1e, e.g. 'C1Y / Unter Vorbehalt…'). AC-05.7.3 records only 'the normal tariff code'. Should this reservation (and a flag for HR) also be recorded with the code?

## Run

Stages run: normalize/hr_followup, extract/hr_followup, judge_facts, knowledge.raw, feature.plan, sections/SEC-08-completion-and-submission, sections/SEC-01-identity-and-address, sections/SEC-07-living-abroad, sections/SEC-04-source-tax-liability, sections/SEC-05-tariff-basics, sections/SEC-06-children, feature.flow, judge_trace, dev_refinement, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator

LLM cost this run: $6.12

Tokens this run: 768,120 in 16 agent calls (32 input, 80,045 cache read, 593,002 cache write, 95,041 output)
