import pytest

from patterns.structural.bridge.pattern import (
    Channel,
    EmailChannel,
    NormalAlert,
    SlackChannel,
    UrgentAlert,
)


class FakeChannel(Channel):
    def __init__(self):
        self.calls = []

    def deliver(self, subject, body):
        self.calls.append((subject, body))
        return "ok"


@pytest.mark.parametrize("alert_cls, subject", [(NormalAlert, "Notice"), (UrgentAlert, "URGENT")])
def test_any_alert_works_with_any_channel(alert_cls, subject):
    ch = FakeChannel()
    alert_cls([ch]).send("hi")
    assert ch.calls[0][0] == subject


def test_urgent_formats_body_and_fans_out():
    a, b = FakeChannel(), FakeChannel()
    out = UrgentAlert([a, b]).send("down")
    assert out == ["ok", "ok"]
    assert a.calls[0][1].startswith("DOWN")


def test_real_channels_differ():
    email, slack = NormalAlert([EmailChannel()]).send("x"), NormalAlert([SlackChannel()]).send("x")
    assert email != slack
