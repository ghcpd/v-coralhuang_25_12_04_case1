import threading
from typing import Dict, Any, Iterable, Optional


class UserIndex:
    """Hash-based index for O(1) lookups by id, with optional sharding."""

    def __init__(self, users: Iterable[Dict[str, Any]], shard_count: int = 1):
        self._shard_count = max(shard_count, 1)
        self._shards: Dict[int, Dict[Any, Dict[str, Any]]] = {i: {} for i in range(self._shard_count)}
        self._lock = threading.RLock()
        self._build(users)

    def _build(self, users: Iterable[Dict[str, Any]]):
        for u in users:
            uid = u.get("id")
            if uid is None:
                continue
            shard_id = self._compute_shard(uid)
            self._shards[shard_id][uid] = u

    def _compute_shard(self, uid: Any) -> int:
        return hash(uid) % self._shard_count

    def get(self, uid: Any) -> Optional[Dict[str, Any]]:
        shard_id = self._compute_shard(uid)
        return self._shards.get(shard_id, {}).get(uid)

    def snapshot(self) -> "UserIndex":
        with self._lock:
            clone = UserIndex([], shard_count=self._shard_count)
            clone._shards = {sid: dict(shard) for sid, shard in self._shards.items()}
        return clone

    def __len__(self):
        return sum(len(shard) for shard in self._shards.values())
