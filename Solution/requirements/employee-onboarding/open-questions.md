# Open questions

What the sources do not settle. Each needs a product decision or a
clarification with the stakeholder. Until then, follow the recommendation.

## OQ-canton-abroad
**What does Pensionskasse Muster expect in 'Canton' for employees living abroad, and does 'Canton' mean canton of residence or of work?**

The field is required and lists only Swiss cantons; employees abroad cannot be registered without an answer.

Options:
- Canton of work (Zurich) for employees abroad
- Canton of residence; the fund gives a rule for employees abroad
- Canton means work canton for everyone

**Recommendation:** Provisionally ask only residents of Switzerland (D-002); verify with a domain expert and the fund.

Affects: Canton
- **F-pension_portal-b359c3**: The label 'Canton' does not state whether it is the canton of residence or of work, and the list only contains Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. a cross-border commuter). — "Canton" (01-empty.png (pension_portal/S01-E10)) — "Zurich" (02-canton-list.png (pension_portal/S02-E37))
- **F-pension_portal-3432a9**: The Canton dropdown offers exactly the 26 Swiss cantons: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for living outside Switzerland. — "Canton" (02-canton-list.png (pension_portal/S02-E10)) — "Aargau" (02-canton-list.png (pension_portal/S02-E12)) — "Appenzell Ausserrhoden" (02-canton-list.png (pension_portal/S02-E13)) — "Appenzell Innerrhoden" (02-canton-list.png (pension_portal/S02-E14)) — "Basel-Landschaft" (02-canton-list.png (pension_portal/S02-E15)) — "Basel-Stadt" (02-canton-list.png (pension_portal/S02-E16)) — "Bern" (02-canton-list.png (pension_portal/S02-E17)) — "Fribourg" (02-canton-list.png (pension_portal/S02-E18)) — "Geneva" (02-canton-list.png (pension_portal/S02-E19)) — "Glarus" (02-canton-list.png (pension_portal/S02-E20)) — "Graubünden" (02-canton-list.png (pension_portal/S02-E21)) — "Jura" (02-canton-list.png (pension_portal/S02-E22)) — "Lucerne" (02-canton-list.png (pension_portal/S02-E23)) — "Neuchâtel" (02-canton-list.png (pension_portal/S02-E24)) — "Nidwalden" (02-canton-list.png (pension_portal/S02-E25)) — "Obwalden" (02-canton-list.png (pension_portal/S02-E26)) — "Schaffhausen" (02-canton-list.png (pension_portal/S02-E27)) — "Schwyz" (02-canton-list.png (pension_portal/S02-E28)) — "Solothurn" (02-canton-list.png (pension_portal/S02-E29)) — "St. Gallen" (02-canton-list.png (pension_portal/S02-E30)) — "Thurgau" (02-canton-list.png (pension_portal/S02-E31)) — "Ticino" (02-canton-list.png (pension_portal/S02-E32)) — "Uri" (02-canton-list.png (pension_portal/S02-E33)) — "Valais" (02-canton-list.png (pension_portal/S02-E34)) — "Vaud" (02-canton-list.png (pension_portal/S02-E35)) — "Zug" (02-canton-list.png (pension_portal/S02-E36)) — "Zurich" (02-canton-list.png (pension_portal/S02-E37))
- **D-002**: Ask for the canton (pension fund 'Canton' field) only from employees living in Switzerland. Provisional - keep OQ-canton-abroad open as non-blocking, to be verified by a domain expert and Pensionskasse Muster (what to enter for employees living abroad, and whether 'Canton' means residence or work).

## OQ-civil-status-partnership
**How does the pension fund want registered partnerships and separated employees registered (the list has only Single, Married, Divorced, Widowed), and does it want partner details?**

A wrong civil status or a missing partner date of birth makes the registration wrong.

Options:
- Keep provisional mapping (both as Married with spouse/partner date of birth)
- Fund gives another mapping

**Recommendation:** Use the provisional mapping (D-003) until a domain expert verifies it.

