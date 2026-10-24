import pytest

from patterns.behavioral.interpreter.pattern import And, parse


def test_and_rule():
    rule = parse("age > 30 AND country == 'IN'")
    assert isinstance(rule, And)
    assert rule.interpret({"age": 31, "country": "IN"})
    assert not rule.interpret({"age": 31, "country": "US"})
    assert not rule.interpret({"age": 30, "country": "IN"})


def test_precedence_not_and_parentheses():
    rule = parse("NOT (a == 1 OR b == 2) AND c >= 3")
    assert rule.interpret({"a": 0, "b": 0, "c": 3})
    assert not rule.interpret({"a": 1, "b": 0, "c": 3})
    assert parse("a == 1 OR b == 1 AND c == 1").interpret({"a": 1, "b": 0, "c": 0})


def test_invalid_expression():
    with pytest.raises(ValueError):
        parse("age >> 3")
    with pytest.raises(ValueError):
        parse("age >")
