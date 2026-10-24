from patterns.structural.composite.pattern import File, Folder


def test_recursive_size():
    inner = Folder("inner").add(File("a", 10))
    root = Folder("root").add(inner).add(File("b", 5))
    assert root.get_size() == 15
    assert inner.get_size() == 10


def test_empty_folder_and_remove():
    root = Folder("root")
    assert root.get_size() == 0
    f = File("x", 7)
    root.add(f)
    assert root.get_size() == 7
    root.remove(f)
    assert root.get_size() == 0


def test_render_tree():
    root = Folder("r").add(Folder("d").add(File("f", 1)))
    assert root.render() == ["r/ (1 B)", "  d/ (1 B)", "    f (1 B)"]
