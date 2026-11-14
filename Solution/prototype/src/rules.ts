// Business rules of the feature spec, as pure functions.
// "undefined" means: not decidable yet, because an answer it depends on is still missing.

import type { Answers, Child, CivilStatus } from './model';

const CH = 'Switzerland';

// ---------- Dates (DD.MM.YYYY) ----------

export interface DayMonthYear { day: number; month: number; year: number }

/** Parses a strict DD.MM.YYYY calendar date (AC-01.1.2). */
export function parseDate(text: string | undefined): DayMonthYear | undefined {
  const m = /^(\d{2})\.(\d{2})\.(\d{4})$/.exec((text ?? '').trim());
  if (!m) return undefined;
  const [day, month, year] = [Number(m[1]), Number(m[2]), Number(m[3])];
  const d = new Date(Date.UTC(year, month - 1, day));
  if (d.getUTCFullYear() !== year || d.getUTCMonth() !== month - 1 || d.getUTCDate() !== day) return undefined;
  return { day, month, year };
}

export const formatDate = ({ day, month, year }: DayMonthYear): string =>
  `${String(day).padStart(2, '0')}.${String(month).padStart(2, '0')}.${year}`;

/** Insurance start date (US-02.2): the first working day if it is the 1st, else the 1st of the following month. */
export function insuranceStartDate(firstWorkingDay: string | undefined): string | undefined {
  const d = parseDate(firstWorkingDay);
  if (!d) return undefined;
  if (d.day === 1) return formatDate(d);
  return d.month === 12
    ? formatDate({ day: 1, month: 1, year: d.year + 1 })
    : formatDate({ day: 1, month: d.month + 1, year: d.year });
}

// ---------- Civil status (US-03.3, US-03.4) ----------

export type PensionFundCivilStatus = 'Single' | 'Married' | 'Divorced' | 'Widowed';

export function pensionFundCivilStatus(cs: CivilStatus | undefined): PensionFundCivilStatus | undefined {
  if (!cs) return undefined;
  if (cs === 'Registered partnership' || cs === 'Separated') return 'Married'; // provisional, D-003
  return cs;
}

export type SourceTaxCivilStatus = 'married' | 'single';

export function sourceTaxCivilStatus(cs: CivilStatus | undefined): SourceTaxCivilStatus | undefined {
  if (!cs) return undefined;
  return cs === 'Married' || cs === 'Registered partnership' ? 'married' : 'single';
}

// ---------- Residence (US-01.3, US-07.1) ----------

export type Residence = 'Switzerland' | 'Germany' | 'Liechtenstein' | 'Other country';

export function residence(country: string | undefined): Residence | undefined {
  if (!country) return undefined;
  if (country === CH || country === 'Germany' || country === 'Liechtenstein') return country;
  return 'Other country';
}

const livesInCH = (a: Answers) => a.country === CH;

// ---------- Which questions are asked ----------
// Each predicate checks the chain of answers it depends on, so a stale answer to a
// question that no longer applies never opens a follow-up question.

const SPOUSE_DOB_STATUSES: CivilStatus[] = ['Married', 'Registered partnership', 'Separated'];

export const asked = {
  canton: (a: Answers) => livesInCH(a),
  nationality: (a: Answers) => livesInCH(a),
  cPermit: (a: Answers) => livesInCH(a) && !!a.nationality && a.nationality !== CH,
  spouseDateOfBirth: (a: Answers) => !!a.civilStatus && SPOUSE_DOB_STATUSES.includes(a.civilStatus),
  spouseCountry: (a: Answers) =>
    asked.cPermit(a) && a.cPermit === 'no' && sourceTaxCivilStatus(a.civilStatus) === 'married',
  spouseNationality: (a: Answers) => asked.spouseCountry(a) && a.spouseCountry === CH,
  spouseCPermit: (a: Answers) =>
    asked.spouseNationality(a) && !!a.spouseNationality && a.spouseNationality !== CH,
  // Step 6 – only for employees subject to source tax (AC-04.3.3)
  denomination: (a: Answers) => subjectToSourceTax(a) === true,
  spouseWorks: (a: Answers) =>
    subjectToSourceTax(a) === true && sourceTaxCivilStatus(a.civilStatus) === 'married',
  hasChildren: (a: Answers) => subjectToSourceTax(a) === true,
  children: (a: Answers) => asked.hasChildren(a) && a.hasChildren === 'yes',
  deDailyReturn: (a: Answers) => subjectToSourceTax(a) === true && a.country === 'Germany',
  deCertificate: (a: Answers) => asked.deDailyReturn(a) && a.deDailyReturn === 'yes',
  deReasonable: (a: Answers) => asked.deDailyReturn(a) && a.deDailyReturn === 'no',
  deMoreThan60: (a: Answers) => asked.deReasonable(a) && a.deReasonable === 'yes',
  liDailyReturn: (a: Answers) => subjectToSourceTax(a) === true && a.country === 'Liechtenstein',
  liMoreThan45: (a: Answers) => asked.liDailyReturn(a) && a.liDailyReturn === 'no',
};

