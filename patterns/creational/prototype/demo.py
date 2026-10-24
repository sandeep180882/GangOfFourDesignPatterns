from patterns.creational.prototype.pattern import ReportTemplate, TemplateRegistry


def run() -> None:
    print("=== Prototype: Report Templates ===")
    registry = TemplateRegistry()
    registry.register(
        "monthly",
        ReportTemplate(
            "Monthly Sales Report",
            ["Summary", "Revenue", "Top Products"],
            {"font": "Calibri", "logo": "acme.png"},
        ),
    )

    emea = registry.create("monthly")
    emea.title = "Monthly Sales Report - EMEA"
    emea.sections.append("EMEA Breakdown")
    emea.style["font"] = "Arial"

    apac = registry.create("monthly")
    apac.title = "Monthly Sales Report - APAC"

    original = registry.create("monthly")
    for r in (original, emea, apac):
        print(f"{r.title}: {r.sections} font={r.style['font']}")
    print(f"emea is apac: {emea is apac}; sections shared: {emea.sections is apac.sections}")


if __name__ == "__main__":
    run()
