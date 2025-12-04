from user_display.store import UserStore


def test_compact_formatter_fields(sample_users):
    store = UserStore(sample_users)
    out = store.display_users(formatter_name="compact", fields=["id", "name"], show_all=False)
    lines = out.strip().split("\n")
    assert lines[0] == "ID=1 | NAME=Alice"


def test_json_formatter(sample_users):
    store = UserStore(sample_users)
    out = store.display_users(formatter_name="json", show_all=True)
    assert "processed" in out  # metadata appended


def test_table_formatter(sample_users):
    store = UserStore(sample_users)
    out = store.display_users(formatter_name="table", fields=["id", "name"], show_all=True)
    assert "PROCESSED=3" in out
