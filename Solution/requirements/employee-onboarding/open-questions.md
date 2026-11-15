# Open questions

What the sources do not settle. Each needs a product decision or a
clarification with the stakeholder. Until then, follow the recommendation.

## OQ-calculator-coverage
**Does Lonio's computed tariff code match the Zurich calculator on the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N, and the per-child rows marked inferred)?**

Lonio now owns the tariff result; an unchecked path could give a wrong tariff code.

Options:
- Domain expert compares computed codes with the calculator before go-live
- Accept as is

**Recommendation:** Domain expert check before go-live (go-live condition, not blocking the spec).

Affects: Source tax tariff code, Per-child source tax result, Base tariff letter, Tariff letter, Child digit of the tariff code
- **D-009**: Before go-live a domain expert compares Lonio's computed tariff code with the calculator for the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N). Special tariffs such as D (second job) are out of scope for onboarding. Keep OQ-calculator-coverage open as a non-blocking go-live condition.
- **D-046**: For the per-child source tax result, observed calculator table rows win over the derived expression. Inferred rows stay under the D-009 go-live check. Assumption - to be verified by a domain expert; state this assumption in the user story.
- **F-zh_source_tax_calculator-66732c**: The residence/cross-border block was explored exhaustively only for married + Y + 1 child and for Ersatzeinkünfte; for tariffs A/B/H it was only spot-checked. — "For A/B/H it was spot-checked only via DE daily return + certificate (L0Y, L1N, M0N, M0Y, P1Y, P3N) and LI more than 45 days / Anderes Land (A0N)." (zh_source_tax_calculator/C-N05)
- **F-zh_source_tax_calculator-332e2a**: The full cross-product of child paths × residence paths × confession × civil status was not enumerated. — "The full cross-product of child paths × residence paths × confession × civil status was not enumerated (combinatorial)." (zh_source_tax_calculator/C-N06)
- **F-zh_source_tax_calculator-4957f6**: Not tested: more than 3 children (upper limit unknown), whether 'Kind löschen' recomputes correctly, and tariff D or other special tariffs. — "Not tested: more than 3 children (the upper limit of 'Ein weiteres Kind erfassen' is unknown); whether 'Kind löschen' recomputes correctly; tariff D or other special tariffs (none appeared in any path)." (zh_source_tax_calculator/C-N07)
- **F-zh_source_tax_calculator-953e8c**: A hidden 'Beispiele' area shows example tariff tags H3N and P3N, which were not used as inputs. — "A visually hidden 'Beispiele' area shows the tags H3N and P3N." (zh_source_tax_calculator/C-N03)

## OQ-fund-divorced-widowed
**Does the pension fund form show any extra field (e.g. a former spouse's date of birth) when civil status is Divorced or Widowed?**

No screenshot shows these values; a hidden required field would block the registration.

Options:
- No extra field (current assumption, D-004)
- Extra field required - add a question

**Recommendation:** Ask the fund or HR to check the portal; proceed with D-004.

Affects: Spouse's / registered partner's date of birth, Civil status for the pension fund
- **F-pension_portal-6d3630**: No screenshot shows the form with Civil status 'Divorced' or 'Widowed'; it is unknown whether Spouse's date of birth (or any other field) appears for those values. — "Divorced" (03-civil-status-list.png (pension_portal/S03-E23)) — "Widowed" (03-civil-status-list.png (pension_portal/S03-E24))
- **D-004**: The spouse's (or registered partner's) date of birth is asked from married employees, registered partners and separated employees (all entered at the fund as Married, see D-003), not from divorced or widowed employees; no spouse data is sent to the fund for them. This closes OQ-spouse-dob-other-status and OQ-separated-spouse-dob. Assumption - to be verified by a domain expert; state this assumption in the user story.

