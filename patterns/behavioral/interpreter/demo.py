"""Demo: user-filter rule engine."""
from patterns.behavioral.interpreter.pattern import parse

USERS = [
    {"name": "Asha", "age": 34, "country": "IN"},
    {"name": "Ben", "age": 28, "country": "IN"},
    {"name": "Chen", "age": 45, "country": "US"},
    {"name": "Dana", "age": 52, "country": "IN"},
]


def run() -> None:
    print("=== Interpreter: Rule Engine / Search Filter DSL ===")
    for rule in ["age > 30 AND country == 'IN'",
                 "country == 'US' OR age < 30",
                 "NOT (country == 'IN') OR age >= 50"]:
        tree = parse(rule)
        matches = [u["name"] for u in USERS if tree.interpret(u)]
        print(f"Rule: {rule}\n  tree: {tree}\n  matches: {matches}")


if __name__ == "__main__":
    run()
