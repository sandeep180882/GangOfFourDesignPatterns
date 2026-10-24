"""Command: text editor with undo/redo."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Document:
    """Receiver: the text being edited."""

    def __init__(self, text: str = "") -> None:
        self.text = text


class Command(ABC):
    """Command: encapsulated request with execute/undo."""

    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


class InsertText(Command):
    """ConcreteCommand: append text."""

    def __init__(self, doc: Document, text: str) -> None:
        self.doc, self.text = doc, text

    def execute(self) -> None:
        self.doc.text += self.text

    def undo(self) -> None:
        self.doc.text = self.doc.text[: len(self.doc.text) - len(self.text)]


class DeleteLast(Command):
    """ConcreteCommand: delete the last n characters."""

    def __init__(self, doc: Document, count: int) -> None:
        self.doc, self.count = doc, count
        self._removed = ""

    def execute(self) -> None:
        keep = max(len(self.doc.text) - self.count, 0)
        self._removed = self.doc.text[keep:]
        self.doc.text = self.doc.text[:keep]

    def undo(self) -> None:
        self.doc.text += self._removed


class Editor:
    """Invoker: runs commands and keeps undo/redo history."""

    def __init__(self) -> None:
        self._undo: list[Command] = []
        self._redo: list[Command] = []

    def run(self, command: Command) -> None:
        command.execute()
        self._undo.append(command)
        self._redo.clear()

    def undo(self) -> bool:
        if not self._undo:
            return False
        command = self._undo.pop()
        command.undo()
        self._redo.append(command)
        return True

    def redo(self) -> bool:
        if not self._redo:
            return False
        command = self._redo.pop()
        command.execute()
        self._undo.append(command)
        return True
