// The questionnaire: steps, questions, when each is asked, validation and the
// "discard answers that no longer apply" step on submission (US-01.5).

import { COUNTRIES, NATIONALITIES } from './countries';
import {
  AGE_STATUSES, CANTONS, CERTIFICATE, CIVIL_STATUSES, CONTRIBUTORS, CUSTODY, DENOMINATIONS,
  type Answers, type Child,
} from './model';
import {
  asked, childAsked, firstWorkingDayInWindow, parseDate, plausibleDateOfBirth, sourceTaxCivilStatus, sourceTaxDetailsNeeded,
} from './rules';

const YES_NO = ['yes', 'no'] as const;

export type Kind = 'text' | 'date' | 'select' | 'radio';
type Label = string | ((a: Answers) => string);

export interface Question {
  id: Exclude<keyof Answers, 'children'>;
  step: StepKey;
  group?: string;
  label: Label;
  hint?: string;
  kind: Kind;
  options?: readonly string[];
  asked: (a: Answers) => boolean;
}

export interface ChildQuestion {
  id: Exclude<keyof Child, 'id'>;
  label: Label;
  kind: 'radio';
  options: readonly string[];
  asked: (c: Child, a: Answers) => boolean;
}

export type StepKey = 'about' | 'address' | 'nationality' | 'family' | 'crossBorder' | 'sourceTax' | 'children' | 'review';

/** The eight steps, in the order fixed by D-047 (US-01.2). */
export const STEPS: { key: StepKey; title: string }[] = [
  { key: 'about', title: 'About you' },
  { key: 'address', title: 'Home address' },
  { key: 'nationality', title: 'Nationality and C permit' },
  { key: 'family', title: 'Civil status and spouse' },
  { key: 'crossBorder', title: 'Cross-border commuting' },
  { key: 'sourceTax', title: 'Source tax details' },
  { key: 'children', title: 'Children' },
  { key: 'review', title: 'Summary and submission' },
];

const always = () => true;
const isMarried = (a: Answers) => sourceTaxCivilStatus(a.civilStatus) === 'married';
const spouse = (a: Answers) =>
  a.civilStatus === 'Registered partnership' ? 'registered partner' : 'spouse';

