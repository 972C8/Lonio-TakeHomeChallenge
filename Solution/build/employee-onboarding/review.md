# Review: employee-onboarding

**Verdict: NOT READY**

Not ready. All 13 persona tests pass. Field and consumer recall are both 1.0, all 2 rules are found, and no errors were reported. Two open questions still block the build:
- **OQ-01:** what the Zurich source tax calculator asks. The calculator source was skipped, so step 6 is incomplete.
- **OQ-03:** what goes in the required 'Canton' field for people living abroad, and whether it means residence or work canton.

The naive builder also raised 6 major questions: an empty step 6, whether the first working day is pre-filled or just confirmed, editing after submission, overall form behaviour, the permit question for cross-border commuters, and whether to build step 6 at all. 12 of the 18 fields and the source tax rule are inferred and only partly backed by sources. Most of these can be settled by product owner decisions in decisions.yaml.

## Reviewer findings

1. **The source tax step (step 6) cannot be specified because the calculator source was never read** – Without the calculator's questions, Lonio cannot collect enough to work out the tax rate code. The package contradicts itself: OQ-01 says not to build step 6 yet, while flow.md fully specifies it with only spouse_employed.  
   Evidence: OQ-01 (blocking); skipped_sources: zh_source_tax_calculator; naive_builder major question on open-questions.md; fields_not_in_gold: spouse_employed  
   Action: Extract the calculator's questions now. Or record in decisions.yaml that release 1 only decides who is subject to source tax: drop step 6 and HR collects the rate inputs by hand.
2. **Step 6 is empty for unmarried people who are subject to source tax** – Single, divorced or widowed people who are subject to source tax, including every unmarried resident abroad, get a step with intro text and no questions. That is a visible UX defect.  
   Evidence: naive_builder major question on flow.md; personas stefan and liechtenstein_resident (subject_to_source_tax=true, civil_status not married)  
   Action: Decide whether to skip the empty step, show it as an information-only page, or add civil_status=='married' to the step condition until OQ-01 is resolved.
3. **Meaning of the required 'Canton' field is unresolved** – The pension portal requires a canton, but the list only has Swiss cantons. Cross-border employees (Konstanz, Liechtenstein) currently get no canton, so their registration cannot be completed in the portal.  
   Evidence: OQ-03 (blocking); F-SC-018; trace_judge partial on field.residence_canton (ask_when and option values not backed)  
   Action: Ask Pensionskasse Muster. Meanwhile, record the interim decision (residence canton, asked only of Swiss residents) and say concretely what the 'flag for HR' is: a stored flag or a marker in the HR output.
4. **Unclear whether the first working day is pre-filled or entered, and how it is confirmed** – This is the field Anna calls most important, and it drives insurance_start_date. Whether HR pre-fills it and whether an explicit confirmation is needed changes the data model and the UI.  
   Evidence: naive_builder major question on fields/first_working_day.md; fact_judge partial on F-TR-015  
   Action: Decide: HR pre-fills the date from the contract or the employee types it, and whether a confirmation checkbox is needed. Add the decision to decisions.yaml.
5. **No overall form behaviour or post-submit editing is specified** – The notice tells employees to 'update it here right away', which implies editing after submission. Going back to earlier steps, save and resume, a review page and submit are all undefined. A builder will guess.  
   Evidence: naive_builder major questions on notices.md and conventions.md  
   Action: Write a short conventions decision covering: back navigation, save and resume, a review page and explicit submit, the confirmation screen, whether editing after submission is in scope, and whether conditions re-run when an answer changes.
6. **Non-Swiss cross-border commuters are never asked their permit** – permit_type is asked only of Swiss residents. Cross-border commuters, such as the Liechtenstein resident, have a Swiss permit too, but HR never gets it for the first day and they never see the reminder to bring it.  
   Evidence: naive_builder major question on fields/permit_type.md; persona liechtenstein_resident (permit_type not asked)  
   Action: Decide whether non-Swiss residents abroad are asked their permit (for example a cross-border permit option) and shown the reminder. Link this to OQ-06.
