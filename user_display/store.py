"""
High-performance user storage with O(1) lookups and sharding.
Includes MVCC-like snapshotting for concurrent reads.
"""

import threading
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict
import time
from .config import get_config
from .metrics import get_metrics
from .logging_utils import get_logger
from .validation import DefaultValidator
from .errors import StorageError


logger = get_logger("UserStore")
metrics = get_metrics()


class UserSnapshot:
    """Immutable snapshot of user data at a point in time (MVCC)."""

    def __init__(self, users: List[Dict[str, Any]], timestamp: float):
        self.users = users.copy()
        self.timestamp = timestamp
        self._index: Dict[Any, int] = {}  # Build index
        for i, user in enumerate(self.users):
            user_id = user.get("id")
            if user_id is not None:
                self._index[user_id] = i

    def get_by_id(self, uid: Any) -> Optional[Dict[str, Any]]:
        """Get user by ID from snapshot."""
        idx = self._index.get(uid)
        if idx is not None:
            return self.users[idx].copy()
        return None

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all users from snapshot."""
        return [u.copy() for u in self.users]


class UserStore:
    """Thread-safe user storage with efficient indexing and sharding."""

    def __init__(self, shard_count: int = 8, validator: Optional[Any] = None):
        self.shard_count = shard_count
        self.validator = validator or DefaultValidator()
        self._shards: List[Dict[Any, Dict[str, Any]]] = [
            {} for _ in range(shard_count)
        ]
        self._id_to_shard: Dict[Any, int] = {}  # Quick shard lookup
        self._lock = threading.RLock()
        self._snapshots: List[UserSnapshot] = []
        self._max_snapshots = 5
        self.created_at = time.time()
        logger.info("UserStore initialized", shard_count=shard_count)

    def _get_shard_id(self, uid: Any) -> int:
        """Get shard ID for user ID using hash."""
        return hash(uid) % self.shard_count

    def add_user(self, user: Dict[str, Any]) -> None:
        """Add or update a user."""
        with self._lock:
            uid = user.get("id")
            if uid is None:
                raise StorageError("User must have 'id' field")

            # Validate and repair
            config = get_config()
            if config.get("validate_on_insert"):
                is_valid, error = self.validator.validate(user)
                if not is_valid:
                    if config.get("soft_fail_on_validation"):
                        logger.warning("Validation failed, repairing", error=error, user_id=uid)
                        metrics.record_validation_warning()
                        user = self.validator.repair(user)
                    else:
                        logger.error("Validation failed", error=error, user_id=uid)
                        metrics.record_validation_error()
                        raise StorageError(f"Validation failed: {error}")

            shard_id = self._get_shard_id(uid)
            self._shards[shard_id][uid] = user.copy()
            self._id_to_shard[uid] = shard_id
            metrics.record_shard_access(shard_id)

    def get_user(self, uid: Any) -> Optional[Dict[str, Any]]:
        """Get user by ID (O(1) lookup)."""
        start_time = time.time()
        with self._lock:
            shard_id = self._id_to_shard.get(uid)
            if shard_id is None:
                duration_ms = (time.time() - start_time) * 1000
                metrics.record_lookup_operation(duration_ms)
                return None

            metrics.record_shard_access(shard_id)
            result = self._shards[shard_id].get(uid)
            duration_ms = (time.time() - start_time) * 1000
            metrics.record_lookup_operation(duration_ms)
            return result.copy() if result else None

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        with self._lock:
            result = []
            for shard in self._shards:
                result.extend(u.copy() for u in shard.values())
            return result

    def remove_user(self, uid: Any) -> bool:
        """Remove a user. Returns True if user existed."""
        with self._lock:
            shard_id = self._id_to_shard.get(uid)
            if shard_id is None:
                return False

            del self._shards[shard_id][uid]
            del self._id_to_shard[uid]
            return True

    def user_count(self) -> int:
        """Get total user count."""
        with self._lock:
            return sum(len(shard) for shard in self._shards)

    def create_snapshot(self) -> UserSnapshot:
        """Create an immutable snapshot of current state."""
        with self._lock:
            all_users = self.get_all_users()
            snapshot = UserSnapshot(all_users, time.time())
            self._snapshots.append(snapshot)
            
            # Keep only last N snapshots
            if len(self._snapshots) > self._max_snapshots:
                self._snapshots.pop(0)
            
            return snapshot

    def get_latest_snapshot(self) -> Optional[UserSnapshot]:
        """Get latest snapshot."""
        with self._lock:
            return self._snapshots[-1] if self._snapshots else None

    def clone(self) -> "UserStore":
        """Create a deep copy of the store."""
        with self._lock:
            new_store = UserStore(self.shard_count, self.validator)
            for user in self.get_all_users():
                new_store.add_user(user)
            return new_store

    def stats(self) -> Dict[str, Any]:
        """Get store statistics."""
        with self._lock:
            return {
                "total_users": self.user_count(),
                "shard_count": self.shard_count,
                "shard_sizes": [len(shard) for shard in self._shards],
                "snapshot_count": len(self._snapshots),
                "created_at": self.created_at,
            }
