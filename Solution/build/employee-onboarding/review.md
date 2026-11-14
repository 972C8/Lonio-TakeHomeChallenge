# Review: employee-onboarding

**Verdict: NOT READY**

Not ready. All 58 examples pass, and item recall and precision are 1.0. Two open questions block release: OQ-01 (the Zurich source tax calculator was never analysed) and OQ-02 (what the pension fund's canton means). Some traceability is broken: FEAT-02 cites G-09 as confirmation, but G-09 is only the language rule, and AC-04.4.5 claims HR checked the rules, which no source supports. Several acceptance criteria describe passing data on to other parties, which G-04 puts out of scope. FEAT-04 contradicts itself on who decides source tax. Dev refinement left about 18 major questions. The biggest gaps are in FEAT-01, which comes from the Julia incident, and in FEAT-04. There are also 9 technical leaks. 14 inferred items or stories still need product owner confirmation.

## Reviewer findings

1. **OQ-01 blocking: the source tax tariff questions are undefined** – The source tax step for employees who are subject to it can't be specified. The calculator may also need data the spec rules out, such as nationality for employees living abroad, which conflicts with AC-02.2.2.  
   Evidence: OQ-01 (blocking); skipped_sources: zh_source_tax_calculator; dev_refinement already_flagged (AC-02.2.2, AC-04.1.2, AC-04.4.4).  
   Action: Either analyse the Zurich calculator now, or record a decision in decisions.yaml to release FEAT-04 as the liability decision only, with no tariff step yet. Re-check AC-02.2.2 against the result.
2. **OQ-02 blocking: the canton's meaning is unknown, but the interim answer is written as final** – The fund requires a canton for every registration. Cross-border employees (Konstanz, Liechtenstein) can't be registered, which contradicts the FEAT-03 goal 'never blocked by missing data'. AC-02.2.2, AC-02.2.3 and US-03.4 treat 'canton not asked abroad' as settled.  
   Evidence: OQ-02; trace_judge partial on item.residence_canton, story.US-02.2 and story.US-03.4; FEAT-03 dev_refinement major question on the 'never blocked' goal.  
   Action: Ask Pensionskasse Muster whether it means canton of residence or of work, and what to enter for people living abroad. Until then, record in decisions.yaml how incomplete registrations are handled, for example flagged to HR. Mark the affected ACs as interim.
3. **Broken traceability: citations that confirm nothing** – The notes for the address country used as country of residence say this is confirmed by G-09, but G-09 is only 'Questionnaire language: English'. AC-04.4.5 claims HR checked the rules against real cases, which no source supports. Both make inferred items look confirmed when they aren't.  
   Evidence: FEAT-02 Notes (G-09); fact_judge partial F-TR-040; trace_judge partial story.US-04.4 (AC-04.4.5).  
   Action: Remove the false G-09 reference and either record a real decision on 'residence = country of home address' or raise an open question. Drop AC-04.4.5 or turn it into a sign-off step under OQ-05 with a named owner.
4. **Acceptance criteria test passing data on, which G-04 puts out of scope** – Engineering can't build or test criteria about how data reaches other parties when that handover is explicitly out of scope.  
   Evidence: AC-01.1.3, AC-02.1.3, AC-02.2.2 ('source tax and HR receive…'), AC-03.1.3; tech_leak FEAT-02; dev_refinement FEAT-01 and FEAT-02.  
   Action: Reword these to say the data is collected once and marked as needed by HR, the fund or source tax. Add guidance that features must not specify how data is passed on.
5. **FEAT-04 contradicts itself: who decides source tax liability?** – AC-04.1.1, AC-04.2.1 and AC-04.3.1 say 'HR uses it to decide', while US-04.4 says Lonio decides automatically and that this decision controls which questions follow. The flow and the option for HR to override depend on which is true.  
   Evidence: dev_refinement FEAT-04 (major); tech_leak FEAT-04.  
   Action: Record in decisions.yaml whether Lonio decides automatically and whether HR can review or override it, especially for cases OQ-05 doesn't cover. Align the ACs with that decision.
6. **FEAT-01 is underspecified on the very incident it is meant to prevent** – Several things are open. Is the first working day the contract start or the first day actually worked? Is it prefilled from HR or typed in by the employee? What happens if the date changes after onboarding, as in Julia's case? Which dates are allowed (past dates, typos)? Each of these can produce a wrong insurance start date again.  
   Evidence: dev_refinement FEAT-01 (4 major); fact_judge partial F-TR-014, F-TR-018, F-TR-019.  
   Action: Ask HR to clarify, then record decisions on: the definition of first working day, the source of the date (prefilled or typed), whether HR or the employee can change it after onboarding with the insurance start date recalculated, and the limits on allowed dates.
7. **The data collected for the source tax rule is not settled** – Unclear whether to collect full nationality or only 'Swiss yes/no' (data minimisation, G-01). Dual nationals, pending or unusual permits, and registered partners have no defined handling. OQ-03 is not linked to FEAT-04.  
   Evidence: dev_refinement FEAT-04 (4 major); OQ-03, OQ-06; eval: source_tax stakeholder missing on nationality, permit_type, spouse_nationality, spouse_permit_type, spouse_residence_country.  
   Action: Record decisions on how much nationality detail to collect, on dual nationals counting as Swiss, on pending permits, and on treating only 'Married' as married until OQ-03 is answered. Link OQ-03 to FEAT-04 and add source_tax as a stakeholder on these items.
8. **No rule for changing earlier answers or for the address details** – If an employee changes their country or civil status, the spec doesn't say whether dependent answers are discarded (G-01) or whether the decision is recalculated. The address also has gaps: a house number is always required, extra parts (c/o, flat) are excluded, and weekly residents aren't handled. Some employees may be unable to finish the address step.  
   Evidence: dev_refinement FEAT-02 (major: house number, extra parts, residence definition, country change); FEAT-03 (major: dependent data); FEAT-04 (minor).  
   Action: Add a cross-cutting guidance rule: answers that no longer apply are discarded and the decisions are recalculated. Confirm with HR how house number and c/o lines are handled, and which address weekly residents should give.
9. **Technical decisions leak into the spec** – Several criteria prescribe UI and data-model choices instead of business needs: DD.MM.YYYY input and separate day, month and year fields, an 'employment details' step, blocking the step until it's complete, and internal field ids (address_country, residence_canton, subject_to_source_tax) used in prose.  
   Evidence: tech_leak findings on FEAT-01 (2), FEAT-02 (2), FEAT-03 (3), FEAT-04 (1) and open-questions.md (1).  
   Action: Rewrite these in business terms, for example 'all five parts are required' and 'country of home address'. Add guidance that input formats and step layout are design decisions.
10. **Canton handling and the fund's open rules** – For Swiss residents the canton could be derived from the postcode, and guidance prefers deriving values over asking. The AC-03.3.1 examples mark Divorced and Widowed as 'not asked ✅' even though OQ-04 is still open. F-SC-020 (unknown error behaviour) is not used anywhere. F-SC-019 still describes the insurance start rule as open even though F-TR-018 settles it.  
   Evidence: dev_refinement FEAT-03 (major, canton derivation); OQ-04; coverage F-SC-019, F-SC-020.  
   Action: Decide whether to derive the canton or ask for it, and how to handle a canton that doesn't match the postcode. Ask HR for portal screenshots with Divorced and Widowed selected. Mark F-SC-019 as superseded by F-TR-018.

## Numbers

266 source units → 61 facts → 17 information items, 2 business rules → 4 features, 12 stories, 37 acceptance criteria; 8 open questions, 5 exclusions.

⚠ Sources without data (not explored / empty): zh_source_tax_calculator

## Errors (0)


## Examples executed against the knowledge model (58/58 pass)

- ✅ AC-01.1.1 / Julia (F-TR-019) (spec)
- ✅ AC-01.2.2 / Starts on the 1st of a month (spec)
- ✅ AC-01.2.2 / Starts on 1st January (spec)
- ✅ AC-01.2.3 / Julia (F-TR-019) (spec)
- ✅ AC-01.2.3 / Starts on the 2nd of a month (spec)
- ✅ AC-01.2.3 / Starts on the last day of a month (spec)
- ✅ AC-01.2.3 / Starts in December (year end) (spec)
- ✅ AC-01.2.4 / Julia moved her start to 15 March (F-TR-019) (spec)
- ✅ AC-02.1.1 / Employee living in Switzerland (spec)
- ✅ AC-02.1.1 / Employee living abroad (spec)
- ✅ AC-02.2.2 / Stefan, Swiss, lives in Konstanz (F-TR-034) (spec)
- ✅ AC-02.2.2 / Employee living in Liechtenstein (spec)
- ✅ AC-02.2.3 / Employee living in Winterthur (spec)
- ✅ AC-03.3.1 / Tomás, married, wife lives with him in Winterthur (F-TR-030) (spec)
- ✅ AC-03.3.1 / Single employee (spec)
- ✅ AC-03.3.1 / Divorced employee (spec)
- ✅ AC-03.3.1 / Widowed employee (spec)
- ✅ AC-03.4.1 / Tomás, lives in Winterthur (F-TR-030) (spec)
- ✅ AC-03.4.1 / Cross-border employee living in Germany (spec)
- ✅ AC-03.4.1 / Employee living in Liechtenstein (spec)
- ✅ AC-04.1.1 / Tomás (F-TR-030), lives in Winterthur (spec)
- ✅ AC-04.1.2 / Stefan (F-TR-034), Swiss, lives in Konstanz (spec)
- ✅ AC-04.1.2 / Employee living in Liechtenstein (spec)
- ✅ AC-04.2.1 / Tomás (F-TR-030), Brazilian living in Winterthur (spec)
- ✅ AC-04.2.1 / Maria (F-TR-025), Portuguese, assumed to live in Switzerland (spec)
- ✅ AC-04.2.2 / Swiss employee living in Switzerland (spec)
- ✅ AC-04.2.2 / Stefan (F-TR-034), lives in Konstanz (spec)
- ✅ AC-04.3.1 / Tomás (F-TR-030), Brazilian, B permit, married (spec)
- ✅ AC-04.3.1 / Single B permit holder in Switzerland (spec)
- ✅ AC-04.3.1 / Married C permit holder in Switzerland (spec)
- ✅ AC-04.3.1 / Married Swiss employee in Switzerland (spec)
- ✅ AC-04.3.1 / Married employee living abroad (spec)
- ✅ AC-04.3.2 / Tomás (F-TR-030), wife is Swiss (spec)
- ✅ AC-04.3.2 / B permit holder with an Italian spouse (spec)
- ✅ AC-04.3.3 / Tomás (F-TR-030), Swiss wife in Winterthur (spec)
- ✅ AC-04.3.3 / Spouse is Italian with a C permit (spec)
- ✅ AC-04.3.3 / Spouse is Italian with a B permit (spec)
- ✅ AC-04.4.1 / Stefan (F-TR-034), Swiss, lives in Konstanz (spec)
- ✅ AC-04.4.2 / Swiss employee living in Switzerland (spec)
- ✅ AC-04.4.2 / Maria (F-TR-025), Portuguese with a C permit, assumed to live in Switzerland (spec)
- ✅ AC-04.4.3 / Tomás (F-TR-030), Brazilian, B permit, Swiss wife in Winterthur (spec)
- ✅ AC-04.4.3 / Spouse is Italian with a C permit and lives in Switzerland (spec)
- ✅ AC-04.4.3 / Swiss spouse lives in Germany (spec)
- ✅ AC-04.4.3 / Spouse is Italian with a B permit (spec)
- ✅ AC-04.4.3 / Single B permit holder in Switzerland (spec)
- ✅ maria (profile: T: Maria in sales, Portuguese, C permit, no source tax)
- ✅ tomas (profile: T: Tomás, Brazilian, B permit, wife Swiss, live in Winterthur -> no source tax)
- ✅ stefan (profile: T: Stefan, Swiss, lives in Konstanz -> source tax regardless of passport)
- ✅ liechtenstein_resident (profile: T: woman in the warehouse who lives in Liechtenstein -> source tax)
- ✅ swiss_resident (profile: T: if you have a Swiss passport (and live here) you do not do source tax)
- ✅ b_permit_single (profile: T: all non-Swiss without C permit do source tax)
- ✅ b_permit_spouse_b_permit (profile: T: spouse exemption only for Swiss or C-permit spouses living here)
- ✅ b_permit_spouse_c_permit (profile: T: married to someone with a C permit who lives here -> no source tax)
- ✅ b_permit_swiss_spouse_abroad (profile: T: spouse exemption requires that the spouse lives here)
- ✅ julia (profile: T: Julia moved her first working day to 15 March -> insurance starts 1 April)
- ✅ starts_on_first (profile: T: unless somebody starts exactly on the first, then it's just that day)
- ✅ marco_married (profile: S: married -> Spouse's date of birth appears and is required (screens 05, 07))
- ✅ lena_single (profile: S: single -> no spouse field (screen 04))

## Open questions (need your decision)

- **OQ-01** (blocking): Which questions does the Zurich source tax calculator ask to set the tariff code, with which options and under which conditions (including the different questions for married employees, such as whether the spouse works, and the extra questions and German forms for employees living abroad)? → recommended: Analyse the calculator before specifying the source tax step; ask its questions only to employees subject to source tax.
- **OQ-02** (blocking): Does the pension fund's 'Canton' mean the canton of residence or of work, and what should be entered for employees living abroad, given that only Swiss cantons are offered? → recommended: Ask Pensionskasse Muster. Until then, ask the canton only of employees living in Switzerland.
- **OQ-03**: How should an employee in a registered partnership (or other status not in the list, e.g. separated) be registered with the pension fund, does the fund want the partner's details, and does a registered partnership count as married for the source tax spouse rule? → recommended: Ask Pensionskasse Muster; do not add values the fund does not accept.
- **OQ-04**: Does the pension fund portal show extra fields (e.g. spouse data) when civil status is Divorced or Widowed? → recommended: Ask HR for screenshots with Divorced and Widowed selected.
- **OQ-05**: Is the source tax rule complete? HR answered 'I think so' / 'I think that's it'. → recommended: Have HR confirm the decision table with a few real cases.
- **OQ-06**: Which permit types may the employee and spouse choose from? Sources mention only the B permit and the C permit. → recommended: Take the list from the Zurich calculator once analysed (OQ-01) or confirm with HR.
- **OQ-07**: Should the questionnaire remind employees to bring their permit, and with which wording? → recommended: Decide with HR; a reminder for non-Swiss employees living in Switzerland seems natural.
- **OQ-08**: The Zurich calculator is used for every employee subject to source tax, though HR knows this is not exactly correct. Should this be revisited? → recommended: Keep for now as agreed and per the assignment's simplification.

## Inferred items to confirm

- item.address_country
- item.nationality
- item.permit_type
- item.residence_canton
- item.spouse_nationality
- item.spouse_permit_type
- item.spouse_residence_country
- rule.subject_to_source_tax
- story.US-02.2
- story.US-03.4
- story.US-04.1
- story.US-04.2
- story.US-04.3
- story.US-04.4
- fact F-TR-005: Source tax questions should only be asked to employees who are subject to source tax, not to everybody.
- fact F-TR-018: Final rule: the insurance start date is derived from the first working day. If the first working day is the 1st of a month, insurance starts that day. Otherwise it starts on the 1st of the following month. The employee is not asked for it.
- fact F-TR-019: Incident: Julia moved her first working day to 15 March, HR did not update it, and the fund ended up with a wrong insurance start date (it should have been 1 April). This led to an unfriendly letter and took weeks to fix. It shows that the insurance start date must follow the latest confirmed first working day.
- fact F-TR-032: Spouse nationality, permit and residence are only needed for married employees whose own status would otherwise make them subject to source tax: non-Swiss, no C permit, living in Switzerland. The spouse permit is only needed if the spouse is not Swiss.
- fact F-TR-037: Consolidated final rule. (1) An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. (2) An employee living in Switzerland who is Swiss or holds a C permit is not subject. (3) An employee living in Switzerland who is non-Swiss without a C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. (4) Otherwise the employee is subject. The stakeholder hedged on completeness ('I think that's it').
- fact F-TR-038: The employee's nationality is needed to decide whether they are subject to source tax.
- fact F-TR-039: Non-Swiss employees' permit type (e.g. B permit, C permit) is needed to decide whether they are subject to source tax.
- fact F-TR-040: 'Lives here' in the source tax rules means living in Switzerland. The employee's country of residence can be taken from the country of the home address.
- fact F-SC-017: The Canton dropdown only lists Swiss cantons; it is unclear what to enter for an employee who lives abroad (e.g. a cross-border commuter living in Germany), and whether the field means the residence canton or the work canton.
- fact F-SC-018: No screenshot shows the form with civil status Divorced or Widowed, so it is unknown whether any extra fields (e.g. spouse data) appear for those values; the list also has no option such as registered partnership or separated, and it is unclear how such cases are to be registered.
- fact F-SC-019: The portal requires an insurance start date that is the 1st of a month, but does not say how it relates to the employee's first working day (e.g. whether a mid-month start rounds to the same or the next month's 1st); the derivation rule is open.
- fact F-SC-020: No screenshot shows the error for a badly formatted date or for an insurance start date that is not the 1st of a month, so the wording and behaviour of these errors are unknown.

## Dev refinement questions (36)

- [major] `features/FEAT-01-first-working-day-insurance-start.md` Does 'first working day' mean the contractual start date or the first day the employee actually works? E.g. a contract starting 01.01.2027 (a public holiday; the spec uses it as an example) where the person first works on 04.01.2027 gives 01.01.2027 under one reading and 01.02.2027 under the other. The same applies to a start on the 1st that falls on a weekend. Which date do we ask for, and how do we word the question?
- [major] `features/FEAT-01-first-working-day-insurance-start.md` 'Confirm' suggests the employee checks a date Lonio already has. Does Lonio get the contract start date from HR and show it for confirmation or correction, or does the employee type the date in from scratch? This changes the flow, and whether HR has to supply data first.
- [major] `features/FEAT-01-first-working-day-insurance-start.md` AC-01.2.4 / F-TR-019: what happens if the start date moves AFTER the employee has finished onboarding (Julia's case)? Can the employee (or HR) change the confirmed date later, and is the insurance start date then worked out again? Or does this feature only cover the date given during onboarding?
- [major] `features/FEAT-01-first-working-day-insurance-start.md` Which first working days are allowed? Can it be in the past (onboarding finished after the start), and how far in the future can it be? Should a weekend or public holiday be rejected or flagged? Without limits, a typo (wrong year) goes straight into a wrong insurance start date, which is exactly the incident this feature is meant to prevent.
- [minor] `features/FEAT-01-first-working-day-insurance-start.md` AC-01.1.3 talks about handing data on to HR and the pension fund, but G-04 / out-of-scope.md exclude transmission. What exactly do we build and test for AC-01.1.3? Does HR see the derived insurance start date, and where?
- [minor] `features/FEAT-01-first-working-day-insurance-start.md` Should the derived insurance start date be shown to the employee (e.g. as information on the summary), or only to HR? AC-01.2.1 only says the employee is not asked for it.
- [minor] `features/FEAT-01-first-working-day-insurance-start.md` AC-01.1.2 ('as currently agreed with Muster AG') cannot be checked by the system. Is it only guidance wording for the question (e.g. a hint that the date may have changed since the contract was signed)? If so, what should the text say?
- [minor] `features/FEAT-01-first-working-day-insurance-start.md` AC-01.1.1 says the question appears 'when they reach the employment details'. No such step is defined in the shared files. Where does this question go in the order of the questionnaire?
- [minor] `features/FEAT-01-first-working-day-insurance-start.md` Does the 1st-of-month rule apply to every employee, including re-hires, short or temporary contracts and people below the BVG thresholds? Or are some employees not registered with the fund at all, so no insurance start date is needed?
- [major] `features/FEAT-02-home-address.md` How is 'country of residence' meant to be defined? The Notes say using the address country as the country of residence is 'confirmed by the product owner convention (G-09)', but G-09 is only 'Questionnaire language: English', so nothing confirms the inference. Which address should the employee give if the address HR posts documents to is not where they legally live? Examples: a weekly resident in Switzerland (Wochenaufenthalter) whose home is abroad, an employee with a second home, or an employee who moves around the start date. The answer decides whether one address is enough or we need a residence question or a separate postal address.
- [major] `features/FEAT-02-home-address.md` Is the house number really required for everyone? The spec says it is 'Always' required, but its own note says 'whether every address has a house number is not discussed'. Some rural or foreign addresses have no number, or use a building name. Should those employees be able to finish the step, for example by leaving the number empty or confirming 'no number'?
- [major] `features/FEAT-02-home-address.md` 'No extra parts' (AC-02.1.2) rules out things like a c/o line, an apartment or flat number, or a second address line. Is that intended even when the post needs them to deliver (e.g. a new employee living c/o someone, or a large building abroad)? Or did HR only mean 'nothing beyond a normal envelope address'? This decides exactly which parts we collect.
- [major] `features/FEAT-02-home-address.md` AC-02.1.3 ('HR receives the complete home address' when 'the onboarding data is made available to the receiving parties') and AC-02.2.2 ('source tax and HR receive the country of residence') describe passing data on to other parties. out-of-scope.md (G-04) says that is a separate topic. What should these criteria be tested against in this feature? Should they be reworded to 'the information is collected and marked as needed by HR / source tax'?
- [major] `features/FEAT-02-home-address.md` What should happen if the employee goes back and changes the country after later steps were answered (e.g. Switzerland → Germany, or the reverse)? Should answers that no longer apply (nationality, canton, permit, spouse data) be discarded, which data minimisation (G-01) suggests? And should questions that now apply be asked again?
- [minor] `features/FEAT-02-home-address.md` Which countries can the employee choose: any country in the world, or a limited list (e.g. Switzerland and neighbouring countries)? The examples confirm that Liechtenstein counts as 'abroad'. Is that confirmed by HR or the source tax office, given how closely Liechtenstein is tied to Switzerland?
- [minor] `features/FEAT-02-home-address.md` Should address parts be checked for plausibility for the chosen country (e.g. a Swiss postcode must exist and match the town)? Or is any non-empty entry accepted? HR's need is mail that arrives, so wrong postcodes matter to them.
- [minor] `features/FEAT-02-home-address.md` Does HR or the employer already know the employee's address before onboarding, so it could be pre-filled for the employee to confirm, or must the employee always type it in?
- [minor] `features/FEAT-02-home-address.md` AC-02.2.4 only says the address step comes before the pension and source tax steps. Does it have to come at a particular place relative to FEAT-01 (first working day) or other steps, or is anything acceptable as long as it comes before the dependent steps?
- [major] `features/FEAT-03-pension-fund-registration-data.md` The goal says a registration is "never blocked by missing data", but the fund requires a canton for every employee and US-03.4 skips the canton for anyone living abroad (Germany, Liechtenstein). Until OQ-02 is answered, these registrations will be blocked. For now, should Lonio still let these employees complete the questionnaire, or should the case be marked as incomplete or flagged to HR? Or do we accept that the goal is not met for them yet? This is separate from OQ-02 itself, which asks what the canton means.
- [major] `features/FEAT-03-pension-fund-registration-data.md` For employees living in Switzerland, the canton follows from the Swiss postcode and town they already give in FEAT-02. Guidance prefers deriving values over asking for them. Should the canton be derived from the address instead of asked? If it is still asked, what happens when the chosen canton does not match the postcode? Should it be checked, or accepted as entered?
- [major] `features/FEAT-03-pension-fund-registration-data.md` Suppose an employee answers a dependent question and then changes the answer it depends on: civil status from Married to something else, or country from Switzerland to abroad. Should the spouse's date of birth or canton they already gave be discarded? Data minimisation (G-01) suggests yes, but the spec does not say.
- [minor] `features/FEAT-03-pension-fund-registration-data.md` Which names should the employee enter: the official names exactly as on their passport or ID, including all first names and middle names, or the name they use day to day? The fund's registration and later matching may depend on this, and it changes the question wording and help text.
- [minor] `features/FEAT-03-pension-fund-registration-data.md` Are there plausibility rules for the employee's date of birth and the spouse's date of birth? For example: not in the future, a minimum or maximum age for the employee, the spouse being an adult. Today the only rules are "not empty" and "a valid date", so a mistyped year would reach the fund.
- [minor] `features/FEAT-03-pension-fund-registration-data.md` AC-03.1.3 ("another part of the onboarding or another receiving party needs the same detail … not asked again") cannot be tested as written. Which other features or parties reuse name and date of birth? The information catalogue lists only the pension fund. What should the test check?
- [minor] `features/FEAT-03-pension-fund-registration-data.md` The title of AC-03.2.3 says civil status is reused "for source tax and HR", but its Then clause covers only source tax. Is there an HR reuse that needs its own acceptance criterion? If not, should "HR" be removed from the title?
- [minor] `features/FEAT-03-pension-fund-registration-data.md` Where in the questionnaire flow does the canton question go? FEAT-02 (AC-02.2.3) says employees living in Switzerland "continue to nationality and canton" straight after the address. FEAT-03 groups name and date of birth under "personal details" and civil status under "family details" but does not place the canton. Is there a required order across FEAT-02, FEAT-03 and FEAT-04?
- [major] `features/FEAT-04-source-tax-liability.md` Who makes the source tax decision: Lonio automatically, or HR? AC-04.1.1, AC-04.2.1 and AC-04.3.1 say 'HR uses it to decide', but US-04.4 and AC-04.4.1–4 say Lonio decides and that this gates the tariff questions straight away. If Lonio decides, can HR review or override it (for example in a case the rule does not cover, OQ-05) before the employee gets or skips the source tax step?
- [major] `features/FEAT-04-source-tax-liability.md` Does the spouse rule apply to anyone other than civil status 'Married'? Registered partners (e.g. Daniel), separated spouses and anyone else outside the pension fund's 4 values would currently go straight to 'subject'. OQ-03 raises this for source tax but is not linked to this feature. Should FEAT-04 wait for it, or ship treating only 'Married' as married?
- [major] `features/FEAT-04-source-tax-liability.md` The rule only needs to know whether someone is Swiss, holds a C permit or lives in Switzerland. Should Lonio ask for the full nationality (employee and spouse) and the spouse's full country of residence, or only 'Swiss yes/no' and 'lives in Switzerland yes/no'? The 'What?' rows say '(whether they hold a Swiss passport)' / '(whether they live in Switzerland)', but the ACs say 'asks for the nationality' and 'asks where the spouse lives'. Under data minimisation (G-01) the answer changes what we collect. Does HR need the actual nationality for anything else?
- [major] `features/FEAT-04-source-tax-liability.md` How should dual nationals be handled? Is someone who holds Swiss and another nationality treated as Swiss, both for the employee and for the spouse? This decides whether one nationality answer is enough or several are allowed.
- [major] `features/FEAT-04-source-tax-liability.md` Permit type is required for every non-Swiss employee living in Switzerland. What should an employee answer if their permit is still being applied for or has not been issued yet, or if they hold something that is not a residence permit (e.g. a short-term or asylum status)? Can they finish the questionnaire, and what does the rule decide for them? This goes beyond OQ-06, which only covers the list of permit types.
- [minor] `features/FEAT-04-source-tax-liability.md` 'Lives in Switzerland' comes only from the country of the home address. What about weekly residents and others with two homes, e.g. a Swiss address during the week and a family home abroad? Which address should the employee give, and does HR accept that the rule follows it?
- [minor] `features/FEAT-04-source-tax-liability.md` If the employee changes an earlier answer (address country, nationality, permit, civil status, spouse details) after the follow-up questions were answered, should the answers that are no longer needed be discarded (data minimisation), and should the source tax decision and the source tax step be recalculated? What happens to tariff answers already given if the employee turns out not to be subject?
- [minor] `features/FEAT-04-source-tax-liability.md` Should the employee see the outcome (e.g. 'you are / are not subject to source tax'), or is it only stored for HR and the source tax step? No AC says who sees the decision or where.
- [minor] `features/FEAT-04-source-tax-liability.md` AC-04.4.5 is a release precondition ('HR has checked the rules against real cases'), not behaviour we can test in the product, and its own trace check says the sources do not support it. Who signs this off, and is it a release gate for this feature or just part of resolving OQ-05?
- [minor] `features/FEAT-04-source-tax-liability.md` Can a spouse who holds a C permit be living abroad (a C permit usually lapses after a long stay abroad)? If not, can we skip the residence question for C-permit spouses? Should the residence question be asked even when the spouse obviously lives with the employee?

## Technical decisions leaking into the spec (9)

- `features/FEAT-01-first-working-day-insurance-start.md` "they give the start date as currently agreed with Muster AG, as a full date in the form DD.MM.YYYY" - Sets the input format the employee must type. G-10 covers business wording for values in examples. The fund's DD.MM.YYYY requirement (F-SC-009) applies to the insurance start date sent to the fund, not to how the employee enters the first working day. How the date is entered (date picker, locale format) is a UI decision for engineering.
- `features/FEAT-01-first-working-day-insurance-start.md` "When they reach the employment details" - Assumes a questionnaire step called 'employment details' that no source asks for. How the questions are split into steps is a design choice.
- `features/FEAT-02-home-address.md` "When the onboarding data is made available to the receiving parties … Then HR receives the complete home address" - This describes how and when the system hands data over to recipients. Nobody asked for that behaviour here, and G-04 puts transmission out of scope. The business need is only that the address is collected once and is available for HR.
- `features/FEAT-02-home-address.md` "and cannot complete the step while any of these five parts is empty" - This prescribes how the form behaves (blocking the step). The business requirement is only that all five parts are required. How completeness is enforced (blocking, warning, review before submitting) is a design decision.
- `features/FEAT-03-pension-fund-registration-data.md` "It depends on address_country from FEAT-02." - Uses an internal field id in business prose. The business term is "country of home address".
- `features/FEAT-03-pension-fund-registration-data.md` "naming the item residence_canton is an unbacked assumption" - Refers to an internal field or data-model name in the body text. What to call the field is an engineering decision.
- `features/FEAT-03-pension-fund-registration-data.md` "they are asked for their date of birth as a day, month and year (shown as DD.MM.YYYY, e.g. 14.02.1990)" - The fund's DD.MM.YYYY format is a constraint on the data delivered to the fund. Telling the questionnaire to ask for day, month and year as separate parts and to display them that way is an input and UI decision that belongs to engineering and design.
- `open-questions.md` "Analyse the Zurich calculator and add its questions, asked only when subject_to_source_tax is true" - Uses an internal field id and a boolean value in prose. The business statement is 'asked only of employees subject to source tax'.
- `features/FEAT-04-source-tax-liability.md` "Lonio asks for the employee's nationality, the employee must answer it, and HR uses it to decide" - Says how the decision is made (a question that HR then uses) instead of what outcome is needed. It also conflicts with US-04.4, where Lonio itself decides. This is a borderline case: how the decision is handled internally should be left to the design.

## Eval against gold set

```
item_recall: 1.0
item_precision: 1.0
stakeholder_recall: 0.74
rules_found: 2/2
exclusions_found: 2/2
open_questions_found: 2/2
stories_found: 2/2
items_not_in_gold: []
```

## Coverage

91/266 source units cited; 51/61 facts used.

Uncited units (confirm they are irrelevant):

- T-000: HR meeting transcript Everyone and everything here is fictional. Anna is the HR manager at Muster AG. Leo works in product at Lonio.
- T-001: Can you hear me okay? You're a bit quiet.
- T-002: Is this better? I'm in the small meeting room, the big one is taken. Sorry, let me just close the door.
- T-003: Much better. So, thanks for making the time. The idea today is simple. We want your new employees to give us everything once, so that you stop chasing them for 
- T-004: Yes, please. Right now it's a mess. I have a Word document, then an Excel file, and then I type everything into the portals by hand. Last month I spent a full a
- T-005: Okay. And how many people do you hire in a year?
- T-006: Around twenty. More in summer. We're about a hundred and fifty people now, mostly here in Zurich.
- T-007: Good. Let's start with the biggest pain. What takes you the most time?
- T-009: So who actually needs to answer them?
- T-011: Okay, that's clear. And the questionnaire itself is what?
- T-015: Anything else on the address?
- T-017: Great. Do you also want a photo? Some customers ask for one.
- T-019: It could. Do you want that from day one?
- T-022: We're with Pensionskasse Muster. They have a portal, it's quite old. I'll send you some screenshots of it after this call, that's easier than me explaining it.
- T-023: Perfect. What do you need for the fund that you don't have?
- T-025: It moves?
- T-027: Ouch.
- T-029: Sorry, one second, someone's at my door. [pause] Okay, I'm back, sorry. Where were we?
- T-030: The Julia story. It doesn't matter.
- T-031: Right. What else about the employee affects the fund? Are they married, things like that?
- T-033: And what are the options in that list?
- T-035: How did you enter him?
- T-037: Okay. Noted. Can I go back to source tax? You said all non-Swiss employees.
- T-041: Sure, send it if it's easy. Do people need anything from you on the first day? Laptops, things like that? I just want to see if that belongs in the same form.
- T-047: Okay. Anything else on who needs to do it? I'd rather hear all of it now.
- T-052: Only the timing. When can we have this?
- T-053: I'll come back to you on that this week, once we've gone through your screenshots.
- T-054: Good. I'll send them after lunch. Thanks, Leo.
- T-055: Thanks, Anna. Talk soon.
- S01-E01: Pensionskasse Muster
- S01-E02: Employer portal
- S01-E03: Muster AG
- S01-E04: Log out
- S01-E05: Home
- S01-E06: Insured persons
- S01-E07: Register new employee
- S01-E08: Register new employee
- S01-E15: Please select
- S01-E20: Please select
- S01-E21: Cancel
- S01-E22: Register
- S02-E01: Pensionskasse Muster
- S02-E02: Employer portal
- S02-E03: Muster AG
- S02-E04: Log out
- S02-E05: Home
- S02-E06: Insured persons
- S02-E07: Register new employee
- S02-E08: Register new employee
- S02-E09: Employee
- S02-E10: First name
- S02-E11: Last name
- S02-E12: Date of birth
- S02-E13: DD.MM.YYYY
- S02-E15: Please select
- S02-E42: Insurance
- S02-E43: Insurance start date
- S02-E44: Civil status
- S02-E45: Cancel
- S02-E46: Register
- S02-E47: Fields marked * are required.
- S03-E01: Pensionskasse Muster
- S03-E02: Employer portal · Muster AG · Log out
- S03-E03: Home > Insured persons > Register new employee
- S03-E04: Register new employee
- S03-E05: Employee
- S03-E06: First name
- S03-E07: Lena
- S03-E08: Last name
- S03-E09: Keller
- S03-E10: Date of birth
- S03-E11: 14.02.1991
- S03-E12: DD.MM.YYYY
- S03-E13: Canton
- S03-E14: Zurich
- S03-E15: Insurance
- S03-E16: Insurance start date
- S03-E17: 01.05.2026
- S03-E18: DD.MM.YYYY. Must be the 1st of a month.
- S03-E20: Please select
- S03-E25: Cancel
- S03-E26: Register
- S03-E27: Fields marked * are required.
- S04-E01: Pensionskasse Muster
- S04-E02: Employer portal · Muster AG · Log out
- S04-E03: Home > Insured persons > Register new employee
- S04-E04: Register new employee
- S04-E05: Employee
- S04-E06: First name
- S04-E07: Lena
- S04-E08: Last name
- S04-E09: Keller
- S04-E10: Date of birth
- S04-E11: 14.02.1991
- S04-E12: DD.MM.YYYY
- S04-E13: Canton
- S04-E14: Zurich
- S04-E15: Insurance
- S04-E16: Insurance start date
- S04-E17: 01.05.2026
- S04-E18: DD.MM.YYYY. Must be the 1st of a month.
- S04-E19: Civil status
- S04-E21: Cancel
- S04-E22: Register
- S04-E23: Fields marked * are required.
- S05-E01: Pensionskasse Muster
- S05-E02: Employer portal · Muster AG · Log out
- S05-E03: Home > Insured persons > Register new employee
- S05-E04: Register new employee
- S05-E05: Employee
- S05-E06: First name
- S05-E07: Marco
- S05-E08: Last name
- S05-E09: Rossi
- S05-E10: Date of birth
- S05-E11: 03.09.1985
- S05-E12: DD.MM.YYYY
- S05-E13: Canton
- S05-E14: Bern
- S05-E15: Insurance
- S05-E16: Insurance start date
- S05-E17: 01.06.2026
- S05-E18: DD.MM.YYYY. Must be the 1st of a month.
- S05-E19: Civil status
- S05-E22: 22.11.1987
- S05-E24: Cancel
- S05-E25: Register
- S05-E26: Fields marked * are required.
- S06-E01: Pensionskasse Muster
- S06-E02: Employer portal · Muster AG · Log out
- S06-E03: Home > Insured persons > Register new employee
- S06-E04: Register new employee
- S06-E06: Employee
- S06-E07: First name
- S06-E08: 
- S06-E10: Last name
- S06-E11: 
- S06-E13: Date of birth
- S06-E14: 
- S06-E15: DD.MM.YYYY
- S06-E17: Canton
- S06-E18: Please select
- S06-E20: Insurance
- S06-E21: Insurance start date
- S06-E22: 
- S06-E23: DD.MM.YYYY. Must be the 1st of a month.
- S06-E25: Civil status
- S06-E26: Please select
- S06-E28: Cancel
- S06-E29: Register
- S06-E30: Fields marked * are required.
- S07-E01: Pensionskasse Muster
- S07-E02: Employer portal · Muster AG · Log out
- S07-E03: Home > Insured persons > Register new employee
- S07-E04: Register new employee
- S07-E05: Employee
- S07-E06: First name
- S07-E07: Marco
- S07-E08: Last name
- S07-E09: Rossi
- S07-E10: Date of birth
- S07-E11: 03.09.1985
- S07-E12: DD.MM.YYYY
- S07-E13: Canton
- S07-E14: Bern
- S07-E15: Insurance
- S07-E16: Insurance start date
- S07-E17: 01.06.2026
- S07-E18: DD.MM.YYYY. Must be the 1st of a month.
- S07-E19: Civil status
- S07-E22: 
- S07-E23: DD.MM.YYYY
- S07-E25: Cancel
- S07-E26: Register
- S07-E27: Fields marked * are required.

## Other warnings (39)

- [fact_judge] `F-TR-001` partial: Goal is stated by Leo (interviewer), and Anna's 'Yes, please' responds to a different question; her explicit agreement to the goal is not clearly shown. | The goal is for new employees to give their information once, so that HR stops chasing them for the same information several times. The stakeholder agreed to this goal.
- [fact_judge] `F-TR-002` partial: Word, Excel, manual typing into 'the portals' and the afternoon for two hires are supported, but 'receiving parties' portals' is an embellishment. | Today HR uses a Word document and an Excel file, then types everything into the receiving parties' portals by hand. Last month this took a full afternoon for two new hires.
- [fact_judge] `F-TR-008` partial: She uses Zurich for everybody, not only those subject to source tax (though only they would use it); interviewer 'keep that for now' is supported. | For now, the Zurich calculator is used for every employee subject to source tax. The stakeholder knows this is not exactly how it works, and the interviewer agreed to keep it this way.
- [fact_judge] `F-TR-014` partial: First working day and confirmation are supported, but it is said to be the number one thing generally, and 'for the pension fund' is reasonable given context; 'changes often' is supported. | HR needs the employee's first working day for the pension fund. It is the most important item, and HR asks the employee to confirm it because it changes often.
- [fact_judge] `F-TR-018` partial: The derivation rule is supported, but 'the employee is not asked for it' is not stated in these units. | Final rule: the insurance start date is derived from the first working day. If the first working day is the 1st of a month, insurance starts that day. Otherwise it starts on the 1st of the following month. The employee is not asked for it.
- [fact_judge] `F-TR-019` partial: The incident is supported, but 'it should have been 1 April' is fine while the 'must follow the latest confirmed first working day' conclusion is an inference; the units also say 'I had entered something else', not specifically that HR failed to update the insurance date, though she did say she didn't update it. | Incident: Julia moved her first working day to 15 March, HR did not update it, and the fund ended up with a wrong insurance start date (it should have been 1 April). This led to an unfriendly letter and took weeks to fix. It shows that the insurance start date must follow the latest confirmed first working day.
- [fact_judge] `F-TR-032` partial: Scoping to otherwise-subject employees and the 'permit only if spouse not Swiss' detail are reasonable readings but not stated. | Spouse nationality, permit and residence are only needed for married employees whose own status would otherwise make them subject to source tax: non-Swiss, no C permit, living in Switzerland. The spouse permit is only needed if the spouse is not Swiss.
- [fact_judge] `F-TR-040` partial: 'Lives here' = Switzerland is supported, but nothing in these units links residence to the home address country. | 'Lives here' in the source tax rules means living in Switzerland. The employee's country of residence can be taken from the country of the home address.
- [fact_judge] `F-SC-001` partial: Page and portal are shown, but 'employer Muster AG' and 'insured employees' are not stated explicitly. | The source is the 'Register new employee' page of the Pensionskasse Muster employer portal, used by the employer Muster AG to register new insured employees.
- [fact_judge] `F-SC-014` partial: Absence in screenshots 01, 02, 03, 06 and 04 is not shown by the units given (only 04 label list lacks it); conditional-only-on-Married is a reasonable inference but the empty-form claims are unverified. | The 'Spouse's date of birth' field appears only when civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in the empty forms (01, 02, 03, 06).
- [fact_judge] `F-SC-020` partial: The units show only a hint (DD.MM.YYYY, must be 1st of month) and a required error, with no format or non-1st-date error visible, but the claim that no screenshot shows them goes beyond these units, which cover only one screenshot. | No screenshot shows the error for a badly formatted date or for an insurance start date that is not the 1st of a month, so the wording and behaviour of these errors are unknown.
- [coverage] `F-SC-019` fact not used anywhere in the spec: The portal requires an insurance start date that is the 1st of a month, but does not say how it relates to the employee's first working day (e.g. whether a mid-month start rounds to the same or the next month's 1st); the derivation rule is open.
- [coverage] `F-SC-020` fact not used anywhere in the spec: No screenshot shows the error for a badly formatted date or for an insurance start date that is not the 1st of a month, so the wording and behaviour of these errors are unknown.
- [eval] `nationality` missing stakeholder source_tax
- [eval] `permit_type` missing stakeholder source_tax
- [eval] `spouse_nationality` missing stakeholder source_tax
- [eval] `spouse_permit_type` missing stakeholder source_tax
- [eval] `spouse_residence_country` missing stakeholder source_tax
- [trace_judge] `item.residence_canton` partial: The restriction to asking only residents of Switzerland is not backed: the fund marks Canton required for everyone, and F-SC-017 says what applies to people living abroad (and residence versus work canton) is unclear.
- [trace_judge] `story.US-02.2` partial: The cited facts never mention a pension fund canton question or say it is skipped for residents abroad and asked for residents in Switzerland (AC-02.2.2, AC-02.2.3), and the claim that source tax and HR receive the country of residence is not backed either.
- [trace_judge] `story.US-03.4` partial: The cited facts leave open whether the canton means residence or work and what applies to people abroad (F-SC-006, F-SC-017), so asking only Swiss-resident employees and naming the item residence_canton is an unbacked assumption.
- [trace_judge] `story.US-04.4` partial: AC-04.4.5 states that HR has checked the rules against Stefan, Maria and Tomás and that gaps go through OQ-05, but the facts only show HR hedging ('I think that's it') and say nothing about such a check or that handling; the other criteria are backed by F-TR-005/025/030/034/037/040.
- [dev_refinement] `features/FEAT-01-first-working-day-insurance-start.md` Does 'first working day' mean the contractual start date or the first day the employee actually works? E.g. a contract starting 01.01.2027 (a public holiday; the spec uses it as an example) where the person first works on 04.01.2027 gives 01.01.2027 under one reading and 01.02.2027 under the other. The same applies to a start on the 1st that falls on a weekend. Which date do we ask for, and how do we word the question?
- [dev_refinement] `features/FEAT-01-first-working-day-insurance-start.md` 'Confirm' suggests the employee checks a date Lonio already has. Does Lonio get the contract start date from HR and show it for confirmation or correction, or does the employee type the date in from scratch? This changes the flow, and whether HR has to supply data first.
- [dev_refinement] `features/FEAT-01-first-working-day-insurance-start.md` AC-01.2.4 / F-TR-019: what happens if the start date moves AFTER the employee has finished onboarding (Julia's case)? Can the employee (or HR) change the confirmed date later, and is the insurance start date then worked out again? Or does this feature only cover the date given during onboarding?
- [dev_refinement] `features/FEAT-01-first-working-day-insurance-start.md` Which first working days are allowed? Can it be in the past (onboarding finished after the start), and how far in the future can it be? Should a weekend or public holiday be rejected or flagged? Without limits, a typo (wrong year) goes straight into a wrong insurance start date, which is exactly the incident this feature is meant to prevent.
- [dev_refinement] `features/FEAT-02-home-address.md` How is 'country of residence' meant to be defined? The Notes say using the address country as the country of residence is 'confirmed by the product owner convention (G-09)', but G-09 is only 'Questionnaire language: English', so nothing confirms the inference. Which address should the employee give if the address HR posts documents to is not where they legally live? Examples: a weekly resident in Switzerland (Wochenaufenthalter) whose home is abroad, an employee with a second home, or an employee who moves around the start date. The answer decides whether one address is enough or we need a residence question or a separate postal address.
- [dev_refinement] `features/FEAT-02-home-address.md` Is the house number really required for everyone? The spec says it is 'Always' required, but its own note says 'whether every address has a house number is not discussed'. Some rural or foreign addresses have no number, or use a building name. Should those employees be able to finish the step, for example by leaving the number empty or confirming 'no number'?
- [dev_refinement] `features/FEAT-02-home-address.md` 'No extra parts' (AC-02.1.2) rules out things like a c/o line, an apartment or flat number, or a second address line. Is that intended even when the post needs them to deliver (e.g. a new employee living c/o someone, or a large building abroad)? Or did HR only mean 'nothing beyond a normal envelope address'? This decides exactly which parts we collect.
- [dev_refinement] `features/FEAT-02-home-address.md` AC-02.1.3 ('HR receives the complete home address' when 'the onboarding data is made available to the receiving parties') and AC-02.2.2 ('source tax and HR receive the country of residence') describe passing data on to other parties. out-of-scope.md (G-04) says that is a separate topic. What should these criteria be tested against in this feature? Should they be reworded to 'the information is collected and marked as needed by HR / source tax'?
- [dev_refinement] `features/FEAT-02-home-address.md` What should happen if the employee goes back and changes the country after later steps were answered (e.g. Switzerland → Germany, or the reverse)? Should answers that no longer apply (nationality, canton, permit, spouse data) be discarded, which data minimisation (G-01) suggests? And should questions that now apply be asked again?
- [dev_refinement] `features/FEAT-03-pension-fund-registration-data.md` The goal says a registration is "never blocked by missing data", but the fund requires a canton for every employee and US-03.4 skips the canton for anyone living abroad (Germany, Liechtenstein). Until OQ-02 is answered, these registrations will be blocked. For now, should Lonio still let these employees complete the questionnaire, or should the case be marked as incomplete or flagged to HR? Or do we accept that the goal is not met for them yet? This is separate from OQ-02 itself, which asks what the canton means.
- [dev_refinement] `features/FEAT-03-pension-fund-registration-data.md` For employees living in Switzerland, the canton follows from the Swiss postcode and town they already give in FEAT-02. Guidance prefers deriving values over asking for them. Should the canton be derived from the address instead of asked? If it is still asked, what happens when the chosen canton does not match the postcode? Should it be checked, or accepted as entered?
- [dev_refinement] `features/FEAT-03-pension-fund-registration-data.md` Suppose an employee answers a dependent question and then changes the answer it depends on: civil status from Married to something else, or country from Switzerland to abroad. Should the spouse's date of birth or canton they already gave be discarded? Data minimisation (G-01) suggests yes, but the spec does not say.
- [dev_refinement] `features/FEAT-04-source-tax-liability.md` Who makes the source tax decision: Lonio automatically, or HR? AC-04.1.1, AC-04.2.1 and AC-04.3.1 say 'HR uses it to decide', but US-04.4 and AC-04.4.1–4 say Lonio decides and that this gates the tariff questions straight away. If Lonio decides, can HR review or override it (for example in a case the rule does not cover, OQ-05) before the employee gets or skips the source tax step?
- [dev_refinement] `features/FEAT-04-source-tax-liability.md` Does the spouse rule apply to anyone other than civil status 'Married'? Registered partners (e.g. Daniel), separated spouses and anyone else outside the pension fund's 4 values would currently go straight to 'subject'. OQ-03 raises this for source tax but is not linked to this feature. Should FEAT-04 wait for it, or ship treating only 'Married' as married?
- [dev_refinement] `features/FEAT-04-source-tax-liability.md` The rule only needs to know whether someone is Swiss, holds a C permit or lives in Switzerland. Should Lonio ask for the full nationality (employee and spouse) and the spouse's full country of residence, or only 'Swiss yes/no' and 'lives in Switzerland yes/no'? The 'What?' rows say '(whether they hold a Swiss passport)' / '(whether they live in Switzerland)', but the ACs say 'asks for the nationality' and 'asks where the spouse lives'. Under data minimisation (G-01) the answer changes what we collect. Does HR need the actual nationality for anything else?
- [dev_refinement] `features/FEAT-04-source-tax-liability.md` How should dual nationals be handled? Is someone who holds Swiss and another nationality treated as Swiss, both for the employee and for the spouse? This decides whether one nationality answer is enough or several are allowed.
- [dev_refinement] `features/FEAT-04-source-tax-liability.md` Permit type is required for every non-Swiss employee living in Switzerland. What should an employee answer if their permit is still being applied for or has not been issued yet, or if they hold something that is not a residence permit (e.g. a short-term or asylum status)? Can they finish the questionnaire, and what does the rule decide for them? This goes beyond OQ-06, which only covers the list of permit types.

## Run

Stages run: knowledge.raw, features.plan, features/FEAT-02-home-address, features/FEAT-01-first-working-day-insurance-start, features/FEAT-03-pension-fund-registration-data, features/FEAT-04-source-tax-liability, judge_trace, dev_refinement/FEAT-01-first-working-day-insurance-start, dev_refinement/FEAT-02-home-address, dev_refinement/FEAT-04-source-tax-liability, dev_refinement/FEAT-03-pension-fund-registration-data, review

Stages reused from cache: normalize/hr_transcript, extract/hr_transcript, normalize/pension_portal, extract/pension_portal, normalize/zh_source_tax_calculator, extract/zh_source_tax_calculator, judge_facts

LLM cost this run: $5.29
