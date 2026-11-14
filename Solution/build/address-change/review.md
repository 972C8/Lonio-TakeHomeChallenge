# Review: address-change

**Verdict: NOT READY**

Not ready. Examples pass (23/23), all 22 facts are used and the gold eval is good (item recall 1.0). Three things block release: (1) the canton logic is circular (lint error on item.new_canton) and its open question OQ-01 is still undecided; (2) dev refinement raised a blocker on who passes moves abroad to payroll, and how; (3) the spec contradicts itself on what payroll receives. Several criteria also prescribe validation behaviour that no stakeholder asked for (tech_leak and trace_judge both flag it). Once HR and payroll have answered, most of the rest can be settled in decisions.yaml.

## Reviewer findings

1. **Canton detection is circular and its open question is unresolved** – FEAT-04 can't be built or tested. The spec asks for the new canton only when the canton changes, but can't know that without the new canton. Three examples (AC-04.1.1, AC-04.2.1, AC-04.3.1) pass only because they assume it is already known.  
   Evidence: lint error: item.new_canton 'asked_when depends on itself'; OQ-01 blocking=true; items new_canton and previous_canton plus rule canton_changes are inferred  
   Action: Decide OQ-01 with HR (Sara) in decisions.yaml. Recommended: take the previous canton from HR records and work out the new canton from the postcode. Then rewrite asked_when for new_canton. Alternatively, take FEAT-04 out of this release and have HR handle canton changes by hand.
2. **No one has decided who informs payroll, or how** – P1 source-tax risk. Engineers can't tell whether to build automatic forwarding to payroll or a step where HR passes the report on. They also don't know whether payroll is an internal team or an external provider.  
   Evidence: dev_refinement blocker on FEAT-03. AC-03.1.1 says payroll is informed 'when the employee submits', but AC-03.2.1 has HR in the loop.  
   Action: Record in decisions.yaml: who sends the report to payroll, when (on submission, after HR accepts it, or before the payroll run on the 25th), and whether payroll is internal or external.
3. **The spec contradicts itself on what payroll receives** – Data minimisation (G-01) depends on this. Some parts say payroll gets the valid-from date, others say it doesn't. No source says payroll gets even the country.  
   Evidence: trace_judge partial: US-03.1 and rule.payroll_must_be_informed (Switzerland row not backed). FEAT-02 lists HR as the only user of the valid-from date, but FEAT-03's context and OQ-05 assume payroll gets it. Payroll was never interviewed.  
   Action: Interview payroll (this also closes OQ-05). Then list exactly what payroll receives: who the employee is, the country, the valid-from date, and whether the full address is included. Confirm whether payroll is involved in Swiss canton changes for source-taxed staff.
4. **Validation and blocking behaviour that no source supports** – These criteria force a UX and system design no stakeholder asked for. Engineering would build rules that may be wrong.  
   Evidence: tech_leak and trace_judge on FEAT-01 'report cannot be completed while any of these four is missing'; FEAT-02 'date is not accepted and the employee is told…' (US-02.2 partial); OQ-03  
   Action: Confirm with HR whether an incomplete or late report is blocked or sent to HR for manual handling (closes OQ-03). Until then, describe only what HR needs and leave out how the system enforces it.
5. **Address completeness rules are not defined** – House number and postcode are always required, which would block rural addresses, named buildings and foreign addresses. There is also no plausibility rule (for example, 4-digit Swiss postcodes).  
   Evidence: dev_refinement major questions on FEAT-01 (house number and postcode, plausibility); trace_judge partial on US-01.1  
   Action: Decide whether the house number and postcode can be left empty, and whether there is any format check beyond 'filled in'. Also decide whether the employee answers a separate 'within Switzerland or abroad?' question, or whether that comes from the country only.
