# Proposal: feature specs as the pipeline's output

_13 Nov 2026 · For TH. Proposal only; the pipeline repo is unchanged._

Files in this folder:
- **proposal.md** (this file): output structure, story template rationale, Linear mapping, pipeline changes
- [user-story-template.md](user-story-template.md): the template
- [example-US-03-source-tax-liability.md](example-US-03-source-tax-liability.md): one story fully worked out from the real facts

## 1. What the output becomes

A **feature spec** is one folder per feature: a short overview plus a set of user stories with acceptance criteria. Each story becomes one Linear issue later; for the exercise they are `.md` files.

```
feature-specs/employee-onboarding/
  README.md            feature overview: goal, personas, receiving parties, story map, success criteria, glossary
  stories/
    US-01-personal-details.md
    US-02-home-address.md
    US-03-source-tax-liability.md      ← worked example
    US-04-source-tax-tariff.md         (blocked by OQ-01, the calculator)
    US-05-civil-status.md
    US-06-first-working-day.md
    US-07-permit-reminder.md
    US-08-ask-once-and-only-what-applies.md   (cross-cutting behaviour)
  information.md       generated index: every piece of information × the five questions, linked to its owning story
  open-questions.md    each one blocks named stories
  out-of-scope.md
  traceability.md      story / rule / AC → fact → verbatim quote
```

**What's in scope:** what the employee is asked, in what form, when, whether it's required, what it depends on, who needs it, the business rules, and examples proving them.

**What's out of scope (engineering's job):** data models, storage formats, APIs, UI components, the condition expression language, validation implementation. The current `conventions.md` and the expression strings leave the deliverable. The pipeline keeps them internally, because it needs them to *check* the stories (see 4b).

**Why `information.md` stays:** the brief requires every piece of information to answer the five questions, and Lonio's promise is "ask once". With stories alone, the same field could appear in three stories with three slightly different conditions. Rule: **each piece of information and each rule is owned by exactly one story**. Other stories reference it under `depends_on`. `information.md` is generated from the stories, so reviewers (and Lonio's agents) can still see the whole questionnaire at a glance.

## 2. The user story template, and why it looks like this

