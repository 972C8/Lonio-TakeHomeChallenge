// Every example table of the feature spec, run against the prototype.
// The examples are read from the pipeline's output (build/<feature>/spec.json), so a new pipeline run that
// changes the requirements makes these tests fail until the prototype follows.

import { describe, expect, it } from 'vitest';
import specJson from '../../build/employee-onboarding/spec.json';
import { emptyAnswers, type Answers, type Child } from '../src/model';
import { QUESTIONS } from '../src/questions';
import {
  asked, baseTariffLetter, childAsked, childDigit, childResult, churchTaxSuffix, crossBorderTariff, dtaReservationNote,
  insuranceStartDate, liechtensteinNotLiable, pensionFundCanton, pensionFundCivilStatus, permitReminder,
  residence, sourceTaxCivilStatus, sourceTaxResult, subjectToSourceTax, tariffLetter,
} from '../src/rules';


interface Example {
  name: string;
  given: { item: string; value: string }[];
  then: { target: string; expect: string }[];
}
const spec = specJson as any;
const cases: { ac: string; ex: Example }[] = spec.feature.sections.flatMap((sec: any) =>
  sec.stories.flatMap((st: any) =>
    st.acceptance_criteria.flatMap((ac: any) => (ac.examples ?? []).map((ex: Example) => ({ ac: ac.id, ex }))),
  ),
);

/** Spec information item -> prototype answer field. */
const FIELD: Record<string, keyof Answers> = {
  first_name: 'firstName', last_name: 'lastName', date_of_birth: 'dateOfBirth', first_working_day: 'firstWorkingDay',
  address_street: 'street', address_house_number: 'houseNumber', address_postcode: 'postcode', address_town: 'town',
  address_country: 'country', residence_canton: 'canton', nationality: 'nationality', holds_c_permit: 'cPermit',
  civil_status: 'civilStatus', spouse_date_of_birth: 'spouseDateOfBirth', spouse_nationality: 'spouseNationality',
  spouse_holds_c_permit: 'spouseCPermit', spouse_residence_country: 'spouseLivesInCH',
  daily_return_germany: 'deDailyReturn', residence_certificate: 'deCertificate', daily_return_reasonable: 'deReasonable',
  non_return_days_60: 'deMoreThan60', daily_return_liechtenstein: 'liDailyReturn', non_return_days_45: 'liMoreThan45',
  confession: 'denomination', spouse_gainful_employment: 'spouseWorks', has_children: 'hasChildren',
};
/** Spec per-child item -> prototype child field (the examples describe one child). */
const CHILD: Record<string, keyof Child> = {
  child_age_status: 'ageStatus', child_same_household: 'inHousehold', child_custody: 'custody',
  child_common_household_other_parent: 'commonHousehold', child_shared_custody: 'sharedCustodyMarried',
  child_parental_care: 'parentalCustodySingle', child_alternating_custody: 'alternatingCare',
  child_main_financial_contributor: 'largerContributor', child_maintenance_over_50: 'moreThan50',
};

function answersOf(ex: Example): Answers {
  const a = emptyAnswers();
  const child: Child = { id: 'c1' };
  let hasChild = false;
  for (const { item, value } of ex.given) {
    if (item === 'address_house_number' && value === 'no house number') a.noHouseNumber = true;
    else if (FIELD[item]) (a as any)[FIELD[item]] = value;
    else if (CHILD[item]) { (child as any)[CHILD[item]] = value; hasChild = true; }
    else throw new Error(`unknown item ${item}`);
  }
  if (hasChild || a.hasChildren === 'yes') a.children = [child];
  return a;
}

function isAsked(item: string, a: Answers): boolean {
  if (CHILD[item]) {
    const q = CHILD[item] as keyof typeof childAsked;
    return asked.children(a) && a.children.length > 0 && childAsked[q](a.children[0], a);
  }
  if (item === 'address_house_number') return true; // a number or 'no house number'
  const q = QUESTIONS.find((x) => x.id === FIELD[item]);
  if (!q) throw new Error(`no question for ${item}`);
  return q.asked(a);
}

const yn = (v: boolean | undefined) => (v === undefined ? undefined : v ? 'yes' : 'no');
const CALC_CS = { married: 'Married or registered partnership', single: 'Single, divorced, separated or widowed' } as const;

/** Spec business rule -> the prototype's value, in the spec's vocabulary. */
function ruleValue(rule: string, a: Answers): string | undefined {
  switch (rule) {
    case 'subject_to_source_tax': return yn(subjectToSourceTax(a));
    case 'permit_reminder': return yn(permitReminder(a));
    case 'insurance_start_date': return insuranceStartDate(a.firstWorkingDay);
    case 'pension_fund_canton': return pensionFundCanton(a);
    case 'pension_fund_civil_status': return pensionFundCivilStatus(a.civilStatus);
    case 'calculator_civil_status': { const s = sourceTaxCivilStatus(a.civilStatus); return s && CALC_CS[s]; }
    case 'calculator_residence': return residence(a.country);
    case 'base_tariff_letter': return baseTariffLetter(a);
    case 'tariff_letter': return tariffLetter(a);
    case 'church_tax_suffix': return churchTaxSuffix(a);
    case 'child_result': return a.children[0] && childResult(a.children[0], a);
    case 'child_count': return String(childDigit(a) ?? '');
    case 'cross_border_tariff': return yn(crossBorderTariff(a));
    case 'liechtenstein_no_source_tax': return yn(liechtensteinNotLiable(a));
    case 'dta_reservation_note': return yn(dtaReservationNote(a));
    case 'tariff_code': {
      const r = sourceTaxResult(a);
      if (!r) return 'incomplete - HR must complete';
      if (r.kind === 'none') return 'no tariff code';
      if (r.kind === 'liechtenstein-no-liability') return r.text;
      return r.code;
    }
  }
  throw new Error(`unknown rule ${rule}`);
}

const norm = (v: string | undefined) => (v ?? '').trim().toLowerCase();

describe('feature spec examples', () => {
  it('finds the examples', () => expect(cases.length).toBeGreaterThan(100));
  for (const { ac, ex } of cases) {
    it(`${ac} / ${ex.name}`, () => {
      const a = answersOf(ex);
      for (const { target, expect: e } of ex.then) {
        const want = norm(e);
        if (FIELD[target] || CHILD[target] || target === 'address_house_number') {
          const got = isAsked(target, a);
          if (want === 'not asked') expect(got, `${target} should not be asked`).toBe(false);
          else expect(got, `${target} should be ${want}`).toBe(true); // every asked question is required
        } else {
          expect(norm(ruleValue(target, a)), target).toBe(want);
        }
      }
    });
  }
});
