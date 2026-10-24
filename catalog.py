"""Discovers every demo in the project and runs it, capturing its output."""

from __future__ import annotations

import contextlib
import importlib
import io
import threading
import traceback
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_RUN_LOCK = threading.Lock()  # redirect_stdout is process-wide


@dataclass(frozen=True)
class Demo:
    id: str  # e.g. "creational.singleton"
    group: str  # "Creational" | "Structural" | "Behavioral" | "SOLID"
    name: str  # human readable
    module: str  # dotted path of demo module
    readme: Path

    def run(self) -> str:
        """Run the demo and return everything it printed."""
        buffer = io.StringIO()
        with _RUN_LOCK, contextlib.redirect_stdout(buffer):
            try:
                importlib.import_module(self.module).run()
            except Exception:  # surface errors in the UI instead of crashing
                traceback.print_exc(file=buffer)
        return buffer.getvalue()

    def readme_text(self) -> str:
        return self.readme.read_text(encoding="utf-8") if self.readme.exists() else ""


def _title(folder: str) -> str:
    return folder.replace("_", " ").title()


def discover() -> list[Demo]:
    demos: list[Demo] = []
    for category in ("creational", "structural", "behavioral"):
        base = ROOT / "patterns" / category
        for folder in sorted(p for p in base.glob("*") if (p / "demo.py").exists()):
            demos.append(
                Demo(
                    id=f"{category}.{folder.name}",
                    group=category.title(),
                    name=_title(folder.name),
                    module=f"patterns.{category}.{folder.name}.demo",
                    readme=folder / "README.md",
                )
            )
    solid = ROOT / "solid"
    for folder in sorted(p for p in solid.glob("*") if (p / "demo.py").exists()):
        demos.append(
            Demo(
                id=f"solid.{folder.name}",
                group="SOLID",
                name=_title(folder.name),
                module=f"solid.{folder.name}.demo",
                readme=folder / "README.md",
            )
        )
    return demos


def find(demo_id: str) -> Demo | None:
    return next((d for d in discover() if d.id == demo_id), None)
