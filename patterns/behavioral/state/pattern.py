"""State pattern: an order whose behaviour depends on its lifecycle state."""
from __future__ import annotations

from abc import ABC


class InvalidTransition(Exception):
    """Raised when an action is not allowed in the current state."""


class OrderState(ABC):
    """State: default behaviour rejects every action; subclasses allow some."""

    name = "Abstract"

    def pay(self, order: Order) -> None:
        self._reject("pay")

    def ship(self, order: Order) -> None:
        self._reject("ship")

    def deliver(self, order: Order) -> None:
        self._reject("deliver")

    def cancel(self, order: Order) -> None:
        self._reject("cancel")

    def _reject(self, action: str) -> None:
        raise InvalidTransition(f"Cannot {action} an order that is {self.name}")


class NewState(OrderState):
    """ConcreteState: awaiting payment."""

    name = "New"

    def pay(self, order: Order) -> None:
        order.state = PaidState()

    def cancel(self, order: Order) -> None:
        order.state = CancelledState()


class PaidState(OrderState):
    """ConcreteState: paid, awaiting shipment."""

    name = "Paid"

    def ship(self, order: Order) -> None:
        order.state = ShippedState()

    def cancel(self, order: Order) -> None:
        order.state = CancelledState()  # refund implied


class ShippedState(OrderState):
    """ConcreteState: in transit; can no longer be cancelled."""

    name = "Shipped"

    def deliver(self, order: Order) -> None:
        order.state = DeliveredState()


class DeliveredState(OrderState):
    """ConcreteState: terminal."""

    name = "Delivered"


class CancelledState(OrderState):
    """ConcreteState: terminal."""

    name = "Cancelled"


class Order:
    """Context: delegates actions to its current state object."""

    def __init__(self, order_id: str) -> None:
        self.order_id = order_id
        self.state: OrderState = NewState()
        self.history: list[str] = [self.state.name]

    @property
    def status(self) -> str:
        return self.state.name

    def _do(self, action: str) -> None:
        getattr(self.state, action)(self)
        self.history.append(self.state.name)

    def pay(self) -> None:
        self._do("pay")

    def ship(self) -> None:
        self._do("ship")

    def deliver(self) -> None:
        self._do("deliver")

    def cancel(self) -> None:
        self._do("cancel")
