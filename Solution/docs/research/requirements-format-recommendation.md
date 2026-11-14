# Which requirements format should the onboarding output use?

_13 Nov 2026 · Decision memo for the Lonio take-home. Research only; the pipeline repo was not changed._

## Recommendation in one paragraph

**Do not make user stories the final output.** Keep the current hybrid (a per-field data dictionary with a machine-readable YAML contract, a small condition language, derived rules, and evidence), because that is the shape the brief asks for and the shape every serious conditional-questionnaire standard uses. Then borrow the one thing each other format does best: **example tables** (Specification by Example) as acceptance tests, **decision tables** for the source-tax rule, **EARS** statements for the few cross-cutting behaviours that are not fields, a **consumer view** per receiving party, and a **JSON Schema** for the front matter so the template is reusable and mechanically checkable. User stories survive only as a short "who and why" header in the README.

## Why not user stories as the unit

The brief's checklist is per **piece of information**: what and in what form, when asked, when required, what it depends on, who needs it. User stories are organised per **actor goal** ("As a new employee I want… so that…"). That mismatch causes concrete problems here:

- **One field, many stories.** `permit_type` is needed by the source-tax liability check and by HR's "bring your permit" reminder. In story form its conditions get written twice, in two places, and can drift. That breaks Lonio's core promise of asking once and reusing everywhere.
- **Conditions end up in prose.** Story acceptance criteria are natural language. "Ask the spouse's permit if the employee is married, foreign, not a C holder and the spouse is not Swiss" is exactly the kind of sentence an agent can implement slightly wrong. The current `ask_when` expressions cannot be read two ways.
- **Form is not part of the format.** Stories have no slot for type, options, stored value vs label, date format or validation. You would bolt a data dictionary on anyway.
- **There is basically one actor.** The employee fills in a form; the "so that" is really the consumer's purpose, which the current `consumers` table already captures with more precision (party, purpose, their field name).
- **What the evidence says.** Spec-driven tools that do use stories (AWS Kiro) pair them with EARS criteria, and even Kiro's advocates note EARS "does not make the acceptance criteria executable on their own" ([codemyspec](https://codemyspec.com/blog/kiro-specs-explained)). Story-first guides for agents ([Bilotta, Oct 2026](https://johnnybilotta.com/post/writing-requirements-for-ai-coding-agents/)) target feature work, not data-collection rules. None of the sources I found measured stories against structured specs for agent accuracy.

Stories are good for alignment with humans and for prioritising features. This deliverable is a contract for a building agent, so they belong in the intro, not as the unit.

## Format comparison

Scored for this case (conditional onboarding questionnaire built by an AI agent, reused for the next process). ●●● strong, ● weak.

| Format | Agent-buildable | Precise | Traceable | Reusable | Verdict |
|---|---|---|---|---|---|
| User stories + Given/When/Then AC | ●● | ● | ●● | ●● | Context only (README) |
| EARS statements | ●● | ●● | ●●● | ●● | Use for cross-cutting behaviours |
| Gherkin scenarios | ●● | ●● | ●● | ●● | Use as *tables* (examples), not prose features |
| Data dictionary / field spec | ●●● | ●●● | ●●● | ●●● | **Keep as the backbone (current)** |
| Decision tables (DMN-style) | ●●● | ●●● | ●● | ●●● | Add for multi-input rules (source tax) |
| Declarative form schema only (JSON Forms, SurveyJS, FHIR Questionnaire) | ●●● | ●●● | ● | ●●● | Too implementation-specific and loses evidence; the current front matter already is this idea in Markdown |
| **Hybrid: field spec + rules + examples + EARS behaviours** | ●●● | ●●● | ●●● | ●●● | **Recommended** |

