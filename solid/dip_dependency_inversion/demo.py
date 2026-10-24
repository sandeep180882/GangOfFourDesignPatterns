from solid.dip_dependency_inversion.bad import OrderService as BadOrderService
from solid.dip_dependency_inversion.good import (
    ConsoleNotifier, InMemoryRepository, OrderService,
)


def run() -> None:
    print("=== DIP: Order service ===")
    print("--- Violation ---")
    try:
        BadOrderService().place_order("ada", "book")
    except ConnectionError as e:
        print("  Cannot even run or test the service:", e)

    print("--- Refactored ---")
    repo = InMemoryRepository()
    OrderService(repo, ConsoleNotifier()).place_order("ada", "book")
    print("  stored:", repo.orders)


if __name__ == "__main__":
    run()
