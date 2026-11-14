# [FEAT-01] Confirmed first working day and derived pension insurance start date

---
id: FEAT-01-first-working-day-insurance-start
title: "Confirmed first working day and derived pension insurance start date"
order: 1
stakeholders: [employee, hr, pension_fund]
stories: [US-01.1, US-01.2]
information: [first_working_day]
rules: [insurance_start_date]
open_questions: []
---

# Confirmed first working day and derived pension insurance start date

**Goal:** Every new employee confirms their first working day, and Lonio works out the pension insurance start date from it, so the fund never gets a wrong or outdated start date.

## Context
HR calls the first working day the most important item. It often changes, so HR asks the employee to confirm it (F-TR-014, F-TR-015). The pension fund requires an insurance start date that is always the 1st of a month (F-SC-008, F-SC-009). HR works it out by hand: if the first working day is the 1st of a month, insurance starts that day, otherwise on the 1st of the following month (F-TR-016, F-TR-017, F-TR-018). Once, an outdated first working day led to a wrong insurance start date at the fund (F-TR-019). Employees cannot know the insurance start date, so Lonio asks only for the primary fact and derives the date (G-08). The employee is not asked for the insurance start date (EX-05).

**Stakeholders:** new employee, HR, pension fund



