import pytest

from patterns.creational.factory_method.pattern import (
    EmailNotification,
    EmailService,
    Notification,
    NotificationFactory,
    NotificationService,
    PushService,
    SmsService,
)


@pytest.mark.parametrize(
    "channel, cls", [("email", EmailService), ("SMS", SmsService), ("push", PushService)]
)
def test_factory_returns_matching_creator(channel, cls):
    assert type(NotificationFactory.create(channel)) is cls


def test_creator_builds_product_and_sends():
    svc = EmailService()
    assert isinstance(svc.create_notification(), EmailNotification)
    assert "bob@x.com" in svc.notify("bob@x.com", "hi")


def test_unknown_channel_raises():
    with pytest.raises(ValueError):
        NotificationFactory.create("pigeon")


def test_register_new_channel():
    class Slack(Notification):
        def send(self, recipient: str, message: str) -> str:
            return "slack"

    class SlackService(NotificationService):
        def create_notification(self) -> Notification:
            return Slack()

    NotificationFactory.register("slack", SlackService)
    try:
        assert NotificationFactory.create("slack").notify("a", "b") == "slack"
    finally:
        NotificationFactory._creators.pop("slack")
