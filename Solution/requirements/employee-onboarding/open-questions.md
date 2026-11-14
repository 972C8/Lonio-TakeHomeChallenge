# Open questions

What the sources do not settle. Each needs a product decision or a
clarification with the stakeholder. Until then, follow the recommendation.

## OQ-canton-abroad
**What should be entered in the pension fund's required 'Canton' field for employees living abroad, and does 'Canton' mean canton of residence or of work?**

The field is required and offers only the 26 Swiss cantons; cross-border employees (Germany, Liechtenstein) cannot be registered without a value. Provisionally only residents of Switzerland are asked (D-002).

Options:
- Canton of work (Zurich) for employees abroad
- Canton of residence; the fund gives a rule for employees abroad
- HR enters a value agreed with the fund

**Recommendation:** Domain expert and Pensionskasse Muster to confirm; keep the provisional rule until then.

Affects: Canton
- **F-pension_portal-b359c3**: The label 'Canton' does not state whether it is the canton of residence or of work, and the list only contains Swiss cantons; it is unclear what to enter for an employee living abroad (e.g. a cross-border commuter). — "Canton" (01-empty.png (pension_portal/S01-E10)) — "Zurich" (02-canton-list.png (pension_portal/S02-E37))
- **F-pension_portal-3432a9**: The Canton dropdown offers exactly the 26 Swiss cantons: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for living outside Switzerland. — "Canton" (02-canton-list.png (pension_portal/S02-E10)) — "Aargau" (02-canton-list.png (pension_portal/S02-E12)) — "Appenzell Ausserrhoden" (02-canton-list.png (pension_portal/S02-E13)) — "Appenzell Innerrhoden" (02-canton-list.png (pension_portal/S02-E14)) — "Basel-Landschaft" (02-canton-list.png (pension_portal/S02-E15)) — "Basel-Stadt" (02-canton-list.png (pension_portal/S02-E16)) — "Bern" (02-canton-list.png (pension_portal/S02-E17)) — "Fribourg" (02-canton-list.png (pension_portal/S02-E18)) — "Geneva" (02-canton-list.png (pension_portal/S02-E19)) — "Glarus" (02-canton-list.png (pension_portal/S02-E20)) — "Graubünden" (02-canton-list.png (pension_portal/S02-E21)) — "Jura" (02-canton-list.png (pension_portal/S02-E22)) — "Lucerne" (02-canton-list.png (pension_portal/S02-E23)) — "Neuchâtel" (02-canton-list.png (pension_portal/S02-E24)) — "Nidwalden" (02-canton-list.png (pension_portal/S02-E25)) — "Obwalden" (02-canton-list.png (pension_portal/S02-E26)) — "Schaffhausen" (02-canton-list.png (pension_portal/S02-E27)) — "Schwyz" (02-canton-list.png (pension_portal/S02-E28)) — "Solothurn" (02-canton-list.png (pension_portal/S02-E29)) — "St. Gallen" (02-canton-list.png (pension_portal/S02-E30)) — "Thurgau" (02-canton-list.png (pension_portal/S02-E31)) — "Ticino" (02-canton-list.png (pension_portal/S02-E32)) — "Uri" (02-canton-list.png (pension_portal/S02-E33)) — "Valais" (02-canton-list.png (pension_portal/S02-E34)) — "Vaud" (02-canton-list.png (pension_portal/S02-E35)) — "Zug" (02-canton-list.png (pension_portal/S02-E36)) — "Zurich" (02-canton-list.png (pension_portal/S02-E37))
- **D-002**: Ask for the canton (pension fund 'Canton' field) only from employees living in Switzerland. Provisional - keep OQ-canton-abroad open as non-blocking, to be verified by a domain expert and Pensionskasse Muster (what to enter for employees living abroad, and whether 'Canton' means residence or work).

## OQ-civil-status-partnership
**How does Pensionskasse Muster want registered partnerships and separated employees registered, and does it want the partner's details?**

The fund's list has only Single, Married, Divorced, Widowed. Provisionally registered partnership and separated are entered as Married with the partner's/spouse's date of birth (D-003).

