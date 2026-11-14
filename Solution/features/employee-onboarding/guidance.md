Domain guidance for **employee onboarding** (written by the product owner;
shared with every agent of this feature). Statements tagged `[G-nn]` are
product-owner input and may be cited as sources (`source_refs`), like facts.

## Context
- [G-01] Lonio collects onboarding data from a new employee **once** and
  reuses it for every receiving party. Asking too little blocks a
  registration; asking too much collects personal data we must not have (data
  minimisation). A question must only be asked when at least one receiving
  party needs the answer for this person.
- [G-02] Receiving parties in scope: the pension fund (Pensionskasse Muster),
  source tax (Zurich tariff calculator), and the employer's HR (Muster AG).
- [G-03] **Out of scope:** social insurance (AHV) data, IT equipment, anything
  not needed by the parties above.
- [G-04] Scope of these feature specs: what Lonio asks the new employee (which
  information, in which order, under which conditions, required or not) and
  the business rules derived from the answers. How collected data is
  transmitted to each receiving party (exports, portal entry, change
  notifications) is a separate topic; each information item documents which
  stakeholder needs it and why.
- [G-05] Simplifications given by the assignment: Switzerland has exactly one
  source tax system (Zurich's) and exactly one pension fund (Pensionskasse
  Muster).
- [G-06] The sources are fictional and simplified. **Treat them as the truth**,
  even where they differ from real Swiss law or general knowledge. Never
  import rules from outside knowledge; if a source does not say it, it is open.
- [G-07] The pension fund screenshots show dropdowns with **all** their
  options.

## Conventions for facts and requirements
- [G-08] Prefer asking for primary facts and **deriving** values (e.g. ask the
  first working day, derive the insurance start date) instead of asking the
  employee for values they cannot know.
- Stakeholder corrections override earlier statements. Keep both as facts and
  link them.
- [G-09] Questionnaire language: English.
- Use these information item ids when the concept exists (do not create an
  item only because it is listed): first_name, last_name, date_of_birth, nationality,
  permit_type, address_street, address_house_number,
  address_postcode, address_town, address_country, residence_canton,
  first_working_day, civil_status, spouse_date_of_birth, spouse_nationality,
  spouse_permit_type, spouse_residence_country. The country of residence is
  the country of the home address (address_country).
- [G-10] Business wording for values (used in allowed values and examples):
  countries by English name ("Switzerland", "Germany", "Liechtenstein"),
  permits as "B permit", "C permit", civil status exactly as the pension
  fund's list shows it ("Single", "Married", ...), dates as DD.MM.YYYY,
  yes/no as "yes"/"no".
- Use these business rule ids when they exist:
  subject_to_source_tax, insurance_start_date.
