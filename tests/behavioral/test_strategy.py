import pytest

from patterns.behavioral.strategy.pattern import Cart, CreditCard, Crypto, UPI


def make_cart() -> Cart:
    c = Cart()
    c.add("a", 100.0)
    c.add("b", 100.0)
    return c


def test_strategies_swap_at_runtime():
    cart = make_cart()
    assert "204.00" in cart.checkout(CreditCard("1234567812345678"))
    assert "5678" in cart.checkout(CreditCard("1234567812345678"))
    assert "200.00" in cart.checkout(UPI("x@upi"))
    assert "0.004000 BTC" in cart.checkout(Crypto("w"))


def test_empty_cart_rejected():
    with pytest.raises(ValueError):
        Cart().checkout(UPI("x@upi"))
