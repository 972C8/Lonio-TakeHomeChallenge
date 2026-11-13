"""Shared data contracts between stages.

Every stage reads and writes these models as JSON under build/. Adapters must
return `Unit` and `Fact` objects; everything downstream only knows these types.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field as F


# ---------------------------------------------------------------- sources ---

class Unit(BaseModel):
    """Smallest addressable piece of a source (a speaker turn, a screen line, a calculator node)."""
    id: str                      # e.g. T-031, S05-L07, C-Q03
    source_id: str
    text: str                    # exact text; anchors quote from here
    meta: dict = F(default_factory=dict)  # speaker, file, screen, ...


class Anchor(BaseModel):
    unit_id: str
    quote: str                   # must be an exact substring of the unit's text


FactKind = Literal[
    "field",        # a piece of information some party needs
    "option",       # allowed values of a field
    "format",       # format / validation of a field
    "condition",    # when something is asked / required / shown
    "rule",         # business logic (derivations, eligibility)
    "decision",     # an explicit product/scope decision by the stakeholder
    "exclusion",    # something explicitly out of scope
    "wish",         # nice-to-have, not decided
    "open",         # stakeholder says they don't know / unclear
    "context",      # background, no requirement
]


class Fact(BaseModel):
    id: str = ""                 # assigned by the engine: F-<SRC>-NNN
    source_id: str = ""
    kind: FactKind
    subject: str                 # short snake_case topic, e.g. civil_status
    statement: str               # one atomic, self-contained claim
    anchors: list[Anchor]
    basis: Literal["explicit", "inferred"] = "explicit"
    temporality: Literal["desired", "current_state"] = "desired"
    supersedes: list[str] = F(default_factory=list)   # local ids within the same source
    local_id: str = ""           # id the extractor used (for supersedes)
    # filled by checks
    anchor_ok: Optional[bool] = None
    judge: Optional[Literal["supported", "partial", "unsupported"]] = None
    judge_note: str = ""
    superseded_by: list[str] = F(default_factory=list)


# ------------------------------------------------------------------- spec ---

class Option(BaseModel):
    value: str
    label: str


class Consumer(BaseModel):
    party: str                   # consumer id from the profile, e.g. pension_fund
    purpose: str                 # why they need it
    target: str = ""             # name of the field on their side, e.g. "Spouse's date of birth"


class FieldReq(BaseModel):
    id: str                      # snake_case, stable across runs
    step: str                    # step id
    order: int                   # order within step
    label: str                   # UI label
    question: str                # wording shown to the employee
    help_text: str = ""
    type: Literal["text", "date", "enum", "boolean", "country", "integer", "file"]
    format: str = ""             # e.g. DD.MM.YYYY, ISO country code
    options: list[Option] = F(default_factory=list)
    validation: list[str] = F(default_factory=list)
    ask_when: str = "true"       # condition expression (see conventions)
    required_when: str = "true"  # condition expression, evaluated only when asked
    consumers: list[Consumer]
    source_refs: list[str]       # fact ids / decision ids
    status: Literal["confirmed", "inferred", "decision"] = "confirmed"
    notes: str = ""
    depends_on: list[str] = F(default_factory=list)   # computed by the engine


class Rule(BaseModel):
    """A derived value. Never asked; computed from answers."""
    id: str
    description: str
    expression: str              # expression over field / rule ids
    output_type: Literal["boolean", "date", "text", "enum"]
    consumers: list[Consumer] = F(default_factory=list)
    source_refs: list[str]
    status: Literal["confirmed", "inferred", "decision"] = "confirmed"
    depends_on: list[str] = F(default_factory=list)


class Step(BaseModel):
    id: str
    order: int
    title: str
    purpose: str
    ask_when: str = "true"
    intro_text: str = ""         # text shown at the top of the step


class Notice(BaseModel):
    """Non-data content shown to the employee (reminders, hints)."""
    id: str
    step: str
    text: str
    show_when: str = "true"
    source_refs: list[str]


class OpenQuestion(BaseModel):
    id: str
    question: str
    why_it_matters: str
    options: list[str] = F(default_factory=list)
    recommendation: str = ""
    affects: list[str] = F(default_factory=list)   # field / rule ids
    source_refs: list[str]
    blocking: bool = False


class Exclusion(BaseModel):
    id: str
    item: str
    reason: str
    source_refs: list[str]


class Spec(BaseModel):
    steps: list[Step]
    fields: list[FieldReq]
    rules: list[Rule] = F(default_factory=list)
    notices: list[Notice] = F(default_factory=list)
    open_questions: list[OpenQuestion] = F(default_factory=list)
    exclusions: list[Exclusion] = F(default_factory=list)


# -------------------------------------------------------------- decisions ---

class Decision(BaseModel):
    id: str                      # D-001
    action: Literal["override", "add", "exclude", "accept", "reject", "resolve"]
    target: str                  # field.<id>.<attr> | field.<id> | rule.<id>... | fact.<id> | open.<id>
    value: object = None
    rationale: str
    by: str = "product"
    evidence: list[str] = F(default_factory=list)          # unit ids the decision is based on/overrides
    evidence_hash: str = ""      # fingerprint of evidence texts at decision time


# ----------------------------------------------------------------- checks ---

class Finding(BaseModel):
    check: str
    severity: Literal["error", "warning", "info"]
    target: str = ""
    message: str