export const QUESTIONS: Question[] = [
  // Step 1 – US-02.1, US-03.1
  { id: 'firstName', step: 'about', label: 'First name', kind: 'text', asked: always },
  { id: 'lastName', step: 'about', label: 'Last name', kind: 'text', asked: always },
  { id: 'dateOfBirth', step: 'about', label: 'Date of birth', kind: 'date', asked: always },
  {
    id: 'firstWorkingDay', step: 'about', label: 'First working day', kind: 'date', asked: always,
    hint: 'Your contractual start date, also if it falls on a weekend or public holiday.',
  },

  // Step 2 – US-02.2, US-02.3, US-02.4 (the address that applies on the first working day, D-041)
  { id: 'street', step: 'address', label: 'Street', kind: 'text', asked: always },
  { id: 'houseNumber', step: 'address', label: 'House number', kind: 'text', asked: (a) => !a.noHouseNumber },
  { id: 'postcode', step: 'address', label: 'Postcode', kind: 'text', asked: always },
  { id: 'town', step: 'address', label: 'Town', kind: 'text', asked: always },
  {
    id: 'country', step: 'address', label: 'Country', kind: 'select', options: COUNTRIES, asked: always,
    hint: 'The country of your home address on your first working day.',
  },
  { id: 'canton', step: 'address', label: 'Canton', kind: 'select', options: CANTONS, asked: asked.canton },

  // Step 3 – US-05.1
  {
    id: 'nationality', step: 'nationality', label: 'Nationality', kind: 'select', options: NATIONALITIES,
    hint: 'If you hold Swiss citizenship, choose Switzerland, even if you have another nationality too.',
    asked: asked.nationality,
  },
  {
    id: 'cPermit', step: 'nationality', label: 'Do you hold a C permit (permanent residence)?',
    kind: 'radio', options: YES_NO, asked: asked.cPermit,
  },

  // Step 4 – US-04.1, US-04.2, US-05.2
  { id: 'civilStatus', step: 'family', label: 'Civil status', kind: 'select', options: CIVIL_STATUSES, asked: always },
  {
    id: 'spouseDateOfBirth', step: 'family', kind: 'date', asked: asked.spouseDateOfBirth,
    label: (a) => `Your ${spouse(a)}'s date of birth`,
  },
  {
    id: 'spouseNationality', step: 'family', kind: 'select', options: NATIONALITIES, asked: asked.spouseNationality,
    label: (a) => `Your ${spouse(a)}'s nationality`,
    hint: 'Anyone holding Swiss citizenship counts as Swiss: choose Switzerland.',
  },
  {
    id: 'spouseCPermit', step: 'family', kind: 'radio', options: YES_NO, asked: asked.spouseCPermit,
    label: (a) => `Does your ${spouse(a)} hold a C permit (permanent residence)?`,
  },
  {
    id: 'spouseLivesInCH', step: 'family', kind: 'radio', options: YES_NO, asked: asked.spouseLivesInCH,
    label: (a) => `Does your ${spouse(a)} live in Switzerland?`,
  },

  // Step 5 – US-08.2, US-08.3 (Germany)
  {
    id: 'deDailyReturn', step: 'crossBorder', group: 'Living in Germany', kind: 'radio', options: YES_NO,
    asked: asked.deDailyReturn,
    label: 'Do you expect to return daily to your main residence in Germany?',
  },
  {
    id: 'deCertificate', step: 'crossBorder', group: 'Living in Germany', kind: 'radio', options: CERTIFICATE,
    asked: asked.deCertificate,
    label: 'Have you provided a certificate of residence (Ansässigkeitsbescheinigung)?',
    hint: 'The certificate itself goes to HR directly; nothing is uploaded here.',
  },
  {
    id: 'deReasonable', step: 'crossBorder', group: 'Living in Germany', kind: 'radio', options: YES_NO,
    asked: asked.deReasonable,
    label: 'Would a daily return to your home in Germany in principle be reasonable (less than 100 km driving distance)?',
  },
  {
    id: 'deMoreThan60', step: 'crossBorder', group: 'Living in Germany', kind: 'radio', options: YES_NO,
    asked: asked.deMoreThan60,
    label: 'Do you expect more than 60 work-related non-return days in the calendar year?',
  },
  // Step 5 – US-08.4 (Liechtenstein, before the source tax details, D-040)
  {
    id: 'liDailyReturn', step: 'crossBorder', group: 'Living in Liechtenstein', kind: 'radio', options: YES_NO,
    asked: asked.liDailyReturn,
    label: 'Do you expect to return daily to your main residence in Liechtenstein?',
  },
  {
    id: 'liMoreThan45', step: 'crossBorder', group: 'Living in Liechtenstein', kind: 'radio', options: YES_NO,
    asked: asked.liMoreThan45,
    label: 'Do you expect more than 45 work-related non-return days in the calendar year?',
  },
  // Step 6 – US-06.2, US-06.3, US-07.1
  {
    id: 'denomination', step: 'sourceTax', label: 'Your denomination',
    kind: 'radio', options: DENOMINATIONS, asked: asked.denomination,
  },
  {
    id: 'spouseWorks', step: 'sourceTax', kind: 'radio', options: YES_NO,
    asked: asked.spouseWorks,
    label: (a) => `Is your ${spouse(a)} gainfully employed or receiving replacement income?`,
  },
  {
    id: 'hasChildren', step: 'sourceTax', kind: 'radio', options: YES_NO,
    asked: asked.hasChildren,
    label: (a) =>
      isMarried(a)
        ? `Do you or your ${spouse(a)} have biological or adopted children?`
        : 'Do you have biological or adopted children?',
  },
];

