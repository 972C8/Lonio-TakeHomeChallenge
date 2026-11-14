# Review: employee-onboarding

**Verdict: not available** – the LLM checks (trace judge, dev refinement, review) did not run for this report. Run `pipeline run` for the full review.

## Numbers

266 source units → 61 facts → 17 information items, 2 business rules → one feature with 4 sections, 12 stories, 37 acceptance criteria; 8 open questions, 5 exclusions.

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

## Technical vocabulary found in the spec (0)


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

## Other warnings (11)

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

## Run

Stages run: (converted, checks and render only)

Stages reused from cache: -

LLM cost this run: $0.0
