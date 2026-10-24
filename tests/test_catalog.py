import pytest

from catalog import discover

DEMOS = discover()


def test_all_patterns_and_principles_discovered():
    groups = [d.group for d in DEMOS]
    assert groups.count("Creational") == 5
    assert groups.count("Structural") == 7
    assert groups.count("Behavioral") == 11
    assert groups.count("SOLID") >= 5


@pytest.mark.parametrize("demo", DEMOS, ids=lambda d: d.id)
def test_demo_runs_and_has_readme(demo):
    output = demo.run()
    assert output.strip()
    assert "Traceback" not in output
    assert "```mermaid" in demo.readme_text()
