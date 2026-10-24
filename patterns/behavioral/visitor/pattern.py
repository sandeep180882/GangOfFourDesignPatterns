"""Visitor pattern: add tax and shipping operations over product types."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class Visitor(ABC):
    """Visitor: one visit method per concrete element type."""

    @abstractmethod
    def visit_book(self, book: Book) -> float: ...

    @abstractmethod
    def visit_electronics(self, item: Electronics) -> float: ...

    @abstractmethod
    def visit_food(self, food: Food) -> float: ...


class Product(ABC):
    """Element: accepts a visitor (double dispatch)."""

    price: float

    @abstractmethod
    def accept(self, visitor: Visitor) -> float: ...


@dataclass
class Book(Product):
    """ConcreteElement."""

    price: float
    pages: int = 300

    def accept(self, visitor: Visitor) -> float:
        return visitor.visit_book(self)


@dataclass
class Electronics(Product):
    """ConcreteElement."""

    price: float
    weight_kg: float = 1.0

    def accept(self, visitor: Visitor) -> float:
        return visitor.visit_electronics(self)


@dataclass
class Food(Product):
    """ConcreteElement."""

    price: float
    perishable: bool = False

    def accept(self, visitor: Visitor) -> float:
        return visitor.visit_food(self)


class TaxVisitor(Visitor):
    """ConcreteVisitor: books 0%, electronics 18%, food 5%."""

    def visit_book(self, book: Book) -> float:
        return 0.0

    def visit_electronics(self, item: Electronics) -> float:
        return round(item.price * 0.18, 2)

    def visit_food(self, food: Food) -> float:
        return round(food.price * 0.05, 2)


class ShippingVisitor(Visitor):
    """ConcreteVisitor: shipping by weight, pages, or cold-chain surcharge."""

    def visit_book(self, book: Book) -> float:
        return 2.0 + book.pages / 500

    def visit_electronics(self, item: Electronics) -> float:
        return 5.0 + 3.0 * item.weight_kg

    def visit_food(self, food: Food) -> float:
        return 8.0 if food.perishable else 3.0


def total(products: list[Product], visitor: Visitor) -> float:
    """Apply a visitor across a product collection and sum the results."""
    return round(sum(p.accept(visitor) for p in products), 2)
