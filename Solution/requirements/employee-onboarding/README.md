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
| 1 | [Questionnaire flow overview](feature.md#SEC-01-questionnaire-flow) | Define the eight steps, their order and the conditions under which each step and question appears. Cover saving and resuming, going back without losing answers, discarding answers that no longer apply, the permit reminder, the summary and confirmation, and read-only after submission. | 8 | 0 |
| 2 | [Personal details and home address](feature.md#SEC-02-personal-details-address) | Collect the employee's name, date of birth and complete home address (as on the first working day), plus the canton for the pension fund. Residents of Switzerland choose their canton; for employees abroad Zurich is recorded and the canton is not asked. | 4 | 0 |
| 3 | [First working day and insurance start date](feature.md#SEC-03-employment-start) | Ask for the first working day (the contractual start date) in step 1, without a separate step, and derive the pension fund's insurance start date from it. | 3 | 0 |
| 4 | [Civil status and spouse data](feature.md#SEC-04-civil-status-spouse) | Ask every employee for their civil status, using six values. Map it to the pension fund's four values and to the calculator's two groups. Ask the spouse's or registered partner's date of birth only of married, registered-partner and separated employees. | 4 | 1 |
| 5 | [Who is subject to source tax](feature.md#SEC-05-source-tax-liability) | Decide whether the employee is subject to source tax. Ask nationality and C permit only of residents of Switzerland. Ask the spouse's nationality, C permit and residence only when needed to check the spouse exemption. | 4 | 0 |
| 6 | [Source tax: residence abroad and cross-border questions](feature.md#SEC-08-cross-border-residence) | Group the country of residence as the calculator does. Ask Liechtenstein and Germany residents the cross-border questions (daily return, non-return days, certificate of residence) and derive whether the employee is in principle not liable to source tax (Liechtenstein) or the cross-border tariff applies (Germany). | 4 | 0 |
| 7 | [Source tax tariff: denomination, spouse employment and tariff code](feature.md#SEC-06-source-tax-tariff-basics) | Ask employees subject to source tax for their denomination, whether the spouse is gainfully employed and whether they have children. Combine these with the cross-border and child results into one tariff code (e.g. 'C1Y'), 'no tariff code', the Liechtenstein note, or 'incomplete - HR must complete'. | 6 | 1 |
| 8 | [Source tax tariff: children](feature.md#SEC-07-source-tax-children) | Ask the child questions in one block per child (no maximum, age judged on the first working day). Derive each child's result (counted, counted with H, or not counted) and the child digit of the tariff code. | 6 | 0 |

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
