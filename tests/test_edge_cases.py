from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string


def test_missing_fields_display_and_filter():
    users = [{"id": 1, "name": None}, {"email": "noid@example.com"}, "notadict"]
    out = display_users(users)
    assert "ID=1" in out
    # missing id user should not break filter
    res = filter_users(users, {"name": ""})
    assert isinstance(res, list)


def test_get_user_by_id_malformed_returns_none():
    users = [{"id": 1}, {"id": None}, {"name": "X"}]
    assert get_user_by_id(users, None) is None


def test_export_fallback_for_bad_date():
    users = [{"id": 1, "last_login": "bad-date"}]
    out = export_users_to_string(users)
    assert "LastLoginParsed: 0.0" in out
