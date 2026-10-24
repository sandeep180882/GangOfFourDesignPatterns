"""Prototype: clone pre-configured report templates, then customize the clone."""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Protocol, TypeVar

T = TypeVar("T")


class Prototype(Protocol):
    """Prototype role: anything that can clone itself."""

    def clone(self: T) -> T: ...


@dataclass
class ReportTemplate:
    """Concrete prototype: an expensive-to-configure template."""

    title: str
    sections: list[str] = field(default_factory=list)
    style: dict[str, str] = field(default_factory=dict)

    def clone(self) -> ReportTemplate:
        return copy.deepcopy(self)  # deep: nested lists/dicts are not shared


class TemplateRegistry:
    """Prototype manager: stores ready-made templates and hands out clones."""

    def __init__(self) -> None:
        self._templates: dict[str, ReportTemplate] = {}

    def register(self, key: str, template: ReportTemplate) -> None:
        self._templates[key] = template

    def create(self, key: str) -> ReportTemplate:
        return self._templates[key].clone()
