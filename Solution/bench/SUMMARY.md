# Token optimisation: before / after

Branch `claude/project-thread-4flsjx` (not merged into `main`). Detailed per-stage tables: `bench/report.md`;
raw results per case: `bench/results/<label>/<case>/` (result.json, run log, review.md, spec diff).

## Result

Over the three delta cases (one new source each), tokens fell **75%** (5.85M → 1.44M) and the SDK cost
estimate **39%** ($17.98 → $10.91). Every case passed the gate: no check that held before fails after, same
verdict, all examples pass, same stories added, same open questions.

| Case | Tokens before | after | Cost before | after | Gate |
|---|---:|---:|---:|---:|---|
| B2 HR email: copy of answers | 1.69M | 0.29M (-83%) | $3.66 | $2.08 | PASS |
| B3 Fund email: 2027 rule, canton abroad | 1.88M | 0.39M (-79%) | $4.97 | $2.71 | PASS |
| B4 HR follow-up: contradicts D-007 | 2.29M | 0.77M (-67%) | $9.35 | $6.12 | PASS |
| B1 fresh full rebuild (baseline) | 2.35M | not rerun | $11.34 | - | - |

Tokens fall more than cost: most of the old tokens were cheap cache reads of the dev-refinement agent's tool loop.

## Where it came from (sum of B2-B4)

| Stage | Before | After | Change |
|---|---:|---:|---|
| Dev refinement | 4.01M tok, $5.63 | 0.34M tok, $2.96 | one call on changed files instead of a 39-turn read loop |
| Section writers | 0.78M tok, $7.26 | 0.56M tok, $5.12 | slice of the knowledge model instead of the whole model |
| Fact judge | 0.55M tok, $1.21 | 0.02M tok, $0.08 | verdicts cached per fact; only new facts judged |
| Review, flow, assign | $1.85 | $0.85 | Sonnet instead of Opus |

## Quality, before → after

- Examples executed: all pass in every run (225, 227→228, 219→220).
- Stories changed/added: identical sets before and after in all cases.
- Verdict: unchanged (not ready in all three; caused by the expected decision flags).
- Open questions: unchanged (6, 5, 5).
- Dev refinement: 1-2 more questions and 1-2 more tech-leak notes per case. In one B3 attempt the same
  2027-vs-portal question came back as blocker instead of major; the rerun rated it major again.

## Two defects the benchmark found (fixed on the branch)

1. **A "new evidence" decision flag vanished on the next rerun** without the product owner re-confirming
   anything. Now kept until `pipeline reconfirm` (unit test added). Verified: B3 + a no-op rerun keeps the flag.
2. **A no-op rerun re-ran the reviewer** because the report's impact section changed. Fixed; the no-op
   rerun after B2 and B3 now calls no agent (B4's after-run predates fix 1, which caused its rerun).

## Not caused by the optimisations, but visible now

Both before and after: B4 (an HR call that only confirms "Swiss yes/no") changes `item.nationality` and
rewrites 6 sections (8 stories); B3 also rewrites US-08.3. This drift in the knowledge-delta step is the
largest remaining cost of a delta run ($3.6 of B4's $6.1) and a quality issue, so it is the next thing to fix.

## Not done

- B1 (full rebuild) not rerun after the changes; the section-writer slice should save most there (~$2-3).
- Proposal steps 5 (knowledge delta slice), 6 (prompt order for caching), 7 and 9 not built.
- Budget used: 10 pipeline runs (about 2.5 benchmark passes, ≈ $48 SDK estimate); the 5-hour Max limit was
  hit once (B4 before was rerun after the reset).
