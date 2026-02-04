import re
from user_display.store import UserStore


def test_regex_filter(sample_users):
    store = UserStore(sample_users)
    res = store.filter_users({"regex:name": "^A"})
    assert len(res) == 1
    assert res[0]["name"] == "Alice"


def test_case_insensitive_contains(sample_users):
    store = UserStore(sample_users)
    res = store.filter_users({"name": "bob"})
    assert len(res) == 1
    assert res[0]["email"] == "bob@example.com"


def test_composite_filter_multiple_fields(sample_users):
    store = UserStore(sample_users)
    res = store.filter_users({"status": "Active", "role": "User"})
    assert len(res) == 1
    assert res[0]["name"] == "Charlie"
