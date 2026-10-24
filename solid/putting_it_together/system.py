"""E-commerce checkout combining Strategy + Factory + Observer + Decorator + Facade.

Each section is annotated with the SOLID principle it satisfies.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable


# --- Strategy: pricing -------------------------------------------------------
# OCP: new discount rules are new classes; checkout code is never edited.
class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float: ...


class NoDiscount(DiscountStrategy):
    def apply(self, amount: float) -> float:
        return amount


class PercentDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, amount: float) -> float:
        return round(amount * (1 - self.percent / 100), 2)


# --- Factory: object creation ------------------------------------------------
# SRP: one place knows how to build strategies from a name.
# DIP: callers receive the DiscountStrategy abstraction, never a concrete class.
def discount_factory(kind: str) -> DiscountStrategy:
    table: dict[str, Callable[[], DiscountStrategy]] = {
        "none": NoDiscount,
        "vip": lambda: PercentDiscount(20),
        "student": lambda: PercentDiscount(15),
    }
    try:
        return table[kind]()
    except KeyError:
        raise ValueError(f"unknown discount kind: {kind}") from None


# --- Payment + Decorator -----------------------------------------------------
# LSP: every decorator is a PaymentProcessor and substitutes for any other.
class PaymentProcessor(ABC):
    @abstractmethod
    def charge(self, customer: str, amount: float) -> str: ...


class CardPayment(PaymentProcessor):
    def charge(self, customer: str, amount: float) -> str:
        return f"card:{customer}:{amount:.2f}"


class PaymentDecorator(PaymentProcessor):
    def __init__(self, inner: PaymentProcessor):
        self.inner = inner


class FraudCheckedPayment(PaymentDecorator):
    """OCP: adds a cross-cutting concern without modifying CardPayment."""

    def __init__(self, inner: PaymentProcessor, limit: float = 1000.0):
        super().__init__(inner)
        self.limit = limit

    def charge(self, customer: str, amount: float) -> str:
        if amount > self.limit:
            raise ValueError(f"fraud check failed: {amount:.2f} > {self.limit:.2f}")
        return self.inner.charge(customer, amount)


class LoggedPayment(PaymentDecorator):
    def __init__(self, inner: PaymentProcessor, log: list[str]):
        super().__init__(inner)
        self.log = log

    def charge(self, customer: str, amount: float) -> str:
        ref = self.inner.charge(customer, amount)
        self.log.append(f"charged {ref}")
        return ref


# --- Observer ----------------------------------------------------------------
# OCP: add listeners (analytics, SMS...) without touching the facade.
# ISP: a listener only needs one tiny method.
class OrderListener(ABC):
    @abstractmethod
    def on_order_placed(self, receipt: "Receipt") -> None: ...


class EventBus:
    def __init__(self) -> None:
        self._listeners: list[OrderListener] = []

    def subscribe(self, listener: OrderListener) -> None:
        self._listeners.append(listener)

    def publish(self, receipt: "Receipt") -> None:
        for listener in self._listeners:
            listener.on_order_placed(receipt)


class EmailReceiptListener(OrderListener):
    def __init__(self) -> None:
        self.sent: list[str] = []

    def on_order_placed(self, receipt: "Receipt") -> None:
        self.sent.append(f"email to {receipt.customer}: paid {receipt.total:.2f}")


class InventoryListener(OrderListener):
    def __init__(self) -> None:
        self.reserved: list[str] = []

    def on_order_placed(self, receipt: "Receipt") -> None:
        self.reserved.extend(receipt.items)


@dataclass
class Receipt:
    customer: str
    items: list[str]
    subtotal: float
    total: float
    payment_ref: str


# --- Facade ------------------------------------------------------------------
# SRP: it only orchestrates; pricing, payment, notification live elsewhere.
# DIP: collaborators are injected as abstractions.
class CheckoutFacade:
    def __init__(self, payment: PaymentProcessor, bus: EventBus,
                 prices: dict[str, float] | None = None):
        self.payment = payment
        self.bus = bus
        self.prices = prices or {}

    def checkout(self, customer: str, items: list[str], discount_kind: str = "none") -> Receipt:
        subtotal = sum(self.prices[i] for i in items)
        total = discount_factory(discount_kind).apply(subtotal)
        ref = self.payment.charge(customer, total)
        receipt = Receipt(customer, items, subtotal, total, ref)
        self.bus.publish(receipt)
        return receipt


def build_default_checkout(log: list[str] | None = None) -> tuple[CheckoutFacade, EmailReceiptListener, InventoryListener]:
    log = log if log is not None else []
    payment = LoggedPayment(FraudCheckedPayment(CardPayment()), log)
    bus = EventBus()
    email, inventory = EmailReceiptListener(), InventoryListener()
    bus.subscribe(email)
    bus.subscribe(inventory)
    prices = {"laptop": 800.0, "mouse": 25.0, "desk": 300.0}
    return CheckoutFacade(payment, bus, prices), email, inventory
