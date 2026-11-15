# Review: employee-onboarding

**Verdict: NOT READY**

Not ready. One example fails (AC-06.2.3 replacement income, 'null' vs None). Two open questions are blocking (OQ-registered-partnership, OQ-canton). The tariff-letter rule contradicts the spec's own evidence. Several major dev-refinement questions have no answer: scope of the tariff result and HR view, post-submission edits, and HR pre-fill. Internal identifiers leak into business prose. Many items and stories are inferred, and some trace judgements are only partial.

## Reviewer findings

1. **Failing example: replacement-income church tax suffix** – The example is the only failed simulation. It expects the programming value 'null' where the business meaning is 'no suffix'. The row is also marked ❌ and repeats the denomination column.  
   Evidence: examples AC-06.2.3 / Replacement income: church_tax_suffix = None, expected 'null'. tech_leak and dev_refinement on US-06.2.  
   Action: Rewrite the expected result as 'no suffix' and define it unambiguously, e.g. empty. Remove the duplicate column and the ❌, then re-run the examples.
2. **Base tariff H vs A rule contradicts its own evidence** – AC-06.4.3 and rule.base_tariff_letter say H requires the child in the household plus sole custody or main contributor. Three cited facts give H1N in cases that rule excludes. The derivation and its tests cannot be written until this is settled.  
   Evidence: dev_refinement US-06.4 (major). Facts F-zh_source_tax_calculator-dc0ae9, -dc6ace, -3eb561. trace_judge on rule.base_tariff_letter. The widowed adult-child example omits the '>50% maintenance' answer.  
   Action: Add a decision in decisions.yaml on the exact H vs A conditions. This could be 'counted child' rather than household plus custody. Fix AC-06.4.3 and its examples to match, including the digit 0 or 1.
3. **Blocking open question: registered partnership** – Employees in a registered partnership (e.g. Daniel) cannot be registered correctly. The pension fund list has no such status, and the question affects the spouse data and the source-tax exemption.  
   Evidence: OQ-registered-partnership (blocking: true). It affects civil_status, the spouse items, subject_to_source_tax and calculator_civil_status. OQ-separated is related.  
   Action: Ask Pensionskasse Muster through HR. Record a decision. The interim recommendation is to treat registered partners as Married, with OQ-separated resolved consistently.
4. **Blocking open question: pension fund 'Canton' meaning** – It is unknown whether the canton means residence or work, and what to enter for cross-border employees. The field is required and the list has only Swiss cantons. residence_canton is also named and described as the canton of residence without backing.  
   Evidence: OQ-canton (blocking: true). fact_judge on F-pension_portal-b359c3. trace_judge on item.residence_canton. US-02.4.  
   Action: Get the fund's answer and decide what is entered for residents of Germany and Liechtenstein. Rename or reword the item to match.
5. **Scope of the tariff output and HR visibility undefined** – The spec derives only the tariff letter. It also defines the suffix, the digit and the cross-border swap, and says HR can see results. It never says what is computed, who sees it, or when. Engineering cannot size the feature without this.  
   Evidence: dev_refinement US-06.4 (major) and US-05.3 AC-05.3.5 (major). US-01.1 (minor, submit and notify flow).  
   Action: Add a decision on the output. Is it the full code, only the letter or nothing? Who sees it? What are the submit and notify semantics? Update the stories or move HR visibility out of scope explicitly.
6. **Post-submission changes and answer invalidation unspecified** – US-03.3 assumes the first working day changes later, but no actor or mechanism is defined. Going back and changing earlier answers can orphan data that data minimisation forbids keeping.  
   Evidence: dev_refinement US-03.3 (major) and US-01.2 (major). AC-03.3.1.  
   Action: Decide who can edit and until when. Decide whether dependent answers are discarded when upstream answers change. Add ACs for both.
7. **First working day inputs and start-date rule ambiguous** – No story covers HR pre-filling the date. Using the actual first working day instead of the contractual start can push the insurance start to the wrong month. The residence-address timing (current vs at start) changes which questions are asked.  
   Evidence: dev_refinement US-03.1 (major), feature.md insurance rule (major), US-02.3 (major). AC-03.1.2 is untestable as written.  
   Action: Decide whether the date is pre-filled by HR. Decide whether the rule uses the contract start or the first working day, and whether the address is current or as at the start date. Add testable wording.
8. **Item expressions and business text do not match their trace** – Several required_when and asked_when expressions contradict their own business text. Some claims have no cited fact: the 'only if subject' condition, the step order, the Germany/Liechtenstein rows citing missing facts, and the 'sensitive data' note. A developer would build from the expressions.  
   Evidence: trace_judge: spouse_permit_type, has_children, confession, income_type, civil_status, calculator_residence, questionnaire_flow, US-01.2, US-02.4, US-06.1 to US-06.3.  
   Action: Align each expression with its text. Cite the missing hr_transcript facts, or mark the items as decisions. Drop or confirm the unbacked claims.
9. **Source-tax rule only partly confirmed** – The rule decides who sees the whole source-tax section. Anna hedged, and 'here' meaning Switzerland is an assumption. The Liechtenstein result conflicts with HR's 'always subject'. Income type is still modelled as asked.  
   Evidence: OQ-source-tax-rule, OQ-liechtenstein, OQ-income-type. fact_judge on F-hr_transcript-550840 and -5af8d0.  
   Action: Have HR confirm the decision table. Record the product decisions on income type (fixed to earned income) and on which Liechtenstein result counts.
10. **Technical identifiers leak into business prose** – Field and rule ids and UI mechanics appear in acceptance criteria and notes, which turns engineering choices into spec content.  
   Evidence: tech_leak: US-08.1 (address_country), feature.md (insurance_start_date, calculator_civil_status), US-07.2 (Child 1/2 blocks with add/remove).  
   Action: Replace the ids with business terms. State only the need that each child is described separately.

## Numbers

342 source units → 177 facts → 36 information items, 7 business rules → one feature with 8 sections, 29 stories, 86 acceptance criteria; 13 open questions, 6 exclusions.

## Errors (1)

- [examples] `AC-06.2.3 / Replacement income` church_tax_suffix = None, expected 'null'

## Examples executed against the knowledge model (150/151 pass)

