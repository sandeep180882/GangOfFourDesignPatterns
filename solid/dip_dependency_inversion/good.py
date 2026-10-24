"""DIP fix: both sides depend on abstractions; dependencies are injected."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def save(self, order: dict) -> None: ...


class Notifier(ABC):
    @abstractmethod
    def send(self, to: str, message: str) -> None: ...


class InMemoryRepository(Repository):
    def __init__(self) -> None:
        self.orders: list[dict] = []

    def save(self, order: dict) -> None:
        self.orders.append(order)


class ConsoleNotifier(Notifier):
    def send(self, to: str, message: str) -> None:
        print(f"  [console] to {to}: {message}")


class FakeNotifier(Notifier):
    """Test double."""

    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send(self, to: str, message: str) -> None:
        self.sent.append((to, message))


class OrderService:
    def __init__(self, repository: Repository, notifier: Notifier):
        self.repository = repository
        self.notifier = notifier

    def place_order(self, customer: str, item: str) -> None:
        self.repository.save({"customer": customer, "item": item})
        self.notifier.send(customer, f"Order for {item} confirmed")
