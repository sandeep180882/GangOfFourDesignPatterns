"""Proxy: rate-limiting and role-checking proxies in front of a real service."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Callable


class ReportService(ABC):
    """Subject role: interface shared by the real service and its proxies."""

    @abstractmethod
    def fetch(self, user: str, report_id: str) -> str: ...


class RealReportService(ReportService):
    """Real subject: the expensive/sensitive object."""

    def __init__(self) -> None:
        self.calls = 0

    def fetch(self, user: str, report_id: str) -> str:
        self.calls += 1
        return f"Report {report_id} contents"


class RateLimitExceeded(Exception):
    pass


class RateLimitedProxy(ReportService):
    """Proxy: allows `limit` calls per `window` seconds per user (injectable clock)."""

    def __init__(
        self,
        service: ReportService,
        limit: int,
        window: float,
        clock: Callable[[], float],
    ) -> None:
        self._service, self._limit, self._window, self._clock = service, limit, window, clock
        self._hits: dict[str, deque[float]] = {}

    def fetch(self, user: str, report_id: str) -> str:
        now = self._clock()
        hits = self._hits.setdefault(user, deque())
        while hits and now - hits[0] >= self._window:
            hits.popleft()
        if len(hits) >= self._limit:
            raise RateLimitExceeded(f"{user} exceeded {self._limit} calls per {self._window:g}s")
        hits.append(now)
        return self._service.fetch(user, report_id)


class AccessDenied(Exception):
    pass


class ProtectedResourceProxy(ReportService):
    """Proxy: role-based access control in front of the service."""

    def __init__(self, service: ReportService, roles: dict[str, str], required: str = "admin"):
        self._service, self._roles, self._required = service, roles, required

    def fetch(self, user: str, report_id: str) -> str:
        if self._roles.get(user) != self._required:
            raise AccessDenied(f"{user} lacks role '{self._required}'")
        return self._service.fetch(user, report_id)
