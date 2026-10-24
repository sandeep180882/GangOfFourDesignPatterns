"""Bridge: alert urgency (abstraction) is independent of delivery channel (implementor)."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Channel(ABC):
    """Implementor role: how a message is delivered."""

    @abstractmethod
    def deliver(self, subject: str, body: str) -> str: ...


class EmailChannel(Channel):
    def deliver(self, subject: str, body: str) -> str:
        return f"EMAIL | {subject} | {body}"


class SlackChannel(Channel):
    def deliver(self, subject: str, body: str) -> str:
        return f"SLACK #ops | *{subject}* {body}"


class SmsChannel(Channel):
    def deliver(self, subject: str, body: str) -> str:
        return f"SMS | {subject}: {body}"[:80]


class Alert(ABC):
    """Abstraction role: holds a reference to a Channel (the bridge)."""

    def __init__(self, channels: list[Channel]) -> None:
        self._channels = channels

    @abstractmethod
    def send(self, message: str) -> list[str]: ...


class NormalAlert(Alert):
    """Refined abstraction: plain formatting."""

    def send(self, message: str) -> list[str]:
        return [c.deliver("Notice", message) for c in self._channels]


class UrgentAlert(Alert):
    """Refined abstraction: loud formatting, with an escalation footer."""

    def send(self, message: str) -> list[str]:
        return [
            c.deliver("URGENT", f"{message.upper()} (action required)") for c in self._channels
        ]
