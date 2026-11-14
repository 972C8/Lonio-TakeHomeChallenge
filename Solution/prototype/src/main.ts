import './style.css';
import { emptyAnswers, type Answers, type Child } from './model';
import {
  CHILD_QUESTIONS, STEPS, labelOf, questionsOf, validateAll, validateStep, visibleSteps,
  type ChildQuestion, type Errors, type Question, type StepKey,
} from './questions';
import { buildRecord, type SubmissionRecord } from './record';
import { permitReminder, type SourceTaxResult } from './rules';

// HR provides the final wording (AC-08.1.3); this is a placeholder with the same purpose.
const PERMIT_REMINDER_TEXT = 'Please bring your permit with you on your first working day.';

interface State {
  answers: Answers;
  step: StepKey;
  errors: Errors;
  submitted?: SubmissionRecord;
}

const STORAGE_KEY = 'lonio-onboarding-prototype';

function load(): State {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null');
    if (saved?.answers) return { answers: saved.answers, step: saved.step ?? 'personal', errors: {}, submitted: saved.submitted };
  } catch { /* ignore */ }
  return { answers: emptyAnswers(), step: 'personal', errors: {} };
}

let state = load();

function save() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ answers: state.answers, step: state.step, submitted: state.submitted }));
  } catch { /* storage unavailable: keep working in memory */ }
}

// ---------- Rendering ----------

