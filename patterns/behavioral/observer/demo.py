from patterns.behavioral.observer.pattern import (
    EmailAlert,
    MobileApp,
    StockTicker,
    TradingBot,
)


def run() -> None:
    print("=== Observer: Stock-Price Alerts ===")
    ticker = StockTicker()
    app = MobileApp(threshold=150)
    email = EmailAlert("trader@example.com")
    bot = TradingBot(buy_below=100, sell_above=160)
    for o in (app, email, bot):
        ticker.attach(o)

    for price in (120, 95, 155, 165):
        print(f"Ticker: ACME -> {price}")
        ticker.set_price("ACME", price)

    print("\nMobileApp notifications:", *app.notifications, sep="\n  ")
    print("EmailAlert emails:", *email.emails, sep="\n  ")
    print("TradingBot orders:", *bot.orders, sep="\n  ")

    ticker.detach(email)
    ticker.set_price("ACME", 170)
    print(f"\nAfter detaching EmailAlert: {len(email.emails)} emails (unchanged), "
          f"{len(bot.orders)} bot orders")


if __name__ == "__main__":
    run()
