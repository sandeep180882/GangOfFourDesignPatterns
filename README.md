# Gang of Four Design Patterns and SOLID in Python

All 23 GoF design patterns and the 5 SOLID principles, each with a real-world scenario, a runnable demo, tests, and a README with a Mermaid UML diagram. See [DESIGN_PATTERNS_PLAN.md](DESIGN_PATTERNS_PLAN.md) for the full plan.

Requires Python 3.11+ (developed on 3.14). The demos use only the standard library.

## Quick start

```bash
pip install -r requirements.txt     # dev tools only (pytest, ruff, mypy)

python main.py                      # interactive CLI menu
python main.py creational.singleton # run one demo by id
python main.py all                  # run everything
python -m ui.server                 # browser UI at http://127.0.0.1:8000
python -m patterns.behavioral.strategy.demo   # run a demo module directly

python -m pytest                    # run all tests
```

The browser UI lists every demo, shows its output, and renders the explanation and UML. Diagrams are drawn with Mermaid loaded from a CDN, so they appear as plain text when you are offline.

## Layout

| Path | Contents |
|---|---|
| `patterns/creational/` | Singleton, Factory Method, Abstract Factory, Builder, Prototype |
| `patterns/structural/` | Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy |
| `patterns/behavioral/` | Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor |
| `solid/` | SRP, OCP, LSP, ISP and DIP (`bad.py` vs `good.py`), plus a capstone checkout system |
| `tests/` | pytest suites that mirror the folders above |
| `catalog.py`, `main.py`, `ui/` | Demo discovery, CLI runner, browser UI |

Each pattern folder has `pattern.py` (implementation), `demo.py` (exposes `run()`) and `README.md` (intent, UML, trade-offs). A new folder with a `demo.py` appears in the CLI and UI automatically.
