from patterns.creational.prototype.pattern import ReportTemplate, TemplateRegistry


def test_clone_is_deep_copy():
    original = ReportTemplate("T", ["a"], {"font": "x"})
    clone = original.clone()
    clone.sections.append("b")
    clone.style["font"] = "y"
    assert clone is not original
    assert original.sections == ["a"]
    assert original.style == {"font": "x"}


def test_registry_hands_out_independent_clones():
    reg = TemplateRegistry()
    reg.register("k", ReportTemplate("T", ["a"]))
    one, two = reg.create("k"), reg.create("k")
    one.sections.append("x")
    assert two.sections == ["a"]
    assert one == ReportTemplate("T", ["a", "x"])
