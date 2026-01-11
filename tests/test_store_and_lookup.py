from user_display.store import UserStore
from user_display.validation.default import DefaultValidator


def test_userstore_basic(sample_users):
    s = UserStore(sample_users)
    assert s.size() == len(sample_users)
    # id lookup
    u = s.get_by_id(5)
    assert u and u["id"] == 5


def test_add_and_snapshot(sample_users):
    s = UserStore(sample_users)
    s.add({"id": 9999, "name": "NewUser"})
    assert s.get_by_id(9999)["name"] == "NewUser"
    snap = s.snapshot()
    assert snap.get_by_id(9999)["name"] == "NewUser"


def test_validator_handles_bad_id():
    v = DefaultValidator()
    u = {"id": "bad", "name": "N"}
    r = v.validate_and_recover(u)
    assert r.get("id") is None
