# Open questions

What the sources do not settle. Each needs a product decision or a
clarification with the stakeholder. Until then, follow the recommendation.

## OQ-calculator-coverage
**Does Lonio's computed tariff code match the Zurich calculator for the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N examples, inferred per-child rows)?**

Lonio now owns the tariff result; unexplored or inferred paths could produce wrong codes.

Options:
- Domain expert compares computed codes with the calculator before go-live
- Ship and correct afterwards

**Recommendation:** Non-blocking for the spec, but a go-live condition: domain expert comparison before release.

Affects: Source tax tariff code, Per-child result, Child digit, Base tariff letter, Cross-border tariff applies
- **F-zh_source_tax_calculator-66732c**: The residence/cross-border block was explored exhaustively only for married + Y + 1 child and for Ersatzeinkünfte; for tariffs A/B/H it was only spot-checked. — "For A/B/H it was spot-checked only via DE daily return + certificate (L0Y, L1N, M0N, M0Y, P1Y, P3N) and LI more than 45 days / Anderes Land (A0N)." (zh_source_tax_calculator/C-N05)
- **F-zh_source_tax_calculator-332e2a**: The full cross-product of child paths × residence paths × confession × civil status was not enumerated. — "The full cross-product of child paths × residence paths × confession × civil status was not enumerated (combinatorial)." (zh_source_tax_calculator/C-N06)
- **F-zh_source_tax_calculator-4957f6**: Not tested: more than 3 children (upper limit unknown), whether 'Kind löschen' recomputes correctly, and tariff D or other special tariffs. — "Not tested: more than 3 children (the upper limit of 'Ein weiteres Kind erfassen' is unknown); whether 'Kind löschen' recomputes correctly; tariff D or other special tariffs (none appeared in any path)." (zh_source_tax_calculator/C-N07)
- **F-zh_source_tax_calculator-953e8c**: A hidden 'Beispiele' area shows example tariff tags H3N and P3N, which were not used as inputs. — "A visually hidden 'Beispiele' area shows the tags H3N and P3N." (zh_source_tax_calculator/C-N03)
- **D-009**: Before go-live a domain expert compares Lonio's computed tariff code with the calculator for the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N). Special tariffs such as D (second job) are out of scope for onboarding. Keep OQ-calculator-coverage open as a non-blocking go-live condition.
- **D-046**: For the per-child source tax result, observed calculator table rows win over the derived expression. Inferred rows stay under the D-009 go-live check. Assumption - to be verified by a domain expert; state this assumption in the user story.

## OQ-hr-side-follow-ups
**How does HR see the Liechtenstein DTA flag and change the first working day or other answers after submission?**

Several decisions rely on HR acting after submission; this belongs to the later HR-side spec.

Options:
- Specify in the HR-side spec

**Recommendation:** Note for the later HR-side spec; not blocking the questionnaire.

Affects: Liechtenstein: in principle no source tax liability, First working day, Read-only after submission
- **D-034**: Only the employee side is in scope. Who starts the onboarding and any HR screen are specified later; the spec says answers are recorded for HR, not 'available to HR'. HR-side needs from D-007 (flag) and D-033 (HR changes the date) are noted for that later spec.
- **D-007**: Liechtenstein residents are asked the source tax questions (HR's rule decides who is asked). The result follows the calculator - with daily return or at most 45 non-return days, Lonio shows 'in principle no source tax liability, subject to the double taxation agreement' instead of a tariff code, flagged for HR; with more than 45 non-return days, the normal tariff code. This closes OQ-liechtenstein-conflict. To be verified by a domain expert.
- **D-033**: The employee enters the first working day. After submission only HR can change it; the latest date always counts and no history of earlier dates is kept.
- **D-037**: After submission the questionnaire is read-only for the employee. Any later change (a move, a marriage, a new child, a certificate of residence handed in later, a corrected nationality) is made by HR and belongs to the later HR-side spec (D-034). Every derived result (insurance start date, civil status for the fund and for source tax, subject to source tax, tariff code) is always derived again from the latest answers, as for the first working day (D-033).