- ✅ AC-01.1.1 / Maria, Portuguese with a C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.1.1 / Tomás, Brazilian with a B permit, Swiss wife, living in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.1.1 / Swiss employee living in Switzerland (spec)
- ✅ AC-01.1.2 / Stefan, Swiss national living abroad (hr_transcript/F-hr_transcript-3f2c2a), country of residence assumed Germany (spec)
- ✅ AC-01.1.2 / Employee living in Liechtenstein (spec)
- ✅ AC-01.1.2 / Single non-Swiss employee with a B permit living in Switzerland (spec)
- ✅ AC-01.1.2 / Married B-permit employee whose spouse is not Swiss and has a B permit (spec)
- ✅ AC-01.1.2 / Married B-permit employee whose Swiss spouse lives in Germany (spec)
- ✅ AC-01.2.2 / Employee living in Germany (spec)
- ✅ AC-01.2.2 / Swiss employee living in Switzerland (spec)
- ✅ AC-01.2.2 / Maria, Portuguese living in Switzerland (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-01.2.3 / Tomás, Brazilian with a B permit, married to a Swiss wife (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-01.2.3 / Single B-permit employee living in Switzerland (spec)
- ✅ AC-01.2.3 / Married Swiss employee living in Switzerland (spec)
- ✅ AC-01.2.3 / Married employee living in Germany (spec)
- ✅ AC-02.1.1 / Employee living in Switzerland (spec)
- ✅ AC-02.1.1 / Employee living in Germany (spec)
- ✅ AC-02.1.2 / Employee born 14.03.1990 (spec)
- ✅ AC-02.1.2 / Employee living in Liechtenstein (spec)
- ✅ AC-02.2.1 / Employee living in Switzerland (spec)
- ✅ AC-02.2.1 / Employee living in Germany (e.g. Konstanz) (spec)
- ✅ AC-02.3.2 / Cross-border employee living in Germany (hr_transcript/F-hr_transcript-3f2c2a, Konstanz) (spec)
- ✅ AC-02.3.2 / Employee living in Liechtenstein (spec)
- ✅ AC-02.3.2 / Employee living in Switzerland (spec)
- ✅ AC-02.4.1 / Employee living in Switzerland (spec)
- ✅ AC-02.4.1 / Cross-border employee living in Germany (Konstanz) (spec)
- ✅ AC-02.4.1 / Cross-border employee living in Liechtenstein (spec)
- ✅ AC-02.4.2 / Employee living in the canton of Zurich (spec)
- ✅ AC-02.4.2 / Employee living in the canton of St. Gallen (spec)
- ✅ AC-03.1.1 / Employee starting mid-month (spec)
- ✅ AC-03.1.1 / Employee starting on the 1st of a month (spec)
- ✅ AC-03.2.1 / Start on the 1st of March (spec)
- ✅ AC-03.2.1 / Start on the 1st of January (spec)
- ✅ AC-03.2.2 / Julia (hr_transcript/F-hr_transcript-30d25c), year illustrative (spec)
- ✅ AC-03.2.2 / Start on the 2nd of a month (spec)
- ✅ AC-03.2.2 / Start on the last day of a month (spec)
- ✅ AC-03.2.2 / Mid-December start crosses the year end (spec)
- ✅ AC-03.3.1 / Julia moved her start to 15.03 (hr_transcript/F-hr_transcript-e18e66), year illustrative (spec)
- ✅ AC-03.3.1 / Start moved one week earlier onto the 1st of a month (spec)
- ✅ AC-03.3.1 / Start moved within the same month (spec)
- ✅ AC-04.1.1 / Single employee (spec)
- ✅ AC-04.1.1 / Married employee (spec)
- ✅ AC-04.2.1 / Married employee (spec)
- ✅ AC-04.2.2 / Single employee (spec)
- ✅ AC-04.2.2 / Divorced employee (spec)
- ✅ AC-04.2.2 / Widowed employee (spec)
- ✅ AC-04.3.1 / Married employee (spec)
- ✅ AC-04.3.2 / Single employee (spec)
- ✅ AC-04.3.2 / Divorced employee (spec)
- ✅ AC-04.3.2 / Widowed employee (spec)
- ✅ AC-05.1.1 / Employee living in Switzerland (spec)
- ✅ AC-05.1.1 / Swiss national living in Germany, like Stefan (F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.1.1 / Employee living in Liechtenstein (spec)
- ✅ AC-05.1.2 / Maria, Portuguese (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.1.2 / Swiss national living in Switzerland (spec)
- ✅ AC-05.1.2 / Employee living in Germany (spec)
- ✅ AC-05.2.1 / Tomás, Brazilian, B permit, married (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.1 / Single employee with a B permit (spec)
- ✅ AC-05.2.1 / Married employee with a C permit (spec)
- ✅ AC-05.2.1 / Married Swiss employee living in Switzerland (spec)
- ✅ AC-05.2.1 / Married employee living in Germany (spec)
- ✅ AC-05.2.2 / Tomás, wife is Swiss (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.2 / Spouse is Italian (spec)
- ✅ AC-05.2.3 / Tomás, wife is Swiss (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.2.3 / Spouse is Italian with a C permit (spec)
- ✅ AC-05.2.3 / Spouse is Italian with a B permit (spec)
- ✅ AC-05.3.1 / Swiss national living in Germany, like Stefan (F-hr_transcript-3f2c2a) (spec)
- ✅ AC-05.3.1 / Employee living in Liechtenstein (spec)
- ✅ AC-05.3.2 / Swiss national living in Switzerland (spec)
- ✅ AC-05.3.2 / Maria, Portuguese, C permit (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-05.3.3 / Single employee with a B permit (spec)
- ✅ AC-05.3.3 / Divorced employee with a B permit (spec)
- ✅ AC-05.3.4 / Tomás, Brazilian, B permit, Swiss wife, living in Winterthur (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-05.3.4 / Spouse is Italian with a C permit and lives in Switzerland (spec)
- ✅ AC-05.3.4 / Spouse is Italian with a B permit (spec)
- ✅ AC-05.3.4 / Spouse is Swiss but lives in Germany (spec)
- ✅ AC-06.1.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9): married to a Swiss wife living in Switzerland, not subject (spec)
- ✅ AC-06.1.1 / Maria (hr_transcript/F-hr_transcript-845204): Portuguese with a C permit, not subject (spec)
- ✅ AC-06.1.1 / Non-Swiss single employee with a B permit living in Switzerland (spec)
- ✅ AC-06.1.1 / Swiss employee living abroad (like Stefan, hr_transcript/F-hr_transcript-3f2c2a) (spec)
- ✅ AC-06.1.1 / Swiss employee living in Switzerland (spec)
- ✅ AC-06.1.3 / Married employee with replacement income (spec)
- ✅ AC-06.2.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9): not subject, denomination never collected (spec)
- ✅ AC-06.2.1 / Maria (hr_transcript/F-hr_transcript-845204): C permit, denomination never collected (spec)
- ✅ AC-06.2.1 / Subject employee with earned income (spec)
- ✅ AC-06.2.1 / Subject employee with replacement income (spec)
- ✅ AC-06.2.3 / Earned income, member of a recognised church (spec)
- ✅ AC-06.2.3 / Earned income, no or another denomination (spec)
- ❌ AC-06.2.3 / Replacement income (spec): church_tax_suffix = None, expected 'null'
- ✅ AC-06.3.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9): married but not subject (spec)
- ✅ AC-06.3.1 / Married, subject, earned income (spec)
- ✅ AC-06.3.1 / Single, subject, earned income (spec)
- ✅ AC-06.3.1 / Married, subject, replacement income (spec)
- ✅ AC-06.4.1 / Replacement income (spec)
- ✅ AC-06.4.2 / Spouse works (spec)
- ✅ AC-06.4.2 / Spouse does not work (spec)
- ✅ AC-06.4.3 / Single without children (spec)
- ✅ AC-06.4.3 / Divorced with a minor child in the household under sole custody (spec)
- ✅ AC-06.4.3 / Widowed with an adult child in first education who lives elsewhere (spec)
- ✅ AC-07.1.1 / Single employee living abroad (spec)
- ✅ AC-07.1.1 / Married B-permit holder with a non-Swiss spouse (spec)
- ✅ AC-07.1.1 / Tomás (hr_transcript/F-hr_transcript-b90bd9) (spec)
- ✅ AC-07.1.1 / Maria (hr_transcript/F-hr_transcript-845204) (spec)
- ✅ AC-07.1.1 / Swiss national living in Switzerland (spec)
- ✅ AC-07.1.2 / Replacement income (spec)
- ✅ AC-07.1.4 / No children (spec)
- ✅ AC-07.1.4 / Has children (spec)
- ✅ AC-07.2.2 / Employee with children (spec)
- ✅ AC-07.2.3 / Married, child neither (zh_source_tax_calculator/F-zh_source_tax_calculator-abe889) (spec)
- ✅ AC-07.2.4 / Minor child (spec)
- ✅ AC-07.2.4 / Adult child in first education (spec)
- ✅ AC-07.3.1 / Single, sole custody (zh_source_tax_calculator/F-zh_source_tax_calculator-d75286) (spec)
- ✅ AC-07.3.2 / Married, shared custody, common household (zh_source_tax_calculator/F-zh_source_tax_calculator-5d8fb0) (spec)
- ✅ AC-07.3.2 / Single, shared custody, common household (zh_source_tax_calculator/F-zh_source_tax_calculator-5686d7) (spec)
- ✅ AC-07.3.3 / Single, no common household, no alternating custody (zh_source_tax_calculator/F-zh_source_tax_calculator-dc0ae9) (spec)
- ✅ AC-07.3.3 / Married, no common household, no alternating custody (zh_source_tax_calculator/F-zh_source_tax_calculator-a4d358) (spec)
- ✅ AC-07.3.4 / Married, alternating custody (zh_source_tax_calculator/F-zh_source_tax_calculator-a4d358) (spec)
- ✅ AC-07.4.1 / Married, child elsewhere, no shared custody (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.2 / Single, child elsewhere, no parental care (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.2 / Divorced, child elsewhere (spec)
- ✅ AC-07.4.3 / Married, shared custody, alternating, employee pays more (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.3 / Single, parental care, alternating, employee pays more (zh_source_tax_calculator/F-zh_source_tax_calculator-dc6ace) (spec)
- ✅ AC-07.4.3 / Single, parental care, no alternating custody (spec)
- ✅ AC-07.5.1 / Married, adult child at home, common household (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.1 / Single, adult child at home, common household (spec)
- ✅ AC-07.5.2 / Single, adult child at home, no common household (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-07.5.2 / Married, adult child elsewhere (zh_source_tax_calculator/F-zh_source_tax_calculator-3eb561) (spec)
- ✅ AC-08.1.2 / Tomás, lives in Winterthur (F-hr_transcript-b90bd9) (spec)
- ✅ AC-08.1.2 / Employee living in Konstanz (F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.1.2 / Employee living in Liechtenstein (F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.1.2 / Employee living in France (spec)
- ✅ AC-08.1.3 / Employee living in France, earned income (spec)
- ✅ AC-08.1.3 / Non-Swiss single employee with B permit living in Switzerland (spec)
- ✅ AC-08.2.1 / Employee living in Konstanz (F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.2.1 / Employee living in Liechtenstein (F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.2.1 / Swiss employee living in Switzerland (spec)
- ✅ AC-08.2.2 / Germany resident with replacement income (spec)
- ✅ AC-08.2.3 / Germany resident returning daily (spec)
- ✅ AC-08.2.3 / Germany resident not returning daily (spec)
- ✅ AC-08.2.3 / Germany resident with replacement income returning daily (spec)
- ✅ AC-08.3.1 / Germany resident not returning daily, earned income (spec)
- ✅ AC-08.3.1 / Germany resident not returning daily, replacement income (spec)
- ✅ AC-08.3.1 / Germany resident returning daily (spec)
- ✅ AC-08.3.2 / Germany resident, daily return reasonable (spec)
- ✅ AC-08.3.2 / Germany resident, daily return not reasonable (spec)
- ✅ AC-08.4.1 / Employee living in Liechtenstein (F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.4.1 / Liechtenstein resident with replacement income (spec)
- ✅ AC-08.4.1 / Employee living in Konstanz (F-hr_transcript-3f2c2a) (spec)
- ✅ AC-08.4.2 / Liechtenstein resident not returning daily (spec)
- ✅ AC-08.4.2 / Liechtenstein resident returning daily (spec)
- ✅ AC-08.4.2 / Liechtenstein resident with replacement income not returning daily (spec)

## Open questions (need your decision)

- **OQ-registered-partnership** (blocking): How should an employee in a registered partnership answer civil status, and do the pension fund and the source tax spouse exemption treat them like married employees (partner's date of birth, partner's nationality/permit/residence)? → recommended: Ask Pensionskasse Muster via HR. Until then, treat registered partners as Married for both parties, because the calculator explicitly groups them together.
- **OQ-separated**: Which civil status should a separated (still married) employee choose? The calculator groups 'separated' with single, but the pension fund has no such option. → recommended: Confirm with HR. Do not add a question until then.
- **OQ-divorced-widowed**: Does the pension fund ask for any spouse data when civil status is Divorced or Widowed? → recommended: Assume no extra fields. Verify with a screenshot of these two cases.
- **OQ-canton** (blocking): Does the pension fund's 'Canton' mean canton of residence or of work, and what is entered for employees who live abroad (Germany, Liechtenstein)? → recommended: Ask Pensionskasse Muster. Meanwhile ask the canton only of Swiss residents.
- **OQ-permit-list**: Which permit types should the employee and spouse be able to choose from, and how does a spouse without any permit answer? → recommended: Ask HR for the list it uses. The rule only needs to tell C permit apart from other permits.
- **OQ-source-tax-rule**: Is the consolidated source tax rule complete and does 'here' mean Switzerland? HR hedged ('I think so') before adding further conditions. → recommended: Have HR confirm the decision table of subject_to_source_tax.
- **OQ-dual-nationality**: How should employees with several nationalities, one of them Swiss, answer the nationality question? → recommended: Confirm with HR that any Swiss citizenship counts as Swiss.
- **OQ-income-type**: Is a new employee's income always earned income (Erwerbseinkommen), so the income-type question can be fixed instead of asked? → recommended: Fix to earned income by product decision. Until then it is modelled as asked.
- **OQ-liechtenstein**: HR says everyone living abroad is subject to source tax, but the calculator can return 'in principle no source tax liability' for Liechtenstein residents. Which result counts? → recommended: Keep asking these employees all source tax questions and let the calculator result decide. Confirm with HR.
- **OQ-proof-documents**: Can a new employee answer 'certificate of residence provided' and 'proof of more than 60 non-return days provided' before starting? To whom are these documents provided? → recommended: Ask HR how this works today for Stefan.
- **OQ-calculator-coverage**: Do the child and cross-border paths behave as modelled for every combination? The calculator was only spot-checked for A/B/H cross-border tariffs, more than 3 children, deleting children and special tariffs (e.g. D). → recommended: Accept for the questionnaire (the question conditions are explicit). Explore further only if the tariff is computed by Lonio.
- **OQ-permit-reminder**: Should the questionnaire remind employees to bring their permit on the first day, and with which wording? → recommended: Product owner to decide. It adds no data collection.
- **OQ-spouse-residence-form**: Should the spouse's residence be asked as a country or only as 'lives in Switzerland: yes/no'? → recommended: Ask yes/no 'Does your spouse live in Switzerland?' if the product owner agrees.

## Inferred items to confirm

- item.address_country
- item.residence_canton
- item.nationality
- item.permit_type
- item.spouse_nationality
- item.spouse_permit_type
- item.spouse_residence_country
- item.income_type
- rule.subject_to_source_tax
- rule.calculator_civil_status
- rule.calculator_residence
- rule.church_tax_suffix
- rule.base_tariff_letter
- rule.questionnaire_flow
- story.US-01.1
- story.US-01.2
- story.US-01.3
- story.US-02.1
- story.US-02.3
- story.US-02.4
- story.US-03.3
- story.US-04.2
- story.US-04.3
- story.US-05.1
- story.US-05.2
- story.US-05.3
- story.US-06.1
- story.US-06.2
- story.US-06.3
- story.US-06.4
- story.US-07.1
- story.US-08.1
- fact F-hr_transcript-b84498: Source tax questions should only be asked of employees who are subject to source tax, not of everybody.
- fact F-hr_transcript-3edf89: HR needs the employee's name. Leo asked about 'Name, address' and Anna answered 'Yes', but she only elaborated on the address.
- fact F-hr_transcript-1d5c07: Consolidated rule: the insurance start date is derived from the first working day. If the first working day is the 1st of a month, insurance starts that day. Otherwise it starts on the 1st of the following month.
- fact F-hr_transcript-e18e66: When the first working day changes, the insurance start date given to the pension fund must be re-derived and updated. A missed update (Julia) caused a wrong date at the fund, an unfriendly letter and weeks of fixing.
- fact F-hr_transcript-35fae3: The employee's nationality is needed to decide whether they are subject to source tax.
- fact F-hr_transcript-c9d9b9: The permit type of non-Swiss employees is needed to decide source tax liability (a C permit exempts them). The permit type is only relevant for non-Swiss employees.
- fact F-hr_transcript-54d011: The spouse's nationality, permit and residence only matter for source tax when the employee is married. They are presumably only needed when the employee would otherwise be subject to source tax (non-Swiss, no C permit, living in Switzerland).
- fact F-hr_transcript-ab3cba: The employee's country of residence (the country of the home address) is needed to decide source tax liability for cross-border employees.
- fact F-hr_transcript-5af8d0: Consolidated final rule. An employee who lives abroad (outside Switzerland) is subject to source tax regardless of nationality. An employee who lives in Switzerland is subject only if they are non-Swiss without a C permit and are not married to a Swiss national or C-permit holder who lives in Switzerland. Note: Anna said 'here', which is read as Switzerland. Her 'I think' hedges remain.
- fact F-pension_portal-6d3630: No screenshot shows the form with Civil status 'Divorced' or 'Widowed'; it is unknown whether Spouse's date of birth (or any other field) appears for those values.
- fact F-pension_portal-b359c3: The portal does not say whether 'Canton' means canton of residence or of work, and the list offers no option for employees living outside Switzerland; how to register such employees is unknown.
- fact F-pension_portal-3a97ab: The portal requires an insurance start date on the 1st of a month but does not show how it relates to the employee's first working day (e.g. which 1st of a month to choose when work starts mid-month); the derivation rule is unknown.
- fact F-pension_portal-e45e5b: No screenshot shows the validation error for an insurance start date that is not the 1st of a month or for a malformed date; its behaviour and wording are unknown.
- fact F-zh_source_tax_calculator-2eab9a: Confession sets the church-tax suffix of the tariff: Y for röm.-kath./christ.-kath./evang.-ref., N for none or other (e.g. A0Y vs A0N).
- fact F-zh_source_tax_calculator-97139a: For married/registered partners, a spouse who is employed or receives replacement income leads to tariff C; otherwise tariff B.
- fact F-zh_source_tax_calculator-037b1c: A single/divorced/separated/widowed person without counted children with earned income and residence in Switzerland gets tariff A (A0Y/A0N).
- fact F-zh_source_tax_calculator-4c53e3: The tariff digit equals the number of children whose per-child result digit is 1 (e.g. three counted children -> C3Y).
- fact F-zh_source_tax_calculator-300c72: For a single/divorced/separated/widowed person, any child counted with H gives an H tariff; a child counts with H when it lives in the household and the person has sole custody or is the main financial contributor.
- fact F-zh_source_tax_calculator-d75286: A minor child in the same household with sole custody counts as a child (married: C1/B1; single: H1).
- fact F-zh_source_tax_calculator-5d8fb0: Married, minor child in household, shared custody and common household with the other parent: the child counts (C1Y).
- fact F-zh_source_tax_calculator-a4d358: Married, minor child in household, shared custody, no common household: alternating custody with the other parent as main contributor, or no alternating custody, gives C0Y (child not counted).
- fact F-zh_source_tax_calculator-dc0ae9: Single, minor child in household, shared custody, no common household and no alternating custody gives H1N (child counted with H).
- fact F-zh_source_tax_calculator-5686d7: Single, minor child in household, shared custody, common household with the other parent and other parent as main contributor gives A0N.
- fact F-zh_source_tax_calculator-dc6ace: Minor child not in the household: with shared custody/parental care, alternating custody and the person as main contributor, the child counts (married B1N, single H1N); without shared custody/parental care it does not count (B0N, A0N).
- fact F-zh_source_tax_calculator-3eb561: Adult child in first education: in household with common household (married) counts (B1N); not in household counts only if more than 50% of maintenance is provided (single A1N; married with Nein -> B0N); single, in household without common household and >50% maintenance gives H1N.
- fact F-zh_source_tax_calculator-993db3: Germany resident with daily return and a residence certificate gets the cross-border (Grenzgänger) tariff: A->L, B->M, C->N, H->P, G->Q; without a certificate the normal tariff applies.
- fact F-zh_source_tax_calculator-c8aa5e: Germany resident without daily return: if return is not reasonable -> normal tariff; if reasonable and >60 non-return days proven -> normal tariff; if reasonable and no proof -> cross-border tariff (L/M/N/P, Q).
- fact F-zh_source_tax_calculator-fb87f1: Liechtenstein residents with daily return, or without daily return and not more than 45 non-return days, get 'Grundsätzlich keine Quellensteuerpflicht' (in principle no source tax liability), subject to the double taxation agreement.
- fact F-zh_source_tax_calculator-cc19c7: Liechtenstein residents without daily return and more than 45 non-return days get the normal tariff plus 'Unter Vorbehalt des Doppelbesteuerungsabkommens'.
- fact F-zh_source_tax_calculator-f86c6b: Residence in Switzerland or in 'Anderes Land' gives the base tariff without further residence questions.
- fact F-zh_source_tax_calculator-2d4dda: Replacement income (Ersatzeinkünfte) yields tariff G (cross-border variant Q), without child digit or confession suffix.
- fact F-zh_source_tax_calculator-2754e8: Replacement income, Germany: daily return with certificate -> Q; daily return without certificate -> G; no daily return, reasonable, no >60-day proof -> Q; with proof -> G; not reasonable -> G.

## Dev refinement questions (15)

- [major] `stories/US-06.4-derive-the-base-source-tax-tariff-letter.md` AC-06.4.3 and the base-tariff rule say an unmarried employee gets H only if a child lives in the household AND the employee has sole custody or is the main financial contributor. The spec's own evidence disagrees. F-zh-dc0ae9 gives H1N for a child in the household with shared custody, no common household and no alternating custody. F-zh-dc6ace gives H1N for a minor child who does NOT live in the household. F-zh-3eb561 gives H1N for an adult child where the deciding answer is 'pays more than 50%', not 'main contributor'. Which rule should we build for H vs A? We cannot write the derivation or its tests until this is settled.
- [major] `stories/US-06.4-derive-the-base-source-tax-tariff-letter.md` What exactly does the questionnaire produce as a tariff result, and who sees it? US-06.4 only derives the letter (A/B/C/G/H). But the spec also defines the church-tax suffix (US-06.2), the rule that the digit is the number of counted children, and the Germany cross-border swap (A→L etc.), and AC-06.4.4 says all of these come from the calculator. Should we compute the full tariff code (e.g. H1N, N1Y), only the letter, or nothing? Is the result shown to HR, to the employee, or to neither?
- [major] `stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md` AC-05.3.5 says 'HR can see for each employee whether they are subject'. No story describes what HR sees, where, or when (live while the employee is filling in, or after submission), and the feature puts 'how data is sent to each party' out of scope. Is an HR view of the results (subject yes/no, insurance start date, expected tariff) part of this feature? Should the employee see these derived results?
- [major] `stories/US-03.3-re-derive-the-insurance-start-date-when-the-first-working.md` AC-03.3.1 assumes the first working day 'later changes' after it was recorded. Who changes it, and through what? Can the employee reopen and edit a submitted questionnaire, can HR edit it, or does a new questionnaire go out? Is there a deadline after which changes are no longer accepted? This decides whether we need editing after submission, an HR edit function and an audit of changes.
- [major] `stories/US-03.1-employee-confirms-the-first-working-day.md` The flow table says the first working day is 'confirmed if HR already knows it', and AC-03.1.2 says to confirm the date 'as currently agreed'. No story covers HR entering a known date in advance. Does HR pre-fill the first working day (and perhaps the name) before inviting the employee, so the employee only confirms or corrects it? Or does the employee always type it in?
- [major] `feature.md` The insurance start rule uses the 'first working day'. If the contract starts on the 1st but the first actual working day is later (weekend or holiday, e.g. contract from Sat 01.06, first day Mon 03.06), the rule gives 01.07 instead of 01.06. Should the rule use the contractual start date or the actual first working day?
- [major] `stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md` New hires often move to Switzerland when they start, or move away from it. Is the home address the current one or the one that applies from the first working day? The country decides source-tax liability, the canton and all the cross-border questions, so the answer changes which questions are asked.
- [major] `stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md` Suppose an employee goes back and changes an earlier answer: the country from Germany to Switzerland, civil status from Married to Single, or the permit to a C permit. Answers they already gave may no longer apply (nationality, spouse data, denomination, children). Under data minimisation, must those answers be thrown away, or may they be kept? Do any rules re-run (e.g. the subject-to-source-tax decision) after submission?
- [minor] `stories/US-01.1-show-the-source-tax-step-only-to-employees-who-are-subject.md` What does finishing the questionnaire mean for the business? Is there a review/summary step and an explicit submit with a confirmation to the employee? Is HR notified? Can the employee save partway and come back later? None of this is specified, but it decides when HR can rely on the data.
- [minor] `stories/US-03.1-employee-confirms-the-first-working-day.md` Are there business limits on the first working day, e.g. it must not be in the past or more than N months ahead? Is there a plausibility check on the employee's and spouse's dates of birth (minimum working age)? The pension fund only requires the DD.MM.YYYY format.
- [minor] `stories/US-05.1-ask-nationality-and-permit-only-of-employees-living-in.md` Nationality is 'a country by English name'. Which list of nationalities should be offered, and how do stateless employees or employees with unclear status answer? Only 'Switzerland vs not' matters for the rule. (Dual nationality is already listed as an open question.)
- [minor] `stories/US-03.1-employee-confirms-the-first-working-day.md` AC-03.1.2 ('the question makes clear the date must be the currently agreed one') cannot be tested as written. Is there agreed wording for the question, or a business requirement such as showing the date HR has on file?
- [minor] `stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md` In the AC-06.2.3 examples, the replacement-income row gives the result 'null', is marked as failing (❌), and has the denomination column twice. Is the expected result for replacement income 'no suffix'? Please fix the example so it can serve as a test case.
- [minor] `stories/US-02.4-ask-swiss-residents-for-their-canton.md` The example tables mix 'required' and 'asked' as expected results for questions that the text says are 'asked and required'. Examples: Canton Zurich 'required' vs St. Gallen 'asked'; the spouse's residence row 'required' vs 'asked'; children 'required' vs 'asked'. Is there a real difference between 'asked' and 'required' (i.e. may some of these be left empty), or are they the same?
- [minor] `stories/US-06.4-derive-the-base-source-tax-tariff-letter.md` The AC-06.4.3 example 'Widowed with an adult child in first education who lives elsewhere → A' leaves out the required 'pays more than 50% of maintenance' answer. Per US-07.5 that answer decides whether the child counts. Which answer is meant, and is the expected digit 0 or 1?

## Technical vocabulary found in the spec (5)

- `stories/US-08.1-derive-the-calculator-s-residence-answers-from-the-home.md` "the employee has entered the country of their home address (address_country) in the home address step" - An internal field identifier appears in the acceptance-criterion prose. Field naming is an engineering choice.
- `feature.md` "If it changes, insurance_start_date must be derived again." - A snake_case field/rule identifier is used in the business notes of the First working day item instead of the business term 'insurance start date'.
- `feature.md` "It also answers the source tax calculator's civil status question (see rule calculator_civil_status)." - Internal rule ids (calculator_civil_status, and likewise subject_to_source_tax / insurance_start_date in many ACs) are written into the business prose. These are code-style identifiers, not business language.
- `stories/US-07.2-one-block-per-child-age-status-and-household.md` "the employee can describe each child in its own block (Child 1, Child 2, ...) and can add or remove a child" - This prescribes UI interaction (repeating blocks with add/remove controls) copied from the calculator's screen. The business need is only that each child is described separately.
- `stories/US-06.2-ask-the-religious-denomination-only-where-source-tax-needs.md` "| Replacement income (illustrative) | Switzerland | Germany | B permit | Single | Replacement income | – | → | null | not asked | ❌ |" - A programming value ('null') appears as the expected business result where the business term 'no suffix' was meant.

## Coverage

166/342 source units cited; 164/177 facts used.

Uncited units (confirm they are irrelevant):

- hr_transcript/T-000: HR meeting transcript Everyone and everything here is fictional. Anna is the HR manager at Muster AG. Leo works in product at Lonio.
- hr_transcript/T-001: Can you hear me okay? You're a bit quiet.
- hr_transcript/T-002: Is this better? I'm in the small meeting room, the big one is taken. Sorry, let me just close the door.
- hr_transcript/T-003: Much better. So, thanks for making the time. The idea today is simple. We want your new employees to give us everything once, so that you stop chasing them for 
- hr_transcript/T-004: Yes, please. Right now it's a mess. I have a Word document, then an Excel file, and then I type everything into the portals by hand. Last month I spent a full a
- hr_transcript/T-005: Okay. And how many people do you hire in a year?
- hr_transcript/T-006: Around twenty. More in summer. We're about a hundred and fifty people now, mostly here in Zurich.
- hr_transcript/T-007: Good. Let's start with the biggest pain. What takes you the most time?
- hr_transcript/T-011: Okay, that's clear. And the questionnaire itself is what?
- hr_transcript/T-015: Anything else on the address?
- hr_transcript/T-017: Great. Do you also want a photo? Some customers ask for one.
- hr_transcript/T-019: It could. Do you want that from day one?
- hr_transcript/T-022: We're with Pensionskasse Muster. They have a portal, it's quite old. I'll send you some screenshots of it after this call, that's easier than me explaining it.
- hr_transcript/T-023: Perfect. What do you need for the fund that you don't have?
- hr_transcript/T-025: It moves?
- hr_transcript/T-027: Ouch.
- hr_transcript/T-029: Sorry, one second, someone's at my door. [pause] Okay, I'm back, sorry. Where were we?
- hr_transcript/T-030: The Julia story. It doesn't matter.
- hr_transcript/T-031: Right. What else about the employee affects the fund? Are they married, things like that?
- hr_transcript/T-033: And what are the options in that list?
- hr_transcript/T-035: How did you enter him?
- hr_transcript/T-037: Okay. Noted. Can I go back to source tax? You said all non-Swiss employees.
- hr_transcript/T-041: Sure, send it if it's easy. Do people need anything from you on the first day? Laptops, things like that? I just want to see if that belongs in the same form.
- hr_transcript/T-047: Okay. Anything else on who needs to do it? I'd rather hear all of it now.
- hr_transcript/T-052: Only the timing. When can we have this?
- hr_transcript/T-053: I'll come back to you on that this week, once we've gone through your screenshots.
- hr_transcript/T-054: Good. I'll send them after lunch. Thanks, Leo.
- hr_transcript/T-055: Thanks, Anna. Talk soon.
- pension_portal/S01-E01: Pensionskasse Muster
- pension_portal/S01-E02: Employer portal · Muster AG · Log out
- pension_portal/S01-E03: Home > Insured persons > Register new employee
- pension_portal/S01-E04: Register new employee
- pension_portal/S01-E05: Employee
- pension_portal/S01-E17: Cancel
- pension_portal/S01-E18: Register
- pension_portal/S02-E01: Pensionskasse Muster
- pension_portal/S02-E02: Employer portal · Muster AG · Log out
- pension_portal/S02-E03: Home > Insured persons > Register new employee
- pension_portal/S02-E04: Register new employee
- pension_portal/S02-E05: Employee
- pension_portal/S02-E06: First name
- pension_portal/S02-E07: Last name
- pension_portal/S02-E08: Date of birth
- pension_portal/S02-E09: DD.MM.YYYY
- pension_portal/S02-E11: Please select
- pension_portal/S02-E38: Insurance
- pension_portal/S02-E39: Insurance start date
- pension_portal/S02-E40: Civil status
- pension_portal/S02-E41: Cancel
- pension_portal/S02-E42: Register
- pension_portal/S02-E43: Fields marked * are required.
- pension_portal/S03-E01: Pensionskasse Muster
- pension_portal/S03-E02: Employer portal · Muster AG · Log out
- pension_portal/S03-E03: Home > Insured persons > Register new employee
- pension_portal/S03-E04: Register new employee
- pension_portal/S03-E05: Employee
- pension_portal/S03-E06: First name
- pension_portal/S03-E07: Lena
- pension_portal/S03-E08: Last name
- pension_portal/S03-E09: Keller
- pension_portal/S03-E10: Date of birth
- pension_portal/S03-E11: 14.02.1991
- pension_portal/S03-E12: DD.MM.YYYY
- pension_portal/S03-E13: Canton
- pension_portal/S03-E14: Zurich
- pension_portal/S03-E15: Insurance
- pension_portal/S03-E16: Insurance start date
- pension_portal/S03-E17: 01.05.2026
- pension_portal/S03-E18: DD.MM.YYYY. Must be the 1st of a month.
- pension_portal/S03-E20: Please select
- pension_portal/S03-E25: Cancel
- pension_portal/S03-E26: Register
- pension_portal/S03-E27: Fields marked * are required.
- pension_portal/S04-E01: Pensionskasse Muster
- pension_portal/S04-E02: Employer portal · Muster AG · Log out
- pension_portal/S04-E03: Home > Insured persons > Register new employee
- pension_portal/S04-E04: Register new employee
- pension_portal/S04-E05: Employee
- pension_portal/S04-E06: First name
- pension_portal/S04-E07: Lena
- pension_portal/S04-E08: Last name
- pension_portal/S04-E09: Keller
- pension_portal/S04-E10: Date of birth
- pension_portal/S04-E11: 14.02.1991
- pension_portal/S04-E12: DD.MM.YYYY
- pension_portal/S04-E13: Canton
- pension_portal/S04-E14: Zurich
- pension_portal/S04-E15: Insurance
- pension_portal/S04-E16: Insurance start date
- pension_portal/S04-E17: 01.05.2026
- pension_portal/S04-E18: DD.MM.YYYY. Must be the 1st of a month.
- pension_portal/S04-E19: Civil status
- pension_portal/S04-E21: Cancel
- pension_portal/S04-E22: Register
- pension_portal/S04-E23: Fields marked * are required.
- pension_portal/S05-E01: Pensionskasse Muster
- pension_portal/S05-E02: Employer portal · Muster AG · Log out
- pension_portal/S05-E03: Home > Insured persons > Register new employee
- pension_portal/S05-E04: Register new employee
- pension_portal/S05-E05: Employee
- pension_portal/S05-E06: First name
- pension_portal/S05-E07: Marco
- pension_portal/S05-E08: Last name
- pension_portal/S05-E09: Rossi
- pension_portal/S05-E10: Date of birth
- pension_portal/S05-E11: 03.09.1985
- pension_portal/S05-E12: DD.MM.YYYY
- pension_portal/S05-E13: Canton
- pension_portal/S05-E14: Bern
- pension_portal/S05-E15: Insurance
- pension_portal/S05-E16: Insurance start date
- pension_portal/S05-E17: 01.06.2026
- pension_portal/S05-E18: DD.MM.YYYY. Must be the 1st of a month.
- pension_portal/S05-E19: Civil status
- pension_portal/S05-E22: 22.11.1987
- pension_portal/S05-E24: Cancel
- pension_portal/S05-E25: Register
- pension_portal/S05-E26: Fields marked * are required.
- pension_portal/S06-E01: Pensionskasse Muster
- pension_portal/S06-E02: Employer portal · Muster AG · Log out
- pension_portal/S06-E03: Home > Insured persons > Register new employee
- pension_portal/S06-E04: Register new employee
- pension_portal/S06-E06: Employee
- pension_portal/S06-E07: First name
- pension_portal/S06-E09: Last name
- pension_portal/S06-E11: Date of birth
- pension_portal/S06-E12: DD.MM.YYYY
- pension_portal/S06-E14: Canton
- pension_portal/S06-E15: Please select
- pension_portal/S06-E17: Insurance
- pension_portal/S06-E18: Insurance start date
- pension_portal/S06-E19: DD.MM.YYYY. Must be the 1st of a month.
- pension_portal/S06-E21: Civil status
- pension_portal/S06-E22: Please select
- pension_portal/S06-E24: Cancel
- pension_portal/S06-E25: Register
- pension_portal/S06-E26: Fields marked * are required.
- pension_portal/S07-E01: Pensionskasse Muster
- pension_portal/S07-E02: Employer portal · Muster AG · Log out
- pension_portal/S07-E03: Home > Insured persons > Register new employee
- pension_portal/S07-E04: Register new employee
- pension_portal/S07-E05: Employee
- pension_portal/S07-E06: First name
- pension_portal/S07-E07: Marco
- pension_portal/S07-E08: Last name
- pension_portal/S07-E09: Rossi
- pension_portal/S07-E10: Date of birth
- pension_portal/S07-E11: 03.09.1985
- pension_portal/S07-E12: DD.MM.YYYY
- pension_portal/S07-E13: Canton
- pension_portal/S07-E14: Bern
- pension_portal/S07-E15: Insurance
- pension_portal/S07-E16: Insurance start date
- pension_portal/S07-E17: 01.06.2026
- pension_portal/S07-E18: DD.MM.YYYY. Must be the 1st of a month.
- pension_portal/S07-E19: Civil status
- pension_portal/S07-E22: 
- pension_portal/S07-E23: DD.MM.YYYY
- pension_portal/S07-E25: Cancel
- pension_portal/S07-E26: Register
- pension_portal/S07-E27: Fields marked * are required.
- zh_source_tax_calculator/C-V04: Answers {"Q01": "Erwerbseinkommen", "Q02": "Verheiratet oder eingetragene Partnerschaft", "Q03": "Keine oder andere", "Q04": "Nein", "Q05": "Nein", "Q16": "Ja"}
- zh_source_tax_calculator/C-V06: Answers {"Q01": "Erwerbseinkommen", "Q02": "Verheiratet oder eingetragene Partnerschaft", "Q03": "Keine oder andere", "Q04": "Ja", "Q05": "Nein", "Q16": "Ja"} -
- zh_source_tax_calculator/C-V24: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "weder noch", "Q16": "Ja"} 
- zh_source_tax_calculator/C-V25: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "Minderjährig (Kind 1) + Mi
- zh_source_tax_calculator/C-V26: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "Kind 1: Minderjährig; Kind
- zh_source_tax_calculator/C-V27: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "Kind 1: Volljährig und in 
- zh_source_tax_calculator/C-V29: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "Minderjährig (Kind 1-3)", 
- zh_source_tax_calculator/C-V30: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "röm.-kath., christ.-kath., evang.-ref.", "Q06": "Nein", "Q16": "Nei
- zh_source_tax_calculator/C-V31: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "Keine oder andere", "Q06": "Ja", "Q07": "Volljährig und in Erstausb
- zh_source_tax_calculator/C-V32: Answers {"Q01": "Erwerbseinkommen", "Q02": "Verheiratet oder eingetragene Partnerschaft", "Q03": "Keine oder andere", "Q04": "Nein", "Q05": "Nein", "Q16": "Nein
- zh_source_tax_calculator/C-V33: Answers {"Q01": "Erwerbseinkommen", "Q02": "Ledig, Geschieden, Getrennt, Verwitwet", "Q03": "röm.-kath., christ.-kath., evang.-ref.", "Q06": "Ja", "Q07": "Minde
- zh_source_tax_calculator/C-V51: Answers {"Q01": "Ersatzeinkünfte", "Q16": "Nein", "Q17": "Liechtenstein", "Q27": "Nein", "Q28": "Nein"} -> result Grundsätzlich keine Quellensteuerpflicht / Unt
- zh_source_tax_calculator/C-N01: The calculator is an Angular app (app-root, ng 11, assets from www.services.zh.ch/app/quest/tarifbestimmung/prod/) rendered inline in the section 'Tarifrechner 
- zh_source_tax_calculator/C-N03: A visually hidden 'Beispiele' area shows the tags H3N and P3N. These were not clicked as inputs.
- zh_source_tax_calculator/C-N08: The answer value in V25–V29 summarises repeated per-child answers (Kind 1/2/3) because the schema allows one value per question id.

## Other warnings (38)

- [fact_judge] `F-hr_transcript-34494f` partial: Leo's 'We'll keep that for now' supports agreement, but 'online tariff calculator' and 'canton of Zurich' are okay; 'acknowledges not exactly how it works' is fine—minor: Leo agreed is supported, so only the 'questionnaire is the calculator' equation is slightly inferred. | The source tax questionnaire is the canton of Zurich's online tariff calculator, which outputs the tariff code. HR uses the Zurich calculator for everybody and acknowledges that this is not exactly how it works. Leo agreed to keep it that way for now.
- [fact_judge] `F-hr_transcript-550840` partial: Leo's summary and Anna's 'I think so' are supported, but 'later added more conditions' is not shown in these units. | Leo summarised the rule as 'non-Swiss, but not with a C permit'. Anna only answered 'I think so' (hedged), and later added more conditions.
- [fact_judge] `F-hr_transcript-a45422` partial: Manual check and email asking are supported, but the email being for the spouse details 'takes forever' is fine; 'I ask them by email' fits, though the exemption check by hand is stated only for the Tomás case. | Today HR checks the spouse exemption by hand and asks for the spouse details by email, which takes forever.
- [fact_judge] `F-hr_transcript-5af8d0` partial: Gist is a reasonable synthesis, but 'here' = Switzerland is an assumption, and the claim that the spouse exemption applies only to Swiss-resident employees is not stated; also 'I think' hedge is Anna's at T-048. | Consolidated final rule. An employee who lives abroad (outside Switzerland) is subject to source tax regardless of nationality. An employee who lives in Switzerland is subject only if they are non-Swiss without a C permit and are not married to a Swiss national or C-permit holder who lives in Switzerland. Note: Anna said 'here', which is read as Switzerland. Her 'I think' hedges remain.
- [fact_judge] `F-pension_portal-39bab1` partial: Units show the field absent for Single and present for Married, but screenshots 01, 02, 03 and 06 are not in these units, and Divorced/Widowed are never shown, so 'only when Married' is overstated. | The 'Spouse's date of birth' field appears only when Civil status is 'Married' (shown in screenshots 05 and 07, both with Married); it is absent in screenshot 04 (Civil status 'Single') and in screenshots 01, 02, 03 and 06 (Civil status not selected).
- [fact_judge] `F-pension_portal-6d3630` partial: Units show only the civil-status dropdown list, so the absence of any Divorced/Widowed form screenshot cannot be confirmed from them. | No screenshot shows the form with Civil status 'Divorced' or 'Widowed'; it is unknown whether Spouse's date of birth (or any other field) appears for those values.
- [fact_judge] `F-pension_portal-b359c3` partial: Units show only part of the canton list (Zug, Zurich) and no help text; the lack of an outside-Switzerland option and the ambiguity are not fully verifiable. | The portal does not say whether 'Canton' means canton of residence or of work, and the list offers no option for employees living outside Switzerland; how to register such employees is unknown.
- [fact_judge] `F-pension_portal-e45e5b` partial: Only the required-field error is visible in these units; absence of other error screenshots cannot be confirmed. | No screenshot shows the validation error for an insurance start date that is not the 1st of a month or for a malformed date; its behaviour and wording are unknown.
- [fact_judge] `F-zh_source_tax_calculator-037b1c` partial: Vectors show A0Y/A0N for single without children with Q16=Ja, but the units never state that Q16 means residence in Switzerland. | A single/divorced/separated/widowed person without counted children with earned income and residence in Switzerland gets tariff A (A0Y/A0N).
- [fact_judge] `F-zh_source_tax_calculator-64ac33` partial: Conditions match, but Q14's meaning ('parental care') is not shown in the units, so that label is an unverified gloss. | Alternating custody is asked only for a minor child when: (in household, shared custody, no common household with other parent) or (married, not in household, shared custody Q13 = Ja) or (non-married, not in household, parental care Q14 = Ja).
- [fact_judge] `F-zh_source_tax_calculator-dc0ae9` partial: V19 gives H1N for these answers, but the units don't give the Q10/Q11 question texts, so mapping them to 'common household' and 'alternating custody' is inferred. | Single, minor child in household, shared custody, no common household and no alternating custody gives H1N (child counted with H).
- [fact_judge] `F-zh_source_tax_calculator-c8aa5e` partial: Q21 help lists only L/M/N/P for the cross-border outcome; adding Q is not stated for this branch. | Germany resident without daily return: if return is not reasonable -> normal tariff; if reasonable and >60 non-return days proven -> normal tariff; if reasonable and no proof -> cross-border tariff (L/M/N/P, Q).
- [fact_judge] `F-zh_source_tax_calculator-2754e8` partial: Outcomes match the vectors, but these units never state that Q19 is the certificate (Ansässigkeitsbescheinigung) question. | Replacement income, Germany: daily return with certificate -> Q; daily return without certificate -> G; no daily return, reasonable, no >60-day proof -> Q; with proof -> G; not reasonable -> G.
- [coverage] `F-pension_portal-e45e5b` fact not used anywhere in the spec: No screenshot shows the validation error for an insurance start date that is not the 1st of a month or for a malformed date; its behaviour and wording are unknown.
- [trace_judge] `item.residence_canton` partial: The facts say it is unknown whether 'Canton' means residence or work canton, so describing and naming it as the canton the employee lives in is an unbacked assumption.
- [trace_judge] `item.nationality` partial: The form 'country by English name' is not backed because G-10 is not cited; the rest is supported.
- [trace_judge] `item.civil_status` partial: The cited facts back the pension-fund use, the values and the calculator's two civil-status groups, but not the claim that civil status decides the spouse exemption.
- [trace_judge] `item.spouse_permit_type` partial: The business text says it is required only if the spouse has a permit, but required_when_expr makes it required whenever asked, so the two do not match.
- [trace_judge] `item.income_type` partial: The claim that replacement income gives tariff G/Q is not in the cited facts, which only say the personal and child questions are skipped.
- [trace_judge] `item.confession` partial: The source-tax-subject condition and the 'sensitive personal data' note are not backed by the cited facts, and the calculator's civil-status-answered precondition is not in the expr.
- [trace_judge] `item.has_children` partial: required_when_expr (is_set(civil_status)) does not match the stated 'always when asked' and the asked_when_expr conditions.
- [trace_judge] `rule.calculator_residence` partial: The Germany and Liechtenstein rows cite F-zh_source_tax_calculator-31d762 and -e22d17, which are not among the provided facts, so the claim that Germany or Liechtenstein questions follow is not backed.
- [trace_judge] `rule.base_tariff_letter` partial: The expression gives H for sole custody alone, but the fact says a child counts with H only if it lives in the household and the person has sole custody or is the main contributor. 'HR keeps the calculator as the authority' is also only loosely backed by the facts.
- [trace_judge] `rule.questionnaire_flow` partial: The cited facts back only the conditional source tax step (steps 1-5 versus 1-6); the order of steps 1-5, the canton, the first working day and the nationality, family and spouse details are not backed by them.
- [trace_judge] `story.US-01.1` partial: The goal and ACs are backed, but the 'religious denomination' example of sensitive data in the so_that is not in the cited facts.
- [trace_judge] `story.US-01.2` partial: AC-01.2.1 states the full step order and the canton for Swiss residents, and the cited facts do not back either.
- [trace_judge] `story.US-02.4` partial: The claim that the canton is asked 'right after the country' is an ordering that none of the cited facts back.
- [trace_judge] `story.US-06.1` partial: The priority reason's claim that the answer is 'presumably always earned income' for a new hire is not in the cited facts, and AC-06.1.3 equates the calculator's 'personal/child questions' with the specific denomination, spouse employment and children items without a fact saying so.
- [trace_judge] `story.US-06.2` partial: The condition 'only if subject to source tax' and the non-illustrative Tomás and Maria examples (not asked) are not backed by any cited fact, because the hr_transcript subject-to-source-tax facts are not cited.
- [trace_judge] `story.US-06.3` partial: The non-illustrative Tomás example (not subject, so not asked) has no cited backing for the not-subject conclusion, and the 'after the denomination question' position is not stated in the cited facts.
- [dev_refinement] `stories/US-06.4-derive-the-base-source-tax-tariff-letter.md` AC-06.4.3 and the base-tariff rule say an unmarried employee gets H only if a child lives in the household AND the employee has sole custody or is the main financial contributor. The spec's own evidence disagrees. F-zh-dc0ae9 gives H1N for a child in the household with shared custody, no common household and no alternating custody. F-zh-dc6ace gives H1N for a minor child who does NOT live in the household. F-zh-3eb561 gives H1N for an adult child where the deciding answer is 'pays more than 50%', not 'main contributor'. Which rule should we build for H vs A? We cannot write the derivation or its tests until this is settled.
- [dev_refinement] `stories/US-06.4-derive-the-base-source-tax-tariff-letter.md` What exactly does the questionnaire produce as a tariff result, and who sees it? US-06.4 only derives the letter (A/B/C/G/H). But the spec also defines the church-tax suffix (US-06.2), the rule that the digit is the number of counted children, and the Germany cross-border swap (A→L etc.), and AC-06.4.4 says all of these come from the calculator. Should we compute the full tariff code (e.g. H1N, N1Y), only the letter, or nothing? Is the result shown to HR, to the employee, or to neither?
- [dev_refinement] `stories/US-05.3-decide-whether-the-employee-is-subject-to-source-tax.md` AC-05.3.5 says 'HR can see for each employee whether they are subject'. No story describes what HR sees, where, or when (live while the employee is filling in, or after submission), and the feature puts 'how data is sent to each party' out of scope. Is an HR view of the results (subject yes/no, insurance start date, expected tariff) part of this feature? Should the employee see these derived results?
- [dev_refinement] `stories/US-03.3-re-derive-the-insurance-start-date-when-the-first-working.md` AC-03.3.1 assumes the first working day 'later changes' after it was recorded. Who changes it, and through what? Can the employee reopen and edit a submitted questionnaire, can HR edit it, or does a new questionnaire go out? Is there a deadline after which changes are no longer accepted? This decides whether we need editing after submission, an HR edit function and an audit of changes.
- [dev_refinement] `stories/US-03.1-employee-confirms-the-first-working-day.md` The flow table says the first working day is 'confirmed if HR already knows it', and AC-03.1.2 says to confirm the date 'as currently agreed'. No story covers HR entering a known date in advance. Does HR pre-fill the first working day (and perhaps the name) before inviting the employee, so the employee only confirms or corrects it? Or does the employee always type it in?
- [dev_refinement] `feature.md` The insurance start rule uses the 'first working day'. If the contract starts on the 1st but the first actual working day is later (weekend or holiday, e.g. contract from Sat 01.06, first day Mon 03.06), the rule gives 01.07 instead of 01.06. Should the rule use the contractual start date or the actual first working day?
- [dev_refinement] `stories/US-02.3-use-the-home-address-country-as-the-country-of-residence.md` New hires often move to Switzerland when they start, or move away from it. Is the home address the current one or the one that applies from the first working day? The country decides source-tax liability, the canton and all the cross-border questions, so the answer changes which questions are asked.
- [dev_refinement] `stories/US-01.2-ask-the-steps-in-an-order-that-avoids-unneeded-questions.md` Suppose an employee goes back and changes an earlier answer: the country from Germany to Switzerland, civil status from Married to Single, or the permit to a C permit. Answers they already gave may no longer apply (nationality, spouse data, denomination, children). Under data minimisation, must those answers be thrown away, or may they be kept? Do any rules re-run (e.g. the subject-to-source-tax decision) after submission?

## Run

Stages run: normalize/hr_transcript, normalize/zh_source_tax_calculator, normalize/pension_portal, extract/hr_transcript, extract/pension_portal, extract/zh_source_tax_calculator, judge_facts, knowledge.raw, feature.plan, sections/SEC-03-employment-start, sections/SEC-04-civil-status-spouse, sections/SEC-02-personal-details-address, sections/SEC-01-questionnaire-flow, sections/SEC-05-source-tax-liability, sections/SEC-06-source-tax-tariff-basics, sections/SEC-08-cross-border-residence, sections/SEC-07-source-tax-children, feature.flow, judge_trace, dev_refinement, review

Stages reused from cache: -

LLM cost this run: $10.2

Tokens this run: 1,983,592 in 55 agent calls (154 input, 835,251 cache read, 933,684 cache write, 214,503 output)
