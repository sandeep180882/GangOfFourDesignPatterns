"""Demo: lazy paginated results."""
from itertools import islice

from patterns.behavioral.iterator.pattern import FakeApi, PaginatedResults


def run() -> None:
    print("=== Iterator: Paginated API Results ===")
    api = FakeApi(total=8, page_size=3)
    results = PaginatedResults(api)
    first_four = list(islice(iter(results), 4))
    print(f"First 4 items: {first_four} (API calls so far: {api.calls})")
    api.calls = 0
    print(f"All items (class iterator): {list(results)} (API calls: {api.calls})")
    api.calls = 0
    print(f"All items (generator):      {list(results.generator())} (API calls: {api.calls})")


if __name__ == "__main__":
    run()
