from user_display.filters.composite_filter import CompositeFilter
from user_display.filters.regex_filter import RegexFilter


def test_composite_contains(sample_users):
    f = CompositeFilter()
    crit = {"name": {"type": "contains", "value": "User1"}}
    res = [u for u in sample_users if f.matches(u, crit)]
    assert any(u["id"] == 1 for u in res)


def test_composite_exact(sample_users):
    f = CompositeFilter()
    crit = {"status": {"type": "exact", "value": "Active"}}
    res = [u for u in sample_users if f.matches(u, crit)]
    assert all(u["status"] == "Active" for u in res)


def test_regex_filter(sample_users):
    f = RegexFilter()
    crit = {"email": r"user(1|2)@example\.com"}
    res = [u for u in sample_users if f.matches(u, crit)]
    assert len(res) == 2
