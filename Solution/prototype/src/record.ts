// What is recorded when the employee submits (only applicable answers + derived values).

import type { Answers } from './model';
import { discardInapplicable } from './questions';
import {
  childResult, insuranceStartDate, pensionFundCivilStatus, permitReminder, residence,
  sourceTaxCivilStatus, sourceTaxResult, subjectToSourceTax, type ChildResult, type SourceTaxResult,
} from './rules';

export interface SubmissionRecord {
  submittedAt: string;
  answers: Answers;
  derived: {
    insuranceStartDate?: string;
    pensionFundCivilStatus?: string;
    sourceTaxCivilStatus?: string;
    residenceForSourceTax?: string;
    subjectToSourceTax?: boolean;
    childResults: { childId: string; result?: ChildResult }[];
    sourceTaxResult?: SourceTaxResult;
    permitReminderShown?: boolean;
  };
}

export function buildRecord(raw: Answers, now = new Date()): SubmissionRecord {
  const a = discardInapplicable(raw);
  return {
    submittedAt: now.toISOString(),
    answers: a,
    derived: {
      insuranceStartDate: insuranceStartDate(a.firstWorkingDay),
      pensionFundCivilStatus: pensionFundCivilStatus(a.civilStatus),
      sourceTaxCivilStatus: sourceTaxCivilStatus(a.civilStatus),
      residenceForSourceTax: residence(a.country),
      subjectToSourceTax: subjectToSourceTax(a),
      childResults: a.children.map((c) => ({ childId: c.id, result: childResult(c, a) })),
      sourceTaxResult: sourceTaxResult(a),
      permitReminderShown: permitReminder(a),
    },
  };
}
