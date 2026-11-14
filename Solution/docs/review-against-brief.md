# Review: the pipeline against the brief

An independent review of `Solution/` against the take-home brief
(`Instructions/Anhang/Lonio Business Interview - Take-Home Challenge.pdf` and
the e-mail). It was written as a critic, not as the builder. Every claim points
to a file. Where the README and the code disagree, the code wins.

State reviewed: commit `7b495da`, last pipeline run of 14 Nov (build output in
`build/employee-onboarding/`, specs in `requirements/employee-onboarding/`).

---

## 1. Verdict in five lines

1. **The engine is strong.** Every line can be traced to a quote, code checks
   those quotes, examples are executed, and the "can it be built without
   questions?" test is automated. That is more rigour than the brief asks for.
2. **The deliverable is not yet what the brief asks for.** One of three
   sources (the Zurich calculator) is missing entirely. There is no step order.
   "Who needs it?" is wrong for 5 of 17 items. An engineer agent still asks 36
   questions (17 major).
3. **The pipeline already knows all of this.** Its own review says
   `NOT READY` for these reasons. The gap is not detection. It is that nobody
   has acted on it yet: `decisions.yaml` is empty.
4. **The change story holds in principle but is oversold in the README.** In
   practice, any source change reruns almost every LLM stage, and the
   rerun produces a fresh, non-deterministic model. Two code bugs break the
   "add a new source" story (section 4).
5. **The best answer to "how do you know it is correct again"** is already in
   the repo: the human-written named cases in `examples.yaml`. It should become
   the centre of the change process (write the expected case first, then
   rerun).

---

## 2. Scorecard against the brief

