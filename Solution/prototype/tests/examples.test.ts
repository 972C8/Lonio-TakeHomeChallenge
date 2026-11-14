// The example tables of the acceptance criteria, as executable tests.
// Test names quote the story/AC and the example row.

import { describe, expect, it } from 'vitest';
import type { Answers, Child } from '../src/model';
import { discardInapplicable, validateAll, visibleSteps } from '../src/questions';
import { buildRecord } from '../src/record';
import {
  asked, childAsked, childDigit, childResult, churchTaxSuffix, crossBorderTariff, insuranceStartDate,
  liechtensteinNoLiability, marriedTariffLetter, parseDate, pensionFundCivilStatus, permitReminder, residence,
  singleParentH, sourceTaxCivilStatus, sourceTaxResult, spouseExemption, subjectToSourceTax, tariffLetter,
} from '../src/rules';

const A = (x: Partial<Answers>): Answers => ({ children: [], ...x });
const kid = (x: Partial<Child>): Child => ({ id: 'c1', ...x });
const withKid = (x: Partial<Answers>, c: Partial<Child>): Answers =>
  A({ hasChildren: 'yes', ...x, children: [kid(c)] });

const CH = 'Switzerland';
const REF = 'Roman Catholic, Christian Catholic or Evangelical Reformed' as const;

describe('US-01 Personal details and home address', () => {
  it('AC-01.1.2 date of birth is a full DD.MM.YYYY date', () => {
    expect(parseDate('12.05.1988')).toEqual({ day: 12, month: 5, year: 1988 });
    expect(parseDate('31.02.2026')).toBeUndefined();
    expect(parseDate('2026-01-01')).toBeUndefined();
  });

  it('AC-01.1.1 / AC-01.2.1 name, date of birth and address are required wherever the employee lives', () => {
    for (const country of [CH, 'Germany', 'Liechtenstein']) {
      const errors = validateAll(A({ country }));
      for (const f of ['firstName', 'lastName', 'dateOfBirth', 'street', 'houseNumber', 'postcode', 'town']) {
        expect(errors[f], `${f} for ${country}`).toBeDefined();
      }
    }
    expect(validateAll(A({}))['country']).toBeDefined();
  });

  it.each([
    [CH, 'Switzerland'], ['Germany', 'Germany'], ['Liechtenstein', 'Liechtenstein'], ['France', 'Other country'],
  ])('AC-01.3.1 / AC-07.1.1 %s -> residence %s', (country, expected) => {
    expect(residence(country)).toBe(expected);
  });

  it.each([
    ['Germany', true, false], ['Italy', true, false], [CH, undefined, true],
  ])('AC-01.3.2 lives in %s -> subject %s, nationality/canton asked %s', (country, subject, askedNat) => {
    const a = A({ country });
    expect(subjectToSourceTax(a)).toBe(subject);
    expect(asked.nationality(a)).toBe(askedNat);
    expect(asked.canton(a)).toBe(askedNat);
  });

  it.each([[CH, true], ['Germany', false], ['Liechtenstein', false]])(
    'AC-01.4.1 lives in %s -> canton asked %s', (country, expected) => {
      expect(asked.canton(A({ country }))).toBe(expected);
    });

  it('AC-01.4.3 canton dropped on submission when the country changes away from Switzerland', () => {
    const a = A({ country: 'Germany', canton: 'Zurich' });
    expect(discardInapplicable(a).canton).toBeUndefined();
  });
});

describe('US-02 First working day and insurance start date', () => {
  it.each([
    ['01.05.2026', '01.05.2026'], ['01.01.2027', '01.01.2027'], // AC-02.2.2
    ['15.03.2026', '01.04.2026'], ['02.06.2026', '01.07.2026'], ['31.12.2026', '01.01.2027'], // AC-02.2.3 / AC-02.2.4 (Julia)
  ])('first working day %s -> insurance start %s', (fwd, expected) => {
    expect(insuranceStartDate(fwd)).toBe(expected);
  });

  it('AC-02.1.1 first working day is required for everyone', () => {
    expect(validateAll(A({ country: CH, nationality: CH })).firstWorkingDay).toBeDefined();
    expect(validateAll(A({ country: 'Germany' })).firstWorkingDay).toBeDefined();
  });

  it('AC-02.2.4 the insurance start follows the latest first working day', () => {
    const rec = buildRecord(A({ firstWorkingDay: '15.03.2026' }));
    expect(rec.derived.insuranceStartDate).toBe('01.04.2026');
  });
});

