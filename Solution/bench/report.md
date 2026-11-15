# Benchmark: before vs after

Tokens are the SDK's counts summed over all agent calls of the run (input + output + cache read + cache write). Cost is the SDK's list-price estimate; the pipeline runs on a Max login, so it is not a bill.

## Summary

| Case | Tokens before | Tokens after | Change | Cost before | Cost after | Verdict | Gate |
|---|---:|---:|---:|---:|---:|---|---|
| B0 | 0 | 0 | - | $0.00 | $0.00 | - → - | - (not run in after) |
| B1 | 2,352,621 | 0 | - | $11.34 | $0.00 | ready_with_caveats → - | - (not run in after) |
| B2 | 1,685,896 | 285,105 | -83% | $3.66 | $2.08 | not_ready → not_ready | PASS |
| B3 | 1,875,015 | 389,817 | -79% | $4.97 | $2.71 | not_ready → not_ready | PASS |
| B4 | 2,293,896 | 768,120 | -67% | $9.35 | $6.12 | not_ready → not_ready | PASS |

## B0

**before**: no metrics

- ❌ no-op rerun calls no agent


## B1

| Stage | Calls | Tokens before | Tokens after | Cost before | Cost after |
|---|---:|---:|---:|---:|---:|
| write_section | 8 → 0 | 543,398 | 0 | $5.45 | $0.00 |
| dev_refinement | 1 → 0 | 1,175,515 | 0 | $1.84 | $0.00 |
| knowledge | 1 → 0 | 92,372 | 0 | $1.28 | $0.00 |
| judge_trace | 14 → 0 | 258,885 | 0 | $1.07 | $0.00 |
| judge_facts | 12 → 0 | 176,975 | 0 | $0.73 | $0.00 |
| plan_feature | 1 → 0 | 42,951 | 0 | $0.41 | $0.00 |
| review | 1 → 0 | 43,044 | 0 | $0.39 | $0.00 |
| flow | 1 → 0 | 19,481 | 0 | $0.18 | $0.00 |

**before**: stories changed -; added -; errors 0; examples 219/219; open questions 5; dev questions 13; verdict ready_with_caveats; 790 s

- ✅ no errors
- ✅ all examples pass: 219


## B2

| Stage | Calls | Tokens before | Tokens after | Cost before | Cost after |
|---|---:|---:|---:|---:|---:|
| dev_refinement | 1 → 1 | 1,291,538 | 90,384 | $1.67 | $0.78 |
| write_section | 1 → 1 | 74,285 | 51,320 | $0.68 | $0.45 |
| knowledge_delta | 1 → 1 | 50,000 | 49,567 | $0.43 | $0.42 |
| review | 1 → 1 | 42,884 | 43,297 | $0.36 | $0.19 |
| judge_facts | 13 → 1 | 183,146 | 6,558 | $0.22 | $0.02 |
| flow | 1 → 1 | 19,766 | 19,896 | $0.14 | $0.09 |
| plan_assign | 1 → 1 | 8,142 | 8,142 | $0.07 | $0.03 |
| extract | 1 → 1 | 6,641 | 6,627 | $0.06 | $0.06 |
| judge_trace | 1 → 1 | 9,494 | 9,314 | $0.04 | $0.03 |

**before**: stories changed -; added US-08.5; errors 1; examples 225/225; open questions 6; dev questions 16; verdict not_ready; 291 s

- ✅ no errors (other than expected flags): decisions D-036 allowed (expectation updated after the run)
- ✅ all examples pass: 225/225
- ✅ only expected stories changed: none changed
- ✅ 1-2 stories added: US-08.5
- ✅ an added story mentions ['email', 'e-mail']
- ❌ no-op rerun calls no agent (B0)

**after**: stories changed -; added US-08.5; errors 0; examples 225/225; open questions 6; dev questions 17; verdict not_ready; 174 s

- ✅ no errors (other than expected flags)
- ✅ all examples pass: 225/225
- ✅ only expected stories changed: none changed
- ✅ 1-2 stories added: US-08.5
- ✅ an added story mentions ['email', 'e-mail']
- ✅ no-op rerun calls no agent (B0)


## B3

| Stage | Calls | Tokens before | Tokens after | Cost before | Cost after |
|---|---:|---:|---:|---:|---:|
| dev_refinement | 1 → 1 | 1,334,793 | 101,610 | $1.92 | $0.85 |
| write_section | 3 → 3 | 199,306 | 122,407 | $1.66 | $1.05 |
| knowledge_delta | 1 → 1 | 51,233 | 51,429 | $0.44 | $0.39 |
| review | 1 → 1 | 44,911 | 45,314 | $0.39 | $0.19 |
| judge_facts | 13 → 1 | 184,492 | 8,261 | $0.23 | $0.03 |
| flow | 1 → 1 | 19,645 | 19,748 | $0.14 | $0.07 |
| judge_trace | 2 → 2 | 25,282 | 25,503 | $0.10 | $0.10 |
| extract | 1 → 1 | 7,393 | 7,494 | $0.07 | $0.04 |
| plan_assign | 1 → 1 | 7,960 | 8,051 | $0.02 | $0.01 |

