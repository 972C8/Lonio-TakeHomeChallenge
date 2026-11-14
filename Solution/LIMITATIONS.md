# Limitations

Where the pipeline stands today, where each problem comes from, and which
direction I would take to improve it. Ordered by impact.

| # | Limitation | Where it comes from | Direction |
|---|---|---|---|
| 1 | **The Zurich source tax calculator is not explored yet.** The source tax tariff questions are an open question in the onboarding specs, so the specs only decide *who* is liable. | Time-boxed. The explorer (Playwright MCP agent), its prompt and `pipeline explore` exist, and a smoke test passed: the calculator sits on the page, is in German and reveals one question at a time. The full crawl has not been run. | Run the explorer. Then make branch enumeration deterministic: the agent maps the controls once, and a Playwright script walks every combination and records input→tariff vectors, which become examples in the acceptance criteria. |
| 2 | **The knowledge model is still one large agent call and not deterministic.** Two runs can model the same thing differently (e.g. 5 vs 4 sections, an item as a question vs a derived rule), and wording drifts, which makes diffs noisy. | One agent consolidates everything at once. Stabilisers: the id vocabulary in guidance, "reuse existing ids", per-section writing. | Model incrementally per subject, against the previous model as a baseline, so the agent proposes *changes* rather than a fresh model. Freeze accepted elements via decisions. |
| 3 | **The internal formalisation can diverge from the business text.** Examples are executed against expressions, but readers see the business-language conditions. If the two disagree, every example can pass while the text says something else. | Two representations of the same rule, both written by an agent. | Generate the business text *from* the decision tables (template) instead of in parallel, or add a deterministic check that every decision-table row is reproduced by the expression. The trace judge covers this partly today. |
| 4 | **Examples are only as good as their authors.** Most acceptance-criterion examples come from the story writer; the named real cases come from a human (`examples.yaml`). A missing branch shows up neither as a failure nor in coverage. | No branch coverage over the conditions. | Measure branch coverage of every condition and rule over the executed examples, and ask the writer to fill uncovered branches. |
| 5 | **LLM judges are noisy.** "Partial" verdicts are often about wording, not substance, and they inflate the warnings. | LLM-as-judge is the weakest verifier; its threshold lives in a prompt. | Calibrate on a small labelled set, auto-downgrade wording-only notes, and keep judges only for claims code cannot check. |
| 6 | **The tech-leak boundary is a judgment call.** "The fund requires DD.MM.YYYY" is knowledge; "the form blocks the step" is design. The vocabulary scan is crude, and the dev-refinement agent sometimes disagrees with the writer. | The boundary rule is clear in principle but fuzzy at the edges. | Turn recurring leak findings into examples for the writer prompt (`/learn`) and into the profile's `tech_vocabulary`. |
| 7 | **Screenshot evidence is text, not pixels.** Anchors point to a transcription, not an image region. | Vision agent, no OCR with coordinates. | OCR with bounding boxes, stored crops, crop links in the evidence. |
| 8 | **Change detection is per file, and prompt changes rerun a lot.** Any byte change to a source reruns its chain; editing `guidance.md` or a stakeholder description reruns extraction and modelling. | Whole-file fingerprints. | Diff units semantically and rerun extraction only for changed units; separate "prompt-relevant" from "display-only" profile fields. |
| 9 | **Decisions target ids.** If an agent renames an item or story, a decision targeting it fails. It's reported, not migrated. | Ids come from agents. | Treat ids as a registry; renames become proposals the human approves, and the decisions are migrated with them. |
| 10 | **Fact-level recall is not measured.** Coverage lists uncited source units, but doesn't prove every relevant statement became a fact. | The gold set is at item/rule level. | A fact-level gold set, plus chunk-pair coverage judging (Inter2US). |
| 11 | **The Linear publisher has not run against a real workspace.** Matching existing issues relies on the agent following its instructions (title-prefix search). | No workspace yet; publishing is outward-facing. | Run it once with `--dry-run`, then for real; if it proves unreliable, keep the agent but add a code check that reads the issues back. Later: pull answers from `needs-decision` issues into `decisions.yaml`. |
| 12 | **Cost and time.** A full onboarding run costs about $5–7 and takes about 15–20 minutes. A rerun after a decision costs a fraction of that. | Many agent calls, each starting a Claude Code process. | Batch judges, use cheaper models where eval numbers allow, and cache per unit (see 8). |

## State of this delivery

- Onboarding: 61 facts → 17 information items, 2 business rules → one feature
  with 4 sections, 12 stories, 37 acceptance criteria. 0 errors, 58/58
  executed examples pass. Stakeholder recall against the gold set is 0.74: the
  model says HR (not the source tax office) needs nationality, permit and the
  spouse's data, because HR decides liability by hand; I left the gold set as
  written. The verdict is "not ready" because of open product questions
  (calculator, fund canton, form lifecycle), not because of pipeline errors.
- **The committed onboarding spec is a mechanical conversion**, not a fresh
  run. When the problem became one feature with sections, the four previous
  features became four sections with their stories, criteria and examples
  unchanged. The checks and rendering were re-run on it (no LLM), but the
  planner and writer prompts have not produced it, and some context
  paragraphs still point to the old features (e.g. "FEAT-02"). The next full
  `pipeline run` regenerates everything (the cache detects the changed
  prompts); the earlier engine fixes (built-in `today`, open questions not
  cited as sources, guidance conventions not extracted as facts) are included.
- Genericity is by construction (nothing domain-specific in `pipeline/`), but
  only one real problem has been run through it so far.
