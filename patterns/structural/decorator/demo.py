from patterns.structural.decorator.pattern import (
    CacheClient,
    HttpApiClient,
    LoggingClient,
    RetryClient,
    logged,
    retry,
)


def run() -> None:
    print("=== Decorator: API Client Middleware ===")

    raw = HttpApiClient(fail_first=2)
    log: list[str] = []
    client = CacheClient(RetryClient(LoggingClient(raw, log), attempts=3))

    print(client.get("/users/1"))
    print(client.get("/users/1"))  # served from cache
    print("Log of calls that reached the server:")
    for line in log:
        print(" ", line)
    print(f"Underlying HTTP calls: {raw.calls} (2 failures + 1 success, 2nd request cached)")

    print("--- Function decorators ---")
    flaky = {"n": 0}
    events: list[str] = []

    @logged(events)
    @retry(attempts=3)
    def fetch_price(sku: str) -> str:
        flaky["n"] += 1
        if flaky["n"] < 3:
            raise ConnectionError("timeout")
        return f"{sku}: $19.99"

    print(fetch_price("SKU-9"), f"(after {flaky['n']} attempts)", events)


if __name__ == "__main__":
    run()
