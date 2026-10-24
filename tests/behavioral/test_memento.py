import dataclasses

import pytest

from patterns.behavioral.memento.pattern import Editor, History


def test_restore_previous_states():
    ed = Editor()
    hist = History(ed)
    ed.type("one")
    hist.snapshot("s1")
    ed.type(" two")
    hist.snapshot("s2")
    ed.type(" three")
    assert hist.undo() == "s2" and ed.text == "one two"
    assert hist.undo() == "s1" and ed.text == "one"
    assert hist.undo() is None


def test_memento_immutable_and_restores_cursor():
    ed = Editor()
    ed.type("hello")
    ed.move_cursor(2)
    m = ed.save("x")
    ed.type("ZZ")
    ed.restore(m)
    assert (ed.text, ed.cursor) == ("hello", 2)
    with pytest.raises(dataclasses.FrozenInstanceError):
        m.text = "tamper"
