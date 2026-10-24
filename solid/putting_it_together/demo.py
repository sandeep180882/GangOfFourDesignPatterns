from solid.putting_it_together.system import build_default_checkout


def run() -> None:
    print("=== Putting it together: e-commerce checkout ===")
    log: list[str] = []
    facade, email, inventory = build_default_checkout(log)
    print("[Facade -> SRP/DIP] one checkout() call hides pricing, payment and events")
    print("[Factory -> SRP/DIP] discount 'vip' built by discount_factory, returned as DiscountStrategy")
    print("[Strategy -> OCP] discount applied via DiscountStrategy.apply")
    receipt = facade.checkout("ada", ["laptop", "mouse"], "vip")
    print(f"  subtotal={receipt.subtotal:.2f} total={receipt.total:.2f} ref={receipt.payment_ref}")
    print("[Decorator -> OCP/LSP] FraudChecked(Card) wrapped by Logged; log:", log)
    print("[Observer -> OCP/ISP] listeners reacted:")
    print("  ", email.sent)
    print("  ", inventory.reserved)
    print("Fraud decorator blocks big orders safely:")
    try:
        facade.checkout("bob", ["laptop"] * 2)
    except ValueError as e:
        print("  rejected:", e)


if __name__ == "__main__":
    run()