Notes behind the scores:
- **Declarative questionnaire standards confirm the backbone.** FHIR Questionnaire models each item with `enableWhen` / `enableBehavior` / `enableWhenExpression` and a `required` flag ([CSIRO Smart Forms](https://smartforms.csiro.au/docs/sdc/conditional)); SurveyJS and JSON Forms do the same with `visibleIf` / rules. Your `ask_when` + `required_when` + expression language is the same model, expressed in Markdown so Lonio's agents can read it. That is a strong argument to make in the video: the format is not invented, it mirrors how mature form standards separate *data*, *visibility* and *requiredness*.
- **Decision tables help LLMs follow rules.** A 2025 study found GPT-4o applying feedback rules structured as DMN decision tables reached F1 0.91 versus 0.53 with chain-of-thought prose ([arXiv 2505.11701](https://arxiv.org/html/2505.11701v2)). It is a small study on a different domain, but it points the same way: tabular rules beat prose rules.
- **Gherkin's value is the examples, not the Given/When/Then wording.** For a form, a table of "these answers → these fields shown/required, these derived values" is denser and directly executable against your condition language.

## Concrete changes to the current template

Ordered by value for the deadline. 1 to 3 are the ones I would do; 4 to 6 are cheap polish.

### 1. Add `scenarios.md`: acceptance examples (highest value)

One table per step or rule, generated by the pipeline and **checked by evaluating the expressions** (no LLM). Each row cites its source. The transcript already gives you named, traceable cases:

| ID | Case | Answers | Expected: shown | Expected: derived | Source |
|---|---|---|---|---|---|
| SC-01 | Maria | `address_country=CH, nationality=PT, permit_type=C, civil_status=single` | steps 1–5; no step 6 | `subject_to_source_tax=false` | F-TR-026 |
| SC-02 | Tomás | `address_country=CH, nationality=BR, permit_type=B, civil_status=married, spouse_nationality=CH, spouse_residence_country=CH` | `spouse_nationality`, `spouse_residence_country`; not `spouse_permit_type`; no step 6 | `subject_to_source_tax=false` | F-TR-031 |
| SC-03 | Stefan | `address_country=DE, civil_status=single` | no step 3; step 6 shown | `subject_to_source_tax=true` | F-TR-037 |
| SC-04 | Julia | `first_working_day=2027-03-15` | – | `insurance_start_date=2027-04-01` | F-TR-016, F-TR-019 |
| SC-05 | Starts on the 1st | `first_working_day=2027-04-01` | – | `insurance_start_date=2027-04-01` | F-TR-019 |

(Answers for fields the transcript doesn't state, such as Maria's civil status, are illustrative and should be marked so.)

Why it matters: the building agent gets ready-made test cases, the pipeline gets a deterministic self-check (if an expression changes and SC-02 flips, you know), and in the video it answers "how would you know your requirements are correct again?" directly: rerun, scenarios still pass. When the calculator facts land (OQ-01), its input → tariff vectors go into the same file.

### 2. Add a decision table to `rules/subject_to_source_tax.md`

Keep the expression as the contract, and add a table the pipeline checks against it (every row evaluated):

| # | Lives in CH | Nationality | Permit | Married to CH/C spouse living in CH | Subject? | Source |
|---|---|---|---|---|---|---|
| 1 | no | any | – | – | yes | F-TR-037 |
| 2 | yes | CH | – | – | no | F-TR-006 |
| 3 | yes | not CH | C | any | no | F-TR-025 |
| 4 | yes | not CH | B / other | yes | no | F-TR-031 |
| 5 | yes | not CH | B / other | no | yes | F-TR-040 |

A reviewer can see at a glance that the table is complete (hit policy: first match, rows exhaustive), which the 300-character boolean expression doesn't allow. It also makes OQ-02 ("I think that's it") concrete: the question becomes "is there a row 6?".

### 3. Turn the cross-cutting behaviours into numbered EARS requirements

`conventions.md` currently has "Behaviour every implementation must follow" as prose bullets with no IDs or sources. Make them `behaviours.md` with stable IDs, EARS wording and evidence, like everything else:

- **BR-01** WHEN an answer changes, THE questionnaire SHALL re-evaluate every `ask_when`, `required_when` and derived rule.
- **BR-02** WHEN a field becomes hidden, THE questionnaire SHALL discard its stored value. _(data minimisation: brief, "collect personal data we should not have")_
- **BR-03** IF a shown field with a true `required_when` is empty, THEN THE questionnaire SHALL prevent completing that step.
- **BR-04** WHEN the employee changes `first_working_day` after submission, THE system SHALL notify HR. _(F-TR-016, Julia; only if you decide it's in scope)_

This keeps EARS where it is strong (behaviour) and away from where it is weak (field data).

### 4. Add a consumer view: `consumers/<party>.md`

Today each field says who needs it; nothing shows the reverse. One generated file per party (pension fund, source tax, HR) listing every value it receives, its target field name, the value mapping (`married` → "Married", ISO date → portal format), and which of its required fields have no source yet. This is where "ask too little → registration blocked" becomes checkable: every required portal field must be mapped or listed as an open question. It also gives the building agent the export/hand-off spec, which is currently implicit.

### 5. Make the template itself a reusable artefact

Split generic from process-specific so the next process (offboarding, address change) starts from the same structure:

- `requirements/_template/` holds `conventions.md`, the condition language, file templates, and a **JSON Schema for the front matter** of fields, rules and notices.
- The pipeline validates every generated file against the schema (fail closed). Agents building from it can also validate their reading.
- `employee-onboarding/` keeps only process content.

### 6. Small fixes

- Add a one-paragraph "Purpose and users" with two or three user stories to the package README. That is the honest place for stories: context, not contract.
- Add `last_changed` (run id or date) to front matter and generate a `CHANGELOG.md` by diffing runs. Cheap, and it is the backbone of the "what if a source changes tomorrow" part of the video.
- Fields with `status: inferred` whose trace judge says "partial" (e.g. `spouse_employed`, where the boolean form isn't backed) should list *which attribute* is unbacked, so an agent knows what is safe to build.

## What not to change

The per-field files with YAML front matter, the five-question sections, the condition language with explicit null semantics, `status` + evidence quotes, open questions with recommendations, and out-of-scope. These already cover what the brief asks for better than any single textbook format.

## Sources

- [Kiro specs explained (EARS)](https://codemyspec.com/blog/kiro-specs-explained), vendor-written, comparison sections promotional
- [Writing requirements for AI coding agents (Bilotta)](https://johnnybilotta.com/post/writing-requirements-for-ai-coding-agents/)
- [Spec-driven development: structuring requirements for AI agents (Synodus)](https://synodus.com/thought-leadership/spec-driven-development-how-to-structure-requirements-for-ai-agents/)
- [DMN-guided prompting (arXiv 2505.11701)](https://arxiv.org/html/2505.11701v2)
- [CSIRO Smart Forms: FHIR SDC conditional logic](https://smartforms.csiro.au/docs/sdc/conditional)
- Earlier project research: [agent-requirements-extraction-patterns.md](agent-requirements-extraction-patterns.md)

---

## Addendum (13 Nov, afternoon): what big tech pipelines actually output

TH asked whether user stories might be the right fit after all. Short answer: the big spec-driven pipelines **do** use user stories, but as the framing layer on top of precise, ID'd requirements, not as the precise layer itself. That supports adding stories to our package, on top of the field specs, not replacing them.

| Who | Pipeline output | Role of user stories | Where the precision lives |
|---|---|---|---|
| **GitHub Spec Kit** (also taught by Microsoft Learn) | `spec.md` → `plan.md` → `tasks.md` | "User Story N – title (Priority P1)", each with *Why this priority*, *Independent Test* and Given/When/Then *Acceptance Scenarios* | `FR-001: System MUST …` functional requirements, a **Key Entities** section for data, `SC-001` measurable success criteria, inline `[NEEDS CLARIFICATION: …]` markers |
| **AWS Kiro** | `requirements.md` → `design.md` → `tasks.md` | Stories group the requirements | Each acceptance criterion is an EARS line ("WHEN … THE SYSTEM SHALL …"); data models go in `design.md` |
| **Uber** PRD Evaluator | Scorecard on a PRD (Ready / Ready with caveats / Not ready) | Not prescribed at all | Fixed review dimensions (scope, UX impact, metric and data rigor) |
| **Thoughtworks / Martin Fowler** (independent review of Kiro, Spec Kit, Tessl) | – | Criticised: Kiro turned a small bug into 4 stories and 16 criteria; "it's sometimes unclear who their intended user is" | Spec Kit's files were "repetitive" and hard to review; more specific specs made agent output more repeatable, and parseable specs allow validity checks that prose loses |

Sources: [Spec Kit spec template](https://github.com/github/spec-kit/blob/main/templates/spec-template.md), [Microsoft Learn: write an effective spec.md](https://learn.microsoft.com/en-us/training/modules/spec-driven-development-github-spec-kit-enterprise-developers/5-write-effective-spec-file), [Kiro: requirements-first](https://kiro.dev/docs/specs/feature-specs/requirements-first/), [Kiro: spec concepts](https://kiro.dev/docs/specs/concepts), [Uber: first-pass PRD](https://www.uber.com/ad/en/blog/first-pass-prd/), [Böckeler on martinfowler.com](https://www.martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html), [Thoughtworks Radar: spec-driven development](https://www.thoughtworks.com/radar/techniques/spec-driven-development). I found no public write-up from Google, Meta or Amazon retail on their internal requirements format for agents; the published, reusable formats are Spec Kit and Kiro.

### What this means for us

Our package already maps almost one-to-one onto Spec Kit, with the data part much stronger because this feature *is* data:

| Spec Kit | Our package |
|---|---|
| User stories + acceptance scenarios | **missing** (scenarios proposed above) |
| `FR-###` "System MUST" | `fields/*.md`, `rules/*.md` (+ proposed `BR-##` behaviours) |
| Key Entities | `fields/*.md` front matter (far more precise) |
| `[NEEDS CLARIFICATION]` | `open-questions.md` (with options and a recommendation) |
| Success criteria | not present; could be "no registration blocked by missing data", "no source-tax questions shown to exempt employees" |

So the revised recommendation is a **two-layer** output:

1. **`stories.md` on top (new).** Six or so stories, each with an ID, priority, the transcript pain point it comes from, the fields/rules it covers and the scenarios that accept it. This is where the *why* lives, and the transcript is full of it. Examples:
   - **US-01 (P1)** As an HR manager, I want only employees who are subject to source tax to see the source-tax questions, so that Swiss employees aren't bothered and don't call me. _Source:_ F-TR-004/005. _Covers:_ `subject_to_source_tax`, step 6. _Accepted by:_ SC-01, SC-02, SC-03.
   - **US-02 (P1)** As the pension fund, I want a complete registration, so that it isn't blocked. _Covers:_ every field with `consumers: pension_fund`. _Accepted by:_ consumer view check (every required portal field mapped).
   - **US-03 (P1)** As an HR manager, I want the first working day confirmed and kept up to date, so that the insurance start date at the fund is right (Julia case). _Covers:_ `first_working_day`, `insurance_start_date`, notice. _Accepted by:_ SC-04, SC-05.
   - **US-04 (P2)** As an HR manager, I want new employees reminded to bring their permit. _Covers:_ `permit_type`, `permit_reminder`.
   - **US-05 (P1)** As a new employee, I want to be asked each thing once and only what applies to me. _Covers:_ BR-01 to BR-03 (conditions, discard hidden values).
2. **Field, rule and behaviour specs underneath (existing, plus the changes above).** Stories link down to them by ID; each field file gets a `stories: [US-01]` key so the link is traceable both ways and the pipeline can check every field belongs to at least one story (no orphan data = data minimisation) and every story has at least one passing scenario.

Why not stories alone, even given big tech's use: in every one of these tools the story is not what the agent implements against; the EARS line, the `FR-###` or the entity definition is. For a conditional questionnaire, those precise items are our field specs. Stories alone would also hit Thoughtworks' criticism directly: here the "user" of most requirements is a receiving party (pension fund, tax office), not the person filling in the form.
