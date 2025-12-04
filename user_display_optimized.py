"""Compatibility wrapper providing optimized implementations of the original API.

This is an incremental, minimal-safe implementation intended to preserve the
public API while removing nondeterminism and performance anti-patterns. More
features (UserStore, formatters, plugins, caching, parallel filtering) will be
added iteratively with tests.
"""
from io import StringIO
from datetime import datetime
from functools import lru_cache
from typing import List, Dict, Any, Optional


def display_users(users: List[Dict[str, Any]], show_all: bool = True, verbose: bool = False, formatter: Optional[str] = None, fields: Optional[List[str]] = None) -> str:
    """Return a human-readable summary for a list of users.

    New optional arguments:
      - formatter: 'compact' (default), 'json', or 'table' or Formatter instance
      - fields: list of fields to include when supported by the formatter

    Preserves original API when called with only (users, show_all, verbose).
    """
    # backward compatible default
    fmt_name = formatter or "compact"

    # Lazy import of formatters to avoid cycles
    from user_display.formatters import CompactFormatter, JsonFormatter, TableFormatter

    if fmt_name == "compact":
        fmt = CompactFormatter()
    elif fmt_name == "json":
        fmt = JsonFormatter()
    elif fmt_name == "table":
        fmt = TableFormatter()
    elif hasattr(formatter, "format"):
        fmt = formatter  # assume Formatter-like instance
    else:
        fmt = CompactFormatter()

    # Delegate formatting; pass show_all and fields if provided
    return fmt.format(list(users), fields=fields, show_all=show_all)



def get_user_by_id(users: List[Dict[str, Any]], uid: Any) -> Optional[Dict[str, Any]]:
    """Efficient deterministic lookup by id.

    Builds a local hash-map for O(1) lookup within the call. Returns None if
    not found. Malformed entries are ignored.
    """
    if not users:
        return None

    # If a UserStore is passed, delegate to its efficient index
    try:
        from user_display import UserStore
    except Exception:
        UserStore = None

    if UserStore and isinstance(users, UserStore):
        return users.get_user_by_id(uid)

    mapping = {u.get("id"): u for u in users if isinstance(u, dict) and u.get("id") is not None}
    return mapping.get(uid)


# Simple in-memory cache for filter results keyed by user ids tuple and frozenset of criteria
_filter_cache = {}
_filter_cache_hits = 0


def filter_users(users: List[Dict[str, Any]], criteria: Dict[str, Any], parallel: bool = False) -> List[Dict[str, Any]]:
    """Single-pass deterministic filter preserving baseline semantics with
    optional parallel execution and simple caching for repeated queries.

    - name: case-insensitive substring
    - email: case-sensitive substring
    - role/status: exact match
    """
    global _filter_cache_hits
    if not criteria:
        return list(users)

    # Build cache key: tuple of user ids (preserves order) and criteria frozenset
    ids_key = tuple(u.get("id") for u in users if isinstance(u, dict) and u.get("id") is not None)
    crit_key = tuple(sorted(criteria.items()))
    cache_key = (ids_key, crit_key, parallel)

    if cache_key in _filter_cache:
        _filter_cache_hits += 1
        return list(_filter_cache[cache_key])

    name_q = criteria.get("name")
    email_q = criteria.get("email")
    role_q = criteria.get("role")
    status_q = criteria.get("status")

    def check(u: Dict[str, Any]) -> bool:
        if not isinstance(u, dict):
            return False
        if name_q is not None:
            if name_q.lower() not in (u.get("name") or "").lower():
                return False
        if email_q is not None:
            if email_q not in (u.get("email") or ""):
                return False
        if role_q is not None:
            if u.get("role") != role_q:
                return False
        if status_q is not None:
            if u.get("status") != status_q:
                return False
        return True

    res = []
    if parallel:
        # lightweight parallel approach for large data: map in threads
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor() as ex:
            futures = list(ex.map(check, users))
            for u, ok in zip(users, futures):
                if ok:
                    res.append(u)
    else:
        for u in users:
            if check(u):
                res.append(u)

    _filter_cache[cache_key] = list(res)
    return res


def get_filter_cache_hits() -> int:
    return _filter_cache_hits


@lru_cache(maxsize=1024)
def _parse_date_to_timestamp(datestr: str) -> float:
    try:
        return datetime.strptime(datestr, "%Y-%m-%d").timestamp()
    except Exception:
        # fallback to epoch
        return 0.0


def export_users_to_string(users: List[Dict[str, Any]]) -> str:
    """Export users to a readable string. Deterministic order and single-pass
    date parsing (cached).
    """
    lines = []
    header = "EXPORT_BEGIN\n" + ("=" * 120) + "\n"
    lines.append(header)

    for u in users:
        uid = u.get("id", "N/A")
        name = u.get("name", "")
        last_login = u.get("last_login", "2000-01-01")
        ts = _parse_date_to_timestamp(last_login)
        lines.append(f"UserID: {uid}\n")
        lines.append(f"  Name: {name}\n")
        lines.append(f"  LastLoginParsed: {ts}\n")
        lines.append("-" * 120 + "\n")

    lines.append("EXPORT_END\n")
    return "".join(lines)
