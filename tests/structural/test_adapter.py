import pytest

from patterns.structural.adapter.pattern import (
    Checkout,
    PayPalAdapter,
    PayPalAPI,
    PaymentProcessor,
    StripeAdapter,
    StripeAPI,
)


def test_stripe_adapter_converts_to_cents():
    assert StripeAdapter(StripeAPI()).pay(10.5) == "ch_1050_usd"


def test_paypal_adapter_formats_payload():
    assert PayPalAdapter(PayPalAPI()).pay(10, "EUR") == "PAYID-10.00-EUR"


@pytest.mark.parametrize("adapter", [StripeAdapter(StripeAPI()), PayPalAdapter(PayPalAPI())])
def test_adapters_are_interchangeable(adapter):
    assert isinstance(adapter, PaymentProcessor)
    assert Checkout(adapter).complete(5)


def test_failed_stripe_charge_raises():
    class Failing(StripeAPI):
        def create_charge(self, amount_cents, currency, source):
            return {"id": "x", "status": "failed"}

    with pytest.raises(RuntimeError):
        StripeAdapter(Failing()).pay(1)
