from user_display import UserStore


def test_userstore_lookup_and_snapshot():
    users = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
    s = UserStore(users)
    assert s.get_user_by_id(1)["name"] == "A"
    snap = s.snapshot()
    # mutate original
    s.add_user({"id": 3, "name": "C"})
    assert len(s) == 3
    # snapshot remains unchanged
    assert len(snap) == 2
    assert snap.get_user_by_id(3) is None


def test_userstore_all_users_returns_copy():
    users = [{"id": 10}, {"id": 20}]
    s = UserStore(users)
    all1 = s.all_users()
    all1.append({"id": 30})
    assert len(s) == 2