The template is **Example Mapping** written down: story → rules → examples → questions (Matt Wynne's technique, the most widely recommended way to get precise acceptance criteria), plus the evidence that makes the pipeline's output provable. That core applies to any feature. For stories that collect data (like onboarding), an optional section adds the five-question table the brief asks for. Tracker fields (Linear milestone, labels, issue id) are optional tooling metadata added by a publisher, not part of the spec.

| Section | Why it's there | Source |
|---|---|---|
| Front matter | Machine contract for the pipeline's checks (id, persona, priority, blocked by, owned rules, sources). `information` / `receiving_parties` only for data-collection stories; Linear fields optional and filled by the publisher | Spec Kit's priority per story; Linear's issue fields |
| Title, outcome-phrased | Linear's own guidance is "short and simple issue titles that directly state what the task is". The title is what people see in Linear | [Linear Method](https://linear.app/method/write-issues-not-user-stories) |
| As a / I want / so that | The "so that" carries the why; the persona comes from a fixed list in the README, to avoid the "unclear who the user is" problem | Connextra format; [Thoughtworks Radar](https://www.thoughtworks.com/radar/techniques/spec-driven-development) critique |
| Why, with a verbatim quote | Linear recommends quoting users directly rather than summarizing. It's also the strongest evidence for a reviewer | [Linear Method](https://linear.app/method/write-issues-not-user-stories) |
| Information collected (five-question table), *optional* | Only for stories that collect data. The brief's checklist, per piece of information. Rule-oriented, because field-level behaviour reads badly as Given/When/Then | [AltexSoft on rule- vs scenario-oriented AC](https://www.altexsoft.com/blog/business/acceptance-criteria-purposes-formats-and-best-practices/) |
| Rules (R1…), decision table when the rules combine | Rules alone "hide the gaps"; more than 3–4 rules means the story should be split | [Wynne](https://mattwynne.net/awesome-acceptance-criteria), [Levison on Example Mapping](https://agilepainrelief.com/blog/example-mapping-your-secret-weapon-for-effective-acceptance-criteria/) |
| Acceptance criteria as Given/When/Then examples | Each proves one rule, pass/fail, using real cases from the sources (Maria, Tomás, Stefan, Julia). Spec Kit and Kiro both use this shape | [Spec Kit template](https://github.com/github/spec-kit/blob/main/templates/spec-template.md) |
| Open questions with "until decided" | Wynne: include "questions we couldn't answer yet". Spec Kit's `[NEEDS CLARIFICATION]`. The recommendation keeps the story buildable | as above |
| Not in this story | Prevents the overlap that breaks "ask once" | – |
| Evidence | Lonio's "proof for every line" | Challenge brief |

**One tension to know about.** Linear's own method argues *against* user stories ("write issues not user stories"). The template answers that by giving each story a plain, outcome-phrased title and a short top section. The story sentence and acceptance criteria sit in the description, and the long evidence table can move to a linked Linear document when publishing. Worth one sentence in the video.

## 3. Mapping to Linear (later, via MCP)

| Feature spec | Linear |
|---|---|
| Feature folder | Project (README → project description) |
| Milestone (optional front matter) | Project milestone, e.g. "Liability check" before "Tariff details" |
| Story | Issue: title = `title`, description = rendered story body, priority, labels (+ receiving parties) |
| `blocked_by: [OQ-…]` | Open question = issue labelled `needs-decision`, with a "blocks" relation to the story |
| Evidence | Collapsed section in the issue, or a linked project document |

The existing `pipeline/publish/linear_plan.py` already has the right idempotency model (an id → issue map plus a content hash; update with a comment; never delete). It only needs to switch from one issue per field to one issue per story. Git stays the source of truth; Linear is a projection. Engineering owns status, estimate, assignee and cycle.

## 4. Pipeline changes

### a. Keep the knowledge model; add stories as a view on it (the core change)

Don't let an agent write stories straight from facts. The pipeline's strength is the canonical, checked `spec.json` (information items, rules, conditions, open questions, each citing facts). Stories should be a **slicing** of that model, not a second source of truth:

```
… synthesize ──► decide ──► slice into stories ──► check ──► render ──► naive builder ──► review ──► publish
                            (agent: story map)     (+ story   (story      (reads stories    
                                                    checks)    templates)  only)             
```

- **New stage: `slice`** (agent, structured output). Input: `spec.json`, personas and story guidance from the profile, and the previous `stories.json` as a baseline. Output: `stories.json`, where each story has persona, I want / so that, owned information and rules, Given/When/Then examples, priority, milestone and blocked_by. The agent only writes prose and groupings. All facts, conditions and options come from `spec.json` by id, so it can't invent requirements.
- **Story ids are a registry.** The same mechanism LIMITATIONS #9 already proposes for field ids: reuse existing story ids, never renumber, and mark a story withdrawn with a reason.
- **Decisions can target stories** (`story.US-03.priority`, `story.US-03.split`), like fields today.
- The current `requirements/` rendering (field and rule files) moves to `build/<problem>/model/` as an internal artefact. It's still useful for debugging and for the video, but it's not the deliverable.

### b. Story checks (deterministic, no LLM)

Add to `checks/mechanical.py`:

1. **Ask once:** every information item and rule is owned by exactly one story; every reference points to an existing story.
2. **Five questions answered** for every owned information item (moved from the field lint).
3. **Every rule has at least one acceptance criterion**, and every criterion names the rule it proves.
4. **Acceptance criteria are executable.** Each Given/When/Then is stored as structured answers → expected shown, hidden, required or derived in `stories.json`, and is run through the existing condition engine. **This replaces hand-written `personas.yaml` with tests that live inside the stories** and fixes LIMITATIONS #3, because every rule must now have an example.
5. **No technical content:** a lint for engineering vocabulary (API, endpoint, database, table, React, JSON, …) in story bodies. It keeps the scope promise enforceable.
6. **Testable wording:** a banned-vague-words list ("fast", "easy", "appropriate"…), as in [requirements-to-backlog](https://github.com/pablodpavon/requirements-to-backlog).
7. **Story size:** warn when a story has more than 4 rules (outside a decision table) or more than ~8 information items.
8. **Blocked stories are consistent:** a story with an open blocking question has `status: needs-decision`.

The naive builder then reads only `feature-specs/`, and its job becomes "could you build *and test* this from the stories alone?"

### c. Extensibility: what to make pluggable

The repo already splits engine, adapters and problems. The remaining hard-coding is the **requirement shape** and the **output format**. Make both declared in `profile.yaml`:

```yaml
requirement_shapes: [data_collection]     # later: workflow, business_rule, notification, integration
output:
  format: feature_spec                    # renderer + templates + checks
  personas: [new_employee, hr_manager]
  publish: [markdown, linear]
```

- **Shape plugin** = one folder: a schema for its knowledge items, synthesis guidance, lint rules and story-slicing hints. `data_collection` is today's field, rule and condition model. A shape like `workflow` (e.g. "HR is notified when the first working day changes", the Julia case) can be added without touching the engine. This is LIMITATIONS #10.
- **Output plugin** = templates + checks + an optional publisher. `feature_spec` (stories) is the default; the old data dictionary stays available as `data_dictionary`.
- **Skills follow:** `/new-problem` scaffolds personas and a story map; a new `/new-shape` skill sits beside `/new-adapter`.

### d. Scalability: many features, many sources, many runs

1. **A shared knowledge base across features.** Today facts live per problem. Lonio's promise ("ask each piece of information once and use it everywhere") is really cross-feature. Onboarding, address change and offboarding all ask about the address. Move normalized units and verified facts to a shared `knowledge/` store keyed by source, plus a shared **information registry** (id, definition, form, receiving parties). Each feature's synthesis then *reuses* registry items instead of re-inventing `address_country` versus `residence_country`. This is the highest-leverage change for "the next process" and for the video.
2. **Incremental synthesis per subject** (LIMITATIONS #2) and **unit-level caching** (#8). A changed transcript turn reruns only the facts from it, the subjects they touch, and the stories that own those subjects. The output diff is then a story-level changelog: "US-03 changed: R3 added, AC-3 new; reason: T-038 changed."
3. **Parallelism:** extraction is already per source. Slicing and judging can run per story in parallel, because each story is independent once the model is fixed.
4. **Model tiering by eval:** keep Opus for synthesis and slicing; move extraction and judges to Sonnet where the gold-set numbers allow (LIMITATIONS #12).
5. **Two-way Linear sync:** answers on `needs-decision` issues flow back into `decisions.yaml` (LIMITATIONS #11). This turns Linear into the human-in-the-loop surface at scale.

## 5. Suggested order for the deadline (Sun 20:00)

| Priority | Work | Rough size |
|---|---|---|
| Must | `Story` schema + `slice` agent + story templates + render `feature-specs/` | ½ day |
| Must | Story checks 1–4 (ask once, five questions, rule ↔ AC, executable AC replacing personas) | ½ day |
| Should | Checks 5–8, naive builder on stories, `linear_plan.py` per story | 2–3 h |
| Could (describe in LIMITATIONS and the video) | Shape and output plugins, shared knowledge base and information registry, incremental synthesis, two-way Linear sync | – |
