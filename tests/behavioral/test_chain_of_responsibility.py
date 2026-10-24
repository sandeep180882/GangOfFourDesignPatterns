from patterns.behavioral.chain_of_responsibility.pattern import ExpenseRequest, build_chain


def test_each_level_handles_its_range():
    chain = build_chain()
    for amount, title in [(500, "Manager"), (5_000, "Director"), (20_000, "VP"), (100_000, "CFO")]:
        assert chain.handle(ExpenseRequest("x", amount, "t")).startswith(title)


def test_over_limit_rejected():
    assert chain_result(1_000_000).startswith("REJECTED")


def chain_result(amount):
    return build_chain().handle(ExpenseRequest("x", amount, "t"))
