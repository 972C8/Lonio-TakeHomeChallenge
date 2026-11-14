# Open questions

What the sources do not settle. Each needs a product decision or a
clarification with the stakeholder. Until then, follow the recommendation.

## OQ-01
**Which questions does the Zurich source tax calculator ask to set the tariff code, with which options and under which conditions (including the different questions for married employees, such as whether the spouse works, and the extra questions and German forms for employees living abroad)?** _(blocking)_

The source tax questions for subject employees cannot be specified; the calculator source has not been analysed yet. It may also need data not asked today (e.g. nationality of employees living abroad).

Options:
- Analyse the Zurich calculator and add its questions, asked only when subject_to_source_tax is true
- Release without source tax questions at first

**Recommendation:** Analyse the calculator before specifying the source tax step; ask its questions only to employees subject to source tax.

Affects: Subject to source tax, Nationality, Civil status, Country of home address (country of residence)
- **F-TR-007**: HR uses the Zurich tariff calculator on the canton's website to get the tariff code, clicking through it with the employee's answers. — "I use the Zurich calculator on the canton's website. The one that gives you the tariff code." (T-012, Anna)
- **F-TR-008**: For now, the Zurich calculator is used for every employee subject to source tax. The stakeholder knows this is not exactly how it works, and the interviewer agreed to keep it this way. — "For everybody I use Zurich, by the way. I know it's not exactly how it works, but that's what we do for now." (T-012, Anna) — "We'll keep that for now." (T-013, Leo)
- **F-TR-029**: For married employees, the source tax calculator asks different questions, for example whether the husband or wife works. — "It changes the questions in the calculator, yes. Whether the husband or wife works." (T-044, Anna)
- **F-TR-036**: For employees living abroad, the source tax calculator asks more questions. Germany has its own forms, which the stakeholder cannot name. The interviewer said the calculator will define these questions. — "And with them the calculator gets much more complicated, there are more questions." (T-050, Anna) — "Germany has its own forms, I can never remember what they're called." (T-050, Anna) — "the calculator will tell us." (T-051, Leo)
- **F-TR-005**: Source tax questions should only be asked to employees who are subject to source tax, not to everybody. — "Because I never know up front who has to answer those questions." (T-008, Anna) — "the Swiss people get annoyed, and they call me." (T-008, Anna)

## OQ-02
**Does the pension fund's 'Canton' mean the canton of residence or of work, and what should be entered for employees living abroad, given that only Swiss cantons are offered?** _(blocking)_

The canton is required for every registration; cross-border employees (e.g. living in Konstanz or Liechtenstein) cannot be registered without an answer.

Options:
- Canton of residence; ask the fund what to use for employees living abroad
- Canton of work (would not need to be asked of the employee, e.g. Zurich)

**Recommendation:** Ask Pensionskasse Muster. Until then, ask the canton only of employees living in Switzerland.

Affects: Canton
- **F-SC-006**: The pension fund registration requires a canton (dropdown in the Employee section, marked required); the portal does not label whether it is the residence or work canton. — "Canton" (01-empty.png (S01-E14)) — "Employee" (01-empty.png (S01-E09))
- **F-SC-007**: The Canton dropdown offers exactly these 26 options: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for living outside Switzerland. — "Canton" (02-canton-list.png (S02-E14)) — "Aargau" (02-canton-list.png (S02-E16)) — "Appenzell Ausserrhoden" (02-canton-list.png (S02-E17)) — "Appenzell Innerrhoden" (02-canton-list.png (S02-E18)) — "Basel-Landschaft" (02-canton-list.png (S02-E19)) — "Basel-Stadt" (02-canton-list.png (S02-E20)) — "Bern" (02-canton-list.png (S02-E21)) — "Fribourg" (02-canton-list.png (S02-E22)) — "Geneva" (02-canton-list.png (S02-E23)) — "Glarus" (02-canton-list.png (S02-E24)) — "Graubünden" (02-canton-list.png (S02-E25)) — "Jura" (02-canton-list.png (S02-E26)) — "Lucerne" (02-canton-list.png (S02-E27)) — "Neuchâtel" (02-canton-list.png (S02-E28)) — "Nidwalden" (02-canton-list.png (S02-E29)) — "Obwalden" (02-canton-list.png (S02-E30)) — "Schaffhausen" (02-canton-list.png (S02-E31)) — "Schwyz" (02-canton-list.png (S02-E32)) — "Solothurn" (02-canton-list.png (S02-E33)) — "St. Gallen" (02-canton-list.png (S02-E34)) — "Thurgau" (02-canton-list.png (S02-E35)) — "Ticino" (02-canton-list.png (S02-E36)) — "Uri" (02-canton-list.png (S02-E37)) — "Valais" (02-canton-list.png (S02-E38)) — "Vaud" (02-canton-list.png (S02-E39)) — "Zug" (02-canton-list.png (S02-E40)) — "Zurich" (02-canton-list.png (S02-E41))
- **F-SC-017**: The Canton dropdown only lists Swiss cantons; it is unclear what to enter for an employee who lives abroad (e.g. a cross-border commuter living in Germany), and whether the field means the residence canton or the work canton. — "Canton" (02-canton-list.png (S02-E14)) — "Zurich" (02-canton-list.png (S02-E41))
- **F-TR-035**: Some employees live across the border, for example in Konstanz (Germany) and in Liechtenstein. — "Stefan lives in Konstanz, and there's a woman in the warehouse who lives in Liechtenstein." (T-048, Anna)

