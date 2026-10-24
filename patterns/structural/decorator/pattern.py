"""Decorator: stack Logging, Retry and Cache around an API client (class and function forms)."""
from __future__ import annotations

import functools
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class ApiClient(ABC):
    """Component role."""

    @abstractmethod
    def get(self, path: str) -> str: ...


class HttpApiClient(ApiClient):
    """Concrete component. `fail_first` simulates transient errors deterministically."""

    def __init__(self, fail_first: int = 0) -> None:
        self.calls = 0
        self._fail_first = fail_first

    def get(self, path: str) -> str:
        self.calls += 1
        if self.calls <= self._fail_first:
            raise ConnectionError("temporary network error")
        return f"200 OK {path}"


class ClientDecorator(ApiClient):
    """Decorator role: same interface, wraps another ApiClient."""

    def __init__(self, inner: ApiClient) -> None:
        self._inner = inner

    def get(self, path: str) -> str:
        return self._inner.get(path)


class LoggingClient(ClientDecorator):
    def __init__(self, inner: ApiClient, log: list[str] | None = None) -> None:
        super().__init__(inner)
        self.log = log if log is not None else []

    def get(self, path: str) -> str:
        self.log.append(f"GET {path}")
        try:
            result = self._inner.get(path)
        except Exception as exc:
            self.log.append(f"  failed: {exc}")
            raise
        self.log.append(f"  -> {result}")
        return result


class RetryClient(ClientDecorator):
    def __init__(self, inner: ApiClient, attempts: int = 3) -> None:
        super().__init__(inner)
        self._attempts = attempts

    def get(self, path: str) -> str:
        for attempt in range(1, self._attempts + 1):
            try:
                return self._inner.get(path)
            except ConnectionError:
                if attempt == self._attempts:
                    raise
        raise AssertionError("unreachable")


class CacheClient(ClientDecorator):
    def __init__(self, inner: ApiClient) -> None:
        super().__init__(inner)
        self._cache: dict[str, str] = {}

    def get(self, path: str) -> str:
        if path not in self._cache:
            self._cache[path] = self._inner.get(path)
        return self._cache[path]


# --- Python function-decorator flavour of the same idea ------------------------
def logged(log: list[str]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log.append(f"call {fn.__name__}{args}")
            return fn(*args, **kwargs)

        return wrapper

    return deco


def retry(attempts: int = 3) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except ConnectionError:
                    if attempt == attempts:
                        raise

        return wrapper

    return deco
