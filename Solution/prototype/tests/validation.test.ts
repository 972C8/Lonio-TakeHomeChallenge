// Prototype checks the spec states as text, not as example tables: D-042/D-049 and D-050 (assumptions).

import { describe, expect, it } from 'vitest';
import { emptyAnswers, type Answers } from '../src/model';
import { discardInapplicable, validateStep, visibleSteps } from '../src/questions';

const sent = new Date(Date.UTC(2026, 10, 15));
const about = (x: Partial<Answers>) =>
  validateStep('about', { ...emptyAnswers(), firstName: 'Lena', lastName: 'Meier', ...x }, sent);

describe('dates (D-050)', () => {
  it('accepts a first working day within one year after the questionnaire is sent', () => {
    expect(about({ dateOfBirth: '12.03.1990', firstWorkingDay: '01.03.2027' })).toEqual({});
  });
  it('rejects a first working day more than a year ahead or before it was sent', () => {
    expect(about({ dateOfBirth: '12.03.1990', firstWorkingDay: '01.12.2027' }).firstWorkingDay).toBeDefined();
    expect(about({ dateOfBirth: '12.03.1990', firstWorkingDay: '01.11.2026' }).firstWorkingDay).toBeDefined();
  });
  it('requires an age of 14 to 100 on the first working day', () => {
    expect(about({ dateOfBirth: '01.03.2013', firstWorkingDay: '01.03.2027' })).toEqual({});
    expect(about({ dateOfBirth: '02.03.2013', firstWorkingDay: '01.03.2027' }).dateOfBirth).toBeDefined();
    expect(about({ dateOfBirth: '01.01.1920', firstWorkingDay: '01.03.2027' }).dateOfBirth).toBeDefined();
  });
});

describe('house number (D-042, D-049)', () => {
  const base = { ...emptyAnswers(), street: 'Hof Unterberg', postcode: '8492', town: 'Wila', country: 'Switzerland', canton: 'Zurich' };
  it('is required', () => expect(validateStep('address', base, sent).houseNumber).toBeDefined());
  it("can be replaced by 'no house number'", () => {
    expect(validateStep('address', { ...base, noHouseNumber: true }, sent)).toEqual({});
    expect(discardInapplicable({ ...base, noHouseNumber: true, houseNumber: '5' }).houseNumber).toBeUndefined();
  });
});

describe('steps (D-047, D-040)', () => {
  it('has the eight steps in the decided order for someone living in Germany with children', () => {
    const a: Answers = { ...emptyAnswers(), country: 'Germany', hasChildren: 'yes', civilStatus: 'Single' };
    expect(visibleSteps(a).map((s) => s.key)).toEqual(
      ['about', 'address', 'family', 'crossBorder', 'sourceTax', 'children', 'review']);
  });
  it('skips the source tax details for Liechtenstein residents who return daily', () => {
    const a: Answers = { ...emptyAnswers(), country: 'Liechtenstein', liDailyReturn: 'yes' };
    expect(visibleSteps(a).map((s) => s.key)).not.toContain('sourceTax');
  });
});
