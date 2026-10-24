import pytest

from patterns.behavioral.state.pattern import InvalidTransition, Order


def test_happy_path():
    o = Order("1")
    o.pay()
    o.ship()
    o.deliver()
    assert o.status == "Delivered"
    assert o.history == ["New", "Paid", "Shipped", "Delivered"]


def test_invalid_transitions_rejected_and_state_kept():
    o = Order("1")
    with pytest.raises(InvalidTransition):
        o.ship()
    assert o.status == "New"
    o.pay()
    o.ship()
    with pytest.raises(InvalidTransition):
        o.cancel()
    assert o.status == "Shipped"


def test_cancelled_is_terminal():
    o = Order("1")
    o.cancel()
    for action in (o.pay, o.ship, o.deliver, o.cancel):
        with pytest.raises(InvalidTransition):
            action()
