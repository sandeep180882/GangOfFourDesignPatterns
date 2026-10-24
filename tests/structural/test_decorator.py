import pytest

from patterns.structural.decorator.pattern import (
    ApiClient,
    CacheClient,
    HttpApiClient,
    LoggingClient,
    RetryClient,
    logged,
    retry,
)


def test_cache_avoids_second_call():
    raw = HttpApiClient()
    client = CacheClient(raw)
    assert client.get("/a") == client.get("/a")
    assert raw.calls == 1


def test_retry_recovers_then_gives_up():
    raw = HttpApiClient(fail_first=2)
    assert RetryClient(raw, attempts=3).get("/a") == "200 OK /a"
    with pytest.raises(ConnectionError):
        RetryClient(HttpApiClient(fail_first=5), attempts=3).get("/a")


def test_stacking_keeps_interface_and_logs():
    log: list[str] = []
    raw = HttpApiClient(fail_first=1)
    client = CacheClient(RetryClient(LoggingClient(raw, log)))
    assert isinstance(client, ApiClient)
    client.get("/x")
    assert log[0] == "GET /x" and "failed" in log[1] and log[-1].startswith("  ->")


def test_function_decorators():
    n = {"c": 0}
    events: list[str] = []

    @logged(events)
    @retry(2)
    def f():
        n["c"] += 1
        if n["c"] == 1:
            raise ConnectionError
        return "ok"

    assert f() == "ok" and n["c"] == 2 and f.__name__ == "f" and len(events) == 1
