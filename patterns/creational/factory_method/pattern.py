"""Factory Method: a notification service that picks the sender by channel."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Notification(ABC):
    """Product role: the interface every concrete sender implements."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> str: ...


class EmailNotification(Notification):
    """Concrete product."""

    def send(self, recipient: str, message: str) -> str:
        return f"[EMAIL] to <{recipient}>: {message}"


class SmsNotification(Notification):
    """Concrete product."""

    def send(self, recipient: str, message: str) -> str:
        return f"[SMS] to {recipient}: {message[:40]}"


class PushNotification(Notification):
    """Concrete product."""

    def send(self, recipient: str, message: str) -> str:
        return f"[PUSH] to device {recipient}: {message}"


class NotificationService(ABC):
    """Creator role: business logic relies on the abstract factory method."""

    @abstractmethod
    def create_notification(self) -> Notification:
        """The factory method; subclasses decide which product to build."""

    def notify(self, recipient: str, message: str) -> str:
        return self.create_notification().send(recipient, message)


class EmailService(NotificationService):
    """Concrete creator."""

    def create_notification(self) -> Notification:
        return EmailNotification()


class SmsService(NotificationService):
    """Concrete creator."""

    def create_notification(self) -> Notification:
        return SmsNotification()


class PushService(NotificationService):
    """Concrete creator."""

    def create_notification(self) -> Notification:
        return PushNotification()


class NotificationFactory:
    """Convenience registry: `create("sms")` hides which creator/product is used."""

    _creators: dict[str, type[NotificationService]] = {
        "email": EmailService,
        "sms": SmsService,
        "push": PushService,
    }

    @classmethod
    def create(cls, channel: str) -> NotificationService:
        try:
            return cls._creators[channel.lower()]()
        except KeyError:
            raise ValueError(f"Unknown channel: {channel!r}") from None

    @classmethod
    def register(cls, channel: str, creator: type[NotificationService]) -> None:
        """Open for extension: add channels without editing existing code."""
        cls._creators[channel.lower()] = creator
