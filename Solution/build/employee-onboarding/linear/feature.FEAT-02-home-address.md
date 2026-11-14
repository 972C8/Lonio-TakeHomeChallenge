# [FEAT-02] Complete home address and country of residence

---
id: FEAT-02-home-address
title: "Complete home address and country of residence"
order: 2
stakeholders: [employee, hr, source_tax]
stories: [US-02.1, US-02.2]
information: [address_street, address_house_number, address_postcode, address_town, address_country]
rules: []
open_questions: []
---

# Complete home address and country of residence

**Goal:** Every new employee gives a complete postal address once, so HR can post documents, and its country tells the other steps whether the employee lives in Switzerland.

## Context
HR posts many documents to employees and needs the complete address as written on an envelope: street, number, postcode, town and country, with no extra parts (F-TR-009, F-TR-010). The country of the home address is also the employee's country of residence (F-TR-040, G-09). Several later questions depend on it. Employees living abroad are always subject to source tax (F-TR-034, F-TR-037), and the pension fund canton is asked only of employees living in Switzerland. This feature therefore comes before the pension and source tax features that depend on it.

**Stakeholders:** new employee, HR, source tax office



