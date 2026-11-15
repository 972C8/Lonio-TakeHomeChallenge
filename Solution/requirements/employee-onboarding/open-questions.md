# Open questions

What the sources do not settle. Each needs a product decision or a
clarification with the stakeholder. Until then, follow the recommendation.

## OQ-calculator-coverage
**Does Lonio's computed tariff code match the Zurich calculator for the unexplored paths: the residence block for tariffs A/B/H, the inferred per-child rows, more than 3 children, and the H3N/P3N examples?**

Lonio now owns the tariff result instead of HR clicking through the calculator; unverified paths could produce wrong source tax codes.

Options:
- Domain expert compares computed codes with the calculator for the listed paths before go-live
- Go live and fall back to HR's manual check for unexplored paths

**Recommendation:** Domain expert check before go-live (D-009); observed rows win over derived ones (D-046).

Affects: Per-child result, Number of counted children (child digit), Base tariff letter, Cross-border (Grenzgänger) tariff applies, Tariff letter, Full source tax tariff code
- **F-zh_source_tax_calculator-66732c**: The residence/cross-border block was explored exhaustively only for married + Y + 1 child and for Ersatzeinkünfte; for tariffs A/B/H it was only spot-checked. — "For A/B/H it was spot-checked only via DE daily return + certificate (L0Y, L1N, M0N, M0Y, P1Y, P3N) and LI more than 45 days / Anderes Land (A0N)." (zh_source_tax_calculator/C-N05)
- **F-zh_source_tax_calculator-332e2a**: The full cross-product of child paths × residence paths × confession × civil status was not enumerated. — "The full cross-product of child paths × residence paths × confession × civil status was not enumerated (combinatorial)." (zh_source_tax_calculator/C-N06)
- **F-zh_source_tax_calculator-4957f6**: Not tested: more than 3 children (upper limit unknown), whether 'Kind löschen' recomputes correctly, and tariff D or other special tariffs. — "Not tested: more than 3 children (the upper limit of 'Ein weiteres Kind erfassen' is unknown); whether 'Kind löschen' recomputes correctly; tariff D or other special tariffs (none appeared in any path)." (zh_source_tax_calculator/C-N07)
- **F-zh_source_tax_calculator-953e8c**: A hidden 'Beispiele' area shows example tariff tags H3N and P3N, which were not used as inputs. — "A visually hidden 'Beispiele' area shows the tags H3N and P3N." (zh_source_tax_calculator/C-N03)
- **D-009**: Before go-live a domain expert compares Lonio's computed tariff code with the calculator for the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N). Special tariffs such as D (second job) are out of scope for onboarding. Keep OQ-calculator-coverage open as a non-blocking go-live condition.
- **D-046**: For the per-child source tax result, observed calculator table rows win over the derived expression. Inferred rows stay under the D-009 go-live check. Assumption - to be verified by a domain expert; state this assumption in the user story.

