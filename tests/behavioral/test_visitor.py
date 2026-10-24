from patterns.behavioral.visitor.pattern import (
    Book,
    Electronics,
    Food,
    ShippingVisitor,
    TaxVisitor,
    Visitor,
    total,
)


def test_tax_and_shipping_dispatch_per_type():
    items = [Book(20.0), Electronics(100.0, weight_kg=1.0), Food(40.0)]
    assert [i.accept(TaxVisitor()) for i in items] == [0.0, 18.0, 2.0]
    assert total(items, TaxVisitor()) == 20.0
    assert Food(1.0, perishable=True).accept(ShippingVisitor()) == 8.0
    assert Electronics(1.0, weight_kg=2.0).accept(ShippingVisitor()) == 11.0


def test_new_operation_without_changing_elements():
    class CountVisitor(Visitor):
        def visit_book(self, book): return 1
        def visit_electronics(self, item): return 1
        def visit_food(self, food): return 1

    assert total([Book(1), Food(1), Electronics(1)], CountVisitor()) == 3
