# Notices

Texts shown to the employee that collect no data.

## permit_reminder
- Step: `citizenship`
- Shown: `is_set(permit_type)`
- Text: "Please bring your residence permit with you on your first working day."
- Evidence:
  - **F-TR-029**: Anna would love the form to remind employees to bring their permit (on the first day), because half of them forget; wording to be looked at later, not decided. — "What I would love is if the form could remind people to bring their permit. Half of them forget." (T-042, Anna) — "We can look at the wording later." (T-043, Leo)

## first_working_day_confirm
- Step: `employment`
- Shown: `is_set(first_working_day)`
- Text: "Your pension fund insurance starts on the 1st of the month on or after your first working day. If your start date changes, please update it here right away."
- Evidence:
  - **F-TR-015**: The employee's first working day is needed (for the pension fund) and is the most important item; the employee should confirm it. — "I need their first working day. That's the number one thing, and I ask them to confirm it" (T-024, Anna)
  - **F-TR-016**: The first working day changes often, e.g. when people negotiate an earlier exit with their old employer; a missed update (Julia) caused a wrong date at the fund and weeks of fixing. — "because it moves more often than you'd think." (T-024, Anna) — "She moved her first working day to the 15th of March, and I didn't update it." (T-026, Anna) — "It took weeks to fix." (T-028, Anna)
  - **F-TR-019**: Consolidated: insurance_start_date is derived from first_working_day: if first_working_day is the 1st of a month, insurance starts that day; otherwise it starts on the 1st of the following month. It should be derived, not asked. — "because insurance starts on the first of the following month." (T-026, Anna) — "Unless somebody starts exactly on the first, of course, then it's just that day." (T-028, Anna)

