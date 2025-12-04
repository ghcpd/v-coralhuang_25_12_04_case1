import time
from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string


def make_users(n):
    return [
        {
            "id": i,
            "name": f"User{i}",
            "email": f"user{i}@example.com",
            "role": "User" if i % 3 else "Admin",
            "status": "Active" if i % 2 else "Inactive",
            "join_date": "2023-01-01",
            "last_login": "2025-11-26",
        }
        for i in range(1, n + 1)
    ]


def test_display_and_lookup():
    users = make_users(100)
    out = display_users(users, show_all=True, verbose=False)
    assert "PROCESSED=" in out
    u = get_user_by_id(users, 10)
    assert u and u["id"] == 10


def test_filter():
    users = make_users(100)
    res = filter_users(users, {"role": "Admin"})
    assert all(u["role"] == "Admin" for u in res)


def test_export_json():
    users = make_users(10)
    out = export_users_to_string(users, fmt="json")
    assert "\"users\"" in out


def test_perf_50k():
    users = make_users(50000)
    t0 = time.time()
    _ = display_users(users, show_all=False)
    t1 = time.time()
    display_ms = (t1 - t0) * 1000
    # best-effort check: should be under a few seconds in CI; strict limits may vary
    assert display_ms < 5000
