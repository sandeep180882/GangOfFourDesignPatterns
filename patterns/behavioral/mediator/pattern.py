"""Mediator: chat room routing messages between users."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Mediator(ABC):
    """Mediator: coordination interface."""

    @abstractmethod
    def send(self, sender: User, text: str, to: str | None = None) -> None: ...


class User:
    """Colleague: knows only the mediator, never other users."""

    def __init__(self, name: str, room: Mediator) -> None:
        self.name = name
        self.room = room
        self.inbox: list[str] = []

    def say(self, text: str) -> None:
        self.room.send(self, text)

    def whisper(self, to: str, text: str) -> None:
        self.room.send(self, text, to=to)

    def receive(self, sender: str, text: str) -> None:
        self.inbox.append(f"{sender}: {text}")


class ChatRoom(Mediator):
    """ConcreteMediator: registers users and routes messages."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def join(self, name: str) -> User:
        user = User(name, self)
        self._users[name] = user
        return user

    def leave(self, name: str) -> None:
        self._users.pop(name, None)

    def send(self, sender: User, text: str, to: str | None = None) -> None:
        if sender.name not in self._users:
            raise PermissionError(f"{sender.name} is not in the room")
        if to is not None:
            self._users[to].receive(f"{sender.name} (private)", text)
            return
        for user in self._users.values():
            if user is not sender:
                user.receive(sender.name, text)
