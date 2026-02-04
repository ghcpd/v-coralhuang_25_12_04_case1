"""UserStore: thread-safe store with indexing, snapshotting and caching"""
from threading import RLock
from copy import deepcopy
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor


class UserStore:
    """Thread-safe user store with O(1) id lookup and snapshot support.

    Built to be lightweight and ready for future sharding/indexing.
    """
    def __init__(self, users=None, max_workers=4):
        self._lock = RLock()
        self._users = list(users) if users else []
        self._index = {}
        self._build_index()
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def _build_index(self):
        self._index = {u.get('id'): u for u in self._users if u.get('id') is not None}

    def add_user(self, user):
        with self._lock:
            self._users.append(user)
            uid = user.get('id')
            if uid is not None:
                self._index[uid] = user

    def get_user_by_id(self, uid):
        # O(1) lookup
        with self._lock:
            return self._index.get(uid)

    def snapshot(self):
        """Return a consistent immutable snapshot (deep copy) of users."""
        with self._lock:
            return deepcopy(self._users)

    def all_users(self):
        with self._lock:
            return list(self._users)

    def size(self):
        with self._lock:
            return len(self._users)

    def replace_all(self, users):
        with self._lock:
            self._users = list(users)
            self._build_index()

    def parallel_filter(self, predicate, users=None):
        """Apply predicate to users in parallel using ThreadPoolExecutor."""
        users = users if users is not None else self.all_users()
        futures = [self._executor.submit(predicate, u) for u in users]
        results = []
        for u, f in zip(users, futures):
            try:
                ok = f.result()
            except Exception:
                ok = False
            if ok:
                results.append(u)
        return results

    def close(self):
        try:
            self._executor.shutdown(wait=False)
        except Exception:
            pass

