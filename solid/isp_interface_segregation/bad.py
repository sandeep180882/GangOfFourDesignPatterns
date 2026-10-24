"""ISP violation: a fat interface forces useless methods on clients."""
from abc import ABC, abstractmethod


class Machine(ABC):
    @abstractmethod
    def print_doc(self, doc: str) -> str: ...

    @abstractmethod
    def scan(self) -> str: ...

    @abstractmethod
    def fax(self, doc: str) -> str: ...


class MultiFunctionPrinter(Machine):
    def print_doc(self, doc: str) -> str:
        return f"printed {doc}"

    def scan(self) -> str:
        return "scanned page"

    def fax(self, doc: str) -> str:
        return f"faxed {doc}"


class OldPrinter(Machine):
    def print_doc(self, doc: str) -> str:
        return f"printed {doc}"

    # Forced to implement methods it cannot support:
    def scan(self) -> str:
        raise NotImplementedError("OldPrinter cannot scan")

    def fax(self, doc: str) -> str:
        raise NotImplementedError("OldPrinter cannot fax")