export const CHILD_QUESTIONS: ChildQuestion[] = [
  { id: 'ageStatus', kind: 'radio', options: AGE_STATUSES, asked: childAsked.ageStatus, label: 'Is the child a minor, an adult in first education, or neither?' },
  { id: 'inHousehold', kind: 'radio', options: YES_NO, asked: childAsked.inHousehold, label: 'Does the child live in your household?' },
  { id: 'custody', kind: 'radio', options: CUSTODY, asked: childAsked.custody, label: 'Is parental custody shared or sole?' },
  { id: 'commonHousehold', kind: 'radio', options: YES_NO, asked: childAsked.commonHousehold, label: "Do you live in a common household with the child's other parent?" },
  { id: 'sharedCustodyMarried', kind: 'radio', options: YES_NO, asked: childAsked.sharedCustodyMarried, label: 'Is custody shared?' },
  { id: 'parentalCustodySingle', kind: 'radio', options: YES_NO, asked: childAsked.parentalCustodySingle, label: 'Do you have parental custody?' },
  { id: 'alternatingCare', kind: 'radio', options: YES_NO, asked: childAsked.alternatingCare, label: 'Is there alternating care with the other parent?' },
  { id: 'largerContributor', kind: 'radio', options: CONTRIBUTORS, asked: childAsked.largerContributor, label: "Who makes the larger financial contribution to the child's maintenance?" },
  { id: 'moreThan50', kind: 'radio', options: YES_NO, asked: childAsked.moreThan50, label: "Do you mainly (more than 50%) provide the child's maintenance?" },
];

export const labelOf = (q: { label: Label }, a: Answers) => (typeof q.label === 'function' ? q.label(a) : q.label);

export const questionsOf = (step: StepKey, a: Answers) => QUESTIONS.filter((q) => q.step === step && q.asked(a));

/** A step is hidden once the answers so far show that none of its questions apply. */
export function visibleSteps(a: Answers) {
  return STEPS.filter((s) => {
    if (s.key === 'nationality') return !a.country || asked.nationality(a);
    if (s.key === 'crossBorder') return !a.country || a.country === 'Germany' || a.country === 'Liechtenstein';
    if (s.key === 'sourceTax') return sourceTaxDetailsNeeded(a) || !a.country;
    if (s.key === 'children') return asked.children(a);
    return true;
  });
}

// ---------- Validation ----------

export type Errors = Record<string, string>;

const isEmpty = (v: unknown) => v === undefined || (typeof v === 'string' && v.trim() === '');

export function validateStep(step: StepKey, a: Answers, sent: Date = new Date()): Errors {
  const errors: Errors = {};
  for (const q of questionsOf(step, a)) {
    const v = a[q.id];
    if (isEmpty(v)) errors[q.id] = 'Please answer this question.';
    else if (q.kind === 'date' && !parseDate(v as string)) errors[q.id] = 'Please enter a valid date as DD.MM.YYYY.';
  }
  if (step === 'address' && !a.noHouseNumber && isEmpty(a.houseNumber)) {
    errors.houseNumber = "Please enter the house number, or tick 'no house number'.";
  }
  if (step === 'about' && !errors.dateOfBirth && !errors.firstWorkingDay) {
    if (firstWorkingDayInWindow(a.firstWorkingDay, sent) === false)
      errors.firstWorkingDay = 'The first working day must lie within one year from today.';
    else if (plausibleDateOfBirth(a.dateOfBirth, a.firstWorkingDay) === false)
      errors.dateOfBirth = 'Please check the date of birth: you must be between 14 and 100 years old on your first working day.';
  }
  if (step === 'children' && asked.children(a)) {
    if (a.children.length === 0) errors.children = 'Please add each child.';
    for (const c of a.children) {
      for (const q of CHILD_QUESTIONS) {
        if (q.asked(c, a) && isEmpty(c[q.id])) errors[`child.${c.id}.${q.id}`] = 'Please answer this question.';
      }
    }
  }
  return errors;
}

export function validateAll(a: Answers, sent: Date = new Date()): Errors {
  return Object.assign({}, ...STEPS.map((s) => validateStep(s.key, a, sent)));
}

/** Keeps only the answers to questions that apply to the final answers (US-01.5). */
export function discardInapplicable(a: Answers): Answers {
  const out: Answers = { children: [] };
  for (const q of QUESTIONS) {
    if (q.asked(a) && !isEmpty(a[q.id])) (out as unknown as Record<string, unknown>)[q.id] = a[q.id];
  }
  if (a.noHouseNumber) out.noHouseNumber = true;
  if (asked.children(a)) {
    out.children = a.children.map((c) => {
      const kept: Child = { id: c.id };
      for (const q of CHILD_QUESTIONS) if (q.asked(c, a) && c[q.id] !== undefined) (kept as unknown as Record<string, unknown>)[q.id] = c[q.id];
      return kept;
    });
  }
  return out;
}