| # | What the brief asks | Verdict | Evidence |
|---|---|---|---|
| 1 | Define **which information** we ask | ✅ Holds, for 2 of 3 sources | 17 items, `requirements/.../information.md`; gold item recall and precision 1.0 (`build/.../report.json` → `eval`) |
| 2 | …in **which steps and order** | ❌ Falls short | There is no flow or step sequence anywhere. Features have an `order`, but that orders features, not questions. The dev-refinement agent asks three times where questions go (review.md lines 159, 169, 177). Only AC-02.2.4 says "address comes before pension and source tax". |
| 3 | …**under which conditions** | ✅ Holds | `asked_when` / `required_when` in business text plus an executable expression; 58/58 examples pass |
| 4 | Checklist: **What?** | ✅ | Every item has a description and form (lint enforces it: `checks/mechanical.py` → `lint`) |
| 5 | Checklist: **When do we ask?** | ✅ | Same |
| 6 | Checklist: **When is it required / can it be left empty?** | ✅ | Same; e.g. spouse's permit type "may be left empty" |
| 7 | Checklist: **What does it depend on?** | ✅ Well done | Computed by code from the expressions (`compute_depends_on`), so it cannot drift from the rule |
| 8 | Checklist: **Who needs it? Which source asks for it?** | ⚠️ Wrong for 5 items | Nationality, permit type and the three spouse items list only `hr`. The source tax office is the party that needs them (`knowledge.raw.json`; eval `stakeholder_recall: 0.74`). The pipeline flags this as a *warning*, so it did not block anything. |
| 9 | **Built without anyone asking a single question** | ❌ Falls short (and measured honestly) | Dev refinement: 36 questions, 17 major, 0 blockers (`report.json`). Examples: first working day vs. contract start, Julia's date moving *after* onboarding, dual nationals, a pending permit. |
| 10 | Sources: Zurich calculator | ❌ Missing | `build/.../extract/zh_source_tax_calculator.json` is `[]`. The full crawl was never run. The source tax questionnaire (Anna's "biggest pain") is open question OQ-01 (blocking). |
| 11 | Sources: screenshots, transcript | ✅ | All 7 portal fields covered; every transcript turn with content is cited (uncited turns are small talk) |
| 12 | Treat sources as truth | ✅ | Guidance G-06, a judge per fact, "no outside knowledge" in the modeller prompt |
| 13 | Ask too little vs. too much | ✅ Strong on minimisation, ⚠️ on "too little" | Source tax questions are asked only when the answer can change the outcome (FEAT-04 examples). But "too little" is not solved: cross-border employees cannot be registered with the fund (canton, OQ-02), and subject employees get no tariff questions. |
| 14 | Markdown, clear templates, **reusable for the next process** | ✅ Design, ⚠️ unproven | Jinja templates, problem profile, `/new-problem`. The only second problem (`address-change`) was deleted in `7b495da`, so reuse is shown by construction only. |
| 15 | Business language, no technical decisions (your own bar) | ⚠️ Partial | 9 tech leaks flagged (e.g. "cannot complete the step", DD.MM.YYYY input, internal ids such as `address_country` in prose) |
| 16 | Pipeline + README: what each stage does and why, in → out, how it ensures completeness and correctness | ✅ | README seven steps; a few claims are stronger than the code (section 4) |
| 17 | Limitations: what, where from, which direction | ✅ Honest | `LIMITATIONS.md`, 12 rows. It is missing the bugs in section 4. |
| 18 | Use AI agents (Opus 5.5) | ✅ | `profile.yaml` → `models` (Opus for the work, Sonnet for judges) |

---

## 3. Where it holds up

- **Proof for every line, checked by code.** Quotes must be exact substrings
  of the unit they cite (`adapters/base.py` → `verify_anchor`). Screen
  summaries cannot be quoted. Facts with broken anchors never reach the model.
- **Interview reality is handled.** Self-corrections (Anna's C-permit and
  spouse corrections), retractions (photo), today's manual process
  (`current_state`) and hedges ("I think so" → OQ-05) all appear correctly.
- **The rule is right.** The source tax liability rule matches the transcript,
  including the corrections, and it passes all nine named source-tax cases
  (Maria, Tomás, Stefan, the Liechtenstein resident and others).
- **Executable examples plus human-written cases.** `examples.yaml` holds 13
  cases written by a human and run on every build. This is the one oracle that
  does not come from the same agent that wrote the rule.
- **"Built without questions" is tested, not claimed.** A separate engineer
  agent sees only the rendered files and lists its questions. That is the
  brief's acceptance test, automated.
- **Decisions are data, applied by code after the agents ran.** No agent can
  reinterpret them, and they are fingerprinted against their evidence.
- **Honest self-assessment.** The review says `NOT READY` for the right
  reasons, and `LIMITATIONS.md` names the real weak spots (non-determinism,
  circular examples, calculator).

## 4. Where it falls short

### 4a. In the deliverable

1. **The calculator is missing.** That leaves a third of the sources and the
   main pain point unaddressed. Everything about source tax is "who", nothing
   is "what we then ask". The calculator may also need data that the spec
   currently excludes on purpose (nationality of people living abroad,
   AC-04.1.2). So even FEAT-04 may change once it is explored.
2. **No step order.** The brief explicitly asks for steps and order. The
   output is organised by feature (stakeholder goal), and there is no
   questionnaire flow. An engineer cannot build the sequence without asking.
3. **"Who needs it?" is wrong for the source tax items.** The checklist row
   the brief asks about most directly is wrong for 5 of 17 items, and the
   pipeline only warns about it.
4. **Contradictions remain.** FEAT-04 says "HR uses it to decide" in three
   criteria and "Lonio decides" in US-04.4 (reviewer finding 5). FEAT-02 cites
   G-09 (the language rule) as proof that the address country is the country
   of residence (reviewer finding 3).
5. **Most stories are `inferred`.** 14 items or stories still need confirmation,
   and no decision has been recorded (`decisions.yaml: decisions: []`). The
   human-in-the-loop step, which is the pipeline's answer to open questions,
   has never been exercised.
6. **The specs predate the last engine fixes** (LIMITATIONS, "State of this
   delivery"). The prompts changed after the run, so the next `pipeline run`
   reruns extraction for every source. The specs will change, not just
   refresh.

### 4b. In the pipeline (found in the code, not mentioned in README or LIMITATIONS)

| # | Finding | Evidence | Effect |
|---|---|---|---|
| B1 | **Unit and fact ids collide across two sources of the same type.** Unit ids are `T-001…` / `S01-E01…` with no source prefix. Fact ids use the adapter *type* prefix (`F-TR-001`), not the source. The schema comment says `F-<SRC>-NNN`. | `adapters/transcript/adapter.py` (`T-{n:03d}`), `adapters/base.py` (`F-{self.prefix}-{i:03d}`), `run.py` → `unit_by_id = {u.id: u …}` | A second transcript (e.g. a follow-up meeting with Anna) overwrites the first one's units in `unit_by_id`. Anchors of the first source are then checked against the wrong text and fail. Fact ids also clash in the judge and in citations. **The README's "new source = one profile entry" does not work for a second source of an existing type.** |
| B2 | **The "reuse existing ids" stabiliser is dead code.** The knowledge stage reads `build/<p>/knowledge.json`, but only `knowledge.raw.json` is ever written. | `run.py` lines 170–175; no `knowledge.json` in `build/` | The modeller always sees "(none yet)", so ids and slicing can change on every rerun. This is visible in `build/.../features/`: two runs six minutes apart produced 5 features (with `FEAT-05-source-tax-tariff-questions`) and then 4 with different ids. |
| B3 | **Fact-level decisions can silently retarget.** Fact ids are positional (`F-TR-031` = 31st fact of this extraction). After a re-extraction, `reject fact.F-TR-031` hits whatever fact now has that number. The evidence hash covers unit text, not the fact. | `engine/decisions.py` → `apply_to_facts`, `evidence_hash` | A wrong fact can be rejected or accepted with no warning. |
| B4 | **Decisions without `evidence` are never flagged.** The hash of an empty list never changes. | `evidence_hash` | Such a decision survives any source change unchecked. |
| B5 | **A change to the live calculator is never detected.** `status` and the cache fingerprint look at the cached `tree.json`, not at the site. Only a manual `explore` refreshes it. | `adapters/web_calculator/adapter.py` → `normalize_inputs` | "If a source changes tomorrow", the one *real* source is the one we would not notice. |
| B6 | **Fingerprint gaps.** These inputs are used but not fingerprinted: the source `description` (used in the extract prompt, not in `extract_inputs`), the `models:` block, and the open-questions/out-of-scope files that the dev-refinement agent reads. | `adapters/base.py`, `run.py` → `stage_dev_refinement` | A changed description or model does not trigger a rerun, so output can go stale silently. |
| B7 | **A new source type needs a code change.** The adapter registry is hard-coded in `get_adapter`. | `adapters/base.py` (bottom) | Minor; the README says "new adapter folder + one entry in profile.yaml". |
| B8 | **Stale build artefacts are committed.** Old feature JSONs and orphaned manifest keys (`spec.raw`, `naive_builder`) sit next to the current ones. | `build/.../features/`, `manifest.json` | They confuse a reviewer who opens `build/`. The rendered `requirements/` is clean, because render deletes the folder first. |
| B9 | **Examples are mostly self-checked.** 45 of the 58 executed examples were written by the same agent family that wrote the formalisation they are checked against. Only 13 are independent. | `report.json` → `examples` (`origin`) | "58/58 ✅" overstates the evidence. LIMITATIONS #3 and #4 say this in general terms. |

---

## 5. If a source changes tomorrow

### 5a. What really reruns (verified against `run.py` and `engine/context.py`)

Every stage is cached by `sha(inputs)` in `manifest.json`. The important
detail is *what each stage takes as input*:

| Stage | Cache key (inputs) | Granularity |
|---|---|---|
| `normalize/<src>` | source file bytes (whole folder for screenshots), adapter config, profile entry (+ reader prompt) | per source |
| `extract/<src>` | that source's units, adapter prompt, `guidance.md` | per source |
| `judge_facts` | **all facts of all sources**, judge prompt | one stage |
| `knowledge.raw` | **all usable facts**, modeller prompt incl. profile, guidance, condition language | one LLM call |
| `features.plan` | whole knowledge model | one call |
| `features/<id>` | feature + **whole knowledge model** + cited facts | per feature, but every feature sees the whole model |
| decisions, checks, render | not cached; code; run every time | – |
| `judge_trace` | all items, rules and stories | one stage |
| `dev_refinement/<id>` | rendered feature file + `information.md` | per feature |
| `review` | the whole report | one call |

So "a changed source reruns only what depends on it" is technically true, but
from `judge_facts` onward **everything depends on every source**. And because
the knowledge model is not deterministic (B2), its new output changes every
downstream key.

| Change | What reruns | Rough cost |
|---|---|---|
| **Transcript edited** (question added or removed, rule changed, new condition) | normalize (code) → extract transcript → judge all facts → knowledge → plan → **all** feature writers → trace judge → render → dev refinement (all, because `information.md` changes) → review. Reused: portal reading and extraction. | close to a full run, minus 14 vision calls |
| **Screenshot added or changed** | all screenshots re-read twice (folder fingerprint), screen numbers shift → extract portal → same cascade | a full run |
| **Calculator changed online** | **nothing**, until someone runs `pipeline explore` (B5); then the same cascade | a full run, plus the crawl |
| **`guidance.md` edited** | extraction for **every** source + cascade | a full run, minus normalize |
| **Decision added** (`decisions.yaml` or `/decide`) | no extraction, model or writers. Spec → trace judge → render → refinement of changed features → review | cheap |
| **`examples.yaml` / `gold.yaml` edited** | checks only, plus review | very cheap |

LIMITATIONS #12 gives about $5–7 and 15–20 minutes for a full run.

### 5b. The steps I would take

Concrete case: **Pensionskasse Muster adds "Registered partnership" to the
civil status list, and the partner's date of birth appears for it.** (This
also answers OQ-03.)

1. **Write the expectation first, before running anything.** In
   `examples.yaml` add the named case `daniel` (registered partnership →
   partner's date of birth *required*), and update `gold.yaml` (new allowed
   value; OQ-03 no longer expected). This is the human-made oracle the
   pipeline cannot write for itself. If the run then gets it wrong, the build
   fails.
2. **Replace the source.** Put the new screenshot into the folder.
   `pipeline status` shows `pension_portal CHANGED`. (For the calculator,
   rerun `pipeline explore` because nothing else would notice; for a new
   meeting, add a profile entry, after fixing B1.)
3. **Run** `pipeline run`. Expect close to a full rerun (5a).
4. **Read `review.md` in this order:**
   - *Errors*: broken anchors, unknown references, and **decisions flagged
     "evidence changed – re-confirm"**. Re-confirm or rewrite each one.
   - *Double-read disagreements* for the new screenshot
     (`normalize/pension_portal.double_read.json`). If the two vision reads
     disagree, I look at the image myself.
   - *Examples*: `daniel` must pass; all old named cases must still pass.
   - *Coverage*: the new units (the new option, the new field) must **not**
     appear in "uncited units".
   - *Open questions*: OQ-03 should be gone or changed; check that no new one
     hides the change.
   - *Dev refinement*: no new major questions about the changed feature.
5. **Diff, and separate signal from noise.**
   `git diff requirements/`. Every changed line should be explained by the
   source change. Lines that changed for no reason (rewording, renamed ids,
   a different feature split) are non-determinism. I either accept them or
   freeze the previous wording with a decision. This is the most
   time-consuming human step today (LIMITATIONS #2, B2).
6. **Decide what the sources leave open** with `/decide` (e.g. is a
   registered partner "married" for the source tax spouse rule?). Rerunning
   after a decision is cheap.
7. **Commit** the sources, examples, decisions and requirements together, so
   the history shows *why* each requirement changed.

**Adding a new source** is the same loop, with three additions: give it an
`authority` and `precedence` in `profile.yaml` (this is what turns conflicts
into open questions instead of silent choices); add an adapter if it is a new
type (plus a registry line, B7); and **expect conflicts**. A new source should
produce new open questions where it disagrees with the old ones. If it
produces none, I check that it was really read.

### 5c. How I would know the requirements are correct again

"Correct" here means *faithful to the sources and to my decisions*. Reality
remains the stakeholder's job. I would call it correct again when all of these
hold:

1. **0 errors** in `review.md`: every quote verified, every reference valid,
   every checklist question answered.
2. **Every named case passes**, including the new one I wrote *before* the
   run. This is the only check that is independent of the model.
3. **No decision is waiting for re-confirmation.**
4. **The new source units are cited**, and no previously used fact became
   unused without a reason.
5. **The diff is explained:** each changed line traces back to the source
   change or to a decision.
6. **The engineer agent has no new major questions** for the affected
   features.
7. **Gold recall stays at 1.0**, and stakeholder recall does not drop.
8. For anything with residual doubt, a **short confirmation with the
   stakeholder** (Anna or the fund) using the changed decision table. That
   confirmation is then recorded as a decision with evidence.

Honest caveat: checks 2 and 7 only test the *internal formalisation*. If the
business text says something different from the expression, all examples can
pass anyway (LIMITATIONS #3). Reading the diff (check 5) covers that today.

---

## 6. Recommended fixes

No pipeline code was changed for this review. In order of value per hour:

**Before submission (Sunday 20:00)**
1. **Rerun the pipeline once** so the specs match the committed engine, and
   commit the result. Today the specs predate the fixes.
2. **Record the obvious decisions** with `/decide`: add `source_tax` to "who
   needs it" for the 5 items; "Lonio decides, HR can see the result"
   (FEAT-04 contradiction); remove the false G-09 citation; an interim rule
   for cross-border canton. This also shows the human-in-the-loop working,
   which is currently only claimed.
3. **Add a step-order view.** At minimum, one product decision or guidance line
   that fixes the questionnaire order (e.g. start date → address → personal
   and family → source tax), rendered as a short flow in `README.md` of the
   requirements. The brief asks for it explicitly.
4. **Run the calculator explorer**, even partially, or state plainly in
   README and video that source tax tariff questions are out of this delivery
   and why.
5. **Add B1–B5 to LIMITATIONS.md.** Finding them yourself is better than an
   interviewer finding them.

**Next (direction, not this week)**
6. Namespace unit and fact ids by source (`hr_transcript:T-012`), and give
   facts content-based ids so decisions do not retarget (B1, B3).
7. Feed the previous knowledge model back as a baseline (fix the
   `knowledge.json` path) and model *changes* instead of a fresh model (B2,
   LIMITATIONS #2).
8. Require `evidence` on every decision (B4).
9. Schedule a cheap "has the calculator changed?" probe, e.g. hash the
   visible question texts, and alert on change (B5).
10. Mark AC examples written by the writer as "self-checked" and the named
    cases as "independent" in the specs, and measure branch coverage
    (B9, LIMITATIONS #4).
11. Make "who needs it" an error-level check against gold, not a warning.

---

## 7. Talking points for the ~5 minute video

| Time | Point |
|---|---|
| 0:00–0:30 | The problem as I read it: requirements an agent can build from, with proof for every line. |
| 0:30–2:00 | The seven steps (README diagram). Why: agents interpret, code checks; proof for every line; the human decides as data. Show one feature file with an examples table and its evidence. |
| 2:00–2:45 | Honest state: 17 items, rules right, 58 examples pass. **Not ready**: calculator not explored, step order missing, 17 major refinement questions. The pipeline told me this itself. |
| 2:45–4:15 | Change scenario (section 5b): write the expected case first → replace the source → `status` → run → read review.md in a fixed order → diff, signal vs. noise → decide → commit. What reruns, and why it is almost everything today. |
| 4:15–4:45 | How I know it is correct again: section 5c, with the independent named cases as the anchor. |
| 4:45–5:00 | What I would fix next: stable ids and incremental modelling, so a source change produces a small, explainable diff. |