**before**: stories changed US-01.4, US-02.2, US-08.3; added US-01.5; errors 4; examples 227/227; open questions 5; dev questions 14; verdict not_ready; 322 s

- ✅ no errors (other than expected flags)
- ✅ all examples pass: 227/227
- ❌ only expected stories changed: US-08.3
- ✅ story US-02.2 changed
- ✅ 0-1 stories added: US-01.5
- ✅ rule.insurance_start_date mentions ['2027']
- ✅ one of: open question OQ-canton-abroad closed / decision D-002 flagged for re-confirmation: decision D-002 flagged for re-confirmation
- ❌ no-op rerun calls no agent (B0)

**after**: stories changed US-01.4, US-02.2, US-08.3; added US-01.5; errors 4; examples 228/228; open questions 6; dev questions 16; verdict not_ready; 189 s

- ✅ no errors (other than expected flags)
- ✅ all examples pass: 228/228
- ❌ only expected stories changed: US-08.3
- ✅ story US-02.2 changed
- ✅ 0-1 stories added: US-01.5
- ✅ rule.insurance_start_date mentions ['2027']
- ✅ one of: open question OQ-canton-abroad closed / decision D-002 flagged for re-confirmation: decision D-002 flagged for re-confirmation
- ✅ no-op rerun calls no agent (B0)


## B4

| Stage | Calls | Tokens before | Tokens after | Cost before | Cost after |
|---|---:|---:|---:|---:|---:|
| write_section | 6 → 6 | 503,723 | 385,833 | $4.92 | $3.62 |
| dev_refinement | 1 → 1 | 1,381,345 | 152,538 | $2.04 | $1.33 |
| judge_facts | 13 → 1 | 183,250 | 7,466 | $0.76 | $0.03 |
| knowledge_delta | 1 → 1 | 55,062 | 55,283 | $0.54 | $0.46 |
| judge_trace | 4 → 4 | 97,672 | 94,306 | $0.43 | $0.38 |
| review | 1 → 1 | 45,901 | 45,667 | $0.41 | $0.19 |
| flow | 1 → 1 | 19,332 | 19,348 | $0.18 | $0.07 |
| extract | 1 → 1 | 7,611 | 7,679 | $0.08 | $0.04 |

**before**: stories changed US-01.3, US-04.1, US-04.2, US-04.3, US-05.3, US-05.4, US-05.6, US-05.7, US-06.1, US-06.2, US-08.1, US-08.2, US-08.4; added -; errors 10; examples 219/219; open questions 5; dev questions 14; verdict not_ready; 460 s

- ✅ no errors (other than expected flags)
- ✅ all examples pass: 219/219
- ❌ only expected stories changed: US-01.3, US-05.3, US-05.4, US-06.1, US-06.2, US-08.1, US-08.2, US-08.4
- ✅ 0-0 stories added: none
- ✅ item.daily_return_liechtenstein still exists
- ✅ item.non_return_days_45 still exists
- ✅ rule.liechtenstein_no_source_tax_in_principle still exists
- ✅ item.daily_return_liechtenstein unchanged in behaviour
- ✅ item.non_return_days_45 unchanged in behaviour
- ❌ item.nationality unchanged in behaviour
- ✅ (soft) one of: decision D-007 flagged for re-confirmation / new or changed open question mentions ['Liechtenstein']: decision D-007 flagged for re-confirmation
- ❌ no-op rerun calls no agent (B0)

**after**: stories changed US-01.3, US-04.1, US-04.2, US-04.3, US-05.3, US-05.4, US-05.6, US-05.7, US-06.1, US-06.2, US-08.1, US-08.2, US-08.4; added -; errors 10; examples 220/220; open questions 5; dev questions 16; verdict not_ready; 311 s

- ✅ no errors (other than expected flags)
- ✅ all examples pass: 220/220
- ❌ only expected stories changed: US-01.3, US-05.3, US-05.4, US-06.1, US-06.2, US-08.1, US-08.2, US-08.4
- ✅ 0-0 stories added: none
- ✅ item.daily_return_liechtenstein still exists
- ✅ item.non_return_days_45 still exists
- ✅ rule.liechtenstein_no_source_tax_in_principle still exists
- ✅ item.daily_return_liechtenstein unchanged in behaviour
- ✅ item.non_return_days_45 unchanged in behaviour
- ❌ item.nationality unchanged in behaviour
- ✅ (soft) one of: decision D-007 flagged for re-confirmation / new or changed open question mentions ['Liechtenstein']: decision D-007 flagged for re-confirmation
- ❌ no-op rerun calls no agent (B0)