describe('US-03 Civil status', () => {
  it.each([
    ['Married', true], ['Registered partnership', true], ['Separated', true],
    ['Single', false], ['Divorced', false], ['Widowed', false],
  ] as const)('AC-03.2.1/2 %s -> spouse date of birth asked %s', (cs, expected) => {
    expect(asked.spouseDateOfBirth(A({ civilStatus: cs }))).toBe(expected);
  });

  it('AC-03.2.4 spouse date of birth discarded after changing to Divorced', () => {
    expect(discardInapplicable(A({ civilStatus: 'Divorced', spouseDateOfBirth: '12.05.1988' })).spouseDateOfBirth).toBeUndefined();
  });

  it.each([
    ['Single', 'Single'], ['Married', 'Married'], ['Divorced', 'Divorced'], ['Widowed', 'Widowed'],
    ['Registered partnership', 'Married'], ['Separated', 'Married'],
  ] as const)('AC-03.3 %s -> pension fund %s', (cs, expected) => {
    expect(pensionFundCivilStatus(cs)).toBe(expected);
  });

  it.each([
    ['Married', 'married'], ['Registered partnership', 'married'],
    ['Single', 'single'], ['Divorced', 'single'], ['Separated', 'single'], ['Widowed', 'single'],
  ] as const)('AC-03.4 %s -> source tax %s', (cs, expected) => {
    expect(sourceTaxCivilStatus(cs)).toBe(expected);
  });
});