/** Per-child questions (US-06.1 to US-06.5). Only meaningful when asked.children(a). */
export const childAsked = {
  ageStatus: (_c: Child, _a: Answers) => true,
  inHousehold: (c: Child, _a: Answers) => c.ageStatus === 'Minor' || c.ageStatus === 'Of age and in first education',
  custody: (c: Child, _a: Answers) => c.ageStatus === 'Minor' && c.inHousehold === 'yes',
  commonHousehold: (c: Child, a: Answers) =>
    (childAsked.custody(c, a) && c.custody === 'Shared custody') ||
    (c.ageStatus === 'Of age and in first education' && c.inHousehold === 'yes'),
  sharedCustodyMarried: (c: Child, a: Answers) =>
    c.ageStatus === 'Minor' && c.inHousehold === 'no' && sourceTaxCivilStatus(a.civilStatus) === 'married',
  parentalCustodySingle: (c: Child, a: Answers) =>
    c.ageStatus === 'Minor' && c.inHousehold === 'no' && sourceTaxCivilStatus(a.civilStatus) === 'single',
  alternatingCare: (c: Child, a: Answers) =>
    (c.ageStatus === 'Minor' && childAsked.commonHousehold(c, a) && c.commonHousehold === 'no') ||
    (childAsked.sharedCustodyMarried(c, a) && c.sharedCustodyMarried === 'yes') ||
    (childAsked.parentalCustodySingle(c, a) && c.parentalCustodySingle === 'yes'),
  largerContributor: (c: Child, a: Answers) =>
    (childAsked.alternatingCare(c, a) && c.alternatingCare === 'yes') ||
    (sourceTaxCivilStatus(a.civilStatus) === 'single' && childAsked.commonHousehold(c, a) && c.commonHousehold === 'yes'),
  moreThan50: (c: Child, a: Answers) =>
    c.ageStatus === 'Of age and in first education' &&
    (c.inHousehold === 'no' || (childAsked.commonHousehold(c, a) && c.commonHousehold === 'no')),
};

// ---------- Source tax liability (US-04.2, US-04.3) ----------

/** Spouse exemption: married/registered partner whose spouse lives in CH and is Swiss or holds a C permit. */
export function spouseExemption(a: Answers): boolean | undefined {
  const st = sourceTaxCivilStatus(a.civilStatus);
  if (!st) return undefined;
  if (st === 'single') return false;
  if (!a.spouseCountry) return undefined;
  if (a.spouseCountry !== CH) return false;
  if (!a.spouseNationality) return undefined;
  if (a.spouseNationality === CH) return true;
  if (!a.spouseCPermit) return undefined;
  return a.spouseCPermit === 'yes';
}

export function subjectToSourceTax(a: Answers): boolean | undefined {
  if (!a.country) return undefined;
  if (a.country !== CH) return true; // living abroad: always subject
  if (!a.nationality) return undefined;
  if (a.nationality === CH) return false;
  if (!a.cPermit) return undefined;
  if (a.cPermit === 'yes') return false;
  const exempt = spouseExemption(a);
  return exempt === undefined ? undefined : !exempt;
}

// ---------- Children (US-06.6) ----------

export type ChildResult = 'counts' | 'counts as H child' | 'does not count';

/** Per-child result, following the "Child result (per child)" decision table. */
export function childResult(c: Child, a: Answers): ChildResult | undefined {
  const st = sourceTaxCivilStatus(a.civilStatus);
  if (!c.ageStatus || !st) return undefined;
  if (c.ageStatus === 'Neither') return 'does not count';
  const counts: ChildResult = st === 'married' ? 'counts' : 'counts as H child';
  const byContributor = (): ChildResult | undefined =>
    c.largerContributor === undefined ? undefined : c.largerContributor === 'The employee' ? counts : 'does not count';
  if (!c.inHousehold) return undefined;

  if (c.ageStatus === 'Minor') {
    if (c.inHousehold === 'yes') {
      if (!c.custody) return undefined;
      if (c.custody === 'Sole custody') return counts;
      if (!c.commonHousehold) return undefined;
      if (c.commonHousehold === 'yes') return st === 'married' ? 'counts' : byContributor();
      if (!c.alternatingCare) return undefined;
      if (c.alternatingCare === 'no') return st === 'married' ? 'does not count' : 'counts as H child';
      return byContributor();
    }
    const custody = st === 'married' ? c.sharedCustodyMarried : c.parentalCustodySingle;
    if (!custody) return undefined;
    if (custody === 'no') return 'does not count';
    if (!c.alternatingCare) return undefined;
    if (c.alternatingCare === 'no') return 'does not count';
    return byContributor();
  }

  // Of age and in first education
  if (c.inHousehold === 'yes') {
    if (!c.commonHousehold) return undefined;
    if (c.commonHousehold === 'yes') return st === 'married' ? 'counts' : byContributor();
    if (!c.moreThan50) return undefined;
    return c.moreThan50 === 'yes' ? counts : 'does not count';
  }
  if (!c.moreThan50) return undefined;
  return c.moreThan50 === 'yes' ? 'counts' : 'does not count'; // never an H child
}

