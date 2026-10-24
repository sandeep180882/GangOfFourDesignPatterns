"""Iterator: lazy traversal over paginated API results."""
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field


class FakeApi:
    """Stand-in remote service returning pages of items (counts calls)."""

    def __init__(self, total: int, page_size: int = 3) -> None:
        self._items = [f"item-{i}" for i in range(1, total + 1)]
        self.page_size = page_size
        self.calls = 0

    def fetch_page(self, page: int) -> list[str]:
        self.calls += 1
        start = page * self.page_size
        return self._items[start:start + self.page_size]


class PaginatedResults:
    """Aggregate: iterable collection; each iter() creates a fresh iterator."""

    def __init__(self, api: FakeApi) -> None:
        self.api = api

    def __iter__(self) -> PageIterator:
        return PageIterator(self.api)

    def generator(self) -> Iterator[str]:
        """Generator-based equivalent of PageIterator."""
        page = 0
        while batch := self.api.fetch_page(page):
            yield from batch
            page += 1


@dataclass
class PageIterator:
    """ConcreteIterator: fetches the next page only when the buffer is empty."""

    api: FakeApi
    _page: int = 0
    _buffer: list[str] = field(default_factory=list)
    _done: bool = False

    def __iter__(self) -> PageIterator:
        return self

    def __next__(self) -> str:
        if not self._buffer and not self._done:
            self._buffer = self.api.fetch_page(self._page)
            self._page += 1
            self._done = not self._buffer
        if not self._buffer:
            raise StopIteration
        return self._buffer.pop(0)
