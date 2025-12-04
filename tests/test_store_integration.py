from user_display import UserStore
from user_display_optimized import get_user_by_id


def test_get_user_by_id_with_store():
    users = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
    s = UserStore(users)
    assert get_user_by_id(s, 2)["name"] == "B"
    assert get_user_by_id(s, 999) is None
