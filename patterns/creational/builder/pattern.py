"""Builder: a fluent SQL QueryBuilder plus a Director with canned queries."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Query:
    """Product: the finished, immutable query."""

    sql: str
    params: tuple[object, ...] = ()


@dataclass
class QueryBuilder:
    """Builder: collects parts step by step; `build()` assembles the product."""

    _columns: list[str] = field(default_factory=list)
    _table: str | None = None
    _conditions: list[str] = field(default_factory=list)
    _params: list[object] = field(default_factory=list)
    _order: str | None = None
    _limit: int | None = None

    def select(self, *columns: str) -> QueryBuilder:
        self._columns.extend(columns)
        return self

    def from_(self, table: str) -> QueryBuilder:
        self._table = table
        return self

    def where(self, condition: str, *params: object) -> QueryBuilder:
        self._conditions.append(condition)
        self._params.extend(params)
        return self

    def order_by(self, column: str, descending: bool = False) -> QueryBuilder:
        self._order = f"{column} {'DESC' if descending else 'ASC'}"
        return self

    def limit(self, n: int) -> QueryBuilder:
        if n <= 0:
            raise ValueError("limit must be positive")
        self._limit = n
        return self

    def build(self) -> Query:
        if not self._table:
            raise ValueError("a table is required: call from_()")
        parts = [f"SELECT {', '.join(self._columns) or '*'}", f"FROM {self._table}"]
        if self._conditions:
            parts.append("WHERE " + " AND ".join(self._conditions))
        if self._order:
            parts.append(f"ORDER BY {self._order}")
        if self._limit is not None:
            parts.append(f"LIMIT {self._limit}")
        return Query(" ".join(parts), tuple(self._params))


class QueryDirector:
    """Director: knows recipes (build order) for frequently used queries."""

    def __init__(self, builder: QueryBuilder | None = None) -> None:
        self._builder = builder or QueryBuilder()

    def recent_orders(self, customer_id: int, count: int = 10) -> Query:
        return (
            self._builder.select("id", "total", "created_at")
            .from_("orders")
            .where("customer_id = ?", customer_id)
            .order_by("created_at", descending=True)
            .limit(count)
            .build()
        )
