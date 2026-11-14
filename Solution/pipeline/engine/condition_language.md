INTERNAL formalisation used by the pipeline to verify examples (never shown
in the feature specs). Conditions and rules are expressions in a tiny,
Python-flavoured language:

- Identifiers are information item ids or rule ids (snake_case). An unanswered or
  not-asked item evaluates to `null`.
- **Null semantics:** any comparison involving `null` is `false` – including
  `!=` and `not in` – unless null is compared explicitly (`x == null`,
  `x != null`). So `country != "CH"` is false while country is
  unanswered: a question never appears, and a rule is never true, because of
  a missing answer. (`not (...)` still negates the whole sub-expression.)
- Built-in context value: `today` (the date the person answers). Examples
  may set it explicitly (`today` as an input) to make date rules testable.
- Literals: `"text"` (double quotes), numbers, `true`, `false`, `null`,
  lists `["a", "b"]`.
- Operators: `and`, `or`, `not`, `==`, `!=`, `in`, `not in`, `<`, `<=`, `>`,
  `>=`, parentheses.
- Functions:
  - `is_set(x)` - true if x has a value
  - `day(d)` - day of month; `first_day_of_month(d)`; `add_months(d, n)`
  - `if_else(condition, a, b)`
  - comparisons work on dates, e.g. `valid_from >= add_months(today, -3)`
  - `date("YYYY-MM-DD")` - a date literal
- Values are compared exactly as written in the examples / allowed values.
- `"true"` as a whole expression means always.

Examples (generic, ids are illustrative only):
    country != "CH" and status != "X"
    choice in ["a", "b"]
    is_set(other_field) or derived_flag
    if_else(day(d) == 1, d, first_day_of_month(add_months(d, 1)))
