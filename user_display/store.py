"""UserStore: basic storage, O(1) ID index, snapshot/clone support.

This is an incremental, tested building block for the full refactor.
"""
from typing import List, Dict, Any, Optional
from threading import RLock
from copy import deepcopy


class UserStore:
    def __init__(self, users: List[Dict[str, Any]] = None):
        self._lock = RLock()
        self._users = list(users or [])
        self._build_index()

    def _build_index(self):
        self._id_map = {u.get("id"): u for u in self._users if isinstance(u, dict) and "id" in u}

    def add_user(self, user: Dict[str, Any]):
        with self._lock:
            self._users.append(user)
            self._id_map[user.get("id")] = user

    def get_user_by_id(self, uid: Any) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._id_map.get(uid)

    def snapshot(self) -> "UserStore":
        """Return a consistent shallow snapshot (copy-on-write friendly)."""
        with self._lock:
            clone = UserStore(self._users.copy())
        return clone

    def all_users(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._users)

    def __len__(self):
        with self._lock:
            return len(self._users)
