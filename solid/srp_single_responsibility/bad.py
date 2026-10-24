"""SRP violation: one class with four reasons to change."""
from __future__ import annotations


class Invoice:
    _db: dict[int, "Invoice"] = {}  # persistence detail baked into the entity

    def __init__(self, number: int, customer: str, items: list[tuple[str, float, int]]):
        self.number = number
        self.customer = customer
        self.items = items  # (name, unit_price, qty)

    # Reason to change #1: pricing / tax rules
    def total(self, tax_rate: float = 0.1) -> float:
        return round(sum(p * q for _, p, q in self.items) * (1 + tax_rate), 2)

    # Reason to change #2: storage technology
    def save(self) -> None:
        Invoice._db[self.number] = self

    # Reason to change #3: presentation format
    def render(self) -> str:
        lines = [f"Invoice #{self.number} for {self.customer}"]
        lines += [f"  {n} x{q} @ {p:.2f}" for n, p, q in self.items]
        lines.append(f"  TOTAL: {self.total():.2f}")
        return "\n".join(lines)

    # Reason to change #4: delivery channel
    def email(self, address: str) -> str:
        return f"To: {address}\n{self.render()}"
