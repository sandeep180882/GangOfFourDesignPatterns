import pytest

from patterns.structural.proxy.pattern import (
    AccessDenied,
    ProtectedResourceProxy,
    RateLimitedProxy,
    RateLimitExceeded,
    RealReportService,
)


def test_rate_limit_blocks_and_recovers():
    real, t = RealReportService(), [0.0]
    proxy = RateLimitedProxy(real, limit=2, window=10, clock=lambda: t[0])
    proxy.fetch("u", "r")
    proxy.fetch("u", "r")
    with pytest.raises(RateLimitExceeded):
        proxy.fetch("u", "r")
    assert real.calls == 2
    t[0] = 10.0
    proxy.fetch("u", "r")
    assert real.calls == 3


def test_rate_limit_is_per_user():
    t = [0.0]
    proxy = RateLimitedProxy(RealReportService(), 1, 10, lambda: t[0])
    proxy.fetch("a", "r")
    proxy.fetch("b", "r")


def test_access_control_blocks_before_reaching_service():
    real = RealReportService()
    proxy = ProtectedResourceProxy(real, {"admin1": "admin", "v": "viewer"})
    assert "R1" in proxy.fetch("admin1", "R1")
    for user in ("v", "ghost"):
        with pytest.raises(AccessDenied):
            proxy.fetch(user, "R1")
    assert real.calls == 1
