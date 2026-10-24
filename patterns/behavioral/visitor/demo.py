from patterns.behavioral.visitor.pattern import (
    Book,
    Electronics,
    Food,
    ShippingVisitor,
    TaxVisitor,
    total,
)


def run() -> None:
    print("=== Visitor: Tax and Shipping over Products ===")
    products = [Book(20.0, pages=500), Electronics(500.0, weight_kg=2.0), Food(10.0, perishable=True)]
    for visitor in (TaxVisitor(), ShippingVisitor()):
        print(f"\n{type(visitor).__name__}")
        for p in products:
            print(f"  {type(p).__name__:<12} price={p.price:>7.2f} -> {p.accept(visitor):.2f}")
        print(f"  Total: {total(products, visitor):.2f}")


if __name__ == "__main__":
    run()
