import threading
from user_display.store import UserStore


def test_parallel_filter_matches_sequential(sample_users):
    store = UserStore(sample_users)
    sequential = store.filter_users({"status": "Active"}, parallel=False)
    parallel = store.filter_users({"status": "Active"}, parallel=True)
    assert sequential == parallel


def test_snapshot_thread_safe(sample_users):
    store = UserStore(sample_users)
    results = []

    def worker():
        snap = store.snapshot()
        results.append(snap.get_user_by_id(1)["name"])

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(name == "Alice" for name in results)