describe('US-04 Source tax liability', () => {
  it('AC-04.1.1/3 nationality and C permit asked only of residents of Switzerland', () => {
    expect(asked.nationality(A({ country: CH }))).toBe(true); // Tomás
    expect(asked.nationality(A({ country: 'Germany' }))).toBe(false); // Stefan
    expect(asked.cPermit(A({ country: 'Germany' }))).toBe(false);
    expect(asked.nationality(A({ country: 'Liechtenstein' }))).toBe(false);
    expect(asked.cPermit(A({ country: CH, nationality: CH }))).toBe(false); // AC-04.1.2
    expect(asked.cPermit(A({ country: CH, nationality: 'Brazil' }))).toBe(true); // Tomás
  });

  const tomas = { country: CH, nationality: 'Brazil', cPermit: 'no' } as const;

  it.each([
    ['Tomás', { ...tomas, civilStatus: 'Married' }, true],
    ['registered partner without C permit', { country: CH, nationality: 'Italy', cPermit: 'no', civilStatus: 'Registered partnership' }, true],
    ['separated', { country: CH, nationality: 'Italy', cPermit: 'no', civilStatus: 'Separated' }, false],
    ['divorced', { country: CH, nationality: 'Italy', cPermit: 'no', civilStatus: 'Divorced' }, false],
    ['married with C permit', { country: CH, nationality: 'Italy', cPermit: 'yes', civilStatus: 'Married' }, false],
    ['married Swiss', { country: CH, nationality: CH, civilStatus: 'Married' }, false],
    ['married living abroad', { country: 'Germany', civilStatus: 'Married' }, false],
  ] as const)('AC-04.2.1 %s -> spouse country asked %s', (_n, x, expected) => {
    expect(asked.spouseCountry(A(x as Partial<Answers>))).toBe(expected);
  });

  it('AC-04.2.2/3 spouse nationality and C permit asked only when needed', () => {
    const base = { ...tomas, civilStatus: 'Married' } as const;
    expect(asked.spouseNationality(A({ ...base, spouseCountry: CH }))).toBe(true);
    expect(asked.spouseNationality(A({ ...base, spouseCountry: 'Brazil' }))).toBe(false);
    expect(asked.spouseCPermit(A({ ...base, spouseCountry: 'Brazil' }))).toBe(false);
    expect(asked.spouseCPermit(A({ ...base, spouseCountry: CH, spouseNationality: CH }))).toBe(false);
    expect(asked.spouseCPermit(A({ ...base, spouseCountry: CH, spouseNationality: 'Portugal' }))).toBe(true);
  });

  it.each([
    ['Tomás', { ...tomas, civilStatus: 'Married', spouseCountry: CH, spouseNationality: CH }, true],
    ['partner with C permit', { ...tomas, civilStatus: 'Registered partnership', spouseCountry: CH, spouseNationality: 'Portugal', spouseCPermit: 'yes' }, true],
    ['non-Swiss spouse without C permit', { ...tomas, civilStatus: 'Married', spouseCountry: CH, spouseNationality: 'Portugal', spouseCPermit: 'no' }, false],
    ['spouse abroad', { ...tomas, civilStatus: 'Married', spouseCountry: 'Brazil' }, false],
    ['separated', { ...tomas, civilStatus: 'Separated' }, false],
    ['single', { ...tomas, civilStatus: 'Single' }, false],
  ] as const)('AC-04.2.4 %s -> exemption %s', (_n, x, expected) => {
    expect(spouseExemption(A(x as Partial<Answers>))).toBe(expected);
  });

  it('AC-04.2.5 spouse answers discarded when they no longer apply', () => {
    const a = A({ ...tomas, cPermit: 'yes', civilStatus: 'Married', spouseCountry: CH, spouseNationality: 'Portugal', spouseCPermit: 'no' });
    const kept = discardInapplicable(a);
    expect([kept.spouseCountry, kept.spouseNationality, kept.spouseCPermit]).toEqual([undefined, undefined, undefined]);
  });

  it.each([
    ['Stefan, Swiss living in Germany', { country: 'Germany', nationality: CH }, true],
    ['Liechtenstein', { country: 'Liechtenstein' }, true],
    ['Swiss in Switzerland', { country: CH, nationality: CH }, false],
    ['C permit', { country: CH, nationality: 'Italy', cPermit: 'yes', civilStatus: 'Single' }, false],
    ['Tomás', { ...tomas, civilStatus: 'Married', spouseCountry: CH, spouseNationality: CH }, false],
    ['single non-Swiss', { ...tomas, civilStatus: 'Single' }, true],
    ['separated non-Swiss', { ...tomas, civilStatus: 'Separated' }, true],
    ['non-Swiss spouse without C permit', { ...tomas, civilStatus: 'Married', spouseCountry: CH, spouseNationality: 'Portugal', spouseCPermit: 'no' }, true],
    ['spouse abroad', { ...tomas, civilStatus: 'Married', spouseCountry: 'Brazil' }, true],
  ] as const)('AC-04.3.1/2 %s -> subject %s', (_n, x, expected) => {
    expect(subjectToSourceTax(A(x as Partial<Answers>))).toBe(expected);
  });

  it('AC-04.3.3 only employees subject to source tax get the source tax questions', () => {
    const tomasMarried = A({ ...tomas, civilStatus: 'Married', spouseCountry: CH, spouseNationality: CH });
    expect(asked.denomination(tomasMarried)).toBe(false);
    expect(visibleSteps(tomasMarried).map((s) => s.key)).not.toContain('sourceTax');
    expect(asked.denomination(A({ country: 'Germany', civilStatus: 'Single' }))).toBe(true);
  });
});