## OQ-03
**How should an employee in a registered partnership (or other status not in the list, e.g. separated) be registered with the pension fund, does the fund want the partner's details, and does a registered partnership count as married for the source tax spouse rule?**

The fund's civil status list has only Single, Married, Divorced, Widowed; such employees cannot answer correctly and the source tax outcome may be wrong.

Options:
- Ask the fund and HR and extend the list if the fund supports it
- Treat registered partnership as Married
- Leave the list as is

**Recommendation:** Ask Pensionskasse Muster; do not add values the fund does not accept.

Affects: Civil status, Spouse's date of birth, Subject to source tax
- **F-TR-023**: One current employee (Daniel, in finance) is in a registered partnership. He was entered before the current HR manager's time. — "we do have one colleague in a registered partnership. Daniel, in finance." (T-034, Anna) — "That was before my time." (T-036, Anna)
- **F-TR-024**: Unresolved: how the pension fund's screen handles a registered partnership, and whether the fund wants the partner's details. — "I honestly don't know what the fund's screen does in that case, or if they want the partner's details too." (T-036, Anna)
- **F-SC-011**: The Civil status dropdown offers exactly these options: Single, Married, Divorced, Widowed. — "Civil status" (03-civil-status-list.png (S03-E19)) — "Single" (03-civil-status-list.png (S03-E21)) — "Married" (03-civil-status-list.png (S03-E22)) — "Divorced" (03-civil-status-list.png (S03-E23)) — "Widowed" (03-civil-status-list.png (S03-E24))
- **F-SC-018**: No screenshot shows the form with civil status Divorced or Widowed, so it is unknown whether any extra fields (e.g. spouse data) appear for those values; the list also has no option such as registered partnership or separated, and it is unclear how such cases are to be registered. — "Divorced" (03-civil-status-list.png (S03-E23)) — "Widowed" (03-civil-status-list.png (S03-E24))

## OQ-04
**Does the pension fund portal show extra fields (e.g. spouse data) when civil status is Divorced or Widowed?**

Missing a field would block registration for these employees.

Options:
- Check the portal with these values
- Assume no extra fields

**Recommendation:** Ask HR for screenshots with Divorced and Widowed selected.

Affects: Civil status, Spouse's date of birth
- **F-SC-018**: No screenshot shows the form with civil status Divorced or Widowed, so it is unknown whether any extra fields (e.g. spouse data) appear for those values; the list also has no option such as registered partnership or separated, and it is unclear how such cases are to be registered. — "Divorced" (03-civil-status-list.png (S03-E23)) — "Widowed" (03-civil-status-list.png (S03-E24))

## OQ-05
**Is the source tax rule complete? HR answered 'I think so' / 'I think that's it'.**

Missing cases would ask the wrong people the source tax questions or skip people who must answer them.

Options:
- Confirm with HR / payroll
- Accept the rule as is

**Recommendation:** Have HR confirm the decision table with a few real cases.

