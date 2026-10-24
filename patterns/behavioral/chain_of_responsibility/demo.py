"""Demo: expense approval chain."""
from patterns.behavioral.chain_of_responsibility.pattern import ExpenseRequest, build_chain


def run() -> None:
    print("=== Chain of Responsibility: Expense Approval ===")
    chain = build_chain()
    for who, amount, why in [("Asha", 250, "Team lunch"), ("Ben", 4_800, "Conference"),
                             ("Chen", 32_000, "Server hardware"), ("Dev", 180_000, "Acquisition"),
                             ("Eli", 900_000, "Office building")]:
        print(f"{who} requests {amount:,}: {chain.handle(ExpenseRequest(who, amount, why))}")


if __name__ == "__main__":
    run()
