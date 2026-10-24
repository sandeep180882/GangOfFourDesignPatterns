"""Demo: text editor undo/redo."""
from patterns.behavioral.command.pattern import DeleteLast, Document, Editor, InsertText


def run() -> None:
    print("=== Command: Text Editor Undo/Redo ===")
    doc, editor = Document(), Editor()
    editor.run(InsertText(doc, "Hello"))
    print(f"Insert 'Hello'   -> {doc.text!r}")
    editor.run(InsertText(doc, ", World"))
    print(f"Insert ', World' -> {doc.text!r}")
    editor.run(DeleteLast(doc, 5))
    print(f"Delete 5 chars   -> {doc.text!r}")
    editor.undo()
    print(f"Undo             -> {doc.text!r}")
    editor.undo()
    print(f"Undo             -> {doc.text!r}")
    editor.redo()
    print(f"Redo             -> {doc.text!r}")


if __name__ == "__main__":
    run()
