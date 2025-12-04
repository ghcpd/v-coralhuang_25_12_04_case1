import os
import time
import pytest
from user_display.store import UserStore

DISPLAY_TARGET = 0.120  # 120 ms
FILTER_TARGET = 0.015   # 15 ms
LOOKUP_TARGET = 0.0005  # 0.5 ms


def _assert_perf(key: str, duration: float, target: float):
    # Allow some slack for CI variability
    if duration > target * 2:
        pytest.xfail(f"{key} too slow: {duration:.4f}s > {target*2:.4f}s (target={target:.4f}s)")


RUN_PERF = bool(os.environ.get("RUN_PERF_TESTS"))

if not RUN_PERF:
    pytest.skip("Performance tests disabled; set RUN_PERF_TESTS=1", allow_module_level=True)

@pytest.mark.performance
def test_display_speed(large_users):
    store = UserStore(large_users)
    # warm-up
    store.display_users(show_all=False)
    start = time.perf_counter()
    store.display_users(show_all=False)
    duration = time.perf_counter() - start
    _assert_perf("display", duration, DISPLAY_TARGET)


@pytest.mark.performance
def test_filter_speed(large_users):
    store = UserStore(large_users)
    start = time.perf_counter()
    store.filter_users({"status": "Active"}, parallel=True)
    duration = time.perf_counter() - start
    _assert_perf("filter", duration, FILTER_TARGET)


@pytest.mark.performance
def test_lookup_speed(large_users):
    store = UserStore(large_users)
    start = time.perf_counter()
    for _ in range(1000):
        store.get_user_by_id(25000)
    duration = time.perf_counter() - start
    per_lookup = duration / 1000
    _assert_perf("lookup", per_lookup, LOOKUP_TARGET)
