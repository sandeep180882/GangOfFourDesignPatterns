"""Strategy pattern: swappable payment methods for a shopping cart."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class PaymentStrategy(ABC):
    """Strategy: interchangeable payment algorithm."""

    @abstractmethod
    def pay(self, amount: float) -> str: ...


@dataclass
class CreditCard(PaymentStrategy):
    """ConcreteStrategy: card payment with a 2% processing fee."""

    card_number: str

    def pay(self, amount: float) -> str:
        total = round(amount * 1.02, 2)
        return f"Charged {total:.2f} to card ****{self.card_number[-4:]} (incl. 2% fee)"


@dataclass
class UPI(PaymentStrategy):
    """ConcreteStrategy: instant UPI transfer, no fee."""

    vpa: str

    def pay(self, amount: float) -> str:
        return f"Collected {amount:.2f} via UPI request to {self.vpa}"


@dataclass
class Crypto(PaymentStrategy):
    """ConcreteStrategy: crypto payment converted at a fixed demo rate."""

    wallet: str
    usd_per_coin: float = 50_000.0

    def pay(self, amount: float) -> str:
        return f"Transferred {amount / self.usd_per_coin:.6f} BTC from wallet {self.wallet}"


@dataclass
class Cart:
    """Context: computes the total and delegates payment to a strategy."""

    items: dict[str, float] = field(default_factory=dict)

    def add(self, name: str, price: float) -> None:
        self.items[name] = price

    @property
    def total(self) -> float:
        return sum(self.items.values())

    def checkout(self, strategy: PaymentStrategy) -> str:
        if not self.items:
            raise ValueError("Cart is empty")
        return strategy.pay(self.total)
