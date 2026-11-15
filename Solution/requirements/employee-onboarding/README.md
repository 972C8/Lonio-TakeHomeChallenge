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
| 1 | [Questionnaire flow overview](feature.md#SEC-01-questionnaire-flow) | Give the employee one English questionnaire with fixed steps, where each question appears only under its condition. At the end come the permit reminder and a submission that discards answers that no longer apply and makes the questionnaire read-only. | 6 | 0 |
| 2 | [Personal details and home address](feature.md#SEC-02-personal-details-address) | Collect the employee's name, date of birth and complete home address once. HR uses them to post documents and the pension fund to register the employee. The country of the address decides which later questions apply, and the canton is asked only of employees living in Switzerland. | 4 | 1 |
| 3 | [First working day and insurance start date](feature.md#SEC-03-employment-start) | Have the employee confirm their first working day, and derive the pension fund insurance start date from it instead of asking for it. The derived date always follows the latest first working day. | 3 | 0 |
| 4 | [Civil status and spouse data](feature.md#SEC-04-civil-status-spouse) | Ask the civil status once and map it both to the pension fund's list and to the calculator's civil status group. The spouse's or partner's date of birth is asked only where the fund needs it. | 3 | 2 |
| 5 | [Who is subject to source tax](feature.md#SEC-05-source-tax-liability) | Decide from as few questions as possible whether the employee is subject to source tax: country of residence, Swiss citizenship, C permit (yes/no), and the spouse's citizenship, C permit and residence. Only employees subject to source tax are asked the tariff questions. | 3 | 1 |
| 6 | [Source tax tariff: denomination, spouse employment and tariff code](feature.md#SEC-06-source-tax-tariff-basics) | Ask employees subject to source tax for their denomination and, if married or in a registered partnership, whether the spouse or partner works. Combine these with the child digit and the cross-border result into the computed Zurich tariff code that Lonio records for HR. | 5 | 0 |
| 7 | [Source tax tariff: children](feature.md#SEC-07-source-tax-children) | Ask employees subject to source tax whether they have children, then ask the calculator's questions once per child. Each child's answers decide whether that child counts toward the child digit, and whether it makes the tariff letter H for single employees. Before go-live, a domain expert checks the paths that were not observed in the calculator. | 6 | 1 |
| 8 | [Source tax: residence abroad and cross-border questions](feature.md#SEC-08-cross-border-residence) | Derive the calculator's residence answer from the home address. Germany residents are asked the cross-border questions (daily return, certificate of residence, reasonable return, more than 60 non-return days), which decide the cross-border tariff. Liechtenstein residents are asked about daily return and more than 45 non-return days, which can lead to 'in principle no source tax liability' flagged for HR. | 4 | 0 |

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
