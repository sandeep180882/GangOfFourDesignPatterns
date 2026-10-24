from patterns.behavioral.strategy.pattern import Cart, CreditCard, Crypto, UPI


def run() -> None:
    print("=== Strategy: Checkout Payment ===")
    cart = Cart()
    cart.add("Keyboard", 80.0)
    cart.add("Monitor", 220.0)
    print(f"Cart total: {cart.total:.2f}")

    strategies = [
        CreditCard("4111111111111111"),
        UPI("shop@upi"),
        Crypto("0xABC123"),
    ]
    for strategy in strategies:
        print(f"[{type(strategy).__name__}] {cart.checkout(strategy)}")


if __name__ == "__main__":
    run()
