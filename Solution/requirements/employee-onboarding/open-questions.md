# Open questions

Things the sources do not settle. Each needs a product decision
(`decisions.yaml`) or clarification with the stakeholder. Until then, builders
implement the **recommendation** and keep it easy to change.

## OQ-01 (blocking): Which questions does the Zurich source tax calculator ask to determine the tariff code (including the extra questions and German forms for residents abroad), with their options and conditions?

No facts were extracted from the calculator source. The source tax step currently holds only 'spouse works' (from the transcript). Without the calculator's questions, Lonio cannot collect enough to determine the tariff.

Options:
- Extract the calculator facts and extend the source_tax step
- Ship liability determination only; HR collects the tariff inputs manually

**Recommendation:** Extract the calculator's questions before building the source_tax step. The liability rule and the other steps can be built now.

Affects: `spouse_employed`, `source_tax`, `nationality`, `permit_type`, `subject_to_source_tax`
- **F-TR-039**: For employees living abroad the calculator asks more questions (Germany has its own forms); Anna cannot name them, and Leo defers to the calculator for the details. — "And with them the calculator gets much more complicated, there are more questions. Germany has its own forms, I can never remember what they're called." (T-050, Anna) — "Okay, that's fine, the calculator will tell us." (T-051, Leo)
- **F-TR-030**: For married employees subject to source tax, the Zurich calculator asks whether the spouse works. — "It changes the questions in the calculator, yes. Whether the husband or wife works." (T-044, Anna)
- **F-TR-007**: The Zurich source tax calculator (canton website, yields the tariff code) is used for every employee regardless of where they actually belong; Anna acknowledges this is not exactly correct but it is what they do for now, and Leo agrees to keep it. — "I use the Zurich calculator on the canton's website. The one that gives you the tariff code." (T-012, Anna) — "For everybody I use Zurich, by the way. I know it's not exactly how it works, but that's what we do for now." (T-012, Anna) — "Understood. We'll keep that for now." (T-013, Leo)

## OQ-03 (blocking): What should be entered in the pension portal's required 'Canton' field for employees living abroad, and does 'Canton' mean the residence canton or the work canton?

The dropdown lists only Swiss cantons, and the field is required. Cross-border employees exist (Konstanz, Liechtenstein). If it means the work canton, the employee should not be asked at all.

Options:
- Residence canton; ask only Swiss residents; ask the fund what to use for residents abroad
- Work canton; do not ask the employee; HR/employer supplies it (e.g. Zurich)
- Ask everyone abroad for a canton

**Recommendation:** Ask Pensionskasse Muster. Until then, ask only Swiss residents for their residence canton and flag registrations of residents abroad for HR.

Affects: `residence_canton`
- **F-SC-005**: The pension fund registration form has a required 'Canton' dropdown. — "Canton" (01-empty.png (S01-E14)) — "Please select" (01-empty.png (S01-E15))
- **F-SC-006**: The Canton dropdown offers exactly 26 Swiss cantons: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for living outside Switzerland. — "Canton" (02-canton-list.png (S02-E14)) — "Aargau" (02-canton-list.png (S02-E16)) — "Appenzell Ausserrhoden" (02-canton-list.png (S02-E17)) — "Appenzell Innerrhoden" (02-canton-list.png (S02-E18)) — "Basel-Landschaft" (02-canton-list.png (S02-E19)) — "Basel-Stadt" (02-canton-list.png (S02-E20)) — "Bern" (02-canton-list.png (S02-E21)) — "Fribourg" (02-canton-list.png (S02-E22)) — "Geneva" (02-canton-list.png (S02-E23)) — "Glarus" (02-canton-list.png (S02-E24)) — "Graubünden" (02-canton-list.png (S02-E25)) — "Jura" (02-canton-list.png (S02-E26)) — "Lucerne" (02-canton-list.png (S02-E27)) — "Neuchâtel" (02-canton-list.png (S02-E28)) — "Nidwalden" (02-canton-list.png (S02-E29)) — "Obwalden" (02-canton-list.png (S02-E30)) — "Schaffhausen" (02-canton-list.png (S02-E31)) — "Schwyz" (02-canton-list.png (S02-E32)) — "Solothurn" (02-canton-list.png (S02-E33)) — "St. Gallen" (02-canton-list.png (S02-E34)) — "Thurgau" (02-canton-list.png (S02-E35)) — "Ticino" (02-canton-list.png (S02-E36)) — "Uri" (02-canton-list.png (S02-E37)) — "Valais" (02-canton-list.png (S02-E38)) — "Vaud" (02-canton-list.png (S02-E39)) — "Zug" (02-canton-list.png (S02-E40)) — "Zurich" (02-canton-list.png (S02-E41))
- **F-SC-018**: The Canton dropdown lists only Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. cross-border commuter), and whether 'Canton' means residence canton or work canton. — "Canton" (02-canton-list.png (S02-E14)) — "Zurich" (02-canton-list.png (S02-E41))
- **F-TR-038**: Muster AG has a few employees living across the border (Germany, Liechtenstein). — "We have a few who live across the border. Stefan lives in Konstanz, and there's a woman in the warehouse who lives in Liechtenstein." (T-048, Anna)

