from patterns.behavioral.iterator.pattern import FakeApi, PaginatedResults


def test_iterates_all_items_both_styles():
    results = PaginatedResults(FakeApi(total=7, page_size=3))
    expected = [f"item-{i}" for i in range(1, 8)]
    assert list(results) == expected
    assert list(results.generator()) == expected


def test_lazy_fetching():
    api = FakeApi(total=10, page_size=3)
    it = iter(PaginatedResults(api))
    assert api.calls == 0
    next(it)
    assert api.calls == 1
    for _ in range(3):
        next(it)
    assert api.calls == 2


def test_empty_source():
    assert list(PaginatedResults(FakeApi(total=0))) == []
