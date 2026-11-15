# Open questions

What the sources do not settle. Each needs a product decision or a
clarification with the stakeholder. Until then, follow the recommendation.

## OQ-registered-partnership
**How should an employee in a registered partnership answer civil status, and do the pension fund and the source tax spouse exemption treat them like married employees (partner's date of birth, partner's nationality/permit/residence)?** _(blocking)_

The pension fund list (Single, Married, Divorced, Widowed) has no registered partnership, but the calculator groups it with married, and such employees exist (Daniel). Without an answer they cannot be registered correctly.

Options:
- Ask them to choose 'Married' and treat them as married everywhere
- Ask the pension fund how to register them and keep a separate answer for source tax
- Ask HR to handle it manually

**Recommendation:** Ask Pensionskasse Muster via HR. Until then, treat registered partners as Married for both parties, because the calculator explicitly groups them together.

Affects: Civil status, Spouse's date of birth, Spouse's nationality, Spouse's permit type, Spouse's country of residence, Employee is subject to source tax, Civil status answer for the source tax calculator
- **F-hr_transcript-3907fe**: At least one current employee (Daniel, finance) is in a registered partnership, so this case occurs. — "we do have one colleague in a registered partnership. Daniel, in finance." (hr_transcript/T-034, Anna)
- **F-hr_transcript-f197d6**: Anna does not know how the pension fund's screen handles a registered partnership, or whether the fund wants the partner's details (for example, date of birth). — "I honestly don't know what the fund's screen does in that case, or if they want the partner's details too." (hr_transcript/T-036, Anna)
- **F-pension_portal-3d1ae4**: The Civil status dropdown offers exactly these options: Single, Married, Divorced, Widowed. — "Civil status" (03-civil-status-list.png (pension_portal/S03-E19)) — "Single" (03-civil-status-list.png (pension_portal/S03-E21)) — "Married" (03-civil-status-list.png (pension_portal/S03-E22)) — "Divorced" (03-civil-status-list.png (pension_portal/S03-E23)) — "Widowed" (03-civil-status-list.png (pension_portal/S03-E24))
- **F-zh_source_tax_calculator-051bb9**: Civil status options are exactly two groups: 'Verheiratet oder eingetragene Partnerschaft' (married or registered partnership) and 'Ledig, Geschieden, Getrennt, Verwitwet' (single, divorced, separated, widowed). — "Options: Verheiratet oder eingetragene Partnerschaft | Ledig, Geschieden, Getrennt, Verwitwet" (zh_source_tax_calculator/C-Q02)
- **G-07**: The pension fund screenshots show dropdowns with **all** their options.

## OQ-separated
**Which civil status should a separated (still married) employee choose? The calculator groups 'separated' with single, but the pension fund has no such option.**

A separated employee would pick Married for the pension fund and get the married source tax path, which may differ from the calculator's grouping.

Options:
- Married for both
- Married for the pension fund, plus an extra 'separated' question for source tax only

**Recommendation:** Confirm with HR. Do not add a question until then.

Affects: Civil status, Civil status answer for the source tax calculator
- **F-zh_source_tax_calculator-051bb9**: Civil status options are exactly two groups: 'Verheiratet oder eingetragene Partnerschaft' (married or registered partnership) and 'Ledig, Geschieden, Getrennt, Verwitwet' (single, divorced, separated, widowed). — "Options: Verheiratet oder eingetragene Partnerschaft | Ledig, Geschieden, Getrennt, Verwitwet" (zh_source_tax_calculator/C-Q02)
- **F-pension_portal-3d1ae4**: The Civil status dropdown offers exactly these options: Single, Married, Divorced, Widowed. — "Civil status" (03-civil-status-list.png (pension_portal/S03-E19)) — "Single" (03-civil-status-list.png (pension_portal/S03-E21)) — "Married" (03-civil-status-list.png (pension_portal/S03-E22)) — "Divorced" (03-civil-status-list.png (pension_portal/S03-E23)) — "Widowed" (03-civil-status-list.png (pension_portal/S03-E24))

## OQ-divorced-widowed
**Does the pension fund ask for any spouse data when civil status is Divorced or Widowed?**

