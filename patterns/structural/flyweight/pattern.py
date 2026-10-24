"""Flyweight: share map-marker icons (intrinsic state) across thousands of markers."""
from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class MarkerIcon:
    """Flyweight role: immutable intrinsic state, shared and heavy (pixel data)."""

    kind: str
    color: str
    pixels: bytes

    def draw(self, x: float, y: float, label: str) -> str:
        """Extrinsic state (position, label) is passed in by the caller."""
        return f"{self.kind}/{self.color} '{label}' at ({x:.1f}, {y:.1f})"


class IconFactory:
    """Flyweight factory: returns an existing icon or creates it once."""

    def __init__(self) -> None:
        self._icons: dict[tuple[str, str], MarkerIcon] = {}

    def get(self, kind: str, color: str) -> MarkerIcon:
        key = (kind, color)
        if key not in self._icons:
            self._icons[key] = MarkerIcon(kind, color, pixels=bytes(4096))  # ~4 KB bitmap
        return self._icons[key]

    @property
    def count(self) -> int:
        return len(self._icons)


@dataclass
class Marker:
    """Context role: stores extrinsic state plus a reference to a shared flyweight."""

    x: float
    y: float
    label: str
    icon: MarkerIcon

    def draw(self) -> str:
        return self.icon.draw(self.x, self.y, self.label)


class MapLayer:
    def __init__(self, factory: IconFactory | None = None) -> None:
        self.factory = factory or IconFactory()
        self.markers: list[Marker] = []

    def add(self, x: float, y: float, label: str, kind: str, color: str) -> Marker:
        marker = Marker(x, y, label, self.factory.get(kind, color))
        self.markers.append(marker)
        return marker

    def icon_memory_bytes(self) -> int:
        """Approximate bytes used by icon bitmaps with sharing."""
        return self.factory.count * sys.getsizeof(bytes(4096))

    def unshared_memory_bytes(self) -> int:
        """Approximate bytes if each marker owned its own bitmap."""
        return len(self.markers) * sys.getsizeof(bytes(4096))
