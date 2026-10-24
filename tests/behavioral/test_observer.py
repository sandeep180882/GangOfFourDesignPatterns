from patterns.behavioral.observer.pattern import (
    EmailAlert,
    MobileApp,
    StockTicker,
    TradingBot,
)


def test_all_observers_notified_independently():
    t = StockTicker()
    app, mail, bot = MobileApp(150), EmailAlert("a@b.c"), TradingBot(100, 160)
    for o in (app, mail, bot):
        t.attach(o)
    t.set_price("X", 90)
    t.set_price("X", 170)
    assert len(mail.emails) == 2
    assert app.notifications == ["Push: X hit 170.00"]
    assert bot.orders == ["BUY X @ 90.00", "SELL X @ 170.00"]


def test_detach_and_unchanged_price_do_not_notify():
    t = StockTicker()
    mail = EmailAlert("a@b.c")
    t.attach(mail)
    t.set_price("X", 10)
    t.set_price("X", 10)  # same price: ignored
    assert len(mail.emails) == 1
    t.detach(mail)
    t.set_price("X", 20)
    assert len(mail.emails) == 1
