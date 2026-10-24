"""Chain of Responsibility: expense approval escalating by amount."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ExpenseRequest:
    """Request passed along the chain."""

    employee: str
    amount: float
    purpose: str


class Approver(ABC):
    """Handler: approves requests within its limit, else forwards to successor."""

    title: str
    limit: float

    def __init__(self) -> None:
        self._next: Approver | None = None

    def set_next(self, handler: Approver) -> Approver:
        """Link the next handler and return it to allow fluent chaining."""
        self._next = handler
        return handler

    def handle(self, request: ExpenseRequest) -> str:
        if request.amount <= self.limit:
            return self._approve(request)
        if self._next is None:
            return f"REJECTED: {request.amount:,.2f} exceeds every approval limit"
        return self._next.handle(request)

    @abstractmethod
    def _approve(self, request: ExpenseRequest) -> str: ...


class _BaseApprover(Approver):
    def _approve(self, request: ExpenseRequest) -> str:
        return (f"{self.title} approved {request.amount:,.2f} "
                f"for {request.employee} ({request.purpose})")


class Manager(_BaseApprover):
    """ConcreteHandler: limit 1,000."""

    title, limit = "Manager", 1_000


class Director(_BaseApprover):
    """ConcreteHandler: limit 10,000."""

    title, limit = "Director", 10_000


class VP(_BaseApprover):
    """ConcreteHandler: limit 50,000."""

    title, limit = "VP", 50_000


class CFO(_BaseApprover):
    """ConcreteHandler: limit 250,000."""

    title, limit = "CFO", 250_000


def build_chain() -> Approver:
    """Client helper: Manager -> Director -> VP -> CFO."""
    manager = Manager()
    manager.set_next(Director()).set_next(VP()).set_next(CFO())
    return manager