describe('US-05 Tariff basics and result', () => {
  it.each([
    ['France', 'Single', undefined, undefined, true],
    [CH, 'Single', 'Germany', 'no', true],
    [CH, 'Single', CH, undefined, false],
    [CH, 'Married', 'Italy', 'yes', false],
  ] as const)('AC-05.3.1 %s %s %s permit %s -> denomination asked %s', (country, civilStatus, nationality, cPermit, expected) => {
    expect(asked.denomination(A({ country, civilStatus, nationality, cPermit }))).toBe(expected);
  });

  it('AC-05.3.3 church-tax suffix', () => {
    expect(churchTaxSuffix(A({ denomination: REF }))).toBe('Y');
    expect(churchTaxSuffix(A({ denomination: 'None or other' }))).toBe('N');
  });

  it.each([
    ['married abroad', { country: 'France', civilStatus: 'Married' }, true],
    ['registered partnership abroad', { country: 'France', civilStatus: 'Registered partnership' }, true],
    ['separated', { country: 'France', civilStatus: 'Separated' }, false],
    ['single', { country: 'France', civilStatus: 'Single' }, false],
    ['married, CH, spouse abroad', { country: CH, civilStatus: 'Married', nationality: 'Germany', cPermit: 'no', spouseCountry: 'Germany' }, true],
    ['married to Swiss spouse in CH', { country: CH, civilStatus: 'Married', nationality: 'Italy', cPermit: 'no', spouseCountry: CH, spouseNationality: CH }, false],
  ] as const)('AC-05.4.1 %s -> spouse works asked %s', (_n, x, expected) => {
    expect(asked.spouseWorks(A(x as Partial<Answers>))).toBe(expected);
  });

  it('AC-05.4.2 married tariff letter', () => {
    expect(marriedTariffLetter(A({ civilStatus: 'Married', spouseWorks: 'yes' }))).toBe('C');
    expect(marriedTariffLetter(A({ civilStatus: 'Married', spouseWorks: 'no' }))).toBe('B');
    expect(marriedTariffLetter(A({ civilStatus: 'Registered partnership', spouseWorks: 'yes' }))).toBe('C');
  });

  const soleMinor = { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Sole custody' } as const;

  it.each([
    ['married, spouse works', A({ country: 'France', civilStatus: 'Married', spouseWorks: 'yes', hasChildren: 'no' }), 'C'],
    ['married, spouse does not work', A({ country: 'France', civilStatus: 'Married', spouseWorks: 'no', hasChildren: 'no' }), 'B'],
    ['A0Y', A({ country: CH, civilStatus: 'Single', nationality: 'Germany', cPermit: 'no', hasChildren: 'no' }), 'A'],
    ['separated, no children', A({ country: 'France', civilStatus: 'Separated', hasChildren: 'no' }), 'A'],
    ['single, sole custody minor', withKid({ country: 'France', civilStatus: 'Single' }, soleMinor), 'H'],
    // AC-05.6.2 cross-border letters
    ['L0Y', A({ country: 'Germany', civilStatus: 'Single', hasChildren: 'no', deDailyReturn: 'yes', deCertificate: 'yes' }), 'L'],
    ['M0N', A({ country: 'Germany', civilStatus: 'Married', hasChildren: 'no', deDailyReturn: 'yes', deCertificate: 'yes', spouseWorks: 'no' }), 'M'],
    ['N1Y', withKid({ country: 'Germany', civilStatus: 'Married', deDailyReturn: 'yes', deCertificate: 'yes', spouseWorks: 'yes' }, soleMinor), 'N'],
    ['P1Y', withKid({ country: 'Germany', civilStatus: 'Single', deDailyReturn: 'yes', deCertificate: 'yes' }, soleMinor), 'P'],
    ['C1Y without certificate', A({ country: 'Germany', civilStatus: 'Married', hasChildren: 'no', deDailyReturn: 'yes', deCertificate: 'not yet', spouseWorks: 'yes' }), 'C'],
    ['no daily return, reasonable, <=60 days', A({ country: 'Germany', civilStatus: 'Single', hasChildren: 'no', deDailyReturn: 'no', deReasonable: 'yes', deMoreThan60: 'no' }), 'L'],
  ])('AC-05.6 %s -> letter %s', (_n, a, expected) => {
    expect(tariffLetter(a)).toBe(expected);
  });

  it.each([
    ['Swiss in CH', A({ country: CH, nationality: CH, civilStatus: 'Single' }), { kind: 'none' }],
    ['LI daily return', A({ country: 'Liechtenstein', civilStatus: 'Single', liDailyReturn: 'yes' }), { kind: 'liechtenstein-no-liability' }],
    ['LI <=45 days', A({ country: 'Liechtenstein', civilStatus: 'Single', liDailyReturn: 'no', liMoreThan45: 'no' }), { kind: 'liechtenstein-no-liability' }],
    ['LI >45 days -> C1Y subject to DTA', withKid({ country: 'Liechtenstein', civilStatus: 'Married', spouseWorks: 'yes', denomination: REF, liDailyReturn: 'no', liMoreThan45: 'yes' }, soleMinor), { kind: 'tariff', code: 'C1Y', subjectToDTA: true }],
    ['N1Y', withKid({ country: 'Germany', civilStatus: 'Married', spouseWorks: 'yes', denomination: REF, deDailyReturn: 'yes', deCertificate: 'yes' }, soleMinor), { kind: 'tariff', code: 'N1Y', subjectToDTA: false }],
    ['M0N', A({ country: 'Germany', civilStatus: 'Married', spouseWorks: 'no', denomination: 'None or other', hasChildren: 'no', deDailyReturn: 'yes', deCertificate: 'yes' }), { kind: 'tariff', code: 'M0N' }],
    ['P1Y', withKid({ country: 'Germany', civilStatus: 'Single', denomination: REF, deDailyReturn: 'yes', deCertificate: 'yes' }, soleMinor), { kind: 'tariff', code: 'P1Y' }],
    ['A0Y', A({ country: CH, nationality: 'Germany', cPermit: 'no', civilStatus: 'Single', denomination: REF, hasChildren: 'no' }), { kind: 'tariff', code: 'A0Y', subjectToDTA: false }],
  ])('AC-05.7 %s', (_n, a, expected) => {
    expect(sourceTaxResult(a)).toMatchObject(expected);
  });
});

describe('US-06 Children', () => {
  it('AC-06.1.1 children question only for employees subject to source tax', () => {
    expect(asked.hasChildren(A({ country: 'Germany', civilStatus: 'Single' }))).toBe(true);
    expect(asked.hasChildren(A({ country: CH, nationality: CH, civilStatus: 'Single' }))).toBe(false);
    expect(asked.children(A({ country: 'Germany', civilStatus: 'Married', hasChildren: 'no' }))).toBe(false);
  });

  it('AC-06.1.2 every added child needs an age status; "yes" needs at least one child', () => {
    const a = A({ country: 'Germany', civilStatus: 'Single', hasChildren: 'yes' });
    expect(validateAll(a).children).toBeDefined();
    expect(validateAll({ ...a, children: [kid({})] })['child.c1.ageStatus']).toBeDefined();
  });

  const M = { country: 'Germany', civilStatus: 'Married' } as const;
  const S = { country: 'Germany', civilStatus: 'Single' } as const;

  it('AC-06.1.3/4 neither ends the block; household asked for minors and children in first education', () => {
    const a = withKid({ ...M, spouseWorks: 'no', denomination: 'None or other', deDailyReturn: 'no', deReasonable: 'no' }, { ageStatus: 'Neither' });
    expect(childAsked.inHousehold(a.children[0], a)).toBe(false);
    expect(childResult(a.children[0], a)).toBe('does not count');
    expect(sourceTaxResult(a)).toMatchObject({ code: 'B0N' }); // calculator: B0N
    expect(childAsked.inHousehold(kid({ ageStatus: 'Minor' }), A(S))).toBe(true);
    expect(childAsked.inHousehold(kid({ ageStatus: 'Of age and in first education' }), A(M))).toBe(true);
  });

  it('AC-06.2.1 custody asked only for a minor in the household', () => {
    expect(childAsked.custody(kid({ ageStatus: 'Minor', inHousehold: 'yes' }), A(S))).toBe(true);
    expect(childAsked.custody(kid({ ageStatus: 'Minor', inHousehold: 'no' }), A(S))).toBe(false);
  });

  // [name, employee, child, expected child result, extra asked/not-asked checks]
  it.each([
    // AC-06.2.2
    ['married, sole custody -> C1Y', M, { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Sole custody' }, 'counts'],
    ['single, sole custody -> H1Y', S, { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Sole custody' }, 'counts as H child'],
    ['separated, sole custody', { ...S, civilStatus: 'Separated' }, { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Sole custody' }, 'counts as H child'],
    // AC-06.2.3
    ['married, shared, common household -> C1Y', M, { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Shared custody', commonHousehold: 'yes' }, 'counts'],
    ['single, common household, other parent -> A0N', S, { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Shared custody', commonHousehold: 'yes', largerContributor: 'The other parent' }, 'does not count'],
    ['single, common household, employee (inferred)', S, { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Shared custody', commonHousehold: 'yes', largerContributor: 'The employee' }, 'counts as H child'],
    // AC-06.2.4
    ['married, no common household, no alternating care -> C0Y', M, { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Shared custody', commonHousehold: 'no', alternatingCare: 'no' }, 'does not count'],
    ['married, alternating care, other parent -> C0Y', M, { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Shared custody', commonHousehold: 'no', alternatingCare: 'yes', largerContributor: 'The other parent' }, 'does not count'],
    ['single, no common household, no alternating care -> H1N', S, { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Shared custody', commonHousehold: 'no', alternatingCare: 'no' }, 'counts as H child'],
    ['married, alternating care, employee (inferred)', M, { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Shared custody', commonHousehold: 'no', alternatingCare: 'yes', largerContributor: 'The employee' }, 'counts'],
    ['divorced, alternating care, employee (inferred)', { ...S, civilStatus: 'Divorced' }, { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Shared custody', commonHousehold: 'no', alternatingCare: 'yes', largerContributor: 'The employee' }, 'counts as H child'],
    ['single, alternating care, other parent (inferred)', S, { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Shared custody', commonHousehold: 'no', alternatingCare: 'yes', largerContributor: 'The other parent' }, 'does not count'],
    // AC-06.3.2 / AC-06.3.3
    ['married, no shared custody -> B0N', M, { ageStatus: 'Minor', inHousehold: 'no', sharedCustodyMarried: 'no' }, 'does not count'],
    ['single, no parental custody -> A0N', S, { ageStatus: 'Minor', inHousehold: 'no', parentalCustodySingle: 'no' }, 'does not count'],
    ['married, shared, alternating, employee -> B1N', M, { ageStatus: 'Minor', inHousehold: 'no', sharedCustodyMarried: 'yes', alternatingCare: 'yes', largerContributor: 'The employee' }, 'counts'],
    ['single, parental, alternating, employee -> H1N', S, { ageStatus: 'Minor', inHousehold: 'no', parentalCustodySingle: 'yes', alternatingCare: 'yes', largerContributor: 'The employee' }, 'counts as H child'],
    ['single, parental, no alternating care (inferred)', S, { ageStatus: 'Minor', inHousehold: 'no', parentalCustodySingle: 'yes', alternatingCare: 'no' }, 'does not count'],
    ['married, shared, alternating, other parent (inferred)', M, { ageStatus: 'Minor', inHousehold: 'no', sharedCustodyMarried: 'yes', alternatingCare: 'yes', largerContributor: 'The other parent' }, 'does not count'],
    // AC-06.5
    ['married, first education, common household -> B1N', M, { ageStatus: 'Of age and in first education', inHousehold: 'yes', commonHousehold: 'yes' }, 'counts'],
    ['single, first education, common household, employee (inferred)', S, { ageStatus: 'Of age and in first education', inHousehold: 'yes', commonHousehold: 'yes', largerContributor: 'The employee' }, 'counts as H child'],
    ['single, first education, common household, other parent (inferred)', S, { ageStatus: 'Of age and in first education', inHousehold: 'yes', commonHousehold: 'yes', largerContributor: 'The other parent' }, 'does not count'],
    ['single, in household, no common household, >50% -> H1N', S, { ageStatus: 'Of age and in first education', inHousehold: 'yes', commonHousehold: 'no', moreThan50: 'yes' }, 'counts as H child'],
    ['married, in household, no common household, >50% (inferred)', M, { ageStatus: 'Of age and in first education', inHousehold: 'yes', commonHousehold: 'no', moreThan50: 'yes' }, 'counts'],
    ['in household, no common household, not mainly maintained (inferred)', S, { ageStatus: 'Of age and in first education', inHousehold: 'yes', commonHousehold: 'no', moreThan50: 'no' }, 'does not count'],
    ['single, outside household, >50% -> A1N', S, { ageStatus: 'Of age and in first education', inHousehold: 'no', moreThan50: 'yes' }, 'counts'],
    ['married, outside household, not mainly maintained -> B0N', M, { ageStatus: 'Of age and in first education', inHousehold: 'no', moreThan50: 'no' }, 'does not count'],
    ['married, outside household, >50% (inferred)', M, { ageStatus: 'Of age and in first education', inHousehold: 'no', moreThan50: 'yes' }, 'counts'],
  ] as const)('AC-06.2 to 06.5 %s', (_n, emp, c, expected) => {
    const a = withKid(emp as Partial<Answers>, c as Partial<Child>);
    expect(childResult(a.children[0], a)).toBe(expected);
    // every answer used in the example is a question that is actually asked
    for (const key of Object.keys(c) as (keyof typeof childAsked)[]) {
      expect(childAsked[key](a.children[0], a), `${key} asked`).toBe(true);
    }
  });

  it('AC-06.2.3 / AC-06.4.1 / AC-06.5.1 follow-up questions asked only where they decide', () => {
    const married = A(M), single = A(S);
    const mCommon = kid({ ageStatus: 'Minor', inHousehold: 'yes', custody: 'Shared custody', commonHousehold: 'yes' });
    expect(childAsked.alternatingCare(mCommon, married)).toBe(false);
    expect(childAsked.largerContributor(mCommon, married)).toBe(false);
    expect(childAsked.largerContributor(mCommon, single)).toBe(true);
    const alt = kid({ ageStatus: 'Minor', inHousehold: 'yes', custody: 'Shared custody', commonHousehold: 'no', alternatingCare: 'yes' });
    expect(childAsked.largerContributor(alt, married)).toBe(true);
    expect(childAsked.largerContributor({ ...alt, alternatingCare: 'no' }, married)).toBe(false);
    const edu = kid({ ageStatus: 'Of age and in first education', inHousehold: 'yes', commonHousehold: 'yes' });
    expect(childAsked.largerContributor(edu, single)).toBe(true);
    expect(childAsked.custody(edu, married)).toBe(false);
    expect(childAsked.moreThan50(edu, married)).toBe(false);
    const eduOut = kid({ ageStatus: 'Of age and in first education', inHousehold: 'no' });
    expect(childAsked.commonHousehold(eduOut, single)).toBe(false);
    expect(childAsked.moreThan50(eduOut, single)).toBe(true);
  });

  it('AC-06.3.1 exactly one custody question for a minor outside the household', () => {
    const c = kid({ ageStatus: 'Minor', inHousehold: 'no' });
    const rp = A({ country: 'Germany', civilStatus: 'Registered partnership' });
    const wid = A({ country: 'Germany', civilStatus: 'Widowed' });
    expect([childAsked.sharedCustodyMarried(c, rp), childAsked.parentalCustodySingle(c, rp)]).toEqual([true, false]);
    expect([childAsked.sharedCustodyMarried(c, wid), childAsked.parentalCustodySingle(c, wid)]).toEqual([false, true]);
  });

  it('AC-06.6 child digit and H tariff', () => {
    const sole = { ageStatus: 'Minor', inHousehold: 'yes', custody: 'Sole custody' } as const;
    const married = withKid({ ...M, spouseWorks: 'yes' }, sole);
    expect(childDigit(married)).toBe(1);
    expect(singleParentH(married)).toBe(false);
    const single = withKid(S, sole);
    expect(childDigit(single)).toBe(1);
    expect(singleParentH(single)).toBe(true);
    const adultOut = withKid(S, { ageStatus: 'Of age and in first education', inHousehold: 'no', moreThan50: 'yes' });
    expect(singleParentH(adultOut)).toBe(false); // A1N
    expect(childDigit(withKid(M, { ageStatus: 'Neither' }))).toBe(0);
    // Spec text: one counting child plus one H child gives H2N
    const two = A({ ...S, hasChildren: 'yes', denomination: 'None or other', deDailyReturn: 'no', deReasonable: 'no', children: [
      kid({ id: 'a', ...sole }),
      kid({ id: 'b', ageStatus: 'Of age and in first education', inHousehold: 'no', moreThan50: 'yes' }),
    ] });
    expect(sourceTaxResult(two)).toMatchObject({ code: 'H2N' });
    // three counting children of a married employee whose spouse works -> C3Y
    const three = A({ ...M, spouseWorks: 'yes', denomination: REF, hasChildren: 'yes', deDailyReturn: 'no', deReasonable: 'no',
      children: ['a', 'b', 'c'].map((id) => kid({ id, ...sole })) });
    expect(sourceTaxResult(three)).toMatchObject({ code: 'C3Y' });
  });
});

describe('US-07 Living abroad', () => {
  it('AC-07.1.2 / AC-07.1.3 cross-border questions only for Germany / Liechtenstein', () => {
    const fr = A({ country: 'France' });
    expect([asked.deDailyReturn(fr), asked.liDailyReturn(fr), crossBorderTariff(fr)]).toEqual([false, false, false]);
    const de = A({ country: 'Germany' }), li = A({ country: 'Liechtenstein' });
    expect([asked.deDailyReturn(de), asked.liDailyReturn(de)]).toEqual([true, false]);
    expect([asked.deDailyReturn(li), asked.liDailyReturn(li)]).toEqual([false, true]);
    expect(asked.deDailyReturn(A({ country: 'Austria' }))).toBe(false);
  });

  it('AC-07.2.2/3 follow-up Germany questions', () => {
    const daily = A({ country: 'Germany', deDailyReturn: 'yes' });
    expect([asked.deCertificate(daily), asked.deReasonable(daily), asked.deMoreThan60(daily)]).toEqual([true, false, false]);
    const reasonable = A({ country: 'Germany', deDailyReturn: 'no', deReasonable: 'yes' });
    expect([asked.deCertificate(reasonable), asked.deReasonable(reasonable), asked.deMoreThan60(reasonable)]).toEqual([false, true, true]);
    expect(asked.deMoreThan60(A({ country: 'Germany', deDailyReturn: 'no', deReasonable: 'no' }))).toBe(false);
  });

  it.each([
    [{ deDailyReturn: 'yes', deCertificate: 'yes' }, true],
    [{ deDailyReturn: 'yes', deCertificate: 'no' }, false],
    [{ deDailyReturn: 'yes', deCertificate: 'not yet' }, false],
    [{ deDailyReturn: 'no', deReasonable: 'no' }, false],
    [{ deDailyReturn: 'no', deReasonable: 'yes', deMoreThan60: 'yes' }, false],
    [{ deDailyReturn: 'no', deReasonable: 'yes', deMoreThan60: 'no' }, true],
  ] as const)('AC-07.2.4 Germany %o -> cross-border %s', (x, expected) => {
    expect(crossBorderTariff(A({ country: 'Germany', ...x }))).toBe(expected);
  });

  it('AC-07.2.4 Liechtenstein never gets the cross-border tariff', () => {
    expect(crossBorderTariff(A({ country: 'Liechtenstein', liDailyReturn: 'no', liMoreThan45: 'yes' }))).toBe(false);
  });

  it('AC-07.3.1/2 Liechtenstein questions and result', () => {
    expect(asked.liMoreThan45(A({ country: 'Liechtenstein', liDailyReturn: 'yes' }))).toBe(false);
    expect(asked.liMoreThan45(A({ country: 'Liechtenstein', liDailyReturn: 'no' }))).toBe(true);
    expect(liechtensteinNoLiability(A({ country: 'Liechtenstein', liDailyReturn: 'yes' }))).toBe(true);
    expect(liechtensteinNoLiability(A({ country: 'Liechtenstein', liDailyReturn: 'no', liMoreThan45: 'no' }))).toBe(true);
    expect(liechtensteinNoLiability(A({ country: 'Liechtenstein', liDailyReturn: 'no', liMoreThan45: 'yes' }))).toBe(false);
    expect(liechtensteinNoLiability(A({ country: 'Germany', deDailyReturn: 'yes', deCertificate: 'yes' }))).toBe(false);
  });
});

describe('US-08 Completion and submission', () => {
  it.each([
    [CH, CH, false], [CH, 'Germany', true], ['Germany', undefined, true], ['Liechtenstein', undefined, true],
  ])('AC-08.1.1 lives in %s, nationality %s -> reminder %s', (country, nationality, expected) => {
    expect(permitReminder(A({ country, nationality }))).toBe(expected);
  });

  it('AC-08.2.2 changed Married -> Single: spouse date of birth not recorded', () => {
    expect(discardInapplicable(A({ civilStatus: 'Single', spouseDateOfBirth: '01.01.1990' })).spouseDateOfBirth).toBeUndefined();
  });

  it('AC-08.2.2 changed Swiss address -> Germany: canton, nationality, C permit not recorded', () => {
    const kept = discardInapplicable(A({ country: 'Germany', canton: 'Zurich', nationality: 'Italy', cPermit: 'no' }));
    expect([kept.canton, kept.nationality, kept.cPermit]).toEqual([undefined, undefined, undefined]);
  });

  it('AC-08.2.2 changed nationality to Switzerland: C permit and source tax answers not recorded', () => {
    const a = A({ country: CH, nationality: CH, cPermit: 'no', civilStatus: 'Single', denomination: REF, hasChildren: 'no' });
    const rec = buildRecord(a);
    expect(rec.answers.cPermit).toBeUndefined();
    expect(rec.answers.denomination).toBeUndefined();
    expect(rec.answers.hasChildren).toBeUndefined();
    expect(rec.derived.subjectToSourceTax).toBe(false);
    expect(rec.derived.sourceTaxResult).toEqual({ kind: 'none' });
  });

  it('AC-08.2.1 answers are kept in the draft while moving back and forth', () => {
    const draft = A({ country: 'Germany', canton: 'Zurich' });
    discardInapplicable(draft);
    expect(draft.canton).toBe('Zurich');
  });
});
