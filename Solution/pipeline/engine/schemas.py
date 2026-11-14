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


# ---------------------------------------------------------- knowledge ---
# What we learned, in business language. Generic across features.
# `*_expr` / `expression` are an INTERNAL formalisation used only by the
# pipeline to verify examples; they are never rendered into the feature specs.

class Need(BaseModel):
    stakeholder: str             # stakeholder id from the profile
    purpose: str                 # why they need it, in business terms


class InfoItem(BaseModel):
    """A piece of information the process needs (asked, provided or produced)."""
    id: str                      # stable snake_case id
    name: str                    # business name
    description: str             # what exactly is needed, in business terms
    form: str = ""               # the form the SOURCES require (e.g. "date as DD.MM.YYYY", "full postal address"), else ""
    allowed_values: list[str] = F(default_factory=list)   # business values, if the sources define a closed list
    asked_when: str              # business-language condition, "Always" if unconditional
    required_when: str           # business-language: when it may not be left empty / when it may
    asked_when_expr: str = "true"     # internal
    required_when_expr: str = "true"  # internal
    needed_by: list[Need]
    source_refs: list[str]
    status: Literal["confirmed", "inferred", "decision"] = "confirmed"
    notes: str = ""
    depends_on: list[str] = F(default_factory=list)   # computed by the engine


class DecisionRow(BaseModel):
    when: list[str]              # one cell per input, business language ("lives abroad", "any")
    then: str
    source_refs: list[str] = F(default_factory=list)


class BusinessRule(BaseModel):
    id: str
    name: str
    statement: str               # the rule in plain business language
    inputs: list[str] = F(default_factory=list)       # column headers of the decision table (business names)
    table: list[DecisionRow] = F(default_factory=list)
    expression: str = ""         # internal formalisation over item / rule ids
    source_refs: list[str]
    status: Literal["confirmed", "inferred", "decision"] = "confirmed"
    depends_on: list[str] = F(default_factory=list)


class OpenQuestion(BaseModel):
    id: str
    question: str
    why_it_matters: str
    options: list[str] = F(default_factory=list)
    recommendation: str = ""
    affects: list[str] = F(default_factory=list)
    source_refs: list[str] = F(default_factory=list)
    blocking: bool = False


class Exclusion(BaseModel):
    id: str
    item: str
    reason: str
    source_refs: list[str]


class KnowledgeModel(BaseModel):
    items: list[InfoItem]
    rules: list[BusinessRule] = F(default_factory=list)
    open_questions: list[OpenQuestion] = F(default_factory=list)
    exclusions: list[Exclusion] = F(default_factory=list)


# -------------------------------------------------------- feature specs ---

class ExampleValue(BaseModel):
    item: str                    # info item id
    value: str                   # business value as the examples are written


class Expectation(BaseModel):
    target: str                  # info item id or business rule id
    expect: str                  # item: asked | not asked | required | optional ; rule: its value ("yes", "no", "01.04.2026"...)


class Example(BaseModel):
    name: str                    # e.g. "Julia (T-021)" - real cases first
    given: list[ExampleValue]
    then: list[Expectation]
    source_refs: list[str] = F(default_factory=list)
    illustrative: bool = False   # true if not a real case from a source


class AcceptanceCriterion(BaseModel):
    id: str                      # AC-03.1
    title: str
    given: str
    when: str
    then: str
    examples: list[Example] = F(default_factory=list)
    source_refs: list[str]


class Story(BaseModel):
    id: str                      # US-03
    title: str
    as_a: str                    # stakeholder id
    i_want: str
    so_that: str
    priority: Literal["P1", "P2", "P3"]
    priority_reason: str
    acceptance_criteria: list[AcceptanceCriterion]
    items: list[str] = F(default_factory=list)       # info items this story covers
    rules: list[str] = F(default_factory=list)       # business rules this story covers
    source_refs: list[str]
    status: Literal["confirmed", "inferred", "decision"] = "confirmed"


class Section(BaseModel):
    """A group of related stories inside the feature (an epic heading, not a separate feature)."""
    id: str                      # SEC-02-home-address
    order: int
    title: str
    purpose: str                 # one sentence, business outcome
    stories: list[Story] = F(default_factory=list)
    items: list[str] = F(default_factory=list)       # info items owned by this section
    rules: list[str] = F(default_factory=list)       # business rules owned by this section
    open_questions: list[str] = F(default_factory=list)
    source_refs: list[str] = F(default_factory=list)


class Feature(BaseModel):
    """One feature (one process to specify): its sections hold all the user stories."""
    id: str                      # the feature id (folder name)
    title: str                   # the feature title
    goal: str
    context: str                 # the situation today, from the sources
    stakeholders: list[str]
    sections: list[Section]
    source_refs: list[str] = F(default_factory=list)


class FeaturePlan(BaseModel):
    """Planner output: goal, context and the sections (stories left empty)."""
    goal: str
    context: str
    stakeholders: list[str]
    sections: list[Section]


class Spec(BaseModel):
    knowledge: KnowledgeModel
    feature: Feature

    def stories(self) -> list[Story]:
        return [s for sec in self.feature.sections for s in sec.stories]


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
