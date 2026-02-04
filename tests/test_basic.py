import time
from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string
from user_display import UserStore


def make_users(n):
    users = []
    for i in range(1, n+1):
        users.append({'id': i, 'name': f'User{i}', 'email': f'user{i}@example.com', 'role': 'User', 'status':'Active', 'join_date':'2023-01-01','last_login':'2025-11-26'})
    return users


def test_lookup_and_display():
    users = make_users(100)
    out = display_users(users, show_all=True, formatter='compact')
    assert 'PROCESSED=100' in out
    u = get_user_by_id(users, 10)
    assert u['id'] == 10


def test_filtering():
    users = make_users(50)
    res = filter_users(users, {'name':'User1'})
    assert any(u['id']==1 for u in res)


def test_export_json_and_table():
    users = make_users(10)
    s1 = export_users_to_string(users, formatter='json')
    assert s1.strip().startswith('[')
    s2 = export_users_to_string(users, formatter='table')
    assert 'User1' in s2
