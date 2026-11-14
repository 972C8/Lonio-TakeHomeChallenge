// The questionnaire: steps, questions, when each is asked, validation and the
// "discard answers that no longer apply" step on submission (US-08.2).

import { COUNTRIES } from './countries';
import {
  AGE_STATUSES, CANTONS, CERTIFICATE, CIVIL_STATUSES, CONTRIBUTORS, CUSTODY, DENOMINATIONS,
  type Answers, type Child,
} from './model';
import { asked, childAsked, parseDate, sourceTaxCivilStatus, subjectToSourceTax } from './rules';

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

export type StepKey = 'personal' | 'address' | 'nationality' | 'employment' | 'family' | 'sourceTax' | 'review';

export const STEPS: { key: StepKey; title: string }[] = [
  { key: 'personal', title: 'Personal details' },
  { key: 'address', title: 'Home address' },
  { key: 'nationality', title: 'Nationality and permit' },
  { key: 'employment', title: 'Employment' },
  { key: 'family', title: 'Family' },
  { key: 'sourceTax', title: 'Source tax' },
  { key: 'review', title: 'Review and submit' },
];

const always = () => true;
const isMarried = (a: Answers) => sourceTaxCivilStatus(a.civilStatus) === 'married';
const spouse = (a: Answers) =>
  a.civilStatus === 'Registered partnership' ? 'registered partner' : 'spouse';

export const QUESTIONS: Question[] = [
  // Step 1 – US-01.1
  { id: 'firstName', step: 'personal', label: 'First name', kind: 'text', asked: always },
  { id: 'lastName', step: 'personal', label: 'Last name', kind: 'text', asked: always },
  { id: 'dateOfBirth', step: 'personal', label: 'Date of birth', kind: 'date', asked: always },

  // Step 2 – US-01.2, US-01.3, US-01.4
  { id: 'street', step: 'address', label: 'Street', kind: 'text', asked: always },
  { id: 'houseNumber', step: 'address', label: 'House number', kind: 'text', asked: always },
  { id: 'postcode', step: 'address', label: 'Postcode', kind: 'text', asked: always },
  { id: 'town', step: 'address', label: 'Town', kind: 'text', asked: always },
  { id: 'country', step: 'address', label: 'Country', kind: 'select', options: COUNTRIES, asked: always },
  { id: 'canton', step: 'address', label: 'Canton', kind: 'select', options: CANTONS, asked: asked.canton },

  // Step 3 – US-04.1
  {
    id: 'nationality', step: 'nationality', label: 'Nationality', kind: 'select', options: COUNTRIES,
    hint: 'If you hold Swiss citizenship, choose Switzerland, even if you have another nationality too.',
    asked: asked.nationality,
  },
  {
    id: 'cPermit', step: 'nationality', label: 'Do you hold a C permit (permanent residence)?',
    kind: 'radio', options: YES_NO, asked: asked.cPermit,
  },

  // Step 4 – US-02.1
  { id: 'firstWorkingDay', step: 'employment', label: 'First working day', kind: 'date', asked: always },

  // Step 5 – US-03.1, US-03.2, US-04.2
  { id: 'civilStatus', step: 'family', label: 'Civil status', kind: 'select', options: CIVIL_STATUSES, asked: always },
  {
    id: 'spouseDateOfBirth', step: 'family', kind: 'date', asked: asked.spouseDateOfBirth,
    label: (a) => `Your ${spouse(a)}'s date of birth`,
  },
  {
    id: 'spouseCountry', step: 'family', kind: 'select', options: COUNTRIES, asked: asked.spouseCountry,
    label: (a) => `In which country does your ${spouse(a)} live?`,
  },
  {
    id: 'spouseNationality', step: 'family', kind: 'select', options: COUNTRIES, asked: asked.spouseNationality,
    label: (a) => `Your ${spouse(a)}'s nationality`,
    hint: 'Anyone holding Swiss citizenship counts as Swiss: choose Switzerland.',
  },
  {
    id: 'spouseCPermit', step: 'family', kind: 'radio', options: YES_NO, asked: asked.spouseCPermit,
    label: (a) => `Does your ${spouse(a)} hold a C permit (permanent residence)?`,
  },

  // Step 6 – US-05.3, US-05.4
  {
    id: 'denomination', step: 'sourceTax', label: 'Your denomination',
    kind: 'radio', options: DENOMINATIONS, asked: asked.denomination,
  },
  {
    id: 'spouseWorks', step: 'sourceTax', kind: 'radio', options: YES_NO,
    asked: asked.spouseWorks,
    label: (a) => `Is your ${spouse(a)} gainfully employed or receiving replacement income?`,
  },
  // Step 6 – US-06.1 (per-child questions below)
  {
    id: 'hasChildren', step: 'sourceTax', group: 'Children', kind: 'radio', options: YES_NO,
    asked: asked.hasChildren,
    label: (a) =>
      isMarried(a)
        ? `Do you or your ${spouse(a)} have biological or adopted children?`
        : 'Do you have biological or adopted children?',
  },
  // Step 6 – US-07.2 (Germany)
  {
    id: 'deDailyReturn', step: 'sourceTax', group: 'Living in Germany', kind: 'radio', options: YES_NO,
    asked: asked.deDailyReturn,
    label: 'Do you expect to return daily to your main residence in Germany?',
  },
  {
    id: 'deCertificate', step: 'sourceTax', group: 'Living in Germany', kind: 'radio', options: CERTIFICATE,
    asked: asked.deCertificate,
    label: 'Have you provided a certificate of residence (Ansässigkeitsbescheinigung)?',
    hint: 'The certificate itself goes to HR directly; nothing is uploaded here.',
  },
  {
    id: 'deReasonable', step: 'sourceTax', group: 'Living in Germany', kind: 'radio', options: YES_NO,
    asked: asked.deReasonable,
    label: 'Would a daily return to your home in Germany in principle be reasonable (less than 100 km driving distance)?',
  },
  {
    id: 'deMoreThan60', step: 'sourceTax', group: 'Living in Germany', kind: 'radio', options: YES_NO,
    asked: asked.deMoreThan60,
    label: 'Do you expect more than 60 work-related non-return days in the calendar year?',
  },
  // Step 6 – US-07.3 (Liechtenstein)
  {
    id: 'liDailyReturn', step: 'sourceTax', group: 'Living in Liechtenstein', kind: 'radio', options: YES_NO,
    asked: asked.liDailyReturn,
    label: 'Do you expect to return daily to your main residence in Liechtenstein?',
  },
  {
    id: 'liMoreThan45', step: 'sourceTax', group: 'Living in Liechtenstein', kind: 'radio', options: YES_NO,
    asked: asked.liMoreThan45,
    label: 'Do you expect more than 45 work-related non-return days in the calendar year?',
  },
];