7. **The source tax rule is true while spouse answers are still missing** – This breaks the convention that 'a rule is never true because of a missing answer'. Step 6 could show or hide wrongly while the employee is still answering.  
   Evidence: naive_builder question on rules/subject_to_source_tax.md; rule.subject_to_source_tax is inferred  
   Action: State that the rule counts as undetermined until all its spouse inputs are answered, or confirm that step order makes this safe. Also confirm the rule is complete with HR (OQ-02).
8. **Validation rules contradict each other and lack sources** – The field files say dates 'must not be in the future', but OQ-09 recommends checking only that a date is a valid calendar date. Trimming, accepting '12a' as a house number, and ISO country codes are also invented. Error wording is undefined, and the portal's error banner (F-SC-014) is not used anywhere.  
   Evidence: trace_judge partials on date_of_birth, spouse_date_of_birth, first_name, last_name, address_house_number, spouse_residence_country, spouse_employed; coverage warning F-SC-014; naive_builder questions on validation wording, length limits and country list  
   Action: Settle the date validation in one place, approve or remove the inferred validations, and decide the error wording (for example reuse the portal's pattern) and the country list.
9. **Guidance ids and decisions.yaml are not in the package** – Requirements cite G-01…G-10, but traceability.md cannot resolve them. A builder cannot check guidance that affects scope, for example G-02.  
   Evidence: naive_builder question on traceability.md; OQ-06 cites G-10  
   Action: Add the product owner guidance document and decisions.yaml to the package, and resolve the G-ids in traceability.md.
10. **Smaller wording and field-type decisions are still open** – The permit reminder also shows for 'no permit yet'. spouse_residence_country is a full country picker where a yes/no question would do (data minimisation, G-01). It is unclear whether insurance_start_date is shown to the employee.  
   Evidence: naive_builder questions on notices.md and fields/spouse_residence_country.md; OQ-08  
   Action: Decide whether the reminder shows only for B/C, whether to ask 'Does your spouse live in Switzerland?' (yes/no), and whether the notice shows the computed insurance start date.

## Numbers

266 source units → 68 facts → 18 fields, 2 rules, 2 notices in 6 steps; 9 open questions, 6 exclusions.

⚠ Sources without data (not explored / empty): zh_source_tax_calculator

## Errors (0)


## Persona tests (13/13 pass)

- ✅ **maria** – T: Maria in sales, Portuguese, C permit, no source tax
- ✅ **tomas** – T: Tomás, Brazilian, B permit, wife Swiss, live in Winterthur -> no source tax
- ✅ **stefan** – T: Stefan, Swiss, lives in Konstanz -> source tax regardless of passport
- ✅ **liechtenstein_resident** – T: woman in the warehouse who lives in Liechtenstein -> source tax
- ✅ **swiss_resident** – T: if you have a Swiss passport (and live here) you do not do source tax
- ✅ **b_permit_single** – T: all non-Swiss without C permit do source tax
- ✅ **b_permit_spouse_b_permit** – T: spouse exemption only for Swiss or C-permit spouses living here
- ✅ **b_permit_spouse_c_permit** – T: married to someone with a C permit who lives here -> no source tax
- ✅ **b_permit_swiss_spouse_abroad** – T: spouse exemption requires that the spouse lives here
- ✅ **julia** – T: Julia moved her first working day to 15 March -> insurance starts 1 April
- ✅ **starts_on_first** – T: unless somebody starts exactly on the first, then it's just that day
- ✅ **marco_married** – S: married -> Spouse's date of birth appears and is required (screens 05, 07)
- ✅ **lena_single** – S: single -> no spouse field (screen 04)

## Open questions (need your decision)

- **OQ-01** (blocking): Which questions does the Zurich source tax calculator ask to determine the tariff code (including the extra questions and German forms for residents abroad), with their options and conditions? → recommended: Extract the calculator's questions before building the source_tax step. The liability rule and the other steps can be built now.
- **OQ-03** (blocking): What should be entered in the pension portal's required 'Canton' field for employees living abroad, and does 'Canton' mean the residence canton or the work canton? → recommended: Ask Pensionskasse Muster. Until then, ask only Swiss residents for their residence canton and flag registrations of residents abroad for HR.
- **OQ-04**: How should employees in a registered partnership (or with other statuses such as separated) be recorded, and does the fund want the partner's date of birth? → recommended: Keep the four portal options for now and ask the fund. Add a 'registered_partnership' option once its mapping and partner-data requirements are known.
- **OQ-02**: Is the source tax liability rule complete? Anna ended with 'I think that's it'. → recommended: Confirm with HR and cross-check against the calculator.
- **OQ-05**: Is 'Spouse's date of birth' hidden in the portal for Divorced and Widowed? → recommended: Keep 'only married' (consistent with the transcript) and verify in the portal.
- **OQ-06**: Which permit types must the permit fields offer? → recommended: Keep B / C / other until the calculator facts are extracted.
- **OQ-07**: Is the postal address always the residence address, so that address_country can serve as the residence country? → recommended: Use one address. Anna described a normal home address.
- **OQ-08**: What exact wording should the permit reminder use, and when should it be shown? → recommended: Use the draft and let HR review it.
- **OQ-09**: Are there limits on dates (e.g. first working day not in the past, or a maximum distance in the future) and how does the portal word date errors? → recommended: Validate as a calendar date only, until HR or the fund defines limits.

## Inferred items to confirm

- field.first_name
- field.last_name
- field.address_country
- field.residence_canton
- field.nationality
- field.permit_type
- field.civil_status
- field.spouse_nationality
- field.spouse_permit_type
- field.spouse_residence_country
- field.spouse_employed
- rule.subject_to_source_tax
- fact F-TR-005: Source tax questions should be asked only to employees who are subject to source tax, not to everybody.
- fact F-TR-019: Consolidated: insurance_start_date is derived from first_working_day: if first_working_day is the 1st of a month, insurance starts that day; otherwise it starts on the 1st of the following month. It should be derived, not asked.
- fact F-TR-035: The spouse's permit is only relevant when the spouse is not Swiss (Swiss nationals have no permit).
- fact F-TR-040: Consolidated final rule (Anna hedged completeness with 'I think'): an employee is subject to source tax if residence_country is not CH (regardless of nationality). If living in CH: not subject if nationality is CH; not subject if permit_type is C; not subject if married to a spouse who is Swiss or holds a C permit and lives in CH; otherwise subject.
- fact F-TR-041: The employee's nationality is needed to determine source tax liability.
- fact F-TR-042: Non-Swiss employees' permit type (at least whether it is a C permit) is needed to determine source tax liability.
- fact F-TR-043: The employee's country of residence is needed to determine source tax liability (living abroad means always subject).
- fact F-TR-044: Spouse nationality, permit and residence only need to be asked when the employee is married and the spouse exemption could apply (i.e. employee is non-Swiss without C permit and lives in CH).
- fact F-TR-045: 'Lives here' in Anna's statements means living in Switzerland.
- fact F-SC-018: The Canton dropdown lists only Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. cross-border commuter), and whether 'Canton' means residence canton or work canton.
- fact F-SC-019: The Civil status list has no option for registered partnership, separated, or other statuses; it is open how employees with such statuses are registered and whether a partner's date of birth is then needed.
- fact F-SC-020: No screenshot shows the form with Civil status 'Divorced' or 'Widowed'; whether Spouse's date of birth is hidden for those values is assumed but not proven.
- fact F-SC-021: The portal requires an insurance start date on the 1st of a month but does not say how it relates to the first working day (e.g. 1st of the start month or next month); the derivation rule insurance_start_date is open.
- fact F-SC-022: No screenshot shows the error for an invalid date format or an insurance start date that is not the 1st of a month; the wording and any other date constraints (e.g. past/future limits) are unknown.

