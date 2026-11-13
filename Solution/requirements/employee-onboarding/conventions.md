# Conventions (requirement shape: data field)

This package follows a fixed structure so that agents can build from it
directly and so the same structure can be reused for the next process.

## Files
- `flow.md` – ordered steps; each step lists its fields in order.
- `fields/<id>.md` – one field. YAML front matter is the machine-readable
  contract; the body explains it for humans. Front matter keys:
  - `id` – stable snake_case id, used in conditions and as storage key
  - `step`, `order` – where it appears
  - `type` – `text | date | enum | boolean | country | integer | file`
  - `format`, `options` – exact form of the value (enum stores option values)
  - `ask_when` – condition: show the field only if true
  - `required_when` – condition, evaluated only if shown: must not be empty
  - `depends_on` – ids its conditions reference (computed)
  - `consumers` – receiving parties that need the value
  - `status` – `confirmed` (backed by explicit source statements), `inferred`
    (backed partly by interpretation – flagged for review), `decision`
    (defined by a product decision)
  - `sources` – fact / decision ids, resolved in `traceability.md`
- `rules/<id>.md` – derived values (`expression`), never asked.
- `notices.md`, `open-questions.md`, `out-of-scope.md`, `traceability.md`.

## Behaviour every implementation must follow
- Evaluate conditions in flow order. A hidden field has no value; when an
  answer change hides a field, discard its value.
- A field is shown if its step's condition **and** its own `ask_when` are
  true.
- Required means: the employee cannot complete the step while it is empty.
- Store enum **values**, display labels. Countries are ISO 3166-1 alpha-2.
  Dates are stored ISO `YYYY-MM-DD`, displayed `DD.MM.YYYY`.
- Derived rules are recomputed whenever an input changes.

## Condition language
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