export const CHILD_QUESTIONS: ChildQuestion[] = [
  { id: 'ageStatus', kind: 'radio', options: AGE_STATUSES, asked: childAsked.ageStatus, label: 'Is the child a minor, of age and in first education, or neither?' },
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
    if (s.key === 'sourceTax') return subjectToSourceTax(a) !== false;
    return true;
  });
}

// ---------- Validation ----------

export type Errors = Record<string, string>;

const isEmpty = (v: unknown) => v === undefined || (typeof v === 'string' && v.trim() === '');

export function validateStep(step: StepKey, a: Answers): Errors {
  const errors: Errors = {};
  for (const q of questionsOf(step, a)) {
    const v = a[q.id];
    if (isEmpty(v)) errors[q.id] = 'Please answer this question.';
    else if (q.kind === 'date' && !parseDate(v as string)) errors[q.id] = 'Please enter a valid date as DD.MM.YYYY.';
  }
  if (step === 'sourceTax' && asked.children(a)) {
    if (a.children.length === 0) errors.children = 'Please add each child.';
    for (const c of a.children) {
      for (const q of CHILD_QUESTIONS) {
        if (q.asked(c, a) && isEmpty(c[q.id])) errors[`child.${c.id}.${q.id}`] = 'Please answer this question.';
      }
    }
  }
  return errors;
}

export function validateAll(a: Answers): Errors {
  return Object.assign({}, ...STEPS.map((s) => validateStep(s.key, a)));
}

/** Keeps only the answers to questions that apply to the final answers (US-08.2, AC-08.2.2). */
export function discardInapplicable(a: Answers): Answers {
  const out: Answers = { children: [] };
  for (const q of QUESTIONS) {
    if (q.asked(a) && !isEmpty(a[q.id])) (out as unknown as Record<string, unknown>)[q.id] = a[q.id];
  }
  if (asked.children(a)) {
    out.children = a.children.map((c) => {
      const kept: Child = { id: c.id };
      for (const q of CHILD_QUESTIONS) if (q.asked(c, a) && c[q.id] !== undefined) (kept as unknown as Record<string, unknown>)[q.id] = c[q.id];
      return kept;
    });
  }
  return out;
}
