import time
from user_display_optimized import display_users, filter_users, get_user_by_id


def make_users(n):
    users = []
    for i in range(1, n+1):
        users.append({'id': i, 'name': f'User{i}', 'email': f'user{i}@example.com', 'role': 'User', 'status':'Active', 'join_date':'2023-01-01','last_login':'2025-11-26'})
    return users


def test_lookup_perf():
    users = make_users(50000)
    start = time.time()
    u = get_user_by_id(users, 49999)
    elapsed = (time.time()-start)*1000
    print('lookup ms', elapsed)
    # allow slight overhead on some Windows hosts; index construction is O(n)
    assert elapsed < 12.0, f'lookup too slow: {elapsed}ms'


def test_display_perf():
    users = make_users(50000)
    start = time.time()
    s = display_users(users, show_all=False, formatter='compact')
    elapsed = (time.time()-start)*1000
    print('display ms', elapsed)
    assert elapsed < 250.0, f'display too slow: {elapsed}ms'


def test_filter_perf():
    users = make_users(50000)
    start = time.time()
    res = filter_users(users, {'name':'User49999'}, parallel=False)
    elapsed = (time.time()-start)*1000
    print('filter ms', elapsed)
    # substring matching should be fast, but allow some margin on CI hosts
    assert elapsed < 250.0, f'filter too slow: {elapsed}ms'
