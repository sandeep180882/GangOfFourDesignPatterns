"""ISP fix: small role interfaces; implement only what you support."""
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Printer(Protocol):
    def print_doc(self, doc: str) -> str: ...


@runtime_checkable
class Scanner(Protocol):
    def scan(self) -> str: ...


@runtime_checkable
class Fax(Protocol):
    def fax(self, doc: str) -> str: ...


class OldPrinter:
    def print_doc(self, doc: str) -> str:
        return f"printed {doc}"


class MultiFunctionPrinter:
    def print_doc(self, doc: str) -> str:
        return f"printed {doc}"

    def scan(self) -> str:
        return "scanned page"

    def fax(self, doc: str) -> str:
        return f"faxed {doc}"


def print_all(printers: list[Printer], doc: str) -> list[str]:
    """Client depends only on the Printer role."""
    return [p.print_doc(doc) for p in printers]


def scan_all(devices: list[object]) -> list[str]:
    return [d.scan() for d in devices if isinstance(d, Scanner)]
