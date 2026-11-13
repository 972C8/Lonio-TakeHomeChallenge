---
id: insurance_start_date
kind: rule
output_type: date
expression: "first_of_month_on_or_after(first_working_day)"
depends_on: [first_working_day]
status: confirmed
sources: [F-TR-017, F-TR-018, F-TR-019, F-SC-007, F-SC-008, F-SC-021, G-08]
---

# Rule: `insurance_start_date`

Pension fund insurance start: the first working day if it is the 1st of a month, otherwise the 1st of the following month.

**Derived, never asked.** Computed from the answers as:

```
insurance_start_date = first_of_month_on_or_after(first_working_day)
```

Output type: `date`. Inputs: `first_working_day`.

## Who needs it?
| Party | Purpose | Their field |
|---|---|---|
| Pensionskasse Muster (BVG registration via employer portal) | BVG registration (required, DD.MM.YYYY, must be the 1st of a month) | Insurance start date |

## Evidence
- **F-TR-017** (hr_transcript): Pension fund insurance starts on the first day of the month following the first working day (e.g. first working day 15 March -> insurance start 1 April).
  - "because insurance starts on the first of the following month. So for her that was the first of April" — T-026, Anna
- **F-TR-018** (hr_transcript): Exception: if the first working day is exactly the first of a month, insurance starts on that same day.
  - "Unless somebody starts exactly on the first, of course, then it's just that day." — T-028, Anna
- **F-TR-019** (hr_transcript, inferred): Consolidated: insurance_start_date is derived from first_working_day: if first_working_day is the 1st of a month, insurance starts that day; otherwise it starts on the 1st of the following month. It should be derived, not asked.
  - "because insurance starts on the first of the following month." — T-026, Anna
  - "Unless somebody starts exactly on the first, of course, then it's just that day." — T-028, Anna
- **F-SC-007** (pension_portal): The pension fund registration form has a required 'Insurance start date' field in the 'Insurance' section.
  - "Insurance start date" — 01-empty.png (S01-E17)
  - "Insurance" — 01-empty.png (S01-E16)
- **F-SC-008** (pension_portal): Insurance start date is entered as DD.MM.YYYY and must be the 1st of a month.
  - "DD.MM.YYYY. Must be the 1st of a month." — 01-empty.png (S01-E18)
- **F-SC-021** (pension_portal, inferred): The portal requires an insurance start date on the 1st of a month but does not say how it relates to the first working day (e.g. 1st of the start month or next month); the derivation rule insurance_start_date is open.
  - "DD.MM.YYYY. Must be the 1st of a month." — 01-empty.png (S01-E18)
- **G-08** (product owner guidance): Prefer asking for primary facts and **deriving** values (e.g. ask the first working day, derive the insurance start date) instead of asking the employee for values they cannot know.

_Trace judge: supported – F-TR-017/018/019 give the derivation rule and F-SC-007/008 give the pension fund's required DD.MM.YYYY 1st-of-month format._