Affects: Civil status for the pension fund, Spouse's or registered partner's date of birth
- **F-pension_portal-9b24c5**: The civil status list has no option for registered partnership or separated; it is unclear how such employees are to be registered. — "Civil status" (03-civil-status-list.png (pension_portal/S03-E19)) — "Widowed" (03-civil-status-list.png (pension_portal/S03-E24))
- **F-hr_transcript-f197d6**: Unknown how the pension fund screen handles a registered partnership and whether the fund wants the partner's details too. — "I honestly don't know what the fund's screen does in that case, or if they want the partner's details too." (hr_transcript/T-036, Anna)
- **D-003**: Civil status offers Single, Married, Divorced, Widowed, Registered partnership and Separated. For source tax, registered partnership counts as married (including the spouse exemption) and separated counts as single, as in the calculator. For the pension fund, provisionally, registered partnership is entered as Married with the partner's date of birth, and separated as Married. Keep OQ-civil-status-partnership open as non-blocking, to be verified by a domain expert.
- **D-004**: The spouse's (or registered partner's) date of birth is asked from married employees, registered partners and separated employees (all entered at the fund as Married, see D-003), not from divorced or widowed employees. Keep OQ-spouse-dob-other-status open as non-blocking, to be verified by a domain expert (screenshot of the fund's screen). This closes OQ-separated-spouse-dob; the separated case is verified together with OQ-civil-status-partnership.

## OQ-spouse-dob-other-status
**Does the fund's screen ask for a spouse's date of birth (or other data) for Divorced or Widowed?**

The screenshots show only Single and Married; a hidden required field would block registration.

Options:
- No extra field (current assumption)
- Extra field shown - add a question

**Recommendation:** Do not ask divorced/widowed employees (D-004); verify with a screenshot of the fund's screen.

Affects: Spouse's or registered partner's date of birth
- **F-pension_portal-6d3630**: Screenshots do not show whether the spouse's date of birth (or other fields) appears for 'Divorced' or 'Widowed'; only Single (no) and Married (yes) are shown. — "Divorced" (03-civil-status-list.png (pension_portal/S03-E23)) — "Widowed" (03-civil-status-list.png (pension_portal/S03-E24))
- **D-004**: The spouse's (or registered partner's) date of birth is asked from married employees, registered partners and separated employees (all entered at the fund as Married, see D-003), not from divorced or widowed employees. Keep OQ-spouse-dob-other-status open as non-blocking, to be verified by a domain expert (screenshot of the fund's screen). This closes OQ-separated-spouse-dob; the separated case is verified together with OQ-civil-status-partnership.

## OQ-calculator-coverage
**Does Lonio's computed tariff code match the calculator on paths not explored: residence block for A/B/H tariffs, more than 3 children, H3N/P3N, and the child paths marked 'inferred' in the child result table?**

Lonio now owns the tariff result; an unverified path could produce a wrong tariff code.

Options:
- Domain expert compares computed codes with the calculator before go-live

**Recommendation:** Go-live condition: domain expert verification (D-009).

Affects: Child result (per child), Child digit of the tariff code, Tariff letter, Cross-border tariff applies, Source tax result
- **F-zh_source_tax_calculator-35dd3d**: The residence/cross-border block was explored exhaustively only for the married + Y + 1 child path and for Ersatzeinkünfte; for A/B/H tariffs it was only spot-checked. — "This block was explored exhaustively under the married + Y + 1 child (C1Y / C0Y) path and for Ersatzeinkünfte. For A/B/H it was spot-checked only" (zh_source_tax_calculator/C-N05)
- **F-zh_source_tax_calculator-332e2a**: The full cross-product of child paths × residence paths × confession × civil status was not enumerated. — "The full cross-product of child paths × residence paths × confession × civil status was not enumerated (combinatorial)." (zh_source_tax_calculator/C-N06)
- **F-zh_source_tax_calculator-4957f6**: Not tested: more than 3 children (upper limit unknown), whether 'Kind löschen' recomputes correctly, and tariff D or other special tariffs. — "Not tested: more than 3 children (the upper limit of 'Ein weiteres Kind erfassen' is unknown); whether 'Kind löschen' recomputes correctly; tariff D or other special tariffs (none appeared in any path)." (zh_source_tax_calculator/C-N07)
- **F-zh_source_tax_calculator-3cdbd7**: A hidden 'Beispiele' area shows tags H3N and P3N, which were not explored as inputs. — "A visually hidden 'Beispiele' area shows the tags H3N and P3N. These were not clicked as inputs." (zh_source_tax_calculator/C-N03)
- **D-009**: Before go-live a domain expert compares Lonio's computed tariff code with the calculator for the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N). Special tariffs such as D (second job) are out of scope for onboarding. Keep OQ-calculator-coverage open as a non-blocking go-live condition.

## OQ-copy-email-retention
**Is the email address for the copy kept after the copy has been sent, and is it recorded for HR, or used only for sending?**

No receiving party needs the address; keeping it would hold personal data no party needs (data minimisation).

Options:
- Use it only to send the copy, do not keep it
- Keep it and record it for HR

**Recommendation:** Use it only to send the copy and do not record it for any receiving party.

Affects: Email address for the copy, Email copy of the submitted answers
- **F-hr_email_copy-fd28be**: The copy email address serves only to send the employee their own copy; it is requested by HR for the employee's benefit, not as data a receiving party (pension fund, source tax) needs. — "the employee should be able to send themselves an email with a copy of their form data" (hr_email_copy/T-001, Anna)
- **G-01**: Lonio collects onboarding data from a new employee **once** and reuses it for every receiving party. Asking too little blocks a registration; asking too much collects personal data we must not have (data minimisation). A question must only be asked when at least one receiving party needs the answer for this person.

