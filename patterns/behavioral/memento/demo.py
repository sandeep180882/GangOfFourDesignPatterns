"""Demo: editor snapshots."""
from patterns.behavioral.memento.pattern import Editor, History


def run() -> None:
    print("=== Memento: Editor Snapshots ===")
    editor = Editor()
    history = History(editor)
    editor.type("Dear team,")
    history.snapshot("greeting")
    editor.type(" the release is delayed.")
    history.snapshot("draft 1")
    editor.type(" (oops, wrong message)")
    print(f"Current text: {editor.text!r}")
    print(f"Snapshots: {history.labels}")
    print(f"Undo to '{history.undo()}' -> {editor.text!r}")
    print(f"Undo to '{history.undo()}' -> {editor.text!r}")


if __name__ == "__main__":
    run()
