"""LSP fix: model only what every subtype can really do; immutable shapes."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class Bird(ABC):
    @abstractmethod
    def move(self) -> str: ...


class FlyingBird(Bird):
    def fly(self) -> str:
        return f"{type(self).__name__} flies"

    def move(self) -> str:
        return self.fly()


class Sparrow(FlyingBird):
    pass


class Eagle(FlyingBird):
    pass


class Penguin(Bird):
    def move(self) -> str:
        return "Penguin swims"


class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...


@dataclass(frozen=True)
class Rectangle(Shape):
    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height


@dataclass(frozen=True)
class Square(Shape):
    side: float

    def area(self) -> float:
        return self.side ** 2


def concrete_subclasses(cls: type) -> list[type]:
    """All non-abstract descendants of cls; used by contract tests."""
    found: list[type] = []
    for sub in cls.__subclasses__():
        if not getattr(sub, "__abstractmethods__", None):
            found.append(sub)
        found.extend(concrete_subclasses(sub))
    return found