6. **Moves by cross-border staff and moves into Switzerland are undefined** – The payroll rule and the canton logic both assume the employee lives in Switzerland today. Someone moving into Switzerland has no previous canton, and payroll could be informed wrongly.  
   Evidence: OQ-04 (not linked in FEAT-01); FEAT-04 dev_refinement major question 'no previous canton'; Liechtenstein, Büsingen and Campione questions  
   Action: Decide OQ-04 with HR and payroll. Add how a move into Switzerland is treated to both FEAT-03 and FEAT-04, and link OQ-04 from FEAT-01.
7. **The canton value and its handover are not specified** – AC-04.1.3 can't be tested without a list of canton names. It is also unclear whether reporting to the tax office is part of the product or a manual HR step.  
   Evidence: dev_refinement major questions on FEAT-04 (canton naming, HR records missing or outdated, tax office handover); trace_judge partial on US-04.3 (AC-04.3.3 and P1 not backed)  
   Action: Add guidance: the 26 cantons and one naming convention. Make the tax office handover a manual HR step, out of scope. Decide what happens when HR's records have no canton or an old one. Confirm the P1 priority for US-04.x.
8. **How reports reach HR is not specified** – Engineering can't tell whether to build a notification, an HR task list, or a direct update of the employee record.  
   Evidence: dev_refinement major question on FEAT-01 (AC-01.1.2 and AC-01.2.3 say HR 'looks at the report')  
   Action: Decide whether HR is notified of new reports, and whether HR updates the master data manually or the report updates it directly.
9. **Wording that describes system internals** – These phrases lock in implementation choices and code names that don't belong in business wording.  
   Evidence: tech_leak on FEAT-02 'rule valid_from_within_three_months'; FEAT-04 'The internal condition can only check…'; FEAT-01 'choose from a fixed list'  
   Action: Rewrite them in business terms: name the rule in plain words, describe the condition by its result, and phrase OQ-06 as 'which countries are allowed'.
10. **Small inconsistencies in traceability and status** – These make it unclear how firm the requirements are, and they make estimates harder.  
   Evidence: The payslip purpose is not sourced (trace_judge on new_street, new_house_number, new_postcode, new_town, new_country and US-01.1). US-02.2 is marked inferred but its rule is marked confirmed. The AC-03.1.1 table shows 'asked' for Germany but '–' for France. AC-03.1.2 duplicates AC-01.2.x. The rule 'no future limit' is not backed (OQ-02).  
   Action: Cite or remove the payslip purpose. Align US-02.2's status with its rule. Fix the AC-03.1.1 table and drop AC-03.1.2. Confirm OQ-02 with HR.

## Numbers

13 source units → 22 facts → 8 information items, 3 business rules → 4 features, 9 stories, 23 acceptance criteria; 6 open questions, 1 exclusions.

## Errors (2)

- [lint] `item.new_canton` asked_when depends on itself
- [dev_refinement] `features/FEAT-03-payroll-move-abroad.md` Who informs payroll, and through what process? Does the report go to payroll automatically when the employee submits it, or does HR receive it, check it and then pass it on? AC-03.1.1 says payroll is informed 'when the employee submits', but AC-03.2.1 says HR handles Swiss moves 'on its own'. That suggests HR is in the loop. Is payroll an internal team or an external payroll provider?

## Examples executed against the knowledge model (23/23 pass)

