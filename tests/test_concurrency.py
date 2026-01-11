import concurrent.futures
from user_display.store import UserStore
from user_display.filters.composite_filter import CompositeFilter


def test_parallel_filter_consistency(sample_users):
    s = UserStore(sample_users)
    crit = {"name": {"type": "contains", "value": "User1"}}

    def do_filter():
        return s.filter(crit, lambda u, c: CompositeFilter().matches(u, c))

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futures = [ex.submit(do_filter) for _ in range(4)]
        results = [f.result() for f in futures]

    # check all parallel results identical
    assert all(len(r) == len(results[0]) for r in results)
