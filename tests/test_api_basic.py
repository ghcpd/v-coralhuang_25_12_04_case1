import pytest
from user_display_optimized import (
    display_users,
    get_user_by_id,
    filter_users,
    export_users_to_string,
)

sample_users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "Admin", "status": "Active", "join_date": "2023-01-01", "last_login": "2025-11-26"},
    {"id": 2, "name": "bob", "email": "bob@example.com", "role": "User", "status": "Inactive", "join_date": "2023-02-01", "last_login": "2025-10-01"},
    {"id": 3, "name": "Carol", "email": "carol@example.com", "role": "Mod", "status": "Active", "join_date": "2023-03-01", "last_login": "2025-09-15"},
]


def test_display_users_basic():
    out = display_users(sample_users, show_all=True, verbose=False)
    assert "ID=1" in out
    assert "NAME=Alice" in out or "NAME=bob" in out
    assert "PROCESSED=3" in out


def test_get_user_by_id_found_and_not_found():
    u = get_user_by_id(sample_users, 2)
    assert isinstance(u, dict)
    assert u.get("id") == 2
    assert get_user_by_id(sample_users, 999) is None


def test_filter_users_criteria():
    # name search should be case-insensitive like baseline
    res = filter_users(sample_users, {"name": "ali"})
    assert len(res) == 1 and res[0]["id"] == 1
    # role exact match
    res2 = filter_users(sample_users, {"role": "User"})
    assert len(res2) == 1 and res2[0]["id"] == 2


def test_export_users_to_string_basic():
    out = export_users_to_string(sample_users)
    assert out.startswith("EXPORT_BEGIN")
    assert "UserID: 1" in out
    assert "LastLoginParsed" in out