- ✅ AC-01.1.1 / Move within Switzerland (spec)
- ✅ AC-01.1.1 / Move abroad (spec)
- ✅ AC-01.2.1 / Move within Switzerland (spec)
- ✅ AC-01.2.1 / Move abroad (spec)
- ✅ AC-02.1.1 / Move within Switzerland (spec)
- ✅ AC-02.1.1 / Move abroad (spec)
- ✅ AC-02.2.1 / Reported about six weeks late (spec)
- ✅ AC-02.2.1 / Exactly three months back (cut-off to be confirmed, see OQ-03) (spec)
- ✅ AC-02.2.2 / One day beyond the three-month window (spec)
- ✅ AC-02.2.2 / Reported about five months late (spec)
- ✅ AC-02.2.3 / Move applies from today (spec)
- ✅ AC-02.2.3 / Move announced several months ahead (spec)
- ✅ AC-03.1.1 / Move to Germany (spec)
- ✅ AC-03.1.1 / Move to France (spec)
- ✅ AC-03.1.2 / Country always asked (spec)
- ✅ AC-03.2.1 / Move within Switzerland (spec)
- ✅ AC-04.1.1 / Move from Bern to Zurich (spec)
- ✅ AC-04.2.1 / Move within Zurich (spec)
- ✅ AC-04.2.2 / Move to Germany (spec)
- ✅ AC-04.3.1 / Swiss move (spec)
- ✅ AC-04.3.2 / Move to Germany (spec)
- ✅ move_abroad (profile: T: moving abroad -> payroll must be informed)
- ✅ move_within_switzerland (profile: T: moves within Switzerland -> only the address)

## Open questions (need your decision)

- **OQ-01** (blocking): How do we find out whether the canton changes for a move within Switzerland? Options: ask the employee for the new canton on every Swiss move, ask them whether the canton changes, or have HR compare the new address with the canton it already has on record. → recommended: Clarify with HR (Sara). Prefer taking the previous canton from HR's existing records so the employee is not asked for data HR already has.
- **OQ-02**: Is there a latest allowed valid-from date in the future? → recommended: Confirm with HR. Until then, apply no future limit.
- **OQ-03**: Does 'not more than three months ago' include a date exactly three months back, and what happens if the employee reports an older date (rejected, or passed to HR for manual handling)? → recommended: Treat a date exactly three months back as allowed, and confirm with HR how older reports are handled.
- **OQ-04**: Does 'move abroad' always mean the new country is not Switzerland? What about employees who already live abroad and move within their country or into Switzerland? → recommended: Clarify with HR and payroll.
- **OQ-05**: Does payroll need any further information from the employee for a move abroad (to assess source tax), beyond the new country and the valid-from date? → recommended: Talk to payroll before finalising the questions for moves abroad.
- **OQ-06**: Is there a fixed list of countries the employee can choose from? → recommended: Use all countries, written by their English names (G-02), unless HR or payroll restricts them.

## Inferred items to confirm

- item.new_canton
- item.previous_canton
- rule.canton_changes
- story.US-02.2
- story.US-03.2
- story.US-04.1
- story.US-04.2
- story.US-04.3
- fact F-TR-016: Final rule for Swiss moves: always ask the new address; additionally ask the new canton only when the canton changes (needed for the tax office); not for moves within the same canton.
- fact F-TR-017: To determine whether the canton changes, the previous canton (or current canton) must be known; the stakeholder did not state how.
- fact F-TR-021: No upper limit for a future valid-from date was stated.

## Dev refinement questions (36)