## Naive builder questions (17)

- [major] `flow.md` Step 6 'Source tax details' is shown whenever subject_to_source_tax is true, but its only field (spouse_employed) is asked only when the employee is married. A single, divorced or widowed person who is subject (including every unmarried resident abroad) would get a step with only the intro text 'You are subject to source tax. We need a few more details…' and no questions. Should an empty step be skipped, shown as an information-only page, or should the step condition include civil_status == "married" until OQ-01 is resolved?
- [major] `open-questions.md` README says to implement each open-question recommendation. OQ-01 recommends extracting the calculator's questions *before building the source_tax step*, yet flow.md and spouse_employed.md fully specify step 6. Should I build step 6 now with only 'spouse_employed', or leave step 6 out of the first release and ship liability determination only?
- [minor] `fields/date_of_birth.md` Contradiction: date_of_birth.md and spouse_date_of_birth.md add the validation 'must not be in the future', but OQ-09's recommendation (affecting date_of_birth and spouse_date_of_birth) says 'validate as a calendar date only'. Which one wins? (The trace judge also notes that no source supports 'not in the future'.)
- [major] `fields/first_working_day.md` The step text says 'Please confirm your first working day' and F-TR-015 says HR asks the employee to *confirm* it. Is first_working_day pre-filled by HR (from the contract) for the employee to confirm, or does the employee type it in with no starting value? Is an explicit confirmation action (checkbox or button) required, or is filling in the date enough?
- [major] `notices.md` The first_working_day_confirm notice and the first_working_day help text tell the employee to 'update it here right away' if the date changes. That means the questionnaire stays editable after it is submitted. Is editing after submission in scope? If so, which steps or fields can be edited, and does a re-submission re-run the conditions (for example a new civil status hiding or adding fields)? Notifications are out of scope, but editing itself is not addressed.
- [minor] `notices.md` The permit_reminder is shown when is_set(permit_type), so it also appears when permit_type == "other", whose label is 'Other permit / no permit yet'. Should someone without a permit yet be told to bring their permit? Should the notice be limited to B/C, or worded differently for 'other'?
- [major] `fields/permit_type.md` permit_type is asked only of Swiss residents, but its consumers include employer_hr for first-day logistics (bring your permit). Non-Swiss cross-border commuters (e.g. the woman living in Liechtenstein) also have a Swiss work permit, but they are never asked and never get the reminder. Should residents abroad who are not Swiss be asked their permit (for example a cross-border permit) and shown the reminder?
- [minor] `notices.md` Should the first_working_day_confirm notice show the computed insurance_start_date (e.g. 'Your insurance starts on 01.04.2026') or only the generic rule text as written? Is insurance_start_date displayed to the employee anywhere?
- [minor] `rules/subject_to_source_tax.md` Because of the outer `not (...)`, subject_to_source_tax is TRUE while the spouse questions are still unanswered (e.g. married B-permit holder, spouse_nationality = CH, spouse_residence_country not yet answered). That contradicts the conventions.md statement that 'a rule is never true because of a missing answer'. Should the rule (and step 6 visibility) count as undetermined/false until every input needed for the spouse exemption is answered, or is this temporary true value acceptable because step 5 must be finished first?
- [minor] `fields/spouse_residence_country.md` The source only needs to know whether the spouse lives in Switzerland ('and that they live here'). For data minimisation (G-01), should this be a yes/no question ('Does your spouse live in Switzerland?') instead of a full country picker? The trace judge flags the country type as unsupported.
- [major] `conventions.md` The general form behaviour is not specified. Can the employee go back to earlier steps? Is there a save-and-resume across sessions? Is there a final review/summary and an explicit submit? What happens after submission (confirmation screen, read-only view)? Is the employee identified or invited (for example with an HR-prefilled name)?
- [minor] `conventions.md` What error/validation messages should our form show (required, invalid date, invalid choice)? Should we reuse the portal's pattern '<Field label> is required.' and the banner 'Please correct the highlighted fields.', or does Lonio have its own wording?
- [minor] `fields/address_country.md` Which country list and labels should the country pickers (address_country, nationality, spouse_nationality, spouse_residence_country) use: all ISO 3166-1 alpha-2 entries with English names? Should Switzerland and neighbouring countries be listed first? How do we handle stateless persons, refugees, or nationality 'unknown', which have no ISO country code?
- [minor] `fields/first_name.md` Are there length or character limits for the text fields (first/last name, street, house number, postcode, town) imposed by the pension portal or HR systems? Should names include middle names / all given names as on the passport? Should values be stored trimmed?
- [minor] `fields/address_house_number.md` The house number is always required, but some addresses (rural or foreign) have no house number. Should it stay mandatory, or be optional, or allow an explicit 'no house number' choice?
- [minor] `open-questions.md` OQ-03's recommendation says to 'flag registrations of residents abroad for HR'. What is this flag in the questionnaire build: a stored derived flag, a visible marker in the HR output, or something else? Transmission to parties is out of scope, so where should the flag live?
- [minor] `traceability.md` Requirements cite product-owner guidance ids (G-01 … G-10, e.g. G-03, G-04, G-05 in out-of-scope.md) and a decisions.yaml, but neither the guidance document nor decisions.yaml is in the package, and traceability.md does not resolve G-ids. Can these be provided, so that no guidance affecting the build (for example G-02) is missing?

