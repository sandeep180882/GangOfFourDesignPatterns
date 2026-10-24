from patterns.structural.adapter.pattern import (
    Checkout,
    PayPalAdapter,
    PayPalAPI,
    StripeAdapter,
    StripeAPI,
)


def run() -> None:
    print("=== Adapter: Payment Gateways ===")
    gateways = {"Stripe": StripeAdapter(StripeAPI()), "PayPal": PayPalAdapter(PayPalAPI())}
    for name, adapter in gateways.items():
        txn = Checkout(adapter).complete(49.99)
        print(f"{name:>6}: paid 49.99 USD -> transaction {txn}")


if __name__ == "__main__":
    run()
