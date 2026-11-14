# [OQ-01] Decision needed: Which questions does the Zurich source tax calculator ask to set the tariff code, with which options and under which conditions (including the different questions for married employees, such as whether the spouse works, and the extra questions and German forms for employees living abroad)?

The source tax questions for subject employees cannot be specified; the calculator source has not been analysed yet. It may also need data not asked today (e.g. nationality of employees living abroad).

- Analyse the Zurich calculator and add its questions, asked only when subject_to_source_tax is true
- Release without source tax questions at first

**Recommendation:** Analyse the calculator before specifying the source tax step; ask its questions only to employees subject to source tax.
