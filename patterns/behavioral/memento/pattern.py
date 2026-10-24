"""Memento: editor snapshots with a history caretaker."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Memento:
    """Memento: immutable snapshot of the editor state (opaque to the caretaker)."""

    text: str
    cursor: int
    label: str


class Editor:
    """Originator: creates and restores mementos."""

    def __init__(self) -> None:
        self.text = ""
        self.cursor = 0

    def type(self, chars: str) -> None:
        self.text = self.text[: self.cursor] + chars + self.text[self.cursor:]
        self.cursor += len(chars)

    def move_cursor(self, position: int) -> None:
        self.cursor = max(0, min(position, len(self.text)))

    def save(self, label: str) -> Memento:
        return Memento(self.text, self.cursor, label)

    def restore(self, memento: Memento) -> None:
        self.text, self.cursor = memento.text, memento.cursor


class History:
    """Caretaker: stores mementos without inspecting their contents."""

    def __init__(self, editor: Editor) -> None:
        self._editor = editor
        self._snapshots: list[Memento] = []

    def snapshot(self, label: str) -> None:
        self._snapshots.append(self._editor.save(label))

    def undo(self) -> str | None:
        """Restore the latest snapshot and drop it; return its label."""
        if not self._snapshots:
            return None
        memento = self._snapshots.pop()
        self._editor.restore(memento)
        return memento.label

    @property
    def labels(self) -> list[str]:
        return [m.label for m in self._snapshots]
