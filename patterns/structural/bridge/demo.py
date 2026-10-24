from patterns.structural.bridge.pattern import (
    EmailChannel,
    NormalAlert,
    SlackChannel,
    SmsChannel,
    UrgentAlert,
)


def run() -> None:
    print("=== Bridge: Alert Type x Channel ===")
    print("-- Normal alert via Email + Slack --")
    for line in NormalAlert([EmailChannel(), SlackChannel()]).send("Nightly backup finished"):
        print(" ", line)
    print("-- Urgent alert via Slack + SMS --")
    for line in UrgentAlert([SlackChannel(), SmsChannel()]).send("Database is down"):
        print(" ", line)


if __name__ == "__main__":
    run()