## Eval against gold set

```
field_recall: 1.0
field_precision: 0.94
consumer_recall: 1.0
rules_found: 2/2
exclusions_found: 2/2
notices_found: 1/1
open_questions_found: 2/2
fields_not_in_gold:
- spouse_employed
```

## Coverage

102/266 source units cited; 59/68 facts used.

Uncovered units (confirm they are irrelevant):

- T-000: HR meeting transcript Everyone and everything here is fictional. Anna is the HR manager at Muster AG. Leo works in product at Lonio.
- T-001: Can you hear me okay? You're a bit quiet.
- T-002: Is this better? I'm in the small meeting room, the big one is taken. Sorry, let me just close the door.
- T-003: Much better. So, thanks for making the time. The idea today is simple. We want your new employees to give us everything once, so that you stop chasing them for 
- T-005: Okay. And how many people do you hire in a year?
- T-007: Good. Let's start with the biggest pain. What takes you the most time?
- T-009: So who actually needs to answer them?
- T-011: Okay, that's clear. And the questionnaire itself is what?
- T-015: Anything else on the address?
- T-017: Great. Do you also want a photo? Some customers ask for one.
- T-019: It could. Do you want that from day one?
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
- T-054: Good. I'll send them after lunch. Thanks, Leo.
- T-055: Thanks, Anna. Talk soon.
- S01-E02: Employer portal
- S01-E04: Log out
- S01-E05: Home
- S01-E07: Register new employee
- S01-E09: Employee
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

