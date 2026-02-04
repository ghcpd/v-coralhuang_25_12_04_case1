import os
import time
import pytest
from user_display_optimized import display_users, filter_users, get_user_by_id

RUN_PERF = os.environ.get("RUN_PERF", "0") == "1"


@pytest.mark.skipif(not RUN_PERF, reason="Performance tests disabled by default")
def test_performance_50k():
    n = 50000
    users = [{"id": i, "name": f"U{i}", "email": f"u{i}@x.com", "role": "User", "status": "Active", "join_date": "2023-01-01", "last_login": "2025-01-01"} for i in range(1, n + 1)]

    # Display
    t0 = time.time()
    display_users(users)
    dt_display = (time.time() - t0) * 1000

    # Filter
    t1 = time.time()
    filter_users(users, {"role": "User"}, parallel=False)
    dt_filter = (time.time() - t1) * 1000

    # Lookup
    t2 = time.time()
    u = get_user_by_id(users, n - 1)
    dt_lookup = (time.time() - t2) * 1000

    print(f"display={dt_display:.2f}ms filter={dt_filter:.2f}ms lookup={dt_lookup:.2f}ms")
    assert dt_display < 120.0
    assert dt_filter < 15.0
    assert dt_lookup < 0.5
