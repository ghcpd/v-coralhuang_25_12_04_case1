import os
import time
import pytest
from user_display_optimized import display_users, filter_users, get_user_by_id


RUN_PERF = os.environ.get("RUN_PERF", "0") == "1"


@pytest.mark.skipif(not RUN_PERF, reason="Performance tests are disabled by default. Set RUN_PERF=1 to run.")
def test_50k_display_filter_lookup():
    # Generate 50k users
    n = 50_000
    users = [
        {
            "id": i,
            "name": f"User{i}",
            "email": f"user{i}@example.com",
            "role": "User",
            "status": "Active" if i % 2 == 0 else "Inactive",
            "join_date": "2023-01-01",
            "last_login": "2025-11-26",
        }
        for i in range(1, n + 1)
    ]

    # display
    t0 = time.perf_counter()
    display_users(users, show_all=False)
    dt = (time.perf_counter() - t0) * 1000
    print(f"display 50k dt={dt:.2f} ms")
    assert dt < 3000, "display 50k must be under 3000ms (adjust this target based on environment)"

    # filter
    t0 = time.perf_counter()
    res = filter_users(users, {"name": "User123"})
    dt = (time.perf_counter() - t0) * 1000
    print(f"filter 50k dt={dt:.2f} ms result={len(res)}")
    assert dt < 2000

    # id lookup
    t0 = time.perf_counter()
    u = get_user_by_id(users, n // 2)
    dt = (time.perf_counter() - t0) * 1000
    print(f"lookup dt={dt:.4f} ms")
    assert u is not None
    assert dt < 50
