# How the pipeline keeps the result complete and correct

Three layers: **code proves** what it can, **LLM judges** cover what code
cannot, and the **product owner decides** the rest.

## 1. Every claim traces back to a verbatim quote
- **Quotes verified by code:** every fact must quote its source; the quote is
  checked against the source text (`verify_anchors`). A fact cannot cite another
  source's unit. Facts without a valid quote are reported as errors.
- **Fact judge (LLM):** checks per fact that the quote really supports the
  statement (supported / partial / unsupported). Unsupported facts never reach
  modelling.
- **Citation is mandatory:** every item, rule, story and acceptance criterion
  cites facts (F-), guidance (G-) or decisions (D-). A missing or unknown
  reference is an error.

## 2. Completeness, checked by code
- **Item checklist** (`profile.yaml`): every information item must answer what,
  when asked, when required, depends on, who needs it.
- **Coverage:** every item and rule is owned by exactly one section and covered
  by at least one story; every requirement fact must be used somewhere; every
  uncited source unit is listed for a human to confirm as irrelevant.
- **Decision tables:** one cell per input. A broken table goes back to the
  modeler once, with the error.

## 3. Correctness, proved by executing the spec
- **Examples run like tests:** every acceptance-criterion example is executed
  against the formal rules (is a question asked or required, what does a rule
  yield). A failing example names its cause and goes back to the writer once.
- **Expressions** must parse and must not depend on themselves.
- **Trace judge (LLM):** checks each item, rule and story against the facts it
  cites, catching claims that go beyond the sources.

## 4. A simulated refinement meeting
- **Dev refinement (LLM):** an engineer agent reads only the rendered spec and
  lists every question it would ask, plus technical decisions that leaked in.
- **Reviewer (LLM):** turns all findings into a verdict (not ready / ready with
  caveats / ready) and an action list in `review.md`.

## 5. The human loop
- **`/review`** walks the product owner through each finding.
- **Answers become decisions** in `decisions.yaml`: patches are applied by code
  after the agents (cannot be reinterpreted); directives steer the agents before
  they write and are an error if nothing cites them.

## Over time
- **Fingerprinted stages:** a changed source, decision or prompt reruns only
  what depends on it.
- **Stable ids:** fact ids are content-based and source-scoped; item, rule and
  story ids of the last run are fed back to the agents. Decisions and Linear
  issues stay attached to the right things.
- **Incremental reruns:** when only facts changed, the modeler returns a delta
  applied by code, the plan keeps its sections, and only sections whose inputs
  changed are rewritten; untouched stories are restored word for word.
- **New evidence flags decisions:** a decision whose shaped elements now cite
  a fact that did not exist when it was made is flagged for re-confirmation.
- **Decisions remember their evidence:** if the source text a decision rests on
  changes, it is flagged "needs re-confirmation" instead of applied silently. A
  decision whose target disappeared is reported.
- **Corrections win:** a stakeholder's later statement supersedes the earlier
  one; both stay linked.
- **`/update-source`** shows what a changed or new source moved in the spec.
- **`/learn`** turns repeated decisions into prompt lines or new code checks, so
  the same mistake does not come back.
- **Linear publishing** finds issues by their US/OQ id prefix and updates them;
  republishing never duplicates.

## Limits (see [LIMITATIONS.md](../LIMITATIONS.md))
- Examples can only check asked / required / rule results. Workflows,
  notifications and permissions cannot be executed.
- Directives are followed by agents: only their citation is guaranteed, not
  that everything they imply was written.
- LLM judges can be wrong. Their findings go to a human, never straight into
  the spec.
