"""Adapter: expose Stripe and PayPal SDKs behind one PaymentProcessor interface."""
from __future__ import annotations

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Target role: the interface the checkout code expects."""

    @abstractmethod
    def pay(self, amount: float, currency: str = "USD") -> str:
        """Charge `amount` and return a transaction id."""


# --- Adaptees: third-party SDKs we cannot (or should not) change -------------
class StripeAPI:
    def create_charge(self, amount_cents: int, currency: str, source: str) -> dict[str, str]:
        return {"id": f"ch_{amount_cents}_{currency.lower()}", "status": "succeeded"}


class PayPalAPI:
    def send_payment(self, payload: dict[str, object]) -> str:
        return f"PAYID-{payload['value']}-{payload['currency_code']}"


# --- Adapters ----------------------------------------------------------------
class StripeAdapter(PaymentProcessor):
    """Adapter: converts dollars to cents and unwraps Stripe's dict response."""

    def __init__(self, api: StripeAPI, source: str = "tok_visa") -> None:
        self._api = api
        self._source = source

    def pay(self, amount: float, currency: str = "USD") -> str:
        result = self._api.create_charge(round(amount * 100), currency, self._source)
        if result["status"] != "succeeded":
            raise RuntimeError("Stripe charge failed")
        return result["id"]


class PayPalAdapter(PaymentProcessor):
    """Adapter: builds PayPal's payload and returns its id string."""

    def __init__(self, api: PayPalAPI) -> None:
        self._api = api

    def pay(self, amount: float, currency: str = "USD") -> str:
        return self._api.send_payment({"value": f"{amount:.2f}", "currency_code": currency})


class Checkout:
    """Client: knows only PaymentProcessor."""

    def __init__(self, processor: PaymentProcessor) -> None:
        self._processor = processor

    def complete(self, amount: float) -> str:
        return self._processor.pay(amount)