## OQ-04: How should employees in a registered partnership (or with other statuses such as separated) be recorded, and does the fund want the partner's date of birth?

Such an employee exists (Daniel), but the portal offers only Single, Married, Divorced, Widowed. Adding an option the fund does not support would break the registration.

Options:
- Keep the four portal options; HR handles partnerships manually
- Add 'registered_partnership' and map it per the fund's answer; ask partner's date of birth if required
- Treat registered partnership as married

**Recommendation:** Keep the four portal options for now and ask the fund. Add a 'registered_partnership' option once its mapping and partner-data requirements are known.

Affects: `civil_status`, `spouse_date_of_birth`, `subject_to_source_tax`
- **F-TR-023**: At least one current employee (Daniel in finance) is in a registered partnership, so this civil status occurs in practice. — "we do have one colleague in a registered partnership. Daniel, in finance." (T-034, Anna)
- **F-TR-024**: Unknown how the pension fund's screen handles registered partnership and whether the fund wants the partner's details (e.g. date of birth) in that case. — "I honestly don't know what the fund's screen does in that case, or if they want the partner's details too." (T-036, Anna)
- **F-SC-019**: The Civil status list has no option for registered partnership, separated, or other statuses; it is open how employees with such statuses are registered and whether a partner's date of birth is then needed. — "Single" (03-civil-status-list.png (S03-E21)) — "Widowed" (03-civil-status-list.png (S03-E24))
- **F-SC-010**: The Civil status dropdown offers exactly four options: Single, Married, Divorced, Widowed. — "Civil status" (03-civil-status-list.png (S03-E19)) — "Single" (03-civil-status-list.png (S03-E21)) — "Married" (03-civil-status-list.png (S03-E22)) — "Divorced" (03-civil-status-list.png (S03-E23)) — "Widowed" (03-civil-status-list.png (S03-E24))

## OQ-02: Is the source tax liability rule complete? Anna ended with 'I think that's it'.

Any missing exemption or condition would wrongly show or hide the source tax questions.

Options:
- Confirm the rule as specified
- Add missing conditions

**Recommendation:** Confirm with HR and cross-check against the calculator.

Affects: `subject_to_source_tax`, `spouse_nationality`, `spouse_permit_type`, `spouse_residence_country`
- **F-TR-040**: Consolidated final rule (Anna hedged completeness with 'I think'): an employee is subject to source tax if residence_country is not CH (regardless of nationality). If living in CH: not subject if nationality is CH; not subject if permit_type is C; not subject if married to a spouse who is Swiss or holds a C permit and lives in CH; otherwise subject. — "If you don't have a Swiss passport, you do source tax." (T-010, Anna) — "So, not the people with a C permit. They're treated like Swiss people for this." (T-038, Anna) — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (T-044, Anna) — "Those people do source tax because they work here and they don't live here. And there it doesn't matter what passport you have, by the way." (T-048, Anna) — "I think that's it." (T-048, Anna)

## OQ-05: Is 'Spouse's date of birth' hidden in the portal for Divorced and Widowed?

No screenshot shows these states. The spec asks for the spouse's date of birth only when the employee is married.

Options:
- Only for Married (as specified)
- Also for divorced/widowed

