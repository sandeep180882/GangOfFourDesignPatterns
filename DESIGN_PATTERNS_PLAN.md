# Gang of Four Design Patterns and SOLID Principles in Python

A plan for a Python project that demonstrates all 23 GoF design patterns, followed by the 5 SOLID principles. Each example uses a realistic scenario instead of the usual `Shape`/`Animal` toys.

> Status: **plan only**. No code has been written yet. Once this is approved, we implement it.

---

## 1. Goals

- Cover all **23 GoF patterns** (5 Creational, 7 Structural, 11 Behavioral).
- Cover all **5 SOLID principles**, each with a "violation" and a "refactored" version.
- Give each pattern a **real-time use case** (payments, notifications, e-commerce, logging and so on).
- Make every example **runnable** (`python -m patterns.creational.singleton.demo`) and **tested** (`pytest`).
- Use modern Python 3.11+: type hints, `dataclasses`, `abc`, `Protocol`, `Enum`.

## 2. Proposed Project Structure

```
GangOfFourDesignPatterns/
├── README.md
├── DESIGN_PATTERNS_PLAN.md
├── pyproject.toml                # pytest, ruff, mypy config
├── requirements.txt
├── main.py                       # CLI menu: list and run any demo
├── patterns/
│   ├── creational/
│   │   ├── singleton/            # each folder: pattern.py, demo.py, README.md
│   │   ├── factory_method/
│   │   ├── abstract_factory/
│   │   ├── builder/
│   │   └── prototype/
│   ├── structural/
│   │   ├── adapter/
│   │   ├── bridge/
│   │   ├── composite/
│   │   ├── decorator/
│   │   ├── facade/
│   │   ├── flyweight/
│   │   └── proxy/
│   └── behavioral/
│       ├── chain_of_responsibility/
│       ├── command/
│       ├── interpreter/
│       ├── iterator/
│       ├── mediator/
│       ├── memento/
│       ├── observer/
│       ├── state/
│       ├── strategy/
│       ├── template_method/
│       └── visitor/
├── solid/
│   ├── srp_single_responsibility/    # bad.py, good.py, demo.py, README.md
│   ├── ocp_open_closed/
│   ├── lsp_liskov_substitution/
│   ├── isp_interface_segregation/
│   └── dip_dependency_inversion/
└── tests/
    ├── creational/
    ├── structural/
    ├── behavioral/
    └── solid/
```

Each pattern folder contains:

| File | Purpose |
|---|---|
| `pattern.py` | The pattern implementation (abstractions and concrete classes) |
| `demo.py` | Runnable real-world scenario that prints visible output |
| `README.md` | Intent, problem, structure (UML in Mermaid), when to use, trade-offs |

---

## 3. Part 1: GoF Design Patterns

### 3.1 Creational Patterns (5)

| # | Pattern | Real-time use case | Demo idea |
|---|---|---|---|
| 1 | **Singleton** | Application configuration / connection pool manager | A `ConfigManager` loads settings once; every module gets the same instance (thread-safe). |
| 2 | **Factory Method** | Notification service | `NotificationFactory.create("email" \| "sms" \| "push")` returns the right sender without the caller knowing the class. |
| 3 | **Abstract Factory** | Cross-cloud infrastructure (AWS vs Azure) | `CloudFactory` produces a matching family: `Storage` + `Queue` + `Compute` for each provider. |
| 4 | **Builder** | Building complex HTTP requests / SQL queries / reports | `QueryBuilder().select(...).from_(...).where(...).limit(...).build()` with a fluent interface and a Director. |
| 5 | **Prototype** | Cloning pre-configured document or game-character templates | Clone a `ReportTemplate` or `Employee` profile with deep copy, then customize the clone. |

### 3.2 Structural Patterns (7)

| # | Pattern | Real-time use case | Demo idea |
|---|---|---|---|
| 6 | **Adapter** | Integrating third-party payment gateways with different APIs | Wrap `StripeAPI` and `PayPalAPI` behind a common `PaymentProcessor` interface. |
| 7 | **Bridge** | Remote controls × devices; notification type × channel | `Alert` (abstraction: Urgent/Normal) is separate from `Channel` (implementation: Email/Slack/SMS). |
| 8 | **Composite** | File system, org chart, shopping cart with bundles | `Folder` and `File` share a `FileSystemItem` interface and `get_size()` works recursively. |
| 9 | **Decorator** | Pizza/coffee toppings, request middleware, logging and caching wrappers | Stack `@Logging`, `@Retry`, and `@Cache` decorators (class-based and Python function decorators) on an API client. |
| 10 | **Facade** | Order placement in e-commerce | `OrderFacade.place_order()` hides inventory, payment, shipping, and email subsystems. |
| 11 | **Flyweight** | Rendering thousands of map markers, text-editor characters, or game particles | Share intrinsic state (icon/font) across 100k objects and show the memory savings. |
| 12 | **Proxy** | Lazy-loaded images, access control, API rate limiting, caching | `RateLimitedApiProxy` and `ProtectedResourceProxy` (role check) wrap a real service. |

### 3.3 Behavioral Patterns (11)

