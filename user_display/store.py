import threading
import os
from typing import Any, Dict, Iterable, List, Optional, Tuple
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
import math

from .config import Config
from .logging_utils import get_logger
from .metrics import Metrics
from .errors import ValidationError
from .index import UserIndex
from .plugins import get_formatter, get_filter

# Ensure built-in formatters/filters/validators are registered
from . import formatters as _fmt  # noqa: F401
from . import filters as _flt  # noqa: F401
from . import validation as _val  # noqa: F401
from .validation.default import DefaultValidator
from .filters.composite_filter import CompositeFilter


class UserStore:
    """Thread-safe storage with id indexing, caching, and snapshots."""

    def __init__(
        self,
        users: Iterable[Dict[str, Any]],
        config: Optional[Config] = None,
        validator: Optional[Any] = None,
        metrics: Optional[Metrics] = None,
        logger=None,
    ):
        self.config = config or Config()
        self.metrics = metrics or Metrics()
        self.logger = logger or get_logger(level=self.config.log_level)
        self._lock = threading.RLock()
        self._version = 0
        self._validator = validator or DefaultValidator(strict=self.config.strict_validation, metrics=self.metrics)

        validated_users = tuple(self._validate_all(users))
        self._users: Tuple[Dict[str, Any], ...] = validated_users
        shard_count = self._compute_shard_count(len(self._users))
        self._index = UserIndex(self._users, shard_count=shard_count)
        self._indexed_fields = ("status", "role")
        self._field_index = self._build_field_index(self._indexed_fields)
        self._filter_cache: "OrderedDict[Any, List[Dict[str, Any]]]" = OrderedDict()

    def _compute_shard_count(self, n: int) -> int:
        if n <= 1000:
            return 1
        return min(32, max(2, n // 5000))

    def _validate_all(self, users: Iterable[Dict[str, Any]]):
        for u in users:
            try:
                yield self._validator.validate(u)
            except ValidationError as exc:
                self.metrics.incr("validation_failures")
                self.logger.warning(
                    "Validation failed",
                    extra={"user": u, "error": str(exc)},
                )
                continue

    def _build_field_index(self, fields):
        idx = {f: {} for f in fields}
        for u in self._users:
            for f in fields:
                val = u.get(f)
                if val is None:
                    continue
                idx[f].setdefault(val, []).append(u)
        return idx

    def snapshot(self) -> "UserStore":
        with self._lock:
            clone = UserStore([], config=self.config, validator=self._validator, metrics=self.metrics, logger=self.logger)
            clone._users = self._users
            clone._index = self._index.snapshot()
            clone._filter_cache = OrderedDict(self._filter_cache)
            clone._version = self._version
        return clone

    def clone(self) -> "UserStore":
        return self.snapshot()

    # ---- core operations ----
    def get_user_by_id(self, uid: Any) -> Optional[Dict[str, Any]]:
        return self._index.get(uid)

    def filter_users(self, criteria: Dict[str, Any], parallel: Optional[bool] = None, cache: bool = True):
        parallel = self.config.parallel_filtering if parallel is None else parallel
        cache_key = None
        if cache:
            cache_key = self._cache_key(criteria, parallel)
            cached = self._filter_cache_get(cache_key)
            if cached is not None:
                self.metrics.incr("filter_cache_hit")
                return cached
        filter_obj = self._criteria_to_filter(criteria)
        with self.metrics.timer("filter_users"):
            # exact-match fast path using secondary index
            if self._can_use_index(criteria):
                res = self._filter_with_index(criteria)
            else:
                candidates = self._select_candidates(criteria) or self._users
                if parallel:
                    res = self._filter_parallel(filter_obj, candidates)
                else:
                    res = [u for u in candidates if filter_obj.match(u)]
        if cache and cache_key is not None:
            self._filter_cache_put(cache_key, res)
        return res

    def display_users(
        self,
        formatter_name: Optional[str] = None,
        fields: Optional[List[str]] = None,
        show_all: bool = True,
        verbose: bool = False,
        parallel: Optional[bool] = None,
        include_metrics: bool = False,
    ) -> str:
        fmt_name = formatter_name or self.config.default_formatter
        formatter_factory = get_formatter(fmt_name)
        formatter = formatter_factory(fields=fields, config=self.config)
        if verbose:
            self.logger.info("BEGIN_DISPLAY", extra={"count": len(self._users)})
        with self.metrics.timer("display_users"):
            out = formatter.format_many(self._users, show_all=show_all, metrics=self.metrics)
        if include_metrics:
            out += "\nMETRICS=" + str(self.metrics.snapshot())
        return out

    def export_users_to_string(self) -> str:
        # Reuse formatter for export; could also implement dedicated exporter
        from .formatters.json_fmt import JsonFormatter  # lazy import

        formatter = JsonFormatter(fields=None, config=self.config)
        with self.metrics.timer("export_users"):
            return formatter.export(self._users)

    # ---- helpers ----
    def _criteria_to_filter(self, criteria: Dict[str, Any]):
        return CompositeFilter.from_criteria(criteria)

    def _cache_key(self, criteria: Dict[str, Any], parallel: bool) -> Tuple:
        # sort items for deterministic key; convert unhashable values to str
        items = []
        for k, v in sorted(criteria.items()):
            try:
                hash(v)
                hv = v
            except Exception:
                hv = str(v)
            items.append((k, hv))
        return (tuple(items), parallel)

    def _filter_cache_get(self, key):
        with self._lock:
            if key in self._filter_cache:
                val = self._filter_cache.pop(key)
                # reinsert to mark as recently used
                self._filter_cache[key] = val
                return val
            return None

    def _filter_cache_put(self, key, value):
        with self._lock:
            self._filter_cache[key] = value
            if len(self._filter_cache) > self.config.filter_cache_size:
                self._filter_cache.popitem(last=False)

    def _filter_parallel(self, filter_obj, candidates=None):
        workers = self.config.max_workers or min(32, os.cpu_count() or 4)
        data = tuple(candidates) if candidates is not None else self._users
        n = len(data)
        if n == 0:
            return []
        chunk_size = math.ceil(n / workers)
        slices = [data[i : i + chunk_size] for i in range(0, n, chunk_size)]
        results: List[Dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for chunk_res in executor.map(lambda chunk: [u for u in chunk if filter_obj.match(u)], slices):
                results.extend(chunk_res)
        return results

    def _can_use_index(self, criteria: Dict[str, Any]) -> bool:
        # Only equality criteria on indexed fields (no regex keys)
        if any(k.startswith("regex:") for k in criteria):
            return False
        return all(k in self._indexed_fields for k in criteria.keys())

    def _filter_with_index(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Intersect candidate lists by id for each criterion
        candidate_lists = []
        for field, val in criteria.items():
            candidates = self._field_index.get(field, {}).get(val)
            if not candidates:
                return []
            candidate_lists.append(candidates)
        if not candidate_lists:
            return []
        # choose smallest list as base for deterministic ordering
        base = min(candidate_lists, key=len)
        other_ids = [
            {u.get("id") for u in lst}
            for lst in candidate_lists
            if lst is not base
        ]
        result = []
        for u in base:
            uid = u.get("id")
            if all(uid in ids for ids in other_ids):
                result.append(u)
        return result

    def _select_candidates(self, criteria: Dict[str, Any]):
        # Use single indexed field to reduce search space
        for field in self._indexed_fields:
            if field in criteria:
                val = criteria[field]
                candidates = self._field_index.get(field, {}).get(val)
                if candidates:
                    return candidates
        return None

    def all_users(self):
        return list(self._users)
