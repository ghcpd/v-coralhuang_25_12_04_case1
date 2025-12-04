"""Compatibility wrapper providing the original functions with improved behavior.

Public functions preserved:
- display_users(users, show_all=True, verbose=False)
- get_user_by_id(users, uid)
- filter_users(users, criteria)
- export_users_to_string(users)

This module builds an internal UserStore and uses formatters & filters.
"""
from typing import Iterable, Dict, Any, Optional, List
from user_display.store import UserStore
from user_display.formatters.compact import CompactFormatter
from user_display.formatters.json_fmt import JSONFormatter
from user_display.formatters.table import TableFormatter
from user_display.filters.composite_filter import CompositeFilter
from user_display.logging_utils import debug, info


def _ensure_store(users: Iterable[Dict[str, Any]]) -> UserStore:
    if isinstance(users, UserStore):
        return users
    # users might be a generator -> make list
    if not isinstance(users, list):
        users = list(users)
    return UserStore(users)


def display_users(users: Iterable[Dict[str, Any]], show_all: bool = True, verbose: bool = False, formatter: Optional[str] = "compact", **kwargs) -> str:
    """Return a formatted representation of users.

    Behavior is deterministic and fast. 'verbose' toggles debug logging.
    """
    st = _ensure_store(users)
    # choose formatter quickly
    if formatter == "json":
        fmt = JSONFormatter()
    elif formatter == "table":
        fmt = TableFormatter()
    else:
        fmt = CompactFormatter()

    if verbose:
        debug("display_users verbose mode active; dataset size=%s", st.size())

    return fmt.format(st.snapshot()._index.values(), show_all=show_all, **kwargs)


def get_user_by_id(users: Iterable[Dict[str, Any]], uid: Any) -> Optional[Dict[str, Any]]:
    """Return user dict with id==uid or None. Deterministic O(1) lookup.

    Accepts raw list or UserStore.
    """
    st = _ensure_store(users)
    return st.get_by_id(uid)


def filter_users(users: Iterable[Dict[str, Any]], criteria: Dict[str, Any], matcher: Optional[callable] = None, **kwargs) -> List[Dict[str, Any]]:
    """Filter users by criteria. Default matcher behaves like legacy behavior:
    - name: case-insensitive substring
    - email: substring
    - role/status: exact
    """
    st = _ensure_store(users)

    def default_matcher(u, crit):
        # convert a flat dict into composite rules
        transformed = {}
        for k, v in crit.items():
            if k == "name":
                transformed[k] = {"type": "contains", "value": v}
            elif k in ("role", "status"):
                transformed[k] = {"type": "exact", "value": v}
            else:
                # fallback to contains
                transformed[k] = {"type": "contains", "value": v}
        return CompositeFilter().matches(u, transformed)

    use_matcher = matcher if matcher is not None else default_matcher
    return st.filter(criteria, use_matcher)


def export_users_to_string(users: Iterable[Dict[str, Any]], formatter: Optional[str] = "table", sort_by: Optional[str] = "id") -> str:
    """Export users to a string with a consistent header/footer, no randomness.

    The default is a table format sorted by 'id'.
    """
    st = _ensure_store(users)
    # create deterministic list
    snap = st.snapshot()
    vals = list(snap._index.values())

    # stable sort
    try:
        vals.sort(key=lambda x: x.get(sort_by, 0) or 0)
    except Exception:
        pass

    header = "EXPORT_BEGIN\n" + ("=" * 120) + "\n"
    footer = "EXPORT_END\n"

    if formatter == "json":
        fmt = JSONFormatter()
        return header + fmt.format(vals) + "\n" + footer
    elif formatter == "compact":
        fmt = CompactFormatter()
        return header + fmt.format(vals, show_all=False) + footer
    else:
        fmt = TableFormatter()
        return header + fmt.format(vals) + footer


# preserve module-level sample_users for compatibility with original baseline
# keep sample alias compatibility (not used further)
