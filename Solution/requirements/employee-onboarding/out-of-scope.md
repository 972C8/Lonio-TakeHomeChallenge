# Out of scope

Explicitly **not** part of these feature specs.

- **Photo for employee badges** – Security is changing the badge system next year; revisit then.
  - F-hr_transcript-7668e6: The photo is out of scope for now because security is changing the badge system next year. It may be revisited next year. — "Let's not do that now. Forget the photo for the moment, we'll talk about it next year." (hr_transcript/T-020, Anna) — "Okay, no photo." (hr_transcript/T-021, Leo)
  - F-hr_transcript-2077cc: HR would like the form to ask for a photo for employee badges. Today reception takes poor phone pictures. — "Oh, that would be so nice, actually. For the badges." (hr_transcript/T-018, Anna) — "Could the form ask for a photo?" (hr_transcript/T-018, Anna)
- **IT equipment (laptops)** – IT has its own process.
  - F-hr_transcript-f23d48: IT equipment (laptops) is out of scope. IT has its own process. — "IT does laptops, they have their own process, keep them out of this, please." (hr_transcript/T-042, Anna)
  - G-03: **Out of scope:** social insurance (AHV) data, IT equipment, anything not needed by the parties above.
- **Social insurance (AHV) data** – Not needed by the receiving parties in scope.
  - G-03: **Out of scope:** social insurance (AHV) data, IT equipment, anything not needed by the parties above.
- **Income type and replacement-income questions (tariffs G and Q)** – A new employee always has earned income.
  - D-006: A new employee always has earned income. Do not ask the income type, and drop the replacement-income questions and the tariff G / Q cases. This closes OQ-income-type. To be verified by a domain expert.
  - F-zh_source_tax_calculator-e06ffd: The calculator asks which income the source tax tariff is to be determined for. — "Für welche Einkünfte möchten Sie den Quellensteuertarif ermitteln?" (zh_source_tax_calculator/C-Q01)
  - F-zh_source_tax_calculator-2d4dda: Replacement income (Ersatzeinkünfte) yields tariff G (cross-border variant Q), without child digit or confession suffix. — "Answers {"Q01": "Ersatzeinkünfte", "Q16": "Ja"} -> result Tarif: G" (zh_source_tax_calculator/C-V43)
- **Permit type of the employee and spouse (permit_type, spouse_permit_type)** – Only 'C permit or not' drives a rule; asked as yes/no instead (data minimisation).
  - D-005: Do not ask for the permit type. Ask non-Swiss employees only whether they hold a C permit (permanent residence), yes or no, and the same for a non-Swiss spouse. No party needs any other permit type. This closes OQ-permit-list. To be verified by a domain expert.
  - G-01: Lonio collects onboarding data from a new employee **once** and reuses it for every receiving party. Asking too little blocks a registration; asking too much collects personal data we must not have (data minimisation). A question must only be asked when at least one receiving party needs the answer for this person.
- **Special tariffs (e.g. D for a second job) and cases the calculator does not cover (artists, board fees, hardship cases, pensions)** – Out of scope for onboarding.
  - D-009: Before go-live a domain expert compares Lonio's computed tariff code with the calculator for the paths not explored (residence block for A/B/H, more than 3 children, H3N/P3N). Special tariffs such as D (second job) are out of scope for onboarding. Keep OQ-calculator-coverage open as a non-blocking go-live condition.
  - F-zh_source_tax_calculator-74fb68: Cases not covered by the calculator: fees to artists, athletes and speakers; board fees paid to persons resident abroad; hardship cases; pensions and capital benefits from pension provision. — "'Gagen an Künstler, Sportler und Referenten', 'Verwaltungsratshonorare, welche an Personen mit Wohnsitz im Ausland bezahlt werden', 'Härtefälle', 'Renten und Kapitalleistungen aus Vorsorge'" (zh_source_tax_calculator/C-N02)
- **Transmission of data to the receiving parties (exports, portal entry, change notifications, portal validation messages)** – Separate topic; this spec covers what is asked.
  - G-04: Scope of these feature specs: what Lonio asks the new employee (which information, in which order, under which conditions, required or not) and the business rules derived from the answers. How collected data is transmitted to each receiving party (exports, portal entry, change notifications) is a separate topic; each information item documents which stakeholder needs it and why.
  - F-pension_portal-e45e5b: No screenshot shows the validation error for an insurance start date that is not the 1st of a month or for a malformed date; its behaviour and wording are unknown. — "DD.MM.YYYY. Must be the 1st of a month." (06-required-errors.png (pension_portal/S06-E19))
- **Starting the onboarding, HR screens, HR changes after submission** – Only the employee side is in scope; HR-side needs (Liechtenstein flag, changing the first working day) go to a later spec.
  - D-034: Only the employee side is in scope. Who starts the onboarding and any HR screen are specified later; the spec says answers are recorded for HR, not 'available to HR'. HR-side needs from D-007 (flag) and D-033 (HR changes the date) are noted for that later spec.
  - D-037: After submission the questionnaire is read-only for the employee. Any later change (a move, a marriage, a new child, a certificate of residence handed in later, a corrected nationality) is made by HR and belongs to the later HR-side spec (D-034). Every derived result (insurance start date, civil status for the fund and for source tax, subject to source tax, tariff code) is always derived again from the latest answers, as for the first working day (D-033).
- **Upload of documents (certificate of residence, proof of non-return days, permit)** – Documents go to HR outside Lonio.
  - D-035: For the cross-border questions the employee states what they expect for the year (non-return days). For the certificate of residence 'not yet' is a valid answer and counts as 'no' for the tariff code. Documents go to HR outside Lonio; no upload.
- **History of earlier first working days** – Only the latest date counts.
  - D-033: The employee enters the first working day. After submission only HR can change it; the latest date always counts and no history of earlier dates is kept.
