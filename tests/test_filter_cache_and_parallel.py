from user_display_optimized import filter_users, get_filter_cache_hits

sample_users = [{"id": i, "name": f"User{i}", "email": f"u{i}@x.com", "role": "User", "status": "Active"} for i in range(1, 201)]


def test_filter_caching_and_hits():
    start = get_filter_cache_hits()
    res1 = filter_users(sample_users, {"name": "User1"}, parallel=False)
    res2 = filter_users(sample_users, {"name": "User1"}, parallel=False)
    assert len(res1) == len(res2)
    assert get_filter_cache_hits() >= start + 1


def test_parallel_equals_sequential():
    seq = filter_users(sample_users, {"role": "User"}, parallel=False)
    par = filter_users(sample_users, {"role": "User"}, parallel=True)
    assert seq == par