- [major] `features/FEAT-01-new-address.md` AC-01.1.1 says the employee is asked for street, house number, postcode and town, "whether the move is within Switzerland or abroad". Does that mean we ask a separate question 'within Switzerland or abroad?', or only that the four parts are required in both cases? US-01.2 and AC-01.2.3 work out Swiss or abroad from the country. A separate question would duplicate that, and the two answers could disagree.
- [major] `features/FEAT-01-new-address.md` The house number is 'required always', but the Notes say the meeting never discussed addresses without one, and the trace check says no source supports 'cannot be completed while any is missing'. Can an employee finish the report if their address has no house number (rural addresses, named buildings, many foreign addresses)? Or with no postcode, in a country that doesn't use postcodes? If yes, what do they enter instead?
- [major] `features/FEAT-01-new-address.md` Should the new address be checked for plausibility, for example a Swiss postcode that has 4 digits and matches the town, or postcode formats for other countries? Or is any text accepted as long as each part is filled in? Nothing in the spec says what makes an address 'given' rather than just non-empty.
- [major] `features/FEAT-01-new-address.md` AC-01.2.3 says HR 'can see whether the move is within Switzerland or abroad'. For employees who already live abroad (cross-border staff), does a move inside their country, or a move into Switzerland, count as abroad? OQ-04 covers this in open-questions.md and lists 'Country of the new address' as affected, but this feature only links OQ-06.
- [major] `features/FEAT-01-new-address.md` AC-01.1.2 and AC-01.2.3 only say HR 'looks at the report' and 'can update the master data'. Is HR told when a new report comes in, or does HR check for reports itself? Is updating master data a manual HR step, or does the report change the employee record directly? This decides whether we build a notification or an integration.
- [minor] `features/FEAT-01-new-address.md` How should the employee enter the country if they type it, or if the source of the country names is open? For example, if they type 'Schweiz', 'Suisse' or 'Deutschland', should it be turned into the English name? G-02 sets English names, but AC-01.2.2 doesn't say what happens to non-English input.
- [minor] `features/FEAT-01-new-address.md` Are address extras such as c/o, apartment or floor, a second address line, or a PO box allowed or needed? The address is defined as exactly five parts, but documents sent to the wrong recipient line could still go astray.
- [minor] `features/FEAT-01-new-address.md` Is Liechtenstein treated as abroad? It uses Swiss postcodes but is a different country, and that affects payroll (source tax) and the canton logic that depend on this feature.
- [minor] `features/FEAT-01-new-address.md` Can an employee correct or withdraw a report after completing it, for example after a typo in the postcode? Can HR send it back? The spec only covers a first, complete report.
- [minor] `features/FEAT-01-new-address.md` Should we stop or warn when the new address is the same as the address HR already has on record?
- [minor] `features/FEAT-01-new-address.md` AC-01.1.3 says the reason for the move must never be asked. Does that also rule out a free-text comment or notes field, where employees could write their reason without being asked?
- [minor] `features/FEAT-01-new-address.md` Does the employee always fill in the report, or can HR enter a move for an employee (for example one reported by phone or letter)? The stakeholders list both, but every AC starts with 'an employee reports'.
- [major] `FEAT-02-valid-from.md` Does payroll also need the valid-from date for moves abroad? FEAT-03's context says the payroll decision uses 'the valid-from date from FEAT-02', and OQ-05 talks about payroll getting 'the new country and the valid-from date'. But here 'Who needs it?' lists only HR, and AC-02.1.3 only says HR gets it. The answer decides whether the date goes to payroll at all.
- [minor] `FEAT-02-valid-from.md` How do we count 'three months before the day of reporting' when that day doesn't exist in the target month? For example, reported on 31.05: is the cut-off 28/29.02, 01.03 or 03.03? Reported on 30.11: is it 30.08 or 31.08? OQ-03 only asks whether the exact day counts, not how month ends work.
- [minor] `FEAT-02-valid-from.md` Which date is 'the day of reporting': the day the employee starts the report, the day they submit it, or the day HR receives or processes it? If a report is started inside the window but submitted after the date falls outside it, is it still accepted?
- [minor] `FEAT-02-valid-from.md` For a late report, is there anything special HR needs? The valid-from date may already be past a payslip run on the 25th (a payslip went to the old address), or fall just before the next run. Does HR need such reports flagged or pointed out, or is it enough to show the date with the address (AC-02.1.3)?
- [minor] `FEAT-02-valid-from.md` Can the employee change or withdraw the valid-from date after submitting, for example if a planned future move is postponed? What happens if the same employee sends several reports with overlapping future dates? Nothing in the spec covers corrections.
- [minor] `FEAT-02-valid-from.md` Is telling the employee about the three-month limit (AC-02.2.2) actually confirmed by HR? The trace check says this is not in the source. And should the employee get guidance on what to do instead (for example, contact HR directly)?
- [minor] `FEAT-02-valid-from.md` US-02.2 is marked 'Status: inferred', but the rule it implements and the Valid from information are marked 'confirmed'. Which is right? It affects how firm the three-month check is before we build it.
- [blocker] `features/FEAT-03-payroll-move-abroad.md` Who informs payroll, and through what process? Does the report go to payroll automatically when the employee submits it, or does HR receive it, check it and then pass it on? AC-03.1.1 says payroll is informed 'when the employee submits', but AC-03.2.1 says HR handles Swiss moves 'on its own'. That suggests HR is in the loop. Is payroll an internal team or an external payroll provider?
- [major] `features/FEAT-03-payroll-move-abroad.md` What exactly does payroll receive for a move abroad? The ACs only name the new country. Payroll would at least need to know which employee moved. Does payroll also get the full new address and the valid-from date? The Context says the decision 'uses the valid-from date from FEAT-02', and OQ-05 assumes payroll has the new country and the valid-from date. But information.md lists Valid from as needed by HR only, and the trace check says nothing sources payroll receiving even the country. Data minimisation (G-01) makes this choice important.
- [major] `features/FEAT-03-payroll-move-abroad.md` When must payroll be informed? Right when the report is submitted, only after HR accepts it, or some time before the valid-from date or the payroll run on the 25th? Is there a deadline after which a notification counts as 'missed'?
- [major] `features/FEAT-03-payroll-move-abroad.md` What happens to the payroll notification in edge cases? Examples: the report is not accepted because the valid-from date is more than three months back (FEAT-02 / OQ-03), the employee corrects or withdraws a report after payroll was informed, or the country is changed from abroad to Switzerland or the other way round. Does payroll get an update or cancellation?
- [major] `features/FEAT-03-payroll-move-abroad.md` The goal says payroll is 'reliably informed', and P1 says a missed notification puts source tax at risk. What counts as reliable, and how do we test it? Must payroll confirm or acknowledge the notification? Must HR see that payroll was informed? Should anyone be alerted if it fails?
- [major] `features/FEAT-03-payroll-move-abroad.md` US-03.2 is inferred and says payroll is never involved in Swiss moves. Source-taxed employees who already live in Switzerland are taxed by canton. Does payroll need to know when such an employee changes canton? Also, how do we test 'payroll is not informed'? Does it only mean no notification is sent, or must payroll also have no access to the report? The answer matters if HR and payroll work in the same tool.
- [minor] `features/FEAT-03-payroll-move-abroad.md` Do special territories count as 'abroad'? For example Liechtenstein (which has special tax arrangements with Switzerland), or the enclaves Büsingen (Germany) and Campione d'Italia (Italy). Under the current rule any country other than Switzerland goes to payroll.
- [minor] `features/FEAT-03-payroll-move-abroad.md` Should the employee be told that their report for a move abroad will be passed to payroll?
- [minor] `features/FEAT-03-payroll-move-abroad.md` The example table in AC-03.1.1 is inconsistent. For Germany the 'Country of the new address' result column says 'asked', and for France it says '–', although the two cases are the same. Which result is correct, and what is this column meant to check?
- [minor] `features/FEAT-03-payroll-move-abroad.md` AC-03.1.2 repeats AC-01.2.1 and AC-01.2.2 from FEAT-01 (country always asked, English name). Does it belong to this feature, or is FEAT-01 the only owner? This matters for estimating and for deciding when each story is done.
- [major] `FEAT-04-canton-change.md` An employee who lives abroad now and moves into Switzerland has no previous canton. Should we ask for the new canton in that case, and does it count as a change of canton for the tax office? The decision table (rows 1–3) and AC-04.3.1 assume a previous canton always exists for Swiss moves. OQ-04 covers the payroll side of this, not the canton side.
- [major] `FEAT-04-canton-change.md` If the previous canton comes from HR's records, what happens when it is missing or out of date for an employee (for example, an earlier move was never reported)? Should the employee be asked, should the canton always be asked, or should HR be flagged to check?
- [major] `FEAT-04-canton-change.md` AC-04.1.2 says HR 'receives the new canton … so it can pass the change of canton to the tax office.' What exactly does HR receive? Is the report clearly marked as a change of canton, or does it just include the canton value? Is passing it to the tax office a manual HR step and out of scope, or should the product notify the tax office?
- [major] `FEAT-04-canton-change.md` AC-04.1.3 says the employee 'names a Swiss canton' but no list or wording is defined. Should the choice be limited to the 26 cantons? Which names count (English, German, French or Italian names, or official abbreviations like ZH or BE)? G-02 only sets the wording for countries. Without this, the criterion cannot be tested.
- [minor] `FEAT-04-canton-change.md` The tax office handles source tax by canton, so a canton change can matter to payroll too. Is 'No other stakeholder receives the new canton' (AC-04.1.2) confirmed with HR or payroll? Also, does the tax office need the previous canton? AC-04.3.3 says the previous canton is not passed on, and its own trace check says no source supports that.
- [minor] `FEAT-04-canton-change.md` If the employee is asked for the new canton and gives one, must it match the canton of the new postcode or town? What should happen if it does not match?
- [minor] `FEAT-04-canton-change.md` The trace check says P1 is 'not backed by the facts'. Can product confirm the priority of US-04.1 and US-04.3? Also, until OQ-01 is decided, should FEAT-01 to FEAT-03 ship without any canton handling, and should HR handle canton changes manually in the meantime?

