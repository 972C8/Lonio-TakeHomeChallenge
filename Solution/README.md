# Requirements pipeline

A pipeline of Claude agents and deterministic checks that turns messy business
sources (meeting transcripts, portal screenshots, live web calculators) into
**traceable, build-ready requirements** in Markdown – here for the onboarding
questionnaire of a new employee.

```
sources ──► normalize ──► extract ──► verify ──► synthesize ──► decide ──► check ──► render ──► naive builder ──► review
            (adapter)     (agent)     (code+     (agent)        (code,     (code+    (code,     (agent)            (agent)
                                       judge)                    human)     judge)    templates)
```

Output: [`requirements/employee-onboarding/`](requirements/employee-onboarding/README.md) ·
review for the product owner: `build/employee-onboarding/review.md`

## Principles

1. **Proof for every line.** Every requirement cites facts; every fact quotes
   its source verbatim; every quote is machine-checked against the source.
2. **Rules before judges.** Everything checkable by code is checked by code
   (quotes, references, condition syntax, ordering, persona tests, gold set).
   LLM judges only cover what code cannot, and judge one item at a time.
3. **Agents interpret, code decides format.** Agents return JSON validated
   against schemas (`pipeline/engine/schemas.py`); Markdown is rendered from
   templates, never free-written.
4. **The human decides, as data.** Open questions and inferred items surface in
   `review.md`. The product owner answers in `decisions.yaml`; code applies
   decisions after the agents ran, so they cannot be ignored or reinterpreted.
5. **Cheap, traceable reruns.** Each stage is cached by a fingerprint of all
   its inputs. A changed source reruns only what depends on it.
6. **Reusable by design.** Engine (shared) · source adapters (shared) ·
   problem profile (one folder per investigation).

## Quick start

```bash
python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pipeline run            # full run (Claude Code login is used; no API key)
.venv/bin/python -m pipeline status         # which sources changed since the last run
.venv/bin/python -m pipeline run --fast     # skip LLM checks while iterating on decisions/templates
.venv/bin/python -m pipeline explore zh_source_tax_calculator   # crawl the live calculator (Playwright MCP)
.venv/bin/python -m pipeline publish --dry-run                  # Linear sync plan, nothing sent
```

## Layout

```
pipeline/
  engine/          schemas, stage cache, Agent SDK wrapper, condition language, decisions
  adapters/        one folder per SOURCE TYPE: adapter.py + agent.md (+ config.yaml)
    transcript/    PDF/text meetings -> speaker turns (deterministic) -> facts (agent)
    screenshots/   images -> verbatim UI elements (vision agent, double read) -> facts (agent)
    web_calculator/ live site -> question tree (Playwright agent, on demand) -> facts (agent)
  agents/          synthesizer, fact judge, requirement judge, naive builder, reviewer
  checks/          deterministic checks: anchors, lint, coverage, personas, gold eval
  render/          Jinja templates for the requirements package
  publish/         Linear sync plan (dry run)
  run.py           the stages in order
problems/
  employee-onboarding/   profile.yaml · guidance.md · decisions.yaml · personas.yaml · gold.yaml
.claude/skills/    /run-pipeline · /decide · /trace · /new-adapter · /new-problem · /learn
build/<problem>/   every intermediate result (units, facts, verdicts, spec, report, review.md)
requirements/<problem>/  the deliverable
```

## Stages: what, why, in → out

| # | Stage | Who | In | Out | Why |
|---|---|---|---|---|---|
| 1 | **normalize** | adapter | raw source | `normalize/<src>.json`: Units with stable ids (`T-031`, `S05-E14`, `C-Q03`) and exact text | Makes sources addressable and quotable. Transcripts are split deterministically; screenshots are transcribed verbatim by a vision agent, twice, and disagreements reported. |
| 2 | **extract** | agent per source (parallel) | units + source-specific prompt + problem guidance | `extract/<src>.json`: atomic Facts with kind, verbatim anchors, `explicit/inferred`, `desired/current_state`, `supersedes` | Small facts are checkable; requirements are not. Per-source agents keep context clean and prompts specific (stakeholder self-corrections, comparing screenshots, ...). |
| 3 | **verify facts** | code + judge agent | facts + units | `facts.json` with `anchor_ok`, judge verdict, `superseded_by` | Quotes must be exact substrings (code). A narrow judge checks each fact against its quoted units and neighbours. Unsupported facts never reach synthesis. |
| 4 | **synthesize** | agent | verified facts, profile (consumers, source authority), guidance, condition language, existing ids | `spec.raw.json`: steps, fields, derived rules, notices, open questions, exclusions | One canonical data dictionary: ask once, merge sources, apply data minimisation in `ask_when`, surface conflicts as open questions instead of choosing silently. |
| 5 | **decide** | code (+ human) | spec + `decisions.yaml` | `spec.json` | Human judgment applied as a deterministic patch, cited as the highest-precedence source, fingerprinted against its evidence. |
| 6 | **check** | code + judge agent | spec, facts, units, personas, gold | findings, persona results, coverage, metrics | Lint (the 5 questions answered, conditions parse and only reference known ids, nothing asked before what it depends on, every item cited), coverage, persona simulations, gold-set eval, per-requirement trace judge. |
| 7 | **render** | code (Jinja) | spec + facts | `requirements/<problem>/` | Fixed, reusable format; front matter is the machine contract, body is for humans; evidence inline. |
| 8 | **naive builder** | agent with only the rendered folder | `requirements/` | list of questions it would have to ask | The acceptance test of the task ("built without asking a single question"). |
| 9 | **review** | agent | full check report | `review.md` with verdict ready / ready with caveats / not ready | One place for the human: decisions needed, failures, inferred items, uncovered source parts. |

## How it makes sure the result is complete and correct

**Correct (nothing invented):**
- verbatim-quote check on every anchor (code); screen transcriptions read twice
- fact judge per fact; trace judge per requirement against its cited facts
- lint: every item cites ≥1 valid fact or decision
- persona tests: real cases from the sources (Maria/C permit, Tomás/Swiss
  spouse, Stefan/Konstanz, Julia/15 March → 1 April, ...) are simulated
  through the generated conditions and rules
- guidance forbids outside knowledge; inferred items are labelled and listed

**Complete (nothing lost):**
- coverage: source units never cited and facts never used are listed for the
  human to confirm as irrelevant
- gold set (hand-written, `gold.yaml`): recall/precision of fields, rules,
  exclusions, notices, open questions
- naive builder: questions an engineer would still need to ask
- lint: each field answers *what / when asked / when required / depends on / who needs it*

## Human in the loop

| When | Where | What |
|---|---|---|
| before a run | `profile.yaml`, `guidance.md` | scope, source authority, conventions, id vocabulary |
| after a run | `build/<p>/review.md` | the one file to read |
| deciding | `decisions.yaml` (or `/decide`) | override / add / exclude / resolve / accept / reject by stable id |
| over time | `/learn` | turn repeated overrides into tests or guidance |

## When a source changes

1. Replace the file (or rerun `explore` for a live site).
2. `pipeline status` shows which sources changed; `pipeline run` reruns only
   that source's chain and everything downstream of it.
3. `review.md` shows new failures, decisions whose evidence changed (flagged
   for re-confirmation), coverage of the new content.
4. `git diff requirements/` shows exactly which requirements changed.

New source → new adapter folder (see `/new-adapter`) + one entry in
`profile.yaml`. New process → new `problems/<name>/` folder (see `/new-problem`).

See [LIMITATIONS.md](LIMITATIONS.md) for where the pipeline stands.
