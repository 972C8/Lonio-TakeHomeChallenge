Conditions and rules are expressions in a tiny, Python-flavoured language:

- Identifiers are field ids or rule ids (snake_case). An unanswered or
  not-asked field evaluates to `null`.
- **Null semantics:** any comparison involving `null` is `false` – including
  `!=` and `not in` – unless null is compared explicitly (`x == null`,
  `x != null`). So `nationality != "CH"` is false while nationality is
  unanswered: a question never appears, and a rule is never true, because of
  a missing answer. (`not (...)` still negates the whole sub-expression.)
- Literals: `"text"` (double quotes), numbers, `true`, `false`, `null`,
  lists `["a", "b"]`.
- Operators: `and`, `or`, `not`, `==`, `!=`, `in`, `not in`, `<`, `<=`, `>`,
  `>=`, parentheses.
- Functions:
  - `is_set(x)` - true if x has a value
  - `first_of_month_on_or_after(d)` - the given date if it is the 1st of a
    month, otherwise the 1st of the following month
  - `date("YYYY-MM-DD")` - a date literal
- Enum fields are compared by option **value**, countries by ISO 3166-1
  alpha-2 code (`"CH"`).
- `"true"` as a whole expression means always.

Examples (generic, ids are illustrative only):
    country != "CH" and status != "X"
    choice in ["a", "b"]
    is_set(other_field) or derived_flag
    first_of_month_on_or_after(some_date)