function applicableChildren(a: Answers): Child[] {
  return asked.children(a) ? a.children : [];
}

/** Child digit: number of children that count (incl. H children). */
export function childDigit(a: Answers): number | undefined {
  let n = 0;
  for (const c of applicableChildren(a)) {
    const r = childResult(c, a);
    if (r === undefined) return undefined;
    if (r !== 'does not count') n++;
  }
  return n;
}

/** Single-parent H tariff: employee counts as single and at least one child is an H child. */
export function singleParentH(a: Answers): boolean | undefined {
  const st = sourceTaxCivilStatus(a.civilStatus);
  if (!st) return undefined;
  if (st === 'married') return false;
  const results = applicableChildren(a).map((c) => childResult(c, a));
  if (results.includes('counts as H child')) return true;
  return results.includes(undefined) ? undefined : false;
}

// ---------- Cross-border (US-07.2, US-07.3) ----------

export function crossBorderTariff(a: Answers): boolean | undefined {
  if (!a.country) return undefined;
  if (a.country !== 'Germany') return false;
  if (!a.deDailyReturn) return undefined;
  if (a.deDailyReturn === 'yes') {
    if (!a.deCertificate) return undefined;
    return a.deCertificate === 'yes'; // "not yet" counts as "no"
  }
  if (!a.deReasonable) return undefined;
  if (a.deReasonable === 'no') return false;
  if (!a.deMoreThan60) return undefined;
  return a.deMoreThan60 === 'no';
}

/** Liechtenstein: in principle no source tax liability (flagged for HR). */
export function liechtensteinNoLiability(a: Answers): boolean | undefined {
  if (!a.country) return undefined;
  if (a.country !== 'Liechtenstein') return false;
  if (!a.liDailyReturn) return undefined;
  if (a.liDailyReturn === 'yes') return true;
  if (!a.liMoreThan45) return undefined;
  return a.liMoreThan45 === 'no';
}

// ---------- Tariff (US-05.3 to US-05.7) ----------

export type TariffLetter = 'A' | 'B' | 'C' | 'H' | 'L' | 'M' | 'N' | 'P';
const CROSS_BORDER: Record<string, TariffLetter> = { A: 'L', B: 'M', C: 'N', H: 'P' };

export function churchTaxSuffix(a: Answers): 'Y' | 'N' | undefined {
  if (!a.denomination) return undefined;
  return a.denomination === 'None or other' ? 'N' : 'Y';
}

export function marriedTariffLetter(a: Answers): 'B' | 'C' | undefined {
  if (sourceTaxCivilStatus(a.civilStatus) !== 'married' || !a.spouseWorks) return undefined;
  return a.spouseWorks === 'yes' ? 'C' : 'B';
}

export function tariffLetter(a: Answers): TariffLetter | undefined {
  const st = sourceTaxCivilStatus(a.civilStatus);
  let base: TariffLetter | undefined;
  if (st === 'married') base = marriedTariffLetter(a);
  else if (st === 'single') {
    const h = singleParentH(a);
    base = h === undefined ? undefined : h ? 'H' : 'A';
  }
  if (!base) return undefined;
  const cb = crossBorderTariff(a);
  if (cb === undefined) return undefined;
  return cb ? CROSS_BORDER[base] : base;
}

export type SourceTaxResult =
  | { kind: 'none' }
  | { kind: 'liechtenstein-no-liability'; text: string; flagForHR: true }
  | { kind: 'tariff'; code: string; subjectToDTA: boolean };

export const LI_NO_LIABILITY_TEXT =
  'In principle no source tax liability, subject to the double taxation agreement';

/** Source tax result recorded for HR (AC-05.7.1, AC-05.7.2). */
export function sourceTaxResult(a: Answers): SourceTaxResult | undefined {
  const subject = subjectToSourceTax(a);
  if (subject === undefined) return undefined;
  if (!subject) return { kind: 'none' };
  const li = liechtensteinNoLiability(a);
  if (li === undefined) return undefined;
  if (li) return { kind: 'liechtenstein-no-liability', text: LI_NO_LIABILITY_TEXT, flagForHR: true };
  const letter = tariffLetter(a);
  const digit = childDigit(a);
  const suffix = churchTaxSuffix(a);
  if (!letter || digit === undefined || !suffix) return undefined;
  return { kind: 'tariff', code: `${letter}${digit}${suffix}`, subjectToDTA: a.country === 'Liechtenstein' };
}

// ---------- Permit reminder (US-08.1) ----------

export function permitReminder(a: Answers): boolean | undefined {
  if (!a.country) return undefined;
  if (a.country !== CH) return true;
  if (!a.nationality) return undefined;
  return a.nationality !== CH;
}