Options:
- Keep the provisional mapping (both as Married)
- Fund specifies another mapping

**Recommendation:** Domain expert to verify with the fund.

Affects: Civil status, Civil status for the pension fund, Spouse's / registered partner's date of birth
- **F-hr_transcript-f197d6**: Unknown how the pension fund screen handles a registered partnership and whether the fund wants the partner's details too. — "I honestly don't know what the fund's screen does in that case, or if they want the partner's details too." (hr_transcript/T-036, Anna)
- **F-hr_transcript-3907fe**: Muster AG has at least one employee (Daniel, finance) in a registered partnership. — "we do have one colleague in a registered partnership. Daniel, in finance." (hr_transcript/T-034, Anna)
- **F-pension_portal-9b24c5**: The civil status list has no option for registered partnership or separated; it is unclear how such employees are to be registered. — "Civil status" (03-civil-status-list.png (pension_portal/S03-E19)) — "Widowed" (03-civil-status-list.png (pension_portal/S03-E24))
- **D-003**: Civil status offers Single, Married, Divorced, Widowed, Registered partnership and Separated. For source tax, registered partnership counts as married (including the spouse exemption) and separated counts as single, as in the calculator. For the pension fund, provisionally, registered partnership is entered as Married with the partner's date of birth, and separated as Married. Keep OQ-civil-status-partnership open as non-blocking, to be verified by a domain expert.
- **D-004**: The spouse's (or registered partner's) date of birth is asked from married employees, registered partners and separated employees (all entered at the fund as Married, see D-003), not from divorced or widowed employees. Keep OQ-spouse-dob-other-status open as non-blocking, to be verified by a domain expert (screenshot of the fund's screen). This closes OQ-separated-spouse-dob; the separated case is verified together with OQ-civil-status-partnership.

## OQ-spouse-dob-other-status
**Does the fund's form ask for a spouse's date of birth (or other fields) for Divorced or Widowed?**

The screenshots show only Single (no) and Married (yes); if the fund needs it for divorced or widowed employees, the registration would be blocked.

Options:
- Not needed (current assumption)
- Needed - ask also divorced/widowed employees

**Recommendation:** Domain expert to provide a screenshot of the fund screen for these statuses.

Affects: Spouse's / registered partner's date of birth
- **F-pension_portal-6d3630**: Screenshots do not show whether the spouse's date of birth (or other fields) appears for 'Divorced' or 'Widowed'; only Single (no) and Married (yes) are shown. — "Divorced" (03-civil-status-list.png (pension_portal/S03-E23)) — "Widowed" (03-civil-status-list.png (pension_portal/S03-E24))
- **F-pension_portal-39bab1**: The 'Spouse's date of birth' field appears only when Civil status is 'Married': it is shown in screenshots 05 and 07 (civil status Married) and absent in screenshot 04 (civil status Single) and in screenshots 01, 02, 03 and 06 (civil status not selected). — "Spouse's date of birth" (05-married.png (pension_portal/S05-E21)) — "Married" (05-married.png (pension_portal/S05-E20)) — "Spouse's date of birth" (07-married-missing-spouse.png (pension_portal/S07-E21)) — "Married" (07-married-missing-spouse.png (pension_portal/S07-E20)) — "Single" (04-single.png (pension_portal/S04-E20))
- **D-004**: The spouse's (or registered partner's) date of birth is asked from married employees, registered partners and separated employees (all entered at the fund as Married, see D-003), not from divorced or widowed employees. Keep OQ-spouse-dob-other-status open as non-blocking, to be verified by a domain expert (screenshot of the fund's screen). This closes OQ-separated-spouse-dob; the separated case is verified together with OQ-civil-status-partnership.

## OQ-calculator-coverage
**Does Lonio's computed tariff code match the calculator for the paths not explored: the residence block for A/B/H tariffs, more than 3 children, H3N/P3N and the full cross-product of paths?**

Lonio now owns the tariff result (D-001); unexplored paths may produce wrong codes. Go-live condition (D-009).

Options:
- Domain expert compares computed codes with the calculator before go-live

**Recommendation:** Run the comparison before release.

Affects: Source tax tariff letter, Tariff child digit, Cross-border tariff applies, Source tax result
- **F-zh_source_tax_calculator-35dd3d**: The residence/cross-border block was explored exhaustively only for the married + Y + 1 child path and for Ersatzeinkünfte; for A/B/H tariffs it was only spot-checked. — "This block was explored exhaustively under the married + Y + 1 child (C1Y / C0Y) path and for Ersatzeinkünfte. For A/B/H it was spot-checked only" (zh_source_tax_calculator/C-N05)
- **F-zh_source_tax_calculator-332e2a**: The full cross-product of child paths × residence paths × confession × civil status was not enumerated. — "The full cross-product of child paths × residence paths × confession × civil status was not enumerated (combinatorial)." (zh_source_tax_calculator/C-N06)
- **F-zh_source_tax_calculator-4957f6**: Not tested: more than 3 children (upper limit unknown), whether 'Kind löschen' recomputes correctly, and tariff D or other special tariffs. — "Not tested: more than 3 children (the upper limit of 'Ein weiteres Kind erfassen' is unknown); whether 'Kind löschen' recomputes correctly; tariff D or other special tariffs (none appeared in any path)." (zh_source_tax_calculator/C-N07)
- **F-zh_source_tax_calculator-3cdbd7**: A hidden 'Beispiele' area shows tags H3N and P3N, which were not explored as inputs. — "A visually hidden 'Beispiele' area shows the tags H3N and P3N. These were not clicked as inputs." (zh_source_tax_calculator/C-N03)
- **D-009**: Before go-live a domain expert compares Lonio's computed tariff code with the calculator for the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N). Special tariffs such as D (second job) are out of scope for onboarding. Keep OQ-calculator-coverage open as a non-blocking go-live condition.

## OQ-child-paths-undetermined
**How does a child count in the child-answer combinations that the calculator exploration did not show (rows marked 'Not determined', e.g. married with alternating care where the employee is main contributor; single with an adult child in first education not mainly maintained)?**

Without these outcomes Lonio cannot compute the tariff code for such employees and the result stays 'cannot be computed yet'.

Options:
- Domain expert runs the missing paths in the calculator and fills the table
- Until then, HR determines the code for these cases

**Recommendation:** Include these paths in the pre-go-live comparison of D-009.

Affects: How a child counts for the tariff, Tariff child digit, Single-parent tariff H, Source tax result
- **F-zh_source_tax_calculator-332e2a**: The full cross-product of child paths × residence paths × confession × civil status was not enumerated. — "The full cross-product of child paths × residence paths × confession × civil status was not enumerated (combinatorial)." (zh_source_tax_calculator/C-N06)
- **F-zh_source_tax_calculator-96658b**: For a single (non-married) person, any child counted with H gives an H tariff overall (e.g. A1 + H1 -> H2N). A child is counted with H when it lives in the household and the person has sole custody or is the main financial contributor. — "For a single person, any child counted with H gives an H tariff (e.g. A1 + H1 -> H2N)." (zh_source_tax_calculator/C-N04) — "A child is counted with H when it lives in the household and the person has sole custody or is the main financial contributor." (zh_source_tax_calculator/C-N04) — "result Tarif: H2N (Kind Ergebnis: A1; Kind Ergebnis: H1)" (zh_source_tax_calculator/C-V27)
- **D-001**: Lonio computes the full Zurich source tax tariff code (tariff letter including the cross-border letters, child digit and church-tax suffix, e.g. "C1Y", "L0Y") for every employee subject to source tax, from the answers it collects, following the calculator's logic. HR no longer clicks through the calculator.
- **D-009**: Before go-live a domain expert compares Lonio's computed tariff code with the calculator for the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N). Special tariffs such as D (second job) are out of scope for onboarding. Keep OQ-calculator-coverage open as a non-blocking go-live condition.

