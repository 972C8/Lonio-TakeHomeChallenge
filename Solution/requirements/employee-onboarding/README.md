# Feature specs: Employee onboarding questionnaire

Define what Lonio asks a new employee during onboarding: which information, in which steps and order, and under which conditions - asking each piece of information once and reusing it for every receiving party. Must include a questionnaire flow overview.


These feature specs describe **what** is needed and **why**, with acceptance
criteria and concrete examples. They contain no technical decisions: how to
build it is up to engineering. Every statement is traceable to a source quote,
a product-owner guideline (G-) or a product decision (D-).

## The feature

This is **one feature**: [Employee onboarding questionnaire](feature.md). Each user story
is its own file in [stories/](stories/); the stories are grouped into sections:

| # | Section | Purpose | Stories | Open questions |
|---|---|---|---|---|
| 1 | [Personal details and home address](feature.md#SEC-01-identity-and-address) | Collect the employee's name, date of birth and full postal address, plus the canton for residents of Switzerland. The pension fund needs these to register the employee, HR needs them to post documents, and the address country decides most later conditions. | 4 | 1 |
| 2 | [First working day and insurance start date](feature.md#SEC-02-start-date-insurance) | The employee enters and thereby confirms the first working day. Lonio derives the pension fund insurance start date from it, always from the latest date. | 2 | 0 |
| 3 | [Civil status and spouse for the pension fund](feature.md#SEC-03-civil-status-spouse) | Ask the civil status once. Map it to the pension fund's list and to the source tax view, and ask the spouse's or registered partner's date of birth when the fund registers the employee as Married. | 4 | 2 |
| 4 | [Source tax liability check](feature.md#SEC-04-source-tax-liability) | Decide whether the employee is subject to source tax with as few questions as possible: home country, then nationality and C permit for residents of Switzerland, then the spouse's residence, nationality and C permit. Only employees subject to source tax get the tariff questions. | 3 | 1 |
| 5 | [Source tax tariff basics and computed result](feature.md#SEC-05-tariff-basics) | For employees subject to source tax, ask the denomination and whether the spouse or partner is employed. Combine these with the child and cross-border results into the full Zurich tariff code (or the Liechtenstein result), so HR no longer uses the calculator. | 4 | 1 |
| 6 | [Children for the source tax tariff](feature.md#SEC-06-children) | For employees subject to source tax, ask whether they have children and go through one block per child. This decides whether each child counts (and whether it counts towards an H tariff), which gives the child digit and the H tariff. | 6 | 0 |
| 7 | [Employees living abroad (Germany, Liechtenstein)](feature.md#SEC-07-living-abroad) | Derive the state of residence from the home address. Ask cross-border commuters in Germany or Liechtenstein about daily return, the certificate of residence and the non-return days they expect, to decide between the cross-border tariff, the normal tariff and the Liechtenstein 'in principle no liability' result. | 3 | 0 |
| 8 | [Completing and submitting the questionnaire](feature.md#SEC-08-completion-and-submission) | Give the employee the step-by-step questionnaire flow. Show the permit reminder at the end, discard answers that no longer apply on submission, and make the questionnaire read-only afterwards, with every derived result always taken from the latest answers. | 4 | 0 |

The order in which the user is asked is in [Questionnaire flow](feature.md#flow).

## How to read the feature spec
- **User stories** (`US-x.y`): who wants what and why, with priority.
- **Acceptance criteria** (`AC-x.y.z`): Given / When / Then in business
  language. Where a criterion involves conditions or rules, an **examples**
  table gives concrete cases – real cases from the sources first. ✅ in the
  "Checked" column means the pipeline executed the example against the
  consolidated business rules and it holds.
- **Information needed**: what, when asked, when required, depends on, who
  needs it – for every piece of information in a section.
- **Business rules**: plain-language rules with decision tables.
- **Evidence**: the source quotes behind the feature.
- The header of each file (between `---` lines) is traceability metadata for
  tools (e.g. syncing to an issue tracker), not a data model.

Also: [information.md](information.md) (all information, asked once),
[open-questions.md](open-questions.md), [out-of-scope.md](out-of-scope.md),
[traceability.md](traceability.md).

## Stakeholders
- new employee - provides the information
- HR - the customer company's HR (Muster AG), runs onboarding and registrations
- pension fund - Pensionskasse Muster, registers the employee for occupational pension (BVG)
- source tax office - source tax tariff determination (Canton of Zurich calculator)

_Generated by the requirements pipeline from the sources. Do not edit by hand:
change sources, guidance or decisions and re-run._
