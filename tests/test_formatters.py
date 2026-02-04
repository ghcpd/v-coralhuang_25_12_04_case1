from user_display_optimized import display_users
import json

sample_users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "Admin", "status": "Active", "join_date": "2023-01-01", "last_login": "2025-11-26"},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "User", "status": "Inactive", "join_date": "2023-02-01", "last_login": "2025-10-01"},
]


def test_compact_formatter_default():
    out = display_users(sample_users)
    assert "ID=1" in out and "PROCESSED=2" in out


def test_json_formatter():
    out = display_users(sample_users, formatter="json")
    parsed = json.loads(out)
    assert parsed["count"] == 2
    assert isinstance(parsed["users"], list)


def test_table_formatter_and_field_selection():
    out = display_users(sample_users, formatter="table", fields=["id", "name"])
    assert "ID" in out and "NAME" in out
    assert "PROCESSED=2" in out
