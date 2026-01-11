"""UserStore - thread-safe, indexed, snapshot-capable user storage.

Design goals:
- O(1) ID lookup via hash index
- Lightweight sharding (partition by id % N) to support concurrent reads
- Snapshot support (shallow copy) for consistent reads
- Optional simple caching for filter results
"""
from threading import RLock
from typing import Any, Dict, Iterable, List, Optional
from .config import get as cfg_get
from .metrics import GLOBAL as METRICS
from .validation.default import DefaultValidator
from .logging_utils import info, debug


class UserStore:
    def __init__(self, users: Iterable[Dict[str, Any]] = (), shard_count: Optional[int] = None):
        self._lock = RLock()
        self._shard_count = shard_count or cfg_get("shard_count")
        # shards as lists; we'll keep an index for O(1) id lookup
        self._shards: List[List[Dict[str, Any]]] = [[] for _ in range(self._shard_count)]
        self._index: Dict[Any, Dict[str, Any]] = {}
        self._validator = DefaultValidator()
        self._filter_cache = {}
        self._fill(users)

    def _fill(self, users: Iterable[Dict[str, Any]]):
        with self._lock:
            for u in users:
                self._add_one(u)

    def _shard_for_id(self, uid: Any) -> int:
        try:
            return int(uid) % self._shard_count
        except Exception:
            return hash(uid) % self._shard_count

    def _add_one(self, u: Dict[str, Any]):
        pv = self._validator.validate_and_recover(u)
        uid = pv.get("id")
        if uid is None:
            METRICS.incr("validation_failures")
            return
        if uid in self._index:
            # update
            self._index[uid].update(pv)
            return
        shard_idx = self._shard_for_id(uid)
        self._shards[shard_idx].append(pv)
        self._index[uid] = pv

    def add(self, u: Dict[str, Any]):
        with self._lock:
            self._add_one(u)

    def size(self) -> int:
        with self._lock:
            return len(self._index)

    def get_by_id(self, uid: Any) -> Optional[Dict[str, Any]]:
        METRICS.incr("id_lookups")
        with self._lock:
            return self._index.get(uid)

    def snapshot(self) -> "UserStore":
        """Return a lightweight copy (shallow) to support consistent concurrent reads."""
        with self._lock:
            new = UserStore(shard_count=self._shard_count)
            # shallow copies are OK for read-only snapshots
            new._shards = [list(s) for s in self._shards]
            new._index = dict(self._index)
            return new

    def _cache_key_for_criteria(self, criteria: Dict[str, Any]) -> Any:
        # Make a deterministic and hashable key even when values are nested dicts.
        def freeze(obj):
            if isinstance(obj, dict):
                return tuple((k, freeze(obj[k])) for k in sorted(obj.keys()))
            if isinstance(obj, list):
                return tuple(freeze(x) for x in obj)
            return obj

        return freeze(criteria)

    def filter(self, criteria: Dict[str, Any], matcher) -> List[Dict[str, Any]]:
        # matcher is any callable taking (user, criteria)->bool
        METRICS.incr("filter_calls")
        key = self._cache_key_for_criteria(criteria)
        with self._lock:
            if key in self._filter_cache:
                METRICS.incr("cache_hits")
                debug("filter cache hit for %s", key)
                return list(self._filter_cache[key])
        # compute without holding lock to allow concurrency; snapshot first
        snap = self.snapshot()
        result = []
        for shard in snap._shards:
            for u in shard:
                try:
                    if matcher(u, criteria):
                        result.append(u)
                except Exception:
                    # robustly skip bad users
                    METRICS.incr("validation_failures")
                    continue

        with self._lock:
            self._filter_cache[key] = list(result)

        METRICS.incr("cache_misses")
        return result
