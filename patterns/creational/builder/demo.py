from patterns.creational.builder.pattern import QueryBuilder, QueryDirector


def run() -> None:
    print("=== Builder: SQL Query Builder ===")

    q = (
        QueryBuilder()
        .select("name", "email")
        .from_("users")
        .where("age > ?", 30)
        .where("country = ?", "IN")
        .order_by("name")
        .limit(5)
        .build()
    )
    print("Fluent build :", q.sql)
    print("Parameters   :", q.params)

    d = QueryDirector().recent_orders(customer_id=42, count=3)
    print("Via Director :", d.sql)
    print("Parameters   :", d.params)

    try:
        QueryBuilder().select("id").build()
    except ValueError as exc:
        print("Invalid build rejected:", exc)


if __name__ == "__main__":
    run()
