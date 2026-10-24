from patterns.structural.facade.pattern import OrderFacade


def run() -> None:
    print("=== Facade: E-commerce Order Placement ===")
    shop = OrderFacade()
    for customer, sku, qty in [("alice", "mouse", 2), ("bob", "laptop", 10), ("carol", "laptop", 5)]:
        result = shop.place_order(customer, sku, qty)
        status = "OK  " if result.success else "FAIL"
        print(f"{status} {customer} x{qty} {sku}: {result.message} {result.tracking_id or ''}".rstrip())
    print("Emails sent:")
    for mail in shop.email.sent:
        print(" ", mail)
    print("Remaining stock:", shop.inventory.stock)


if __name__ == "__main__":
    run()
