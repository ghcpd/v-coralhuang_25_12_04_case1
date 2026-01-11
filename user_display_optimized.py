"""Compatibility wrapper that preserves the original API but uses the new package.

Public functions:
- display_users(users, show_all=True, verbose=False)
- get_user_by_id(users, uid)
- filter_users(users, criteria)
- export_users_to_string(users)
"""
from user_display import UserStore
from user_display.formatters.compact import CompactFormatter
from user_display.formatters.json_fmt import JsonFormatter
from user_display.filters.base import BaseFilter
from user_display.validation.default import DefaultValidator
from user_display.logging_utils import info, debug
from user_display.metrics import incr


_default_store = None


def _ensure_store(users):
    global _default_store
    if _default_store is None or _default_store.size() != len(users):
        _default_store = UserStore(users=users, validator=DefaultValidator())
    return _default_store


def display_users(users, show_all=True, verbose=False, formatter="compact", fields=None):
    """Display users using a buffered formatter. Preserves legacy signature.

    Extra options: `formatter` can be 'compact' or 'json' or 'table'.
    """
    store = _ensure_store(users)
    users = store.all()
    if verbose:
        debug("display_users called", count=len(users))
    if formatter == "json":
        out = JsonFormatter().format_many(users, fields=fields, show_all=show_all)
    else:
        out = CompactFormatter().format_many(users, fields=fields, show_all=show_all)
    incr("display_calls")
    return out


def get_user_by_id(users, uid):
    store = _ensure_store(users)
    u = store.get_by_id(uid)
    incr("lookup_calls")
    return u


def filter_users(users, criteria, parallel=False):
    store = _ensure_store(users)
    all_users = store.all()
    # Build composite filter from criteria
    filters = []
    from user_display.filters.regex_filter import RegexFilter

    for k, v in criteria.items():
        if isinstance(v, str) and ("*" in v or "." in v):
            # simple wildcard/regex heuristic
            filters.append(RegexFilter(k, v.replace("*", ".*"), flags=0))
        else:
            # exact match
            filters.append(type("EqFilter", (), {"match": lambda self, user, k=k, v=v: user.get(k) == v})())

    from user_display.filters.composite_filter import CompositeFilter

    comp = CompositeFilter(filters)
    res = comp.filter(all_users)
    incr("filter_calls")
    return res


def export_users_to_string(users, fmt="compact"):
    store = _ensure_store(users)
    users = store.all()
    if fmt == "json":
        return JsonFormatter().format_many(users, show_all=True)
    else:
        return CompactFormatter().format_many(users, show_all=True)
