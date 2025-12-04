import os
from user_display_optimized import display_users, get_user_by_id, filter_users, export_users_to_string


def test_display_and_lookup_and_filter(sample_users):
    s = sample_users[:200]
    s_str = display_users(s, show_all=True, verbose=False)
    assert "PROCESSED=" in s_str

    u = get_user_by_id(s, 3)
    assert u and u["id"] == 3

    res = filter_users(s, {"name": "User1", "status": "Active"})
    # should include at least user 10 (User10) and other matches
    assert any("User1" in u["name"] for u in res)

    out = export_users_to_string(s[:5])
    assert out.startswith("EXPORT_BEGIN") and out.endswith("EXPORT_END\n")
