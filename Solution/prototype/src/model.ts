// Answer vocabulary, worded as in the spec (G-10: English names, "yes"/"no", DD.MM.YYYY).

export type YesNo = 'yes' | 'no';

export const CIVIL_STATUSES = [
  'Single',
  'Married',
  'Divorced',
  'Widowed',
  'Registered partnership',
  'Separated',
] as const;
export type CivilStatus = (typeof CIVIL_STATUSES)[number];

export const AGE_STATUSES = ['Minor', 'Adult in first education', 'Neither'] as const;
export type AgeStatus = (typeof AGE_STATUSES)[number];

export const CUSTODY = ['Shared custody', 'Sole custody'] as const;
export type Custody = (typeof CUSTODY)[number];

export const CONTRIBUTORS = ['Myself', 'Other parent'] as const;
export type Contributor = (typeof CONTRIBUTORS)[number];

export const DENOMINATIONS = [
  'Roman Catholic, Christ Catholic or Evangelical Reformed',
  'None or other',
] as const;
export type Denomination = (typeof DENOMINATIONS)[number];

export const CERTIFICATE = ['yes', 'no', 'not yet'] as const;
export type Certificate = (typeof CERTIFICATE)[number];

export const CANTONS = [
  'Aargau', 'Appenzell Ausserrhoden', 'Appenzell Innerrhoden', 'Basel-Landschaft', 'Basel-Stadt',
  'Bern', 'Fribourg', 'Geneva', 'Glarus', 'Graubünden', 'Jura', 'Lucerne', 'Neuchâtel', 'Nidwalden',
  'Obwalden', 'Schaffhausen', 'Schwyz', 'Solothurn', 'St. Gallen', 'Thurgau', 'Ticino', 'Uri',
  'Valais', 'Vaud', 'Zug', 'Zurich',
] as const;

/** One block of questions per child (US-07.2 to US-07.5). */
export interface Child {
  id: string;
  ageStatus?: AgeStatus;
  inHousehold?: YesNo;
  custody?: Custody; // minor child in the household
  commonHousehold?: YesNo; // common household with the other parent
  sharedCustodyMarried?: YesNo; // minor child not in household, married or registered partnership: shared custody?
  parentalCustodySingle?: YesNo; // minor child not in household, otherwise: parental care?
  alternatingCare?: YesNo;
  largerContributor?: Contributor;
  moreThan50?: YesNo; // employee covers more than 50% of maintenance
}

/** Everything the employee can answer. Values may be stale while moving back and forth (AC-08.2.1). */
export interface Answers {
  // Step 1 – about you (D-047)
  firstName?: string;
  lastName?: string;
  dateOfBirth?: string;
  firstWorkingDay?: string;
  // Step 2 – home address
  street?: string;
  houseNumber?: string;
  noHouseNumber?: boolean; // 'no house number' instead of a number (D-042, D-049)
  postcode?: string;
  town?: string;
  country?: string;
  canton?: string;
  // Step 3 – nationality and permit
  nationality?: string;
  cPermit?: YesNo;
  // Step 4 – civil status and spouse
  civilStatus?: CivilStatus;
  spouseDateOfBirth?: string;
  spouseNationality?: string;
  spouseCPermit?: YesNo;
  spouseLivesInCH?: YesNo; // asked as yes/no, not as a country (D-050)
  // Step 5 – cross-border commuting
  deDailyReturn?: YesNo;
  deCertificate?: Certificate;
  deReasonable?: YesNo;
  deMoreThan60?: YesNo;
  liDailyReturn?: YesNo;
  liMoreThan45?: YesNo;
  // Step 6 – source tax details
  denomination?: Denomination;
  spouseWorks?: YesNo;
  hasChildren?: YesNo;
  // Step 7 – children
  children: Child[];
}

export const emptyAnswers = (): Answers => ({ children: [] });
