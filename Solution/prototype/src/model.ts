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

export const AGE_STATUSES = ['Minor', 'Of age and in first education', 'Neither'] as const;
export type AgeStatus = (typeof AGE_STATUSES)[number];

export const CUSTODY = ['Shared custody', 'Sole custody'] as const;
export type Custody = (typeof CUSTODY)[number];

export const CONTRIBUTORS = ['The employee', 'The other parent'] as const;
export type Contributor = (typeof CONTRIBUTORS)[number];

export const DENOMINATIONS = [
  'Roman Catholic, Christian Catholic or Evangelical Reformed',
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

/** One block of questions per child (US-06.1 to US-06.5). */
export interface Child {
  id: string;
  ageStatus?: AgeStatus;
  inHousehold?: YesNo;
  custody?: Custody; // minor child in the household
  commonHousehold?: YesNo; // common household with the other parent
  sharedCustodyMarried?: YesNo; // minor child not in household, employee counts as married
  parentalCustodySingle?: YesNo; // minor child not in household, employee counts as single
  alternatingCare?: YesNo;
  largerContributor?: Contributor;
  moreThan50?: YesNo; // employee covers more than 50% of maintenance
}

/** Everything the employee can answer. Values may be stale while moving back and forth (AC-08.2.1). */
export interface Answers {
  // Step 1 – personal details
  firstName?: string;
  lastName?: string;
  dateOfBirth?: string;
  // Step 2 – home address
  street?: string;
  houseNumber?: string;
  postcode?: string;
  town?: string;
  country?: string;
  canton?: string;
  // Step 3 – nationality and permit
  nationality?: string;
  cPermit?: YesNo;
  // Step 4 – employment
  firstWorkingDay?: string;
  // Step 5 – family
  civilStatus?: CivilStatus;
  spouseDateOfBirth?: string;
  spouseCountry?: string;
  spouseNationality?: string;
  spouseCPermit?: YesNo;
  // Step 6 – source tax
  denomination?: Denomination;
  spouseWorks?: YesNo;
  hasChildren?: YesNo;
  children: Child[];
  deDailyReturn?: YesNo;
  deCertificate?: Certificate;
  deReasonable?: YesNo;
  deMoreThan60?: YesNo;
  liDailyReturn?: YesNo;
  liMoreThan45?: YesNo;
}

export const emptyAnswers = (): Answers => ({ children: [] });
