from solid.ocp_open_closed.bad import DiscountEngine as BadEngine
from solid.ocp_open_closed.good import (
    DiscountEngine, EmployeeDiscount, StudentDiscount, VipDiscount,
)


def run() -> None:
    print("=== OCP: Discount engine ===")
    print("--- Violation ---")
    bad = BadEngine()
    print("vip 100 ->", bad.apply("vip", 100.0))
    try:
        bad.apply("student", 100.0)
    except ValueError as e:
        print(f"New 'student' type fails ({e}); fix = edit the if/elif chain.")

    print("--- Refactored ---")
    engine = DiscountEngine()
    engine.register("vip", VipDiscount())
    engine.register("employee", EmployeeDiscount())
    print("vip 100 ->", engine.apply("vip", 100.0))
    engine.register("student", StudentDiscount())  # extension, no modification
    print("student 100 ->", engine.apply("student", 100.0))


if __name__ == "__main__":
    run()
