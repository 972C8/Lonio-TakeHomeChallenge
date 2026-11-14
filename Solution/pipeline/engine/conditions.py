"""The condition language used in requirements (ask_when, required_when, rule expressions).

It is a deliberately tiny, Python-flavoured expression language so that it is
unambiguous for builder agents, parseable by our linter and executable in tests:

    nationality != "CH" and permit_type != "C"
    country != "CH" and status != "X"
    choice in ["a", "b"]
    if_else(day(d) == 1, d, first_day_of_month(add_months(d, 1)))
    is_set(other_item)

Identifiers are field ids or rule ids. Literals: strings, numbers, true/false/null.
Operators: and, or, not, ==, !=, in, not in, <, <=, >, >=.
Functions: see FUNCTIONS. A missing answer evaluates as null; any comparison
with null is false (also != and not in), except explicit `== null` / `!= null`.
"""
from __future__ import annotations

import ast
import datetime as dt
from typing import Any


def _as_date(v):
    if v is None or isinstance(v, dt.date):
        return v
    s = str(v)
    if "." in s:  # DD.MM.YYYY
        d, m, y = s.split(".")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s)


def _add_months(d, n):
    if d is None:
        return None
    d = _as_date(d)
    m = d.month - 1 + int(n)
    y, m = d.year + m // 12, m % 12 + 1
    import calendar
    return dt.date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def _first_day_of_month(d):
    return None if d is None else _as_date(d).replace(day=1)


# Generic functions only. Domain logic (e.g. "insurance starts on the 1st of
# the following month") is expressed WITH these in a business rule of the
# problem, never added here.
FUNCTIONS = {
    "is_set": lambda v: v not in (None, "", []),
    "date": _as_date,
    "day": lambda d: None if d is None else _as_date(d).day,
    "first_day_of_month": _first_day_of_month,
    "add_months": _add_months,
    "if_else": lambda c, a, b: a if c else b,
}

_ALLOWED = (
    ast.Expression, ast.BoolOp, ast.And, ast.Or, ast.UnaryOp, ast.Not, ast.USub, ast.Compare,
    ast.Eq, ast.NotEq, ast.In, ast.NotIn, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Name, ast.Load, ast.Constant, ast.List, ast.Tuple, ast.Call,
)


_CONSTS = {"true": True, "false": False, "null": None, "True": True, "False": False, "None": None}


BUILTINS = {"today"}  # context values every problem may use; examples may set them


class ConditionError(ValueError):
    pass


def parse(expr: str) -> ast.Expression:
    src = expr.strip() or "true"
    try:
        tree = ast.parse(src, mode="eval")
    except SyntaxError as e:
        raise ConditionError(f"syntax error in {expr!r}: {e.msg}") from e
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED):
            raise ConditionError(f"construct {type(node).__name__} not allowed in {expr!r}")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in FUNCTIONS:
                raise ConditionError(f"unknown function in {expr!r}")
    return tree


def references(expr: str) -> set[str]:
    """Identifiers (field / rule ids) referenced by an expression."""
    tree = parse(expr)
    funcs = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call)}
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    return names - funcs - set(_CONSTS) - BUILTINS


def evaluate(expr: str, env: dict[str, Any]) -> Any:
    tree = parse(expr)
    return _eval(tree.body, env)


def _eval(node, env):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in _CONSTS:
            return _CONSTS[node.id]
        if node.id == "today" and "today" not in env:
            return dt.date.today()
        return env.get(node.id)
    if isinstance(node, (ast.List, ast.Tuple)):
        return [_eval(e, env) for e in node.elts]
    if isinstance(node, ast.BoolOp):
        vals = (_eval(v, env) for v in node.values)
        return all(bool(v) for v in vals) if isinstance(node.op, ast.And) else any(bool(v) for v in vals)
    if isinstance(node, ast.UnaryOp):
        v = _eval(node.operand, env)
        if isinstance(node.op, ast.USub):
            return None if v is None else -v
        return not bool(v)
    if isinstance(node, ast.Call):
        return FUNCTIONS[node.func.id](*[_eval(a, env) for a in node.args])
    if isinstance(node, ast.Compare):
        left, lnode = _eval(node.left, env), node.left
        for op, comp in zip(node.ops, node.comparators):
            right = _eval(comp, env)
            explicit_null = _is_null_literal(lnode) or _is_null_literal(comp)
            if not _cmp(op, left, right, explicit_null):
                return False
            left, lnode = right, comp
        return True
    raise ConditionError(f"cannot evaluate {ast.dump(node)}")


def _is_null_literal(node) -> bool:
    return (isinstance(node, ast.Constant) and node.value is None) or \
        (isinstance(node, ast.Name) and node.id in ("null", "None"))


def _cmp(op, a, b, explicit_null=False):
    # Null semantics: a comparison with an unanswered value (null) is FALSE -
    # for every operator, including != and not in - unless null is compared
    # explicitly (x == null / x != null). "Not yet known" never shows a
    # question or makes a rule true by accident.
    if a is None or b is None:
        if explicit_null and isinstance(op, ast.Eq):
            return a is b
        if explicit_null and isinstance(op, ast.NotEq):
            return a is not b
        return False
    if isinstance(op, ast.Eq):
        return a == b
    if isinstance(op, ast.NotEq):
        return a != b
    if isinstance(op, (ast.In, ast.NotIn)):
        res = a in b
        return res if isinstance(op, ast.In) else not res
    a, b = (_as_date(a), _as_date(b)) if isinstance(a, dt.date) or isinstance(b, dt.date) else (a, b)
    return {ast.Lt: a < b, ast.LtE: a <= b, ast.Gt: a > b, ast.GtE: a >= b}[type(op)]