No screenshot shows these cases. Asking too little could block the registration.

Options:
- No extra fields (as for Single)
- Spouse's date of birth also appears

**Recommendation:** Assume no extra fields. Verify with a screenshot of these two cases.

Affects: Spouse's date of birth
- **F-pension_portal-6d3630**: No screenshot shows the form with Civil status 'Divorced' or 'Widowed'; it is unknown whether Spouse's date of birth (or any other field) appears for those values. — "Divorced" (03-civil-status-list.png (pension_portal/S03-E23)) — "Widowed" (03-civil-status-list.png (pension_portal/S03-E24))

## OQ-canton
**Does the pension fund's 'Canton' mean canton of residence or of work, and what is entered for employees who live abroad (Germany, Liechtenstein)?** _(blocking)_

The field is required, but the list only has the 26 Swiss cantons. Cross-border employees could not be registered.

Options:
- Canton of residence; ask the fund what to enter for residents abroad
- Canton of work (e.g. Zurich), so it is not asked of the employee

**Recommendation:** Ask Pensionskasse Muster. Meanwhile ask the canton only of Swiss residents.

Affects: Canton of residence
- **F-pension_portal-b359c3**: The portal does not say whether 'Canton' means canton of residence or of work, and the list offers no option for employees living outside Switzerland; how to register such employees is unknown. — "Canton" (01-empty.png (pension_portal/S01-E10)) — "Zurich" (02-canton-list.png (pension_portal/S02-E37))
- **F-pension_portal-3432a9**: The Canton dropdown offers exactly these 26 options: Aargau, Appenzell Ausserrhoden, Appenzell Innerrhoden, Basel-Landschaft, Basel-Stadt, Bern, Fribourg, Geneva, Glarus, Graubünden, Jura, Lucerne, Neuchâtel, Nidwalden, Obwalden, Schaffhausen, Schwyz, Solothurn, St. Gallen, Thurgau, Ticino, Uri, Valais, Vaud, Zug, Zurich. There is no option for a residence outside Switzerland. — "Canton" (02-canton-list.png (pension_portal/S02-E10)) — "Aargau" (02-canton-list.png (pension_portal/S02-E12)) — "Appenzell Ausserrhoden" (02-canton-list.png (pension_portal/S02-E13)) — "Appenzell Innerrhoden" (02-canton-list.png (pension_portal/S02-E14)) — "Basel-Landschaft" (02-canton-list.png (pension_portal/S02-E15)) — "Basel-Stadt" (02-canton-list.png (pension_portal/S02-E16)) — "Bern" (02-canton-list.png (pension_portal/S02-E17)) — "Fribourg" (02-canton-list.png (pension_portal/S02-E18)) — "Geneva" (02-canton-list.png (pension_portal/S02-E19)) — "Glarus" (02-canton-list.png (pension_portal/S02-E20)) — "Graubünden" (02-canton-list.png (pension_portal/S02-E21)) — "Jura" (02-canton-list.png (pension_portal/S02-E22)) — "Lucerne" (02-canton-list.png (pension_portal/S02-E23)) — "Neuchâtel" (02-canton-list.png (pension_portal/S02-E24)) — "Nidwalden" (02-canton-list.png (pension_portal/S02-E25)) — "Obwalden" (02-canton-list.png (pension_portal/S02-E26)) — "Schaffhausen" (02-canton-list.png (pension_portal/S02-E27)) — "Schwyz" (02-canton-list.png (pension_portal/S02-E28)) — "Solothurn" (02-canton-list.png (pension_portal/S02-E29)) — "St. Gallen" (02-canton-list.png (pension_portal/S02-E30)) — "Thurgau" (02-canton-list.png (pension_portal/S02-E31)) — "Ticino" (02-canton-list.png (pension_portal/S02-E32)) — "Uri" (02-canton-list.png (pension_portal/S02-E33)) — "Valais" (02-canton-list.png (pension_portal/S02-E34)) — "Vaud" (02-canton-list.png (pension_portal/S02-E35)) — "Zug" (02-canton-list.png (pension_portal/S02-E36)) — "Zurich" (02-canton-list.png (pension_portal/S02-E37))
- **F-hr_transcript-b582c0**: A few employees live across the border, for example Stefan in Konstanz (Germany) and a warehouse employee in Liechtenstein. — "We have a few who live across the border. Stefan lives in Konstanz, and there's a woman in the warehouse who lives in Liechtenstein." (hr_transcript/T-048, Anna)

