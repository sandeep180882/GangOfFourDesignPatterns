"""Demo: chat room."""
from patterns.behavioral.mediator.pattern import ChatRoom


def run() -> None:
    print("=== Mediator: Chat Room ===")
    room = ChatRoom()
    alice, bob, carol = room.join("Alice"), room.join("Bob"), room.join("Carol")
    alice.say("Hi everyone!")
    bob.whisper("Alice", "Lunch at 1?")
    room.leave("Carol")
    bob.say("Carol left, so she misses this.")
    for user in (alice, bob, carol):
        print(f"{user.name}'s inbox:")
        for line in user.inbox:
            print(f"  {line}")


if __name__ == "__main__":
    run()