**Recommendation:** Keep 'only married' (consistent with the transcript) and verify in the portal.

Affects: `spouse_date_of_birth`
- **F-SC-020**: No screenshot shows the form with Civil status 'Divorced' or 'Widowed'; whether Spouse's date of birth is hidden for those values is assumed but not proven. — "Divorced" (03-civil-status-list.png (S03-E23)) — "Widowed" (03-civil-status-list.png (S03-E24))
- **F-SC-013**: 'Spouse's date of birth' appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in 01, 02, 03, 06 (civil status not selected). — "Married" (05-married.png (S05-E20)) — "Spouse's date of birth" (05-married.png (S05-E21)) — "Married" (07-married-missing-spouse.png (S07-E20)) — "Spouse's date of birth" (07-married-missing-spouse.png (S07-E21)) — "Single" (04-single.png (S04-E20))
- **F-TR-021**: If the employee is married, the pension fund wants the spouse's date of birth. — "And if someone is married, they want the date of birth of the husband or wife." (T-032, Anna)

## OQ-06: Which permit types must the permit fields offer?

The sources name only B and C. The calculator may need to distinguish other permits.

Options:
- B, C, other (as specified)
- The full permit list from the calculator

**Recommendation:** Keep B / C / other until the calculator facts are extracted.

Affects: `permit_type`, `spouse_permit_type`
- **F-TR-025**: Correction: non-Swiss employees holding a C permit are not subject to source tax; they are treated like Swiss people for this. — "No, that's actually not right." (T-038, Anna) — "So, not the people with a C permit. They're treated like Swiss people for this." (T-038, Anna) — "Okay, so non-Swiss, but not with a C permit." (T-039, Leo)
- **F-TR-031**: An employee married to a Swiss national or to a C permit holder who lives in Switzerland is not subject to source tax (e.g. Tomás: Brazilian, B permit, Swiss wife, living in Winterthur). — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (T-044, Anna) — "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." (T-044, Anna)
- **F-TR-034**: For married employees (source tax determination), the spouse's permit type is needed if the spouse has one. — "their permit if they have one" (T-046, Anna)
- **G-10**: Option values (stored values) for enums: permit types use the official letter as value ("B", "C", ...; a value "other" if needed); civil status uses lower-case snake_case of the label ("single", "married", "divorced", "widowed", ...). Labels are free.

## OQ-07: Is the postal address always the residence address, so that address_country can serve as the residence country?

Liability depends on the country of residence. A different mailing address would give the wrong result.

Options:
- Yes, one address (as specified)
- Ask for the residence country separately

**Recommendation:** Use one address. Anna described a normal home address.

Affects: `address_country`, `subject_to_source_tax`, `residence_canton`
- **F-TR-011**: Nothing beyond a normal postal address (as written on an envelope) is needed for the address. — "No, no. Just a normal address, the way you would write it on an envelope." (T-016, Anna)
- **F-TR-043**: The employee's country of residence is needed to determine source tax liability (living abroad means always subject). — "Those people do source tax because they work here and they don't live here." (T-048, Anna)

## OQ-08: What exact wording should the permit reminder use, and when should it be shown?

Anna deferred the wording.

Options:
- Use the drafted wording
- HR provides the wording

**Recommendation:** Use the draft and let HR review it.

Affects: `permit_reminder`
- **F-TR-029**: Anna would love the form to remind employees to bring their permit (on the first day), because half of them forget; wording to be looked at later, not decided. — "What I would love is if the form could remind people to bring their permit. Half of them forget." (T-042, Anna) — "We can look at the wording later." (T-043, Leo)

## OQ-09: Are there limits on dates (e.g. first working day not in the past, or a maximum distance in the future) and how does the portal word date errors?

The sources give only formats.

Options:
- Validate only as a calendar date (as specified)
- Add range limits

**Recommendation:** Validate as a calendar date only, until HR or the fund defines limits.

Affects: `first_working_day`, `date_of_birth`, `spouse_date_of_birth`
- **F-SC-022**: No screenshot shows the error for an invalid date format or an insurance start date that is not the 1st of a month; the wording and any other date constraints (e.g. past/future limits) are unknown. — "DD.MM.YYYY. Must be the 1st of a month." (06-required-errors.png (S06-E23))

