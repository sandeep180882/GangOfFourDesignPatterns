"""Interpreter: tiny rule/filter DSL, e.g. "age > 30 AND country == 'IN'"."""
from __future__ import annotations

import operator
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

Record = dict[str, Any]


class Expression(ABC):
    """AbstractExpression: evaluates against a record (the context)."""

    @abstractmethod
    def interpret(self, record: Record) -> bool: ...


_OPS = {">": operator.gt, "<": operator.lt, ">=": operator.ge,
        "<=": operator.le, "==": operator.eq, "!=": operator.ne}


@dataclass(frozen=True)
class Comparison(Expression):
    """TerminalExpression: field <op> literal."""

    field: str
    op: str
    value: Any

    def interpret(self, record: Record) -> bool:
        return _OPS[self.op](record[self.field], self.value)


@dataclass(frozen=True)
class And(Expression):
    """NonterminalExpression."""

    left: Expression
    right: Expression

    def interpret(self, record: Record) -> bool:
        return self.left.interpret(record) and self.right.interpret(record)


@dataclass(frozen=True)
class Or(Expression):
    """NonterminalExpression."""

    left: Expression
    right: Expression

    def interpret(self, record: Record) -> bool:
        return self.left.interpret(record) or self.right.interpret(record)


@dataclass(frozen=True)
class Not(Expression):
    """NonterminalExpression."""

    inner: Expression

    def interpret(self, record: Record) -> bool:
        return not self.inner.interpret(record)


_TOKEN = re.compile(r"\s*(>=|<=|==|!=|>|<|\(|\)|'[^']*'|\d+(?:\.\d+)?|\w+)")


class Parser:
    """Client-side parser. Grammar: or := and (OR and)*; and := not (AND not)*;
    not := NOT not | '(' or ')' | field op literal."""

    def __init__(self, text: str) -> None:
        self.tokens: list[str] = []
        end = 0
        while text[end:].strip():
            match = _TOKEN.match(text, end)
            if not match:
                raise ValueError(f"Unparseable expression near {text[end:].strip()!r}")
            self.tokens.append(match.group(1))
            end = match.end()
        self.pos = 0

    def parse(self) -> Expression:
        expr = self._or()
        if self.pos != len(self.tokens):
            raise ValueError(f"Unexpected token {self.tokens[self.pos]!r}")
        return expr

    def _peek(self) -> str | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _take(self) -> str:
        token = self._peek()
        if token is None:
            raise ValueError("Unexpected end of expression")
        self.pos += 1
        return token

    def _or(self) -> Expression:
        node = self._and()
        while (self._peek() or "").upper() == "OR":
            self._take()
            node = Or(node, self._and())
        return node

    def _and(self) -> Expression:
        node = self._not()
        while (self._peek() or "").upper() == "AND":
            self._take()
            node = And(node, self._not())
        return node

    def _not(self) -> Expression:
        if (self._peek() or "").upper() == "NOT":
            self._take()
            return Not(self._not())
        if self._peek() == "(":
            self._take()
            node = self._or()
            if self._take() != ")":
                raise ValueError("Expected ')'")
            return node
        field, op, raw = self._take(), self._take(), self._take()
        if op not in _OPS:
            raise ValueError(f"Unknown operator {op!r}")
        return Comparison(field, op, _literal(raw))


def _literal(raw: str) -> Any:
    if raw.startswith("'"):
        return raw[1:-1]
    return float(raw) if "." in raw else int(raw)


def parse(text: str) -> Expression:
    """Build the expression tree for a rule string."""
    return Parser(text).parse()
