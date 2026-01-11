import os
import sys
import pytest

# Ensure the repository root is on sys.path so tests can import the package
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture
def sample_users():
    # small deterministic sample for unit tests
    roles = ["Admin", "User", "Mod"]
    users = []
    for i in range(1, 201):
        users.append(
            {
                "id": i,
                "name": f"User{i}",
                "email": f"user{i}@example.com",
                "role": roles[i % len(roles)],
                "status": "Active" if i % 2 == 0 else "Inactive",
                "join_date": "2023-01-01",
                "last_login": "2025-11-26",
            }
        )
    return users
