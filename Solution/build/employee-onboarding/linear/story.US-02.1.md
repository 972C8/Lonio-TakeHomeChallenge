# [US-02.1] Complete postal address for HR mail

**As** HR, **I want** every new employee to give their complete home address (street, house number, postcode, town and country) as it would be written on an envelope, **so that** I can post documents to the employee without chasing missing address parts

Priority P1: HR posts many documents to employees and states the address 'has to be complete'; an incomplete address blocks HR's postal communication (F-TR-010).

## Acceptance criteria

**AC-02.1.1 All address parts are always asked and required**
- Given a new employee is filling in the onboarding questionnaire
- When they reach the home address step
- Then they are asked for street, house number, postcode, town and country of their home address, and cannot complete the step while any of these five parts is empty

| Example | Country of home address (country of residence) | → | Street | House number | Postcode | Town | Country of home address (country of residence) |
|---|---|---|---|---|---|---|---|
| Employee living in Switzerland | Switzerland | → | required | required | required | required | required |
| Employee living abroad | Germany | → | required | required | required | required | required |

**AC-02.1.2 Normal postal address with no extra parts**
- Given a new employee is at the home address step
- When they enter their address
- Then only the parts of a normal postal address as written on an envelope are asked (street, house number, postcode, town, country); no further address parts are asked

**AC-02.1.3 Address is asked once and received by HR**
- Given a new employee has completed the home address step
- When the onboarding data is made available to the receiving parties
- Then HR receives the complete home address, and the employee is not asked for the address again in any later step

+++ Evidence

- F-TR-009: HR needs the employee's full address: street, house number, postcode, town and country. — "Yes, I need the address, obviously. The full address. Street, number, postcode, town, country." (T-014)
- F-TR-010: The address must be complete, because HR posts many documents to employees. It is a normal postal address, as you would write it on an envelope, with no extra parts. — "We post a lot of documents to people, so it has to be complete." (T-014) — "No, no. Just a normal address, the way you would write it on an envelope." (T-016)
- G-01

Spec: `requirements/employee-onboarding/features/FEAT-02-home-address.md`
+++