| # | Pattern | Real-time use case | Demo idea |
|---|---|---|---|
| 13 | **Chain of Responsibility** | Support-ticket escalation, HTTP middleware, approval workflow | Expense approval: Manager → Director → VP → CFO by amount. |
| 14 | **Command** | Text-editor undo/redo, job queues, smart-home remote | `Command` objects with `execute()`/`undo()` and an `Invoker` that keeps history. |
| 15 | **Interpreter** | Simple rule engine / search-filter DSL | Parse `"age > 30 AND country == 'IN'"` into an expression tree and evaluate it against records. |
| 16 | **Iterator** | Paginated API results, tree traversal, playlist | Custom iterator (and generator-based version) over paginated results with lazy fetching. |
| 17 | **Mediator** | Chat room, air-traffic control, UI component coordination | `ChatRoom` mediator routes messages between `User` objects, which don't know each other. |
| 18 | **Memento** | Editor snapshots, game save points, form drafts | `Editor` creates `Memento` snapshots, and a `History` caretaker restores them. |
| 19 | **Observer** | Stock-price alerts, event bus, pub/sub notifications | `StockTicker` (subject) notifies `MobileApp`, `EmailAlert`, and `TradingBot` observers. |
| 20 | **State** | Order lifecycle, vending machine, traffic light, media player | `Order` moves through `New → Paid → Shipped → Delivered / Cancelled`, with invalid transitions rejected. |
| 21 | **Strategy** | Payment methods, shipping cost, pricing/discount rules, sorting, compression | `Cart.checkout(strategy)` swaps `CreditCard`, `UPI`, and `Crypto` strategies at runtime. |
| 22 | **Template Method** | Data-processing pipelines (ETL), report generation | `DataPipeline.run()` fixes the steps (extract → transform → load); `CsvPipeline` and `ApiPipeline` override the steps. |
| 23 | **Visitor** | Tax calculation across product types, AST operations, export formats | Add `TaxVisitor` and `ShippingVisitor` over `Book`, `Electronics`, and `Food` without changing those classes. |

---

## 4. Part 2: SOLID Principles

Each principle gets a **`bad.py`** (violation), a **`good.py`** (refactored), and a demo that shows what breaks when requirements change.

| Principle | Scenario | Violation shown | Fix shown | Related GoF patterns |
|---|---|---|---|---|
| **S: Single Responsibility** | Invoice / Employee management | One `Invoice` class that calculates, persists, prints, and emails | Split into `InvoiceCalculator`, `InvoiceRepository`, `InvoicePrinter`, `InvoiceMailer` | Facade, Command |
| **O: Open/Closed** | Discount engine for e-commerce | `if/elif` chain that is edited for every new customer type | New discount classes are added without touching existing code | Strategy, Decorator, Visitor |
| **L: Liskov Substitution** | Bird / Rectangle–Square / Payment hierarchy | `Penguin.fly()` raises an error, or `Square` breaks `Rectangle` area expectations | Redesign the hierarchy (`FlyingBird` vs `Bird`; immutable shapes), plus contract tests | Template Method, Factory Method |
| **I: Interface Segregation** | Multifunction printer / worker roles | A fat `Machine` interface forces `OldPrinter` to implement `scan()` and `fax()` | Small `Printer`, `Scanner`, and `Fax` protocols | Adapter, Facade |
| **D: Dependency Inversion** | Order service with notifications and database | `OrderService` creates `MySQLDatabase` and `GmailSender` directly | Depend on `Repository` and `Notifier` abstractions, with injected implementations | Abstract Factory, Observer, Bridge |

A closing **"Putting it together"** demo, an e-commerce checkout system, combines Strategy + Factory + Observer + Decorator + Facade and annotates which SOLID principle each one satisfies.

---

## 5. Pattern ↔ SOLID Cross-Reference (to be included in README)

| SOLID | Patterns that embody it |
|---|---|
| SRP | Facade, Command, Mediator, Iterator |
| OCP | Strategy, Decorator, Observer, Visitor, Factory Method, State |
| LSP | Template Method, Composite, Proxy |
| ISP | Adapter, Facade |
| DIP | Abstract Factory, Bridge, Observer, Strategy |

---

## 6. Tech and Tooling

- **Python** 3.11+
- **pytest** for tests, with at least one behavior test per pattern and per SOLID example
- **ruff** (lint/format) and **mypy** (type checks)
- **Mermaid** UML class diagrams in each pattern README
- Standard library only for the demos, with no external dependencies other than dev tools
- `main.py` provides an interactive menu: `python main.py` → pick a pattern → see the output

## 7. Implementation Phases

| Phase | Deliverable |
|---|---|
| 1 | Project scaffold: `pyproject.toml`, `main.py` runner, root README, shared utilities |
| 2 | 5 Creational patterns, with tests and READMEs |
| 3 | 7 Structural patterns, with tests and READMEs |
| 4 | 11 Behavioral patterns, with tests and READMEs |
| 5 | 5 SOLID principles (bad vs good), with tests |
| 6 | Capstone "Putting it together" demo, cross-reference docs, final lint and test pass |

## 8. Definition of Done

- [ ] All 23 patterns are implemented and have a runnable demo.
- [ ] All 5 SOLID principles show a violation and a fix.
- [ ] `pytest` passes; `ruff` and `mypy` are clean.
- [ ] Every folder has a README with intent, UML, use case, pros/cons.
- [ ] `python main.py` lists and runs every demo.

## 9. Open Questions

1. Python version: 3.11+ OK, or a lower minimum?
2. Do you want the READMEs to include Mermaid UML diagrams?
3. Should the demos be CLI output only, or should a small FastAPI/Streamlit UI be added later?
4. Should I implement phase by phase with a review after each, or everything in one pass?
