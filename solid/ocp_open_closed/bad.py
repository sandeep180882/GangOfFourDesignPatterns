"""OCP violation: every new customer type means editing this function."""


class DiscountEngine:
    def apply(self, customer_type: str, amount: float) -> float:
        # Each new customer type forces a modification here (and re-testing
        # every existing branch).
        if customer_type == "regular":
            return amount
        elif customer_type == "vip":
            return amount * 0.8
        elif customer_type == "employee":
            return amount * 0.7
        raise ValueError(f"unknown customer type: {customer_type}")
