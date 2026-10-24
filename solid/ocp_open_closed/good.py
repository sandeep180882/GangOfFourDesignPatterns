"""OCP fix: extend by adding classes; the engine is never edited."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Discount(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float: ...


class NoDiscount(Discount):
    def apply(self, amount: float) -> float:
        return amount


class PercentDiscount(Discount):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, amount: float) -> float:
        return amount * (1 - self.percent / 100)


class VipDiscount(PercentDiscount):
    def __init__(self) -> None:
        super().__init__(20)


class EmployeeDiscount(PercentDiscount):
    def __init__(self) -> None:
        super().__init__(30)


class StudentDiscount(PercentDiscount):
    """Added later: no existing code touched."""

    def __init__(self) -> None:
        super().__init__(15)


class DiscountEngine:
    def __init__(self) -> None:
        self._discounts: dict[str, Discount] = {"regular": NoDiscount()}

    def register(self, customer_type: str, discount: Discount) -> None:
        self._discounts[customer_type] = discount

    def apply(self, customer_type: str, amount: float) -> float:
        try:
            return self._discounts[customer_type].apply(amount)
        except KeyError:
            raise ValueError(f"unknown customer type: {customer_type}") from None
