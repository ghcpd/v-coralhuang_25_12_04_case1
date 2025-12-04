import json
from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string
from user_display.store import UserStore


def test_display_users_compact(sample_users):
    out = display_users(sample_users, show_all=True)
    assert "PROCESSED=3" in out
    assert "ID=1" in out


def test_get_user_by_id(sample_users):
    u = get_user_by_id(sample_users, 2)
    assert u["name"] == "Bob"


def test_filter_users_criteria(sample_users):
    res = filter_users(sample_users, {"status": "Active"})
    assert len(res) == 2


def test_export_users_json(sample_users):
    out = export_users_to_string(sample_users)
    assert out.startswith("EXPORT_BEGIN")
    assert out.strip().endswith("EXPORT_END")
    payload = out.split("\n", 2)[2]  # after header line
    data = json.loads(payload.split("\nEXPORT_END", 1)[0])
    assert isinstance(data, list)
    assert len(data) == 3


def test_userstore_snapshot(sample_users):
    store = UserStore(sample_users)
    snap = store.snapshot()
    assert snap.get_user_by_id(1)["name"] == "Alice"
    assert store.get_user_by_id(1) is snap.get_user_by_id(1)
