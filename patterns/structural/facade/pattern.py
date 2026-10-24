"""Facade: OrderFacade.place_order() hides four e-commerce subsystems."""
from __future__ import annotations

from dataclasses import dataclass, field


# --- Subsystems --------------------------------------------------------------
@dataclass
class InventoryService:
    stock: dict[str, int] = field(default_factory=lambda: {"laptop": 5, "mouse": 20})

    def reserve(self, sku: str, qty: int) -> bool:
        if self.stock.get(sku, 0) >= qty:
            self.stock[sku] -= qty
            return True
        return False

    def release(self, sku: str, qty: int) -> None:
        self.stock[sku] = self.stock.get(sku, 0) + qty


class PaymentService:
    def charge(self, customer: str, amount: float) -> bool:
        return amount <= 5000  # simple credit rule

    def refund(self, customer: str, amount: float) -> None:
        pass


class ShippingService:
    def schedule(self, customer: str, sku: str, qty: int) -> str:
        return f"TRACK-{customer[:3].upper()}-{sku.upper()}-{qty}"


@dataclass
class EmailService:
    sent: list[str] = field(default_factory=list)

    def send(self, customer: str, text: str) -> None:
        self.sent.append(f"to {customer}: {text}")


@dataclass
class OrderResult:
    success: bool
    message: str
    tracking_id: str | None = None


# --- Facade ------------------------------------------------------------------
PRICES = {"laptop": 1200.0, "mouse": 25.0}


class OrderFacade:
    """Facade role: one simple call coordinates all subsystems in the right order."""

    def __init__(
        self,
        inventory: InventoryService | None = None,
        payment: PaymentService | None = None,
        shipping: ShippingService | None = None,
        email: EmailService | None = None,
    ) -> None:
        self.inventory = inventory or InventoryService()
        self.payment = payment or PaymentService()
        self.shipping = shipping or ShippingService()
        self.email = email or EmailService()

    def place_order(self, customer: str, sku: str, qty: int) -> OrderResult:
        if not self.inventory.reserve(sku, qty):
            return OrderResult(False, f"{sku} out of stock")
        total = PRICES.get(sku, 0.0) * qty
        if not self.payment.charge(customer, total):
            self.inventory.release(sku, qty)  # compensate
            self.email.send(customer, "Payment declined")
            return OrderResult(False, "payment declined")
        tracking = self.shipping.schedule(customer, sku, qty)
        self.email.send(customer, f"Order confirmed, tracking {tracking}")
        return OrderResult(True, f"order placed, total ${total:.2f}", tracking)
