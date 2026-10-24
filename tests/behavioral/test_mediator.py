import pytest

from patterns.behavioral.mediator.pattern import ChatRoom


def test_broadcast_excludes_sender():
    room = ChatRoom()
    a, b, c = room.join("a"), room.join("b"), room.join("c")
    a.say("hi")
    assert b.inbox == ["a: hi"] and c.inbox == ["a: hi"]
    assert a.inbox == []


def test_private_message_and_leave():
    room = ChatRoom()
    a, b, c = room.join("a"), room.join("b"), room.join("c")
    a.whisper("b", "psst")
    assert b.inbox == ["a (private): psst"] and c.inbox == []
    room.leave("c")
    b.say("bye")
    assert c.inbox == []
    with pytest.raises(PermissionError):
        c.say("still here?")
