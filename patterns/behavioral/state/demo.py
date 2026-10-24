from patterns.behavioral.state.pattern import InvalidTransition, Order


def run() -> None:
    print("=== State: Order Lifecycle ===")
    order = Order("A-1001")
    print(f"Order {order.order_id} created: {order.status}")
    for action in ("pay", "ship", "deliver"):
        getattr(order, action)()
        print(f"  after {action}(): {order.status}")
    print("History:", " -> ".join(order.history))

    print("\nInvalid transitions are rejected:")
    for action in ("cancel", "pay"):
        try:
            getattr(order, action)()
        except InvalidTransition as exc:
            print(f"  {action}() -> {exc}")

    other = Order("A-1002")
    other.pay()
    other.cancel()
    print(f"\nOrder {other.order_id}: {' -> '.join(other.history)}")
    try:
        other.ship()
    except InvalidTransition as exc:
        print(f"  ship() -> {exc}")


if __name__ == "__main__":
    run()