const esc = (s: unknown) =>
  String(s ?? '').replace(/[&<>"']/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch]!);

const root = document.getElementById('app')!;

function field(id: string, label: string, control: string, error?: string, hint?: string) {
  return `<div class="field${error ? ' has-error' : ''}" id="field-${esc(id)}">
    <div class="label">${esc(label)}</div>
    ${hint ? `<div class="hint">${esc(hint)}</div>` : ''}
    ${control}
    ${error ? `<div class="error">${esc(error)}</div>` : ''}
  </div>`;
}

function control(name: string, kind: Question['kind'], value: string | undefined, options: readonly string[] = [], label = '') {
  const v = value ?? '';
  switch (kind) {
    case 'text':
      return `<input type="text" id="in-${esc(name)}" data-q="${esc(name)}" value="${esc(v)}" aria-label="${esc(label)}" />`;
    case 'date':
      return `<input type="text" id="in-${esc(name)}" data-q="${esc(name)}" value="${esc(v)}" placeholder="DD.MM.YYYY" inputmode="numeric" aria-label="${esc(label)}" />`;
    case 'select':
      return `<select id="in-${esc(name)}" data-q="${esc(name)}" aria-label="${esc(label)}">
        <option value="">Please choose…</option>
        ${options.map((o) => `<option${o === v ? ' selected' : ''}>${esc(o)}</option>`).join('')}
      </select>`;
    case 'radio':
      return `<div class="radios" role="radiogroup" aria-label="${esc(label)}">${options
        .map((o, i) => `<label><input type="radio" id="in-${esc(name)}-${i}" name="${esc(name)}" data-q="${esc(name)}" value="${esc(o)}"${o === v ? ' checked' : ''} /> ${esc(o)}</label>`)
        .join('')}</div>`;
  }
}

function renderQuestion(q: Question, a: Answers) {
  const label = labelOf(q, a);
  return field(q.id, label, control(q.id, q.kind, a[q.id] as string | undefined, q.options, label), state.errors[q.id], q.hint);
}

function renderChild(c: Child, index: number, a: Answers) {
  const qs = CHILD_QUESTIONS.filter((q) => q.asked(c, a));
  const body = qs
    .map((q: ChildQuestion) => {
      const key = `child.${c.id}.${q.id}`;
      const label = labelOf(q, a);
      return field(key, label, control(key, q.kind, c[q.id], q.options, label), state.errors[key]);
    })
    .join('');
  return `<fieldset class="child">
    <legend>Child ${index + 1}</legend>
    ${body}
    <button type="button" class="link" data-action="remove-child" data-child="${esc(c.id)}">Remove this child</button>
  </fieldset>`;
}

function renderStepForm(step: StepKey) {
  const a = state.answers;
  let html = '';
  let group: string | undefined;
  for (const q of questionsOf(step, a)) {
    if (q.group !== group) {
      group = q.group;
      if (group) html += `<h3>${esc(group)}</h3>`;
    }
    html += renderQuestion(q, a);
    if (q.id === 'hasChildren' && a.hasChildren === 'yes') {
      html += a.children.map((c, i) => renderChild(c, i, a)).join('');
      if (state.errors.children) html += `<div class="error">${esc(state.errors.children)}</div>`;
      html += `<button type="button" class="secondary" data-action="add-child">Add a child</button>`;
    }
  }
  return html;
}

function summaryValue(q: Question, a: Answers) {
  return esc(a[q.id] as string);
}

function renderReview() {
  const a = state.answers;
  const sections = visibleSteps(a)
    .filter((s) => s.key !== 'review')
    .map((s) => {
      const rows = questionsOf(s.key, a)
        .map((q) => `<tr><th>${esc(labelOf(q, a))}</th><td>${summaryValue(q, a)}</td></tr>`)
        .join('');
      const kids =
        s.key === 'sourceTax' && a.hasChildren === 'yes'
          ? a.children
              .map(
                (c, i) =>
                  `<tr><th colspan="2" class="sub">Child ${i + 1}</th></tr>` +
                  CHILD_QUESTIONS.filter((q) => q.asked(c, a))
                    .map((q) => `<tr><th>${esc(labelOf(q, a))}</th><td>${esc(c[q.id])}</td></tr>`)
                    .join(''),
              )
              .join('')
          : '';
      return `<section class="summary">
        <div class="summary-head"><h3>${esc(s.title)}</h3><button type="button" class="link" data-action="goto" data-step="${s.key}">Edit</button></div>
        <table>${rows}${kids}</table>
      </section>`;
    })
    .join('');
  const reminder = permitReminder(a)
    ? `<div class="notice" role="note"><strong>Reminder:</strong> ${esc(PERMIT_REMINDER_TEXT)}</div>`
    : '';
  const hasErrors = Object.keys(state.errors).length > 0;
  return `${sections}${reminder}${hasErrors ? '<div class="error">Some answers are missing. Please complete the highlighted steps.</div>' : ''}`;
}

function describeResult(r: SourceTaxResult | undefined) {
  if (!r) return '–';
  if (r.kind === 'none') return 'Not subject to source tax (no source tax result)';
  if (r.kind === 'liechtenstein-no-liability') return `${r.text} <span class="flag">flag for HR</span>`;
  return `Tariff code <strong>${esc(r.code)}</strong>${r.subjectToDTA ? ', subject to the double taxation agreement' : ''}`;
}

function renderSubmitted(rec: SubmissionRecord) {
  const a = rec.answers;
  const d = rec.derived;
  const row = (k: string, v: string | undefined, raw = false) =>
    v === undefined || v === '' ? '' : `<tr><th>${esc(k)}</th><td>${raw ? v : esc(v)}</td></tr>`;
  const address = [`${a.street ?? ''} ${a.houseNumber ?? ''}`.trim(), `${a.postcode ?? ''} ${a.town ?? ''}`.trim(), a.country]
    .filter(Boolean)
    .join(', ');
  return `<div class="card">
    <h2>Thank you, your answers have been submitted.</h2>
    <p>You can no longer change them here. If your first working day moves, HR will update it.</p>
    ${d.permitReminderShown ? `<div class="notice"><strong>Reminder:</strong> ${esc(PERMIT_REMINDER_TEXT)}</div>` : ''}
  </div>
  <div class="card proto">
    <h2>Recorded on submission</h2>
    <p class="hint">Prototype view only: shows what Lonio records. Transmission to the parties and HR screens are out of scope.</p>
    <h3>Pension fund</h3>
    <table>
      ${row('First name', a.firstName)}${row('Last name', a.lastName)}${row('Date of birth', a.dateOfBirth)}
      ${row('Canton', a.canton)}${row('Civil status', d.pensionFundCivilStatus)}
      ${row("Spouse's / registered partner's date of birth", a.spouseDateOfBirth)}
      ${row('Insurance start date', d.insuranceStartDate)}
    </table>
    <h3>HR</h3>
    <table>
      ${row('Home address', address)}${row('First working day', a.firstWorkingDay)}
      ${row('Nationality', a.nationality)}${row('Holds a C permit', a.cPermit)}
      ${row('Source tax result', describeResult(d.sourceTaxResult), true)}
    </table>
    <details><summary>All recorded data (JSON)</summary><pre>${esc(JSON.stringify(rec, null, 2))}</pre></details>
  </div>
  <p><button type="button" class="link" data-action="reset">Start a new questionnaire (prototype reset)</button></p>`;
}

function render() {
  const focusedId = (document.activeElement as HTMLElement | null)?.id;
  if (state.submitted) {
    root.innerHTML = `<header><h1>Welcome to Muster AG</h1></header>${renderSubmitted(state.submitted)}`;
    return;
  }
  const steps = visibleSteps(state.answers);
  if (!steps.some((s) => s.key === state.step)) state.step = nearestStep(state.step, steps);
  const idx = steps.findIndex((s) => s.key === state.step);
  const current = steps[idx];
  const stepErrors = (k: StepKey) => Object.keys(validateStep(k, state.answers)).length > 0;
  const nav = steps
    .map((s, i) => {
      const cls = [s.key === state.step ? 'current' : '', Object.keys(state.errors).length && stepErrors(s.key) ? 'invalid' : '']
        .filter(Boolean)
        .join(' ');
      return `<li class="${cls}"><button type="button" class="link" data-action="goto" data-step="${s.key}">${i + 1}. ${esc(s.title)}</button></li>`;
    })
    .join('');
  root.innerHTML = `
    <header>
      <h1>Welcome to Muster AG</h1>
      <p class="hint">Your onboarding questionnaire. We only ask what the pension fund, source tax and HR need from you.</p>
    </header>
    <ol class="steps">${nav}</ol>
    <form class="card" novalidate>
      <h2>Step ${idx + 1} of ${steps.length}: ${esc(current.title)}</h2>
      ${current.key === 'review' ? renderReview() : renderStepForm(current.key) || '<p class="hint">Please answer the earlier steps first.</p>'}
      <div class="actions">
        ${idx > 0 ? '<button type="button" class="secondary" data-action="back">Back</button>' : '<span></span>'}
        ${current.key === 'review'
          ? '<button type="button" data-action="submit">Submit</button>'
          : '<button type="button" data-action="next">Next</button>'}
      </div>
    </form>`;
  if (focusedId) document.getElementById(focusedId)?.focus();
}

/** If the current step disappeared (e.g. no more source tax questions), go to the next one that exists. */
function nearestStep(step: StepKey, steps: { key: StepKey }[]): StepKey {
  const order = STEPS.map((s) => s.key);
  const from = order.indexOf(step);
  return steps.find((s) => order.indexOf(s.key) > from)?.key ?? 'review';
}

// ---------- Events ----------

function setAnswer(target: HTMLInputElement | HTMLSelectElement) {
  const key = target.dataset.q!;
  const value = target.value === '' ? undefined : target.value;
  if (key.startsWith('child.')) {
    const [, childId, q] = key.split('.');
    const child = state.answers.children.find((c) => c.id === childId);
    if (child) (child as unknown as Record<string, unknown>)[q] = value;
  } else {
    (state.answers as unknown as Record<string, unknown>)[key] = value;
  }
  delete state.errors[key];
  save();
}

root.addEventListener('input', (e) => {
  const t = e.target as HTMLInputElement;
  if (t.dataset.q && t.type === 'text') setAnswer(t);
});

root.addEventListener('change', (e) => {
  const t = e.target as HTMLInputElement | HTMLSelectElement;
  if (!t.dataset.q || (t as HTMLInputElement).type === 'text') return;
  setAnswer(t);
  render(); // follow-up questions may appear or disappear
});

function go(step: StepKey) {
  state.step = step;
  save();
  render();
  window.scrollTo({ top: 0 });
}

root.addEventListener('click', (e) => {
  const btn = (e.target as HTMLElement).closest<HTMLElement>('[data-action]');
  if (!btn) return;
  const steps = visibleSteps(state.answers);
  const idx = steps.findIndex((s) => s.key === state.step);
  switch (btn.dataset.action) {
    case 'goto':
      go(btn.dataset.step as StepKey);
      break;
    case 'back':
      go(steps[Math.max(0, idx - 1)].key);
      break;
    case 'next': {
      const errors = validateStep(state.step, state.answers);
      state.errors = errors;
      if (Object.keys(errors).length) {
        render();
        root.querySelector('.has-error input, .has-error select')?.scrollIntoView({ block: 'center' });
        return;
      }
      go(steps[idx + 1].key);
      break;
    }
    case 'submit': {
      const errors = validateAll(state.answers);
      state.errors = errors;
      if (Object.keys(errors).length) {
        render();
        return;
      }
      state.submitted = buildRecord(state.answers);
      save();
      render();
      window.scrollTo({ top: 0 });
      break;
    }
    case 'add-child':
      state.answers.children.push({ id: Math.random().toString(36).slice(2, 10) });
      delete state.errors.children;
      save();
      render();
      break;
    case 'remove-child':
      state.answers.children = state.answers.children.filter((c) => c.id !== btn.dataset.child);
      save();
      render();
      break;
    case 'reset':
      state = { answers: emptyAnswers(), step: 'personal', errors: {} };
      save();
      render();
      break;
  }
});

render();