## OQ-permit-list
**Which permit types should the employee and spouse be able to choose from, and how does a spouse without any permit answer?**

No source lists the permits. Only 'C permit' changes the outcome, but the employee needs a list they recognise.

Options:
- Full list from HR
- 'C permit' / 'Other permit' / 'No permit'

**Recommendation:** Ask HR for the list it uses. The rule only needs to tell C permit apart from other permits.

Affects: Permit type, Spouse's permit type
- **F-hr_transcript-c9d9b9**: The permit type of non-Swiss employees is needed to decide source tax liability (a C permit exempts them). The permit type is only relevant for non-Swiss employees. — "So, not the people with a C permit." (hr_transcript/T-038, Anna)
- **F-hr_transcript-76eacc**: For source tax, HR needs the spouse's permit, if the spouse has one. — "their permit if they have one" (hr_transcript/T-046, Anna)

## OQ-source-tax-rule
**Is the consolidated source tax rule complete and does 'here' mean Switzerland? HR hedged ('I think so') before adding further conditions.**

The rule decides who sees the whole source tax section and the spouse questions. A wrong rule asks Swiss employees too much or misses people who are subject.

Options:
- Confirm the rule as modelled
- HR adds more conditions

**Recommendation:** Have HR confirm the decision table of subject_to_source_tax.

Affects: Employee is subject to source tax, Nationality, Permit type, Spouse's nationality, Spouse's permit type, Spouse's country of residence
- **F-hr_transcript-550840**: Leo summarised the rule as 'non-Swiss, but not with a C permit'. Anna only answered 'I think so' (hedged), and later added more conditions. — "Okay, so non-Swiss, but not with a C permit. Is that everything?" (hr_transcript/T-039, Leo) — "I think so." (hr_transcript/T-040, Anna)
- **F-hr_transcript-5af8d0**: Consolidated final rule. An employee who lives abroad (outside Switzerland) is subject to source tax regardless of nationality. An employee who lives in Switzerland is subject only if they are non-Swiss without a C permit and are not married to a Swiss national or C-permit holder who lives in Switzerland. Note: Anna said 'here', which is read as Switzerland. Her 'I think' hedges remain. — "If you don't have a Swiss passport, you do source tax." (hr_transcript/T-010, Anna) — "So, not the people with a C permit. They're treated like Swiss people for this." (hr_transcript/T-038, Anna) — "If you're married to someone Swiss, or to someone with a C permit, and that person lives here, then you don't do source tax either." (hr_transcript/T-044, Anna) — "Those people do source tax because they work here and they don't live here." (hr_transcript/T-048, Anna) — "Yes." (hr_transcript/T-050, Anna)

## OQ-dual-nationality
**How should employees with several nationalities, one of them Swiss, answer the nationality question?**

HR's rule is 'Swiss passport'. Dual nationals could pick their other nationality and be wrongly sent the source tax questions.

Options:
- Ask 'Do you hold Swiss citizenship?' first
- Allow several nationalities

**Recommendation:** Confirm with HR that any Swiss citizenship counts as Swiss.

Affects: Nationality, Spouse's nationality, Employee is subject to source tax
- **F-hr_transcript-b0527c**: First version: all non-Swiss employees (anyone without a Swiss passport) are subject to source tax. — "All the non-Swiss employees. Simple as that. If you don't have a Swiss passport, you do source tax." (hr_transcript/T-010, Anna)

## OQ-income-type
**Is a new employee's income always earned income (Erwerbseinkommen), so the income-type question can be fixed instead of asked?**

Asking a new hire about replacement income is confusing and collects unnecessary data. Fixing it also removes the replacement-income cross-border variants.

Options:
- Fix to 'Earned income' (product decision)
- Ask the employee

**Recommendation:** Fix to earned income by product decision. Until then it is modelled as asked.