## Technical decisions leaking into the spec (5)

- `features/FEAT-01-new-address.md` "the report cannot be completed while any of these four is missing" - This blocks the employee from finishing the report. The spec's own trace check says no source supports it. It is invented system behaviour, not a stakeholder requirement: HR only said what it needs, not that incomplete reports must be blocked.
- `features/FEAT-01-new-address.md` "Whether employees choose from a fixed list of countries or from all countries is still open (see OQ-06)" - Calling it 'choose from a list' assumes a picker-style control. The business question is only which countries are allowed; how the country is entered is up to engineering.
- `FEAT-02-valid-from.md` "It may be in the past, but not more than three months ago (see rule valid_from_within_three_months)." - A code-style rule identifier (snake_case) appears in the business prose. This is an internal naming decision, not business wording.
- `FEAT-02-valid-from.md` "the date is not accepted and the employee is told that a valid-from date may lie at most three months in the past" - This prescribes validation and feedback behaviour that no stakeholder asked for (the trace check admits the source doesn't state it). How the system checks the date and responds should be left to engineering and UX, or confirmed by HR first.
- `FEAT-04-canton-change.md` "The internal condition can only check this once both cantons are known." - Describes how the system evaluates the rule internally instead of what the business needs. How and when the comparison runs should be left to engineering.

## Eval against gold set

```
item_recall: 1.0
item_precision: 0.88
stakeholder_recall: null
rules_found: 1/1
exclusions_found: 1/1
open_questions_found: 0/0
stories_found: 0/0
items_not_in_gold:
- previous_canton
```

## Coverage

8/13 source units cited; 22/22 facts used.

Uncited units (confirm they are irrelevant):

- T-000: # Meeting notes: address change (fictional test source for pipeline genericity)
- T-001: Thanks for joining, Sara. Today it's about employees who move. What do you need when someone changes address?
- T-003: Does the employee give you a reason for the move?
- T-005: Anything that changes when the country changes?
- T-011: Anything else?

## Other warnings (27)

- [trace_judge] `item.new_street` partial: Street, form and always asked/required are backed, but the purpose 'update master data and send documents (e.g. payslips)' is not stated in the cited facts.
- [trace_judge] `item.new_house_number` partial: Form and always asked/required are backed, but the purpose 'update master data and send documents' is not in the cited facts.
- [trace_judge] `item.new_postcode` partial: Form and always asked/required are backed, but the purpose 'update master data and send documents' is not in the cited facts.
- [trace_judge] `item.new_town` partial: Form and always asked/required are backed, but the purpose 'update master data and send documents' is not in the cited facts.
- [trace_judge] `item.new_country` partial: Payroll source-tax need, English-name form and always asked are backed, but the HR purpose 'update master data and send documents' is not in the cited facts.
- [trace_judge] `item.previous_canton` partial: F-TR-017 only says the previous canton must be known to detect a change; the facts don't say it is asked for every Swiss move, and the question of asking versus HR records is open, so the asked_when_expr/required_when_expr are inferred.
- [trace_judge] `rule.payroll_must_be_informed` partial: Abroad row is backed by F-TR-011/012, but the 'payroll does not have to be informed' for Swiss moves is not stated in F-TR-013/016, which cover only the address, so the Switzerland row is not backed.
- [trace_judge] `rule.valid_from_within_three_months` partial: The three-month limit and late reporting are backed, but 'The meeting set no limit for future dates' is not backed because F-TR-021 quotes only the past-limit sentence, which doesn't state anything about future dates.
- [trace_judge] `story.US-01.1` partial: The facts back the four address items, the Swiss and abroad cases and the reason never being asked, but they don't support the payslip purpose or the 'cannot be completed while any is missing' requirement.
- [trace_judge] `story.US-02.2` partial: The exact three-month boundary (on or after the same date three months back) and telling the employee about the limit are not stated in F-TR-019, which only says 'not more than three months ago'.
- [trace_judge] `story.US-03.1` partial: The facts say payroll must be informed of a move abroad, but nothing says payroll receives the new country of residence (F-TR-010 is about HR's need).
- [trace_judge] `story.US-04.3` partial: AC-04.3.3 claims the previous canton is used only by HR and not passed to any other stakeholder, which F-TR-017 and G-01 do not state; AC-04.3.2 (not asked abroad) is also only inferred, and the P1 priority is not backed by the facts.
- [dev_refinement] `features/FEAT-01-new-address.md` AC-01.1.1 says the employee is asked for street, house number, postcode and town, "whether the move is within Switzerland or abroad". Does that mean we ask a separate question 'within Switzerland or abroad?', or only that the four parts are required in both cases? US-01.2 and AC-01.2.3 work out Swiss or abroad from the country. A separate question would duplicate that, and the two answers could disagree.
- [dev_refinement] `features/FEAT-01-new-address.md` The house number is 'required always', but the Notes say the meeting never discussed addresses without one, and the trace check says no source supports 'cannot be completed while any is missing'. Can an employee finish the report if their address has no house number (rural addresses, named buildings, many foreign addresses)? Or with no postcode, in a country that doesn't use postcodes? If yes, what do they enter instead?
- [dev_refinement] `features/FEAT-01-new-address.md` Should the new address be checked for plausibility, for example a Swiss postcode that has 4 digits and matches the town, or postcode formats for other countries? Or is any text accepted as long as each part is filled in? Nothing in the spec says what makes an address 'given' rather than just non-empty.
- [dev_refinement] `features/FEAT-01-new-address.md` AC-01.2.3 says HR 'can see whether the move is within Switzerland or abroad'. For employees who already live abroad (cross-border staff), does a move inside their country, or a move into Switzerland, count as abroad? OQ-04 covers this in open-questions.md and lists 'Country of the new address' as affected, but this feature only links OQ-06.
- [dev_refinement] `features/FEAT-01-new-address.md` AC-01.1.2 and AC-01.2.3 only say HR 'looks at the report' and 'can update the master data'. Is HR told when a new report comes in, or does HR check for reports itself? Is updating master data a manual HR step, or does the report change the employee record directly? This decides whether we build a notification or an integration.
- [dev_refinement] `FEAT-02-valid-from.md` Does payroll also need the valid-from date for moves abroad? FEAT-03's context says the payroll decision uses 'the valid-from date from FEAT-02', and OQ-05 talks about payroll getting 'the new country and the valid-from date'. But here 'Who needs it?' lists only HR, and AC-02.1.3 only says HR gets it. The answer decides whether the date goes to payroll at all.
- [dev_refinement] `features/FEAT-03-payroll-move-abroad.md` What exactly does payroll receive for a move abroad? The ACs only name the new country. Payroll would at least need to know which employee moved. Does payroll also get the full new address and the valid-from date? The Context says the decision 'uses the valid-from date from FEAT-02', and OQ-05 assumes payroll has the new country and the valid-from date. But information.md lists Valid from as needed by HR only, and the trace check says nothing sources payroll receiving even the country. Data minimisation (G-01) makes this choice important.
- [dev_refinement] `features/FEAT-03-payroll-move-abroad.md` When must payroll be informed? Right when the report is submitted, only after HR accepts it, or some time before the valid-from date or the payroll run on the 25th? Is there a deadline after which a notification counts as 'missed'?
- [dev_refinement] `features/FEAT-03-payroll-move-abroad.md` What happens to the payroll notification in edge cases? Examples: the report is not accepted because the valid-from date is more than three months back (FEAT-02 / OQ-03), the employee corrects or withdraws a report after payroll was informed, or the country is changed from abroad to Switzerland or the other way round. Does payroll get an update or cancellation?
- [dev_refinement] `features/FEAT-03-payroll-move-abroad.md` The goal says payroll is 'reliably informed', and P1 says a missed notification puts source tax at risk. What counts as reliable, and how do we test it? Must payroll confirm or acknowledge the notification? Must HR see that payroll was informed? Should anyone be alerted if it fails?
- [dev_refinement] `features/FEAT-03-payroll-move-abroad.md` US-03.2 is inferred and says payroll is never involved in Swiss moves. Source-taxed employees who already live in Switzerland are taxed by canton. Does payroll need to know when such an employee changes canton? Also, how do we test 'payroll is not informed'? Does it only mean no notification is sent, or must payroll also have no access to the report? The answer matters if HR and payroll work in the same tool.
- [dev_refinement] `FEAT-04-canton-change.md` An employee who lives abroad now and moves into Switzerland has no previous canton. Should we ask for the new canton in that case, and does it count as a change of canton for the tax office? The decision table (rows 1–3) and AC-04.3.1 assume a previous canton always exists for Swiss moves. OQ-04 covers the payroll side of this, not the canton side.
- [dev_refinement] `FEAT-04-canton-change.md` If the previous canton comes from HR's records, what happens when it is missing or out of date for an employee (for example, an earlier move was never reported)? Should the employee be asked, should the canton always be asked, or should HR be flagged to check?
- [dev_refinement] `FEAT-04-canton-change.md` AC-04.1.2 says HR 'receives the new canton … so it can pass the change of canton to the tax office.' What exactly does HR receive? Is the report clearly marked as a change of canton, or does it just include the canton value? Is passing it to the tax office a manual HR step and out of scope, or should the product notify the tax office?
- [dev_refinement] `FEAT-04-canton-change.md` AC-04.1.3 says the employee 'names a Swiss canton' but no list or wording is defined. Should the choice be limited to the 26 cantons? Which names count (English, German, French or Italian names, or official abbreviations like ZH or BE)? G-02 only sets the wording for countries. Without this, the criterion cannot be tested.

## Run

Stages run: extract/hr_meeting, judge_facts, knowledge.raw, features.plan, features/FEAT-03-payroll-move-abroad, features/FEAT-01-new-address, features/FEAT-02-valid-from, features/FEAT-04-canton-change, judge_trace, dev_refinement/FEAT-04-canton-change, dev_refinement/FEAT-02-valid-from, dev_refinement/FEAT-01-new-address, dev_refinement/FEAT-03-payroll-move-abroad, review

Stages reused from cache: normalize/hr_meeting

LLM cost this run: $3.12
