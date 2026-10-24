from patterns.behavioral.command.pattern import DeleteLast, Document, Editor, InsertText


def test_undo_redo_cycle():
    doc, ed = Document(), Editor()
    ed.run(InsertText(doc, "abc"))
    ed.run(DeleteLast(doc, 2))
    assert doc.text == "a"
    ed.undo()
    assert doc.text == "abc"
    ed.redo()
    assert doc.text == "a"


def test_new_command_clears_redo_and_empty_undo_is_safe():
    doc, ed = Document(), Editor()
    assert ed.undo() is False
    ed.run(InsertText(doc, "a"))
    ed.undo()
    ed.run(InsertText(doc, "b"))
    assert ed.redo() is False
    assert doc.text == "b"
