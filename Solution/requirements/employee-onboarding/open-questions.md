# Open questions

What the sources do not settle. Each needs a product decision or a
clarification with the stakeholder. Until then, follow the recommendation.

## OQ-canton-abroad
**What does Pensionskasse Muster expect in its required 'Canton' field for employees living abroad, and does 'Canton' mean canton of residence or canton of work?**

The fund's list has only the 26 Swiss cantons and the field is required; employees abroad (e.g. Konstanz, Liechtenstein) cannot be registered without an answer. Provisionally the canton is asked only of employees living in Switzerland.

Options:
- Canton of work (e.g. Zurich) for everyone, entered by HR
- Canton of residence; the fund has another way for employees abroad
- Ask everyone the canton

**Recommendation:** Keep D-002 (ask residents only); a domain expert verifies with Pensionskasse Muster.

Affects: Canton, Country of residence (country of the home address)
- **F-pension_portal-b359c3**: The portal does not say whether 'Canton' means canton of residence or of work, and the list offers no option for employees living outside Switzerland; how to register such employees is unknown. — "Canton" (01-empty.png (pension_portal/S01-E10)) — "Zurich" (02-canton-list.png (pension_portal/S02-E37))
- **F-pension_portal-3432a9**: The Canton dropdown offers exactly these 26 options: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for a residence outside Switzerland. — "Canton" (02-canton-list.png (pension_portal/S02-E10)) — "Aargau" (02-canton-list.png (pension_portal/S02-E12)) — "Appenzell Ausserrhoden" (02-canton-list.png (pension_portal/S02-E13)) — "Appenzell Innerrhoden" (02-canton-list.png (pension_portal/S02-E14)) — "Basel-Landschaft" (02-canton-list.png (pension_portal/S02-E15)) — "Basel-Stadt" (02-canton-list.png (pension_portal/S02-E16)) — "Bern" (02-canton-list.png (pension_portal/S02-E17)) — "Fribourg" (02-canton-list.png (pension_portal/S02-E18)) — "Geneva" (02-canton-list.png (pension_portal/S02-E19)) — "Glarus" (02-canton-list.png (pension_portal/S02-E20)) — "Graubünden" (02-canton-list.png (pension_portal/S02-E21)) — "Jura" (02-canton-list.png (pension_portal/S02-E22)) — "Lucerne" (02-canton-list.png (pension_portal/S02-E23)) — "Neuchâtel" (02-canton-list.png (pension_portal/S02-E24)) — "Nidwalden" (02-canton-list.png (pension_portal/S02-E25)) — "Obwalden" (02-canton-list.png (pension_portal/S02-E26)) — "Schaffhausen" (02-canton-list.png (pension_portal/S02-E27)) — "Schwyz" (02-canton-list.png (pension_portal/S02-E28)) — "Solothurn" (02-canton-list.png (pension_portal/S02-E29)) — "St. Gallen" (02-canton-list.png (pension_portal/S02-E30)) — "Thurgau" (02-canton-list.png (pension_portal/S02-E31)) — "Ticino" (02-canton-list.png (pension_portal/S02-E32)) — "Uri" (02-canton-list.png (pension_portal/S02-E33)) — "Valais" (02-canton-list.png (pension_portal/S02-E34)) — "Vaud" (02-canton-list.png (pension_portal/S02-E35)) — "Zug" (02-canton-list.png (pension_portal/S02-E36)) — "Zurich" (02-canton-list.png (pension_portal/S02-E37))
- **D-002**: Ask for the canton (pension fund 'Canton' field) only from employees living in Switzerland. Provisional - keep OQ-canton-abroad open as non-blocking, to be verified by a domain expert and Pensionskasse Muster (what to enter for employees living abroad, and whether 'Canton' means residence or work).

## OQ-civil-status-partnership
**How does Pensionskasse Muster want registered partnerships and separated employees entered, given its list offers only Single, Married, Divorced, Widowed?**

Provisionally both are entered as Married with the partner's/spouse's date of birth; a wrong mapping gives wrong registrations (the case occurs: Daniel).

Options:
- Keep provisional mapping (both as Married)
- Separated as another value
- The fund adds values

**Recommendation:** Keep D-003 provisional mapping; domain expert verifies with the fund.