## Warnings (21)

- [fact_judge] `F-TR-015` partial: First working day and confirmation are supported, but 'for the pension fund' is only implied by Leo's question and 'most important item' is 'number one thing' for the fund context. | The employee's first working day is needed (for the pension fund) and is the most important item; the employee should confirm it.
- [fact_judge] `F-TR-030` partial: Calculator asking whether the spouse works is supported, but 'Zurich' is not mentioned in these units. | For married employees subject to source tax, the Zurich calculator asks whether the spouse works.
- [fact_judge] `F-TR-044` partial: Gist is reasonable, but the explicit condition about when to ask spouse data is not stated; it is an inferred design choice. | Spouse nationality, permit and residence only need to be asked when the employee is married and the spouse exemption could apply (i.e. employee is non-Swiss without C permit and lives in CH).
- [fact_judge] `F-SC-013` partial: Shown for Married (05, 07) and absent for Single (04), and no spouse field appears in 01/03 units, but screenshot 06 and 02 are not evidenced and 'only when' is an inference. | 'Spouse's date of birth' appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in 01, 02, 03, 06 (civil status not selected).
- [fact_judge] `F-SC-014` partial: The banner text is shown in screenshot 06, but the units don't show the submit trigger or that every empty required field is highlighted (only an error-highlighted spouse field in 07). | Submitting the form with missing required fields shows the banner 'Please correct the highlighted fields.' and highlights each empty required field.
- [fact_judge] `F-SC-018` partial: Only Zug and Zurich options are visible, so 'only Swiss cantons' is plausible but the ambiguity about residence/work canton is the extractor's inference, not in the units. | The Canton dropdown lists only Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. cross-border commuter), and whether 'Canton' means residence canton or work canton.
- [coverage] `F-SC-014` fact not used by any requirement, exclusion or open question: Submitting the form with missing required fields shows the banner 'Please correct the highlighted fields.' and highlights each empty required field.
- [trace_judge] `field.first_name` partial: Pension portal required field is backed, but the HR consumer (correspondence and payroll administration) is only weakly inferred from the address quote, and the passport/ID help text and trim validation are not backed by any cited fact.
- [trace_judge] `field.last_name` partial: Pension fund required field is backed, but HR consumer (correspondence/payroll), the passport/ID help text and trim validation are not supported by the cited facts.
- [trace_judge] `field.date_of_birth` partial: Required field, DD.MM.YYYY display and ISO storage are backed, but the validation rules (valid calendar date, not in the future) are not supported by any cited fact.
- [trace_judge] `field.address_house_number` partial: Required house number for HR is backed, but the free-text allowing '12a' is not stated in the cited facts.
- [trace_judge] `field.residence_canton` partial: The 26 labels and required status are backed, but the two-letter option values and the ask_when address_country=="CH" restriction are not backed by the cited facts (F-SC-018 leaves residents abroad and residence-vs-work canton unresolved).
- [trace_judge] `field.spouse_date_of_birth` partial: Asking when married, required, and the DD.MM.YYYY format are backed, but the 'must not be in the future' validation is not backed by any cited fact.
- [trace_judge] `field.spouse_residence_country` partial: Facts support asking spouse residence for the exemption, but the country-type ISO alpha-2 format/validation and required_when=true are not backed, and the 'ask_when' narrowing is only inferred, since facts only give 'lives here' (in CH), not a country field.
- [trace_judge] `field.spouse_employed` partial: Calculator asking whether the spouse works for married employees is supported (F-TR-030), but the boolean yes/no format, validation and required_when=true are not backed, and the notes admit the calculator wording is unknown.
- [naive_builder] `flow.md` Step 6 'Source tax details' is shown whenever subject_to_source_tax is true, but its only field (spouse_employed) is asked only when the employee is married. A single, divorced or widowed person who is subject (including every unmarried resident abroad) would get a step with only the intro text 'You are subject to source tax. We need a few more details…' and no questions. Should an empty step be skipped, shown as an information-only page, or should the step condition include civil_status == "married" until OQ-01 is resolved?
- [naive_builder] `open-questions.md` README says to implement each open-question recommendation. OQ-01 recommends extracting the calculator's questions *before building the source_tax step*, yet flow.md and spouse_employed.md fully specify step 6. Should I build step 6 now with only 'spouse_employed', or leave step 6 out of the first release and ship liability determination only?
- [naive_builder] `fields/first_working_day.md` The step text says 'Please confirm your first working day' and F-TR-015 says HR asks the employee to *confirm* it. Is first_working_day pre-filled by HR (from the contract) for the employee to confirm, or does the employee type it in with no starting value? Is an explicit confirmation action (checkbox or button) required, or is filling in the date enough?
- [naive_builder] `notices.md` The first_working_day_confirm notice and the first_working_day help text tell the employee to 'update it here right away' if the date changes. That means the questionnaire stays editable after it is submitted. Is editing after submission in scope? If so, which steps or fields can be edited, and does a re-submission re-run the conditions (for example a new civil status hiding or adding fields)? Notifications are out of scope, but editing itself is not addressed.
- [naive_builder] `fields/permit_type.md` permit_type is asked only of Swiss residents, but its consumers include employer_hr for first-day logistics (bring your permit). Non-Swiss cross-border commuters (e.g. the woman living in Liechtenstein) also have a Swiss work permit, but they are never asked and never get the reminder. Should residents abroad who are not Swiss be asked their permit (for example a cross-border permit) and shown the reminder?
- [naive_builder] `conventions.md` The general form behaviour is not specified. Can the employee go back to earlier steps? Is there a save-and-resume across sessions? Is there a final review/summary and an explicit submit? What happens after submission (confirmation screen, read-only view)? Is the employee identified or invited (for example with an HR-prefilled name)?

## Run

Stages run: extract/zh_source_tax_calculator, extract/pension_portal, extract/hr_transcript, judge_facts, spec.raw, judge_trace, naive_builder, review

Stages reused from cache: normalize/hr_transcript, normalize/pension_portal, normalize/zh_source_tax_calculator

LLM cost this run: $2.38