Affects: Subject to source tax
- **F-TR-025**: Correction: employees with a C permit are not subject to source tax and are treated like Swiss nationals (example: Maria, Portuguese with a C permit). So the rule becomes non-Swiss, except C permit holders. Asked if that was everything, the stakeholder answered only 'I think so'. — "So, not the people with a C permit. They're treated like Swiss people for this." (T-038, Anna) — "Okay, so non-Swiss, but not with a C permit." (T-039, Leo) — "I think so." (T-040, Anna)
- **F-TR-037**: Consolidated final rule. (1) An employee whose home address is outside Switzerland is subject to source tax, whatever their nationality. (2) An employee living in Switzerland who is Swiss or holds a C permit is not subject. (3) An employee living in Switzerland who is non-Swiss without a C permit is not subject if married to a spouse who is Swiss or holds a C permit and lives in Switzerland. (4) Otherwise the employee is subject. The stakeholder hedged on completeness ('I think that's it'). — "If you don't have a Swiss passport, you do source tax." (T-010, Anna) — "So, not the people with a C permit. They're treated like Swiss people for this." (T-038, Anna) — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (T-044, Anna) — "Those people do source tax because they work here and they don't live here." (T-048, Anna) — "I think that's it." (T-048, Anna)

## OQ-06
**Which permit types may the employee and spouse choose from? Sources mention only the B permit and the C permit.**

The question needs a list of answers; only 'C permit' versus other matters for the source tax rule.

Options:
- Get the list from HR or the calculator
- Offer B permit, C permit and 'other'

**Recommendation:** Take the list from the Zurich calculator once analysed (OQ-01) or confirm with HR.

Affects: Permit type, Spouse's permit type
- **F-TR-025**: Correction: employees with a C permit are not subject to source tax and are treated like Swiss nationals (example: Maria, Portuguese with a C permit). So the rule becomes non-Swiss, except C permit holders. Asked if that was everything, the stakeholder answered only 'I think so'. — "So, not the people with a C permit. They're treated like Swiss people for this." (T-038, Anna) — "Okay, so non-Swiss, but not with a C permit." (T-039, Leo) — "I think so." (T-040, Anna)
- **F-TR-030**: Addition: an employee married to someone who is Swiss or holds a C permit, and who lives in Switzerland, is not subject to source tax. Example: Tomás, Brazilian with a B permit, whose Swiss wife lives with him in Winterthur. — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (T-044, Anna) — "Brazilian, B permit, but his wife is Swiss, and they live in Winterthur. So no source tax for him." (T-044, Anna)
- **F-TR-039**: Non-Swiss employees' permit type (e.g. B permit, C permit) is needed to decide whether they are subject to source tax. — "She has a C permit. So, not the people with a C permit." (T-038, Anna)

## OQ-07
**Should the questionnaire remind employees to bring their permit, and with which wording?**

HR wished for it because half of new employees forget; wording was deferred.

Options:
- Add a reminder for employees with a permit
- Leave it out

**Recommendation:** Decide with HR; a reminder for non-Swiss employees living in Switzerland seems natural.

Affects: Permit type
- **F-TR-028**: The stakeholder would love the form to remind employees to bring their permit, because half of them forget. Not decided: the interviewer deferred the wording to later. — "What I would love is if the form could remind people to bring their permit. Half of them forget." (T-042, Anna) — "We can look at the wording later." (T-043, Leo)

## OQ-08
**The Zurich calculator is used for every employee subject to source tax, though HR knows this is not exactly correct. Should this be revisited?**

Known simplification agreed for now; may produce incorrect tariffs for employees in other cantons.

Options:
- Keep Zurich for all (current decision)
- Revisit later

**Recommendation:** Keep for now as agreed and per the assignment's simplification.

Affects: Subject to source tax
- **F-TR-008**: For now, the Zurich calculator is used for every employee subject to source tax. The stakeholder knows this is not exactly how it works, and the interviewer agreed to keep it this way. — "For everybody I use Zurich, by the way. I know it's not exactly how it works, but that's what we do for now." (T-012, Anna) — "We'll keep that for now." (T-013, Leo)
- **G-05**: Simplifications given by the assignment: Switzerland has exactly one source tax system (Zurich's) and exactly one pension fund (Pensionskasse Muster).

