"""DIP violation: high-level OrderService builds its concrete low-level deps."""


class MySQLDatabase:
    def save(self, order: dict) -> None:
        raise ConnectionError("cannot reach MySQL server at localhost:3306")


class GmailSender:
    def send(self, to: str, message: str) -> None:
        raise ConnectionError("cannot reach smtp.gmail.com")


class OrderService:
    def __init__(self) -> None:
        # Hard-wired: can't test without MySQL/Gmail, can't swap either.
        self.db = MySQLDatabase()
        self.mailer = GmailSender()

    def place_order(self, customer: str, item: str) -> None:
        self.db.save({"customer": customer, "item": item})
        self.mailer.send(customer, f"Order for {item} confirmed")