Affects: Type of income (source tax), Religious denomination (church tax), Spouse works or receives replacement income, Has biological or adopted children, Returns daily to the home in Germany, Daily return reasonable (under 100 km), Proof of more than 60 work-related non-return days, Returns daily to the home in Liechtenstein, More than 45 work-related non-return days
- **F-zh_source_tax_calculator-e06ffd**: The calculator asks which income the source tax tariff is to be determined for. — "Für welche Einkünfte möchten Sie den Quellensteuertarif ermitteln?" (zh_source_tax_calculator/C-Q01)
- **F-zh_source_tax_calculator-351289**: If the income type is Ersatzeinkünfte, all personal and child questions are skipped and the calculator goes straight to the main-residence question (Q16). — "Ersatzeinkünfte skips all personal/child questions and goes straight to Q16." (zh_source_tax_calculator/C-Q01)
- **G-08**: Prefer asking for primary facts and **deriving** values (e.g. ask the first working day, derive the insurance start date) instead of asking the employee for values they cannot know.

## OQ-liechtenstein
**HR says everyone living abroad is subject to source tax, but the calculator can return 'in principle no source tax liability' for Liechtenstein residents. Which result counts?**

It affects what HR does after the questionnaire. It does not change which questions are asked.

Options:
- Calculator result is final
- HR decides case by case

**Recommendation:** Keep asking these employees all source tax questions and let the calculator result decide. Confirm with HR.

Affects: Employee is subject to source tax, Returns daily to the home in Liechtenstein, More than 45 work-related non-return days
- **F-hr_transcript-3f2c2a**: Employees who work here but live abroad (examples: Konstanz in Germany, Liechtenstein) are always subject to source tax, regardless of nationality. Even a Swiss citizen living abroad (Stefan) is subject. — "Those people do source tax because they work here and they don't live here." (hr_transcript/T-048, Anna) — "And there it doesn't matter what passport you have, by the way. Stefan is actually Swiss, and he still has it." (hr_transcript/T-048, Anna) — "So someone living abroad and working here always does it?" (hr_transcript/T-049, Leo) — "Yes." (hr_transcript/T-050, Anna)
- **F-zh_source_tax_calculator-fb87f1**: Liechtenstein residents with daily return, or without daily return and not more than 45 non-return days, get 'Grundsätzlich keine Quellensteuerpflicht' (in principle no source tax liability), subject to the double taxation agreement. — "Ja -> 'Grundsätzlich keine Quellensteuerpflicht'" (zh_source_tax_calculator/C-Q22) — ""Q22": "Ja"} -> result Grundsätzlich keine Quellensteuerpflicht / Unter Vorbehalt des Doppelbesteuerungsabkommens" (zh_source_tax_calculator/C-V39) — ""Q23": "Nein"} -> result Grundsätzlich keine Quellensteuerpflicht" (zh_source_tax_calculator/C-V41) — ""Q27": "Ja"} -> result Grundsätzlich keine Quellensteuerpflicht" (zh_source_tax_calculator/C-V49)
- **F-zh_source_tax_calculator-cc19c7**: Liechtenstein residents without daily return and more than 45 non-return days get the normal tariff plus 'Unter Vorbehalt des Doppelbesteuerungsabkommens'. — "Ja -> normal tariff + 'Unter Vorbehalt des Doppelbesteuerungsabkommens'" (zh_source_tax_calculator/C-Q23) — "result Tarif: C1Y / Unter Vorbehalt des Doppelbesteuerungsabkommens" (zh_source_tax_calculator/C-V40) — "result Tarif: G / Unter Vorbehalt des Doppelbesteuerungsabkommens" (zh_source_tax_calculator/C-V50)

## OQ-proof-documents
**Can a new employee answer 'certificate of residence provided' and 'proof of more than 60 non-return days provided' before starting? To whom are these documents provided?**

These questions ask about documents, possibly the 'German forms' HR mentioned. The employee may not have them yet.

Options:
- Ask as yes/no and let HR collect the documents
- Ask whether the employee will provide them

**Recommendation:** Ask HR how this works today for Stefan.

