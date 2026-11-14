# Information catalogue

Every piece of information the process needs, **asked once** and reused by
every stakeholder. This view answers, for each piece: what, when we ask, when
it is required, what it depends on, and who needs it.

| Information | What? | When do we ask? | When is it required? | Depends on | Who needs it? | Feature |
|---|---|---|---|---|---|---|
| **Street of the new address** | The street of the address the employee is moving to. Form: Part of the new address: street, number, postcode, town and country. | Always | Always |  | hr | [FEAT-01-new-address](features/FEAT-01-new-address.md) |
| **House number of the new address** | The house number of the address the employee is moving to. Form: Part of the new address: street, number, postcode, town and country. | Always | Always |  | hr | [FEAT-01-new-address](features/FEAT-01-new-address.md) |
| **Postcode of the new address** | The postcode of the address the employee is moving to. Form: Part of the new address: street, number, postcode, town and country. | Always | Always |  | hr | [FEAT-01-new-address](features/FEAT-01-new-address.md) |
| **Town of the new address** | The town of the address the employee is moving to. Form: Part of the new address: street, number, postcode, town and country. | Always | Always |  | hr | [FEAT-01-new-address](features/FEAT-01-new-address.md) |
| **Country of the new address** | The country the employee is moving to (the new country of residence). It shows whether the move is within Switzerland or abroad. Form: Part of the new address: street, number, postcode, town and country. Country written as its English name, e.g. "Switzerland", "Germany". | Always | Always |  | hr, payroll | [FEAT-01-new-address](features/FEAT-01-new-address.md) |
| **Valid from** | The date from which the new address applies. Form: Date in the format DD.MM.YYYY. | Always | Always. It may be in the past, but not more than three months ago (see rule valid_from_within_three_months). |  | hr | [FEAT-02-valid-from](features/FEAT-02-valid-from.md) |
| **New canton** | The Swiss canton the employee is moving to. Only needed if the employee moves to a different canton. | Only if the employee moves within Switzerland to a different canton than before. Not asked if the move stays in the same canton or is abroad. | Whenever it is asked | Country of the new address, Previous canton | hr | [FEAT-04-canton-change](features/FEAT-04-canton-change.md) |
| **Previous canton** | The Swiss canton the employee lived in before the move. It is used only to tell whether the canton changes. | Only for moves within Switzerland. It is open whether the employee is asked or HR takes it from its own employee records (see OQ-01). | For moves within Switzerland, so HR can tell whether the canton changes | Country of the new address | hr | [FEAT-04-canton-change](features/FEAT-04-canton-change.md) |

## Derived results (never asked)

- **Payroll must be informed of a move abroad** – If the employee moves abroad (the new country is not Switzerland), payroll must be informed, because the employee may then be subject to source tax. For moves within Switzerland, payroll does not have to be informed. ([FEAT-03-payroll-move-abroad](features/FEAT-03-payroll-move-abroad.md))
- **Move to a different canton** – A move within Switzerland changes canton when the new canton is different from the previous canton. Only then is the new canton needed for the tax office. ([FEAT-04-canton-change](features/FEAT-04-canton-change.md))
- **Valid-from date at most three months in the past** – The valid-from date may be in the past, because people often report late, but not more than three months before the day the employee reports the move. The meeting set no limit for future dates. ([FEAT-02-valid-from](features/FEAT-02-valid-from.md))
