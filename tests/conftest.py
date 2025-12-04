import random
import pytest


def make_user(i: int):
    return {
        "id": i,
        "name": f"User{i}",
        "email": f"user{i}@example.com",
        "role": random.choice(["Admin", "User", "Mod"]),
        "status": random.choice(["Active", "Inactive"]),
        "join_date": "2023-01-01",
        "last_login": "2025-11-26",
    }


@pytest.fixture
def sample_users():
    return [
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "role": "Admin",
            "status": "Active",
            "join_date": "2023-01-01",
            "last_login": "2025-11-26",
        },
        {
            "id": 2,
            "name": "Bob",
            "email": "bob@example.com",
            "role": "User",
            "status": "Inactive",
            "join_date": "2023-01-01",
            "last_login": "2025-11-25",
        },
        {
            "id": 3,
            "name": "Charlie",
            "email": "charlie@example.com",
            "role": "User",
            "status": "Active",
            "join_date": "2023-01-02",
            "last_login": "2025-11-20",
        },
    ]


@pytest.fixture(scope="session")
def large_users():
    random.seed(0)
    return [make_user(i) for i in range(1, 50001)]
