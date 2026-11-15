# Prototype changes, 15 Nov 2026

The previous build (commit 6ff2df9, 14 Nov) followed the spec with 28 stories. This build
follows the spec after decisions D-039 to D-054: 40 stories, verdict "ready with caveats".

## What the employee sees differently

| Change | Before | Now | Why |
|---|---|---|---|
| Step order | 7 steps: personal details, address, nationality, employment, family, source tax, review | 8 steps: about you (incl. first working day), address, nationality and C permit, civil status and spouse, cross-border commuting, source tax details, children, summary | D-047 fixes one step order |
| First working day | own step 4 | in step 1, with the hint that it is the contractual start date, even on a weekend or holiday | D-047, D-039 |
| Spouse questions | "In which country does your spouse live?" (country list); nationality only if the spouse lives in Switzerland | "Does your spouse live in Switzerland?" (yes/no); nationality and C permit asked regardless | D-050 (data minimisation) |
| Germany and Liechtenstein questions | at the end of the source tax step | own step 5, before denomination, spouse and children | D-040, D-047 |
| Liechtenstein, daily return or at most 45 non-return days | denomination, spouse and children still asked | source tax details and children skipped | D-040 |
| Liechtenstein, more than 45 days | code shown "subject to the double taxation agreement" | plain code (e.g. C1Y), DTA note recorded next to it and flagged for HR | D-054 |
| Children | inside the source tax step | own step 7, "no maximum number of children" | D-044, D-047 |
| House number | free text, required | required, or tick "My address has no house number" | D-042, D-049 |
| Date checks | valid DD.MM.YYYY only | also: age 14 to 100 on the first working day; first working day within one year after the questionnaire was sent | D-050 |
| Nationality list | countries | countries plus "stateless" | D-050 |
| Wording | "Of age and in first education", "The employee / The other parent", "Christian Catholic" | "Adult in first education", "Myself / Other parent", "Christ Catholic" | spec vocabulary |
| Submit | "Submit" | "Confirm and submit" on the summary, with a note that answers can't be changed afterwards | US-01.8, D-050 |

## What is recorded differently

- **Pension fund canton**: for employees living abroad it is now Zurich, the canton of the
  place of work (D-002, assumption). Before it was left empty.
- **Source tax result** for Liechtenstein >45 days carries a separate DTA note and an HR flag
  instead of a "subject to DTA" marker on the code.

## Unchanged

Insurance start date, the per-child decision table, the child digit, the base and
cross-border tariff letters, the church-tax suffix, source tax liability (apart from the new
spouse residence question), the permit reminder, discarding answers that no longer apply,
and read-only after submission all still follow the same rules. The 268 spec examples
confirm this.

## How it is tested now

The old test file copied the example tables of the 28-story spec by hand (148 tests).
It is replaced by `tests/spec-examples.test.ts`, which reads all 268 examples from the
pipeline output and runs them against the prototype, plus 7 checks in
`tests/validation.test.ts` for rules the spec states only as text. 276 tests pass, the
type check and the production build pass, and a browser click-through (Germany, single,
one child, daily return with certificate) ends with tariff code P1N, as the spec expects.