Affects: Certificate of residence provided, Proof of more than 60 work-related non-return days
- **F-hr_transcript-8595fb**: For employees living abroad, the calculator asks more questions, and Germany has its own forms. Anna cannot remember what they are called. Leo deferred to the calculator, so the exact questions are unresolved in this transcript. — "And with them the calculator gets much more complicated, there are more questions. Germany has its own forms, I can never remember what they're called." (hr_transcript/T-050, Anna) — "Okay, that's fine, the calculator will tell us." (hr_transcript/T-051, Leo)
- **F-zh_source_tax_calculator-687e8b**: The calculator asks whether a certificate of residence (Ansässigkeitsbescheinigung) has been provided. — "Ansässigkeitsbescheinigung beigebracht?" (zh_source_tax_calculator/C-Q19)
- **F-zh_source_tax_calculator-e8ffac**: The calculator asks whether proof of more than 60 work-related non-return days in the calendar year has been provided. — "Nachweis von mehr als 60 beruflich bedingten Nichtrückkehrtagen im Kalenderjahr beigebracht?" (zh_source_tax_calculator/C-Q21)

## OQ-calculator-coverage
**Do the child and cross-border paths behave as modelled for every combination? The calculator was only spot-checked for A/B/H cross-border tariffs, more than 3 children, deleting children and special tariffs (e.g. D).**

Untested paths could need more questions.

Options:
- Explore the remaining paths
- Accept the current coverage

**Recommendation:** Accept for the questionnaire (the question conditions are explicit). Explore further only if the tariff is computed by Lonio.

Affects: Has biological or adopted children, Child: minor or adult in first education, Base tariff letter (source tax)
- **F-zh_source_tax_calculator-66732c**: The residence/cross-border block was explored exhaustively only for married + Y + 1 child and for Ersatzeinkünfte; for tariffs A/B/H it was only spot-checked. — "For A/B/H it was spot-checked only via DE daily return + certificate (L0Y, L1N, M0N, M0Y, P1Y, P3N) and LI more than 45 days / Anderes Land (A0N)." (zh_source_tax_calculator/C-N05)
- **F-zh_source_tax_calculator-332e2a**: The full cross-product of child paths × residence paths × confession × civil status was not enumerated. — "The full cross-product of child paths × residence paths × confession × civil status was not enumerated (combinatorial)." (zh_source_tax_calculator/C-N06)
- **F-zh_source_tax_calculator-4957f6**: Not tested: more than 3 children (upper limit unknown), whether 'Kind löschen' recomputes correctly, and tariff D or other special tariffs. — "Not tested: more than 3 children (the upper limit of 'Ein weiteres Kind erfassen' is unknown); whether 'Kind löschen' recomputes correctly; tariff D or other special tariffs (none appeared in any path)." (zh_source_tax_calculator/C-N07)

## OQ-permit-reminder
**Should the questionnaire remind employees to bring their permit on the first day, and with which wording?**

HR asked for it, but Leo deferred the wording, so it is undecided.

Options:
- Add a reminder for non-Swiss employees
- Leave it out

**Recommendation:** Product owner to decide. It adds no data collection.

Affects: Permit type
- **F-hr_transcript-c53552**: HR would love the form to remind employees to bring their permit on the first day, because half of them forget. Leo deferred the wording, so this is not decided. — "What I would love is if the form could remind people to bring their permit. Half of them forget." (hr_transcript/T-042, Anna) — "We can look at the wording later." (hr_transcript/T-043, Leo)

## OQ-spouse-residence-form
**Should the spouse's residence be asked as a country or only as 'lives in Switzerland: yes/no'?**

Only whether the spouse lives in Switzerland matters, and data minimisation favours the narrower question.

Options:
- Country
- yes/no

**Recommendation:** Ask yes/no 'Does your spouse live in Switzerland?' if the product owner agrees.

Affects: Spouse's country of residence
- **F-hr_transcript-e5337d**: For source tax, HR needs to know whether the spouse lives 'here'. — "and that they live here." (hr_transcript/T-046, Anna)
- **G-01**: Lonio collects onboarding data from a new employee **once** and reuses it for every receiving party. Asking too little blocks a registration; asking too much collects personal data we must not have (data minimisation). A question must only be asked when at least one receiving party needs the answer for this person.

