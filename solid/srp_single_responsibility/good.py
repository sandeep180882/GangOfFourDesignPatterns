"""SRP fix: each class has exactly one reason to change."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class LineItem:
    name: str
    unit_price: float
    qty: int


@dataclass
class Invoice:
    """Pure data."""
    number: int
    customer: str
    items: list[LineItem] = field(default_factory=list)


class InvoiceCalculator:
    """Only pricing rules."""

    def __init__(self, tax_rate: float = 0.1):
        self.tax_rate = tax_rate

    def total(self, invoice: Invoice) -> float:
        subtotal = sum(i.unit_price * i.qty for i in invoice.items)
        return round(subtotal * (1 + self.tax_rate), 2)


class InvoiceRepository:
    """Only storage."""

    def __init__(self) -> None:
        self._db: dict[int, Invoice] = {}

    def save(self, invoice: Invoice) -> None:
        self._db[invoice.number] = invoice

    def get(self, number: int) -> Invoice:
        return self._db[number]


class InvoicePrinter(Protocol):
    def render(self, invoice: Invoice, total: float) -> str: ...


class TextInvoicePrinter:
    def render(self, invoice: Invoice, total: float) -> str:
        lines = [f"Invoice #{invoice.number} for {invoice.customer}"]
        lines += [f"  {i.name} x{i.qty} @ {i.unit_price:.2f}" for i in invoice.items]
        lines.append(f"  TOTAL: {total:.2f}")
        return "\n".join(lines)


class HtmlInvoicePrinter:
    """New format added without touching any existing class."""

    def render(self, invoice: Invoice, total: float) -> str:
        rows = "".join(f"<li>{i.name} x{i.qty}</li>" for i in invoice.items)
        return f"<h1>Invoice #{invoice.number}</h1><ul>{rows}</ul><b>{total:.2f}</b>"


class InvoiceMailer:
    """Only delivery."""

    def __init__(self) -> None:
        self.outbox: list[str] = []

    def send(self, address: str, body: str) -> str:
        message = f"To: {address}\n{body}"
        self.outbox.append(message)
        return message
