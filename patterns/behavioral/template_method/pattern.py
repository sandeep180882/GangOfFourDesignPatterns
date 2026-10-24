"""Template Method pattern: an ETL pipeline with a fixed skeleton."""
from __future__ import annotations

import csv
import io
import json
from abc import ABC, abstractmethod

Record = dict[str, object]


class DataPipeline(ABC):
    """AbstractClass: run() is the template method fixing the step order."""

    def run(self) -> list[str]:
        """Template method: extract -> transform -> load (do not override)."""
        self.log: list[str] = []
        raw = self.extract()
        self.log.append(f"extracted {len(raw)} records")
        records = self.transform(raw)
        self.log.append(f"transformed to {len(records)} records")
        self.load(records)
        if self.should_notify():  # hook
            self.log.append("notification sent")
        return self.log

    @abstractmethod
    def extract(self) -> list[Record]: ...

    def transform(self, records: list[Record]) -> list[Record]:
        """Default step: drop records with missing values."""
        return [r for r in records if all(v not in (None, "") for v in r.values())]

    @abstractmethod
    def load(self, records: list[Record]) -> None: ...

    def should_notify(self) -> bool:
        """Hook: subclasses may opt in."""
        return False


class CsvPipeline(DataPipeline):
    """ConcreteClass: reads CSV text, loads into an in-memory 'warehouse'."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.warehouse: list[Record] = []

    def extract(self) -> list[Record]:
        return list(csv.DictReader(io.StringIO(self.text)))

    def load(self, records: list[Record]) -> None:
        self.warehouse.extend(records)


class ApiPipeline(DataPipeline):
    """ConcreteClass: reads a JSON API payload, normalises names, prints-free load."""

    def __init__(self, payload: str) -> None:
        self.payload = payload
        self.warehouse: list[Record] = []

    def extract(self) -> list[Record]:
        return json.loads(self.payload)["results"]

    def transform(self, records: list[Record]) -> list[Record]:
        cleaned = super().transform(records)
        return [{**r, "name": str(r["name"]).title()} for r in cleaned]

    def load(self, records: list[Record]) -> None:
        self.warehouse.extend(records)

    def should_notify(self) -> bool:
        return True