Affects: Civil status, Civil status entered at the pension fund, Spouse's / registered partner's date of birth
- **F-hr_transcript-f197d6**: Anna does not know how the pension fund's screen handles a registered partnership, or whether the fund wants the partner's details (for example, date of birth). — "I honestly don't know what the fund's screen does in that case, or if they want the partner's details too." (hr_transcript/T-036, Anna)
- **F-hr_transcript-3907fe**: At least one current employee (Daniel, finance) is in a registered partnership, so this case occurs. — "we do have one colleague in a registered partnership. Daniel, in finance." (hr_transcript/T-034, Anna)
- **F-pension_portal-3d1ae4**: The Civil status dropdown offers exactly these options: Single, Married, Divorced, Widowed. — "Civil status" (03-civil-status-list.png (pension_portal/S03-E19)) — "Single" (03-civil-status-list.png (pension_portal/S03-E21)) — "Married" (03-civil-status-list.png (pension_portal/S03-E22)) — "Divorced" (03-civil-status-list.png (pension_portal/S03-E23)) — "Widowed" (03-civil-status-list.png (pension_portal/S03-E24))
- **D-003**: Civil status offers Single, Married, Divorced, Widowed, Registered partnership and Separated. For source tax, registered partnership counts as married (including the spouse exemption) and separated counts as single, as in the calculator. For the pension fund, provisionally, registered partnership is entered as Married with the partner's date of birth, and separated as Married. Keep OQ-civil-status-partnership open as non-blocking, to be verified by a domain expert.
- **D-004**: The spouse's (or registered partner's) date of birth is asked from married employees, registered partners and separated employees (all entered at the fund as Married, see D-003), not from divorced or widowed employees. Keep OQ-spouse-dob-other-status open as non-blocking, to be verified by a domain expert (screenshot of the fund's screen). This closes OQ-separated-spouse-dob; the separated case is verified together with OQ-civil-status-partnership.

## OQ-spouse-dob-other-status
**Does the fund's screen ask for a spouse's date of birth (or other fields) when civil status is Divorced or Widowed?**

No screenshot shows these states; if the fund requires data there, registration would be blocked.

Options:
- No extra field (current assumption)
- Extra field required - add a question

**Recommendation:** Get a screenshot of the fund's screen for Divorced and Widowed.

Affects: Spouse's / registered partner's date of birth
- **F-pension_portal-6d3630**: No screenshot shows the form with Civil status 'Divorced' or 'Widowed'; it is unknown whether Spouse's date of birth (or any other field) appears for those values. — "Divorced" (03-civil-status-list.png (pension_portal/S03-E23)) — "Widowed" (03-civil-status-list.png (pension_portal/S03-E24))
- **D-004**: The spouse's (or registered partner's) date of birth is asked from married employees, registered partners and separated employees (all entered at the fund as Married, see D-003), not from divorced or widowed employees. Keep OQ-spouse-dob-other-status open as non-blocking, to be verified by a domain expert (screenshot of the fund's screen). This closes OQ-separated-spouse-dob; the separated case is verified together with OQ-civil-status-partnership.

## OQ-calculator-coverage
**Does Lonio's computed tariff code match the calculator for the paths not explored: residence block for A/B/H tariffs, more than 3 children, H3N/P3N, and the per-child results marked as inferred?**

Lonio now owns the tariff result; unverified paths could produce wrong tariff codes.

Options:
- Domain expert compares computed codes with the calculator before go-live

**Recommendation:** Go-live condition per D-009: compare all inferred rows of child_result and the cross-border paths.

Affects: Per-child result, Child digit of the tariff code, Base tariff letter, Final tariff letter, Cross-border (Grenzgänger) tariff applies, Source tax tariff code
- **F-zh_source_tax_calculator-66732c**: The residence/cross-border block was explored exhaustively only for married + Y + 1 child and for Ersatzeinkünfte; for tariffs A/B/H it was only spot-checked. — "For A/B/H it was spot-checked only via DE daily return + certificate (L0Y, L1N, M0N, M0Y, P1Y, P3N) and LI more than 45 days / Anderes Land (A0N)." (zh_source_tax_calculator/C-N05)
- **F-zh_source_tax_calculator-332e2a**: The full cross-product of child paths × residence paths × confession × civil status was not enumerated. — "The full cross-product of child paths × residence paths × confession × civil status was not enumerated (combinatorial)." (zh_source_tax_calculator/C-N06)
- **F-zh_source_tax_calculator-4957f6**: Not tested: more than 3 children (upper limit unknown), whether 'Kind löschen' recomputes correctly, and tariff D or other special tariffs. — "Not tested: more than 3 children (the upper limit of 'Ein weiteres Kind erfassen' is unknown); whether 'Kind löschen' recomputes correctly; tariff D or other special tariffs (none appeared in any path)." (zh_source_tax_calculator/C-N07)
- **F-zh_source_tax_calculator-953e8c**: A hidden 'Beispiele' area shows example tariff tags H3N and P3N, which were not used as inputs. — "A visually hidden 'Beispiele' area shows the tags H3N and P3N." (zh_source_tax_calculator/C-N03)
- **D-009**: Before go-live a domain expert compares Lonio's computed tariff code with the calculator for the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N). Special tariffs such as D (second job) are out of scope for onboarding. Keep OQ-calculator-coverage open as a non-blocking go-live condition.

## OQ-source-tax-rule-confirmation
**Is HR's final source tax liability rule complete, and does 'lives here' mean lives in Switzerland?**

Anna hedged ('I think so') and added conditions several times; the rule decides who is asked the source tax questions.

Options:
- Confirm as modelled
- HR adds further conditions

**Recommendation:** Confirm the decision table of subject_to_source_tax with HR.

Affects: Subject to source tax, Spouse's / registered partner's country of residence
- **F-hr_transcript-550840**: Leo summarised the rule as 'non-Swiss, but not with a C permit'. Anna only answered 'I think so' (hedged), and later added more conditions. — "Okay, so non-Swiss, but not with a C permit. Is that everything?" (hr_transcript/T-039, Leo) — "I think so." (hr_transcript/T-040, Anna)
- **F-hr_transcript-5af8d0**: Consolidated final rule. An employee who lives abroad (outside Switzerland) is subject to source tax regardless of nationality. An employee who lives in Switzerland is subject only if they are non-Swiss without a C permit and are not married to a Swiss national or C-permit holder who lives in Switzerland. Note: Anna said 'here', which is read as Switzerland. Her 'I think' hedges remain. — "If you don't have a Swiss passport, you do source tax." (hr_transcript/T-010, Anna) — "So, not the people with a C permit. They're treated like Swiss people for this." (hr_transcript/T-038, Anna) — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (hr_transcript/T-044, Anna) — "Those people do source tax because they work here and they don't live here." (hr_transcript/T-048, Anna) — "Yes." (hr_transcript/T-050, Anna)
- **F-hr_transcript-54d011**: The spouse's nationality, permit and residence only matter for source tax when the employee is married. They are presumably only needed when the employee would otherwise be subject to source tax (non-Swiss, no C permit, living in Switzerland). — "it also changes who has to do it at all." (hr_transcript/T-044, Anna) — "then you don't do source tax either." (hr_transcript/T-044, Anna)

