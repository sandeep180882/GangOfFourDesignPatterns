from patterns.creational.factory_method.pattern import NotificationFactory


def run() -> None:
    print("=== Factory Method: Notification Service ===")
    prefs = [
        ("email", "alice@example.com", "Your order #1001 has shipped."),
        ("sms", "+91-98765-43210", "OTP 482913. Do not share it with anyone."),
        ("push", "device-77", "Flash sale starts now!"),
    ]
    for channel, recipient, message in prefs:
        service = NotificationFactory.create(channel)
        print(f"{channel:>5} -> {type(service).__name__}: {service.notify(recipient, message)}")

    try:
        NotificationFactory.create("fax")
    except ValueError as exc:
        print(f"Unsupported channel rejected: {exc}")


if __name__ == "__main__":
    run()
