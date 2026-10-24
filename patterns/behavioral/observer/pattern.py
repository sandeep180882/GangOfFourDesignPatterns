"""Observer pattern: a stock ticker notifies subscribers of price changes."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Observer(ABC):
    """Observer: interface notified when the subject changes."""

    @abstractmethod
    def update(self, symbol: str, price: float) -> None: ...


class StockTicker:
    """Subject: keeps prices and notifies attached observers on change."""

    def __init__(self) -> None:
        self._observers: list[Observer] = []
        self._prices: dict[str, float] = {}

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def set_price(self, symbol: str, price: float) -> None:
        if self._prices.get(symbol) == price:
            return  # no change, no notification
        self._prices[symbol] = price
        for observer in list(self._observers):  # copy: observers may detach
            observer.update(symbol, price)


class MobileApp(Observer):
    """ConcreteObserver: pushes a notification when a price crosses a threshold."""

    def __init__(self, threshold: float) -> None:
        self.threshold = threshold
        self.notifications: list[str] = []

    def update(self, symbol: str, price: float) -> None:
        if price >= self.threshold:
            self.notifications.append(f"Push: {symbol} hit {price:.2f}")


class EmailAlert(Observer):
    """ConcreteObserver: records every price change as an email."""

    def __init__(self, address: str) -> None:
        self.address = address
        self.emails: list[str] = []

    def update(self, symbol: str, price: float) -> None:
        self.emails.append(f"To {self.address}: {symbol} is now {price:.2f}")


class TradingBot(Observer):
    """ConcreteObserver: buys below a buy-price and sells above a sell-price."""

    def __init__(self, buy_below: float, sell_above: float) -> None:
        self.buy_below = buy_below
        self.sell_above = sell_above
        self.orders: list[str] = []

    def update(self, symbol: str, price: float) -> None:
        if price < self.buy_below:
            self.orders.append(f"BUY {symbol} @ {price:.2f}")
        elif price > self.sell_above:
            self.orders.append(f"SELL {symbol} @ {price:.2f}")
