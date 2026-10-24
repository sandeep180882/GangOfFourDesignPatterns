"""Composite: files and folders share one interface; sizes aggregate recursively."""
from __future__ import annotations

from abc import ABC, abstractmethod


class FileSystemItem(ABC):
    """Component role: common interface for leaves and containers."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def get_size(self) -> int:
        """Size in bytes."""

    @abstractmethod
    def render(self, indent: int = 0) -> list[str]:
        """Tree view lines."""


class File(FileSystemItem):
    """Leaf role."""

    def __init__(self, name: str, size: int) -> None:
        super().__init__(name)
        self._size = size

    def get_size(self) -> int:
        return self._size

    def render(self, indent: int = 0) -> list[str]:
        return [f"{'  ' * indent}{self.name} ({self._size} B)"]


class Folder(FileSystemItem):
    """Composite role: holds children (files or folders) and delegates to them."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._children: list[FileSystemItem] = []

    def add(self, item: FileSystemItem) -> Folder:
        self._children.append(item)
        return self

    def remove(self, item: FileSystemItem) -> None:
        self._children.remove(item)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self._children)

    def render(self, indent: int = 0) -> list[str]:
        lines = [f"{'  ' * indent}{self.name}/ ({self.get_size()} B)"]
        for child in self._children:
            lines.extend(child.render(indent + 1))
        return lines
