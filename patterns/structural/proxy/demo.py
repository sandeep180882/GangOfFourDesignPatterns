from patterns.structural.proxy.pattern import (
    AccessDenied,
    ProtectedResourceProxy,
    RateLimitedProxy,
    RateLimitExceeded,
    RealReportService,
)


def run() -> None:
    print("=== Proxy: Rate Limiting + Access Control ===")
    real = RealReportService()
    now = [0.0]  # fake clock keeps the demo deterministic
    service = ProtectedResourceProxy(
        RateLimitedProxy(real, limit=2, window=60, clock=lambda: now[0]),
        roles={"alice": "admin", "bob": "viewer"},
    )

    for user in ("bob", "alice", "alice", "alice"):
        try:
            print(f"{user:>5}: {service.fetch(user, 'Q3-sales')}")
        except (AccessDenied, RateLimitExceeded) as exc:
            print(f"{user:>5}: BLOCKED ({type(exc).__name__}: {exc})")

    now[0] = 61.0
    print(f"alice after 61s: {service.fetch('alice', 'Q3-sales')}")
    print(f"Real service was called {real.calls} time(s)")


if __name__ == "__main__":
    run()
