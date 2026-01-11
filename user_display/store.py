"""Thread-safe UserStore with indexing, snapshotting, and simple caching."""
from threading import RLock
from copy import deepcopy
from io import StringIO
import time


class UserStore:
    def __init__(self, users=None, validator=None):
        self._lock = RLock()
        self._users = list(users or [])
        self._index = {u.get("id"): u for u in self._users}
        self._validator = validator
        self._last_snapshot = None

    def add(self, user):
        with self._lock:
            if self._validator:
                ok, user = self._validator.validate_and_recover(user)
                if not ok:
                    # import here to avoid circular imports during package init
                    from .errors import ValidationError

                    raise ValidationError("User failed validation and could not be recovered")
            uid = user.get("id")
            self._users.append(user)
            self._index[uid] = user

    def get_by_id(self, uid):
        # O(1) lookup
        return self._index.get(uid)

    def snapshot(self):
        with self._lock:
            self._last_snapshot = deepcopy(self._users)
            return self._last_snapshot

    def all(self):
        with self._lock:
            return list(self._users)

    def size(self):
        with self._lock:
            return len(self._users)
