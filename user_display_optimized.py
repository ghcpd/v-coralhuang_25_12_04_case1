"""Compatibility wrapper exposing the original functions backed by optimized package.

Public API:
- display_users(users, show_all=True, verbose=False, formatter='compact', fields=None)
- get_user_by_id(users, uid)
- filter_users(users, criteria, parallel=False)
- export_users_to_string(users, formatter='table')
"""
from user_display import UserStore
from user_display.formatters.compact import CompactFormatter
from user_display.formatters.json_fmt import JsonFormatter
from user_display.formatters.table import TableFormatter
from user_display.validation.default import DefaultValidator
from user_display.filters.regex_filter import RegexFilter
from user_display.filters.composite_filter import CompositeFilter
from user_display.metrics import incr
from user_display.logging_utils import log_structured
from functools import lru_cache
from typing import Iterable


def _ensure_store(users):
    if isinstance(users, UserStore):
        return users
    return UserStore(users)


def display_users(users, show_all=True, verbose=False, formatter='compact', fields=None):
    store = _ensure_store(users)
    snapshot = store.snapshot()
    fmt = {'compact': CompactFormatter, 'json': JsonFormatter, 'table': TableFormatter}.get(formatter, CompactFormatter)()
    if verbose:
        log_structured(20, 'display_start', size=len(snapshot))
    out = fmt.format(snapshot, show_all=show_all, fields=fields)
    incr('display_calls')
    return out


def get_user_by_id(users, uid):
    store = _ensure_store(users)
    u = store.get_user_by_id(uid)
    incr('lookup_calls')
    if u is None:
        log_structured(30, 'lookup_miss', id=uid)
    return u


def _criteria_to_filter(criteria):
    # build simple composite filter - name/email substrings, role/status exact
    filters = []
    if 'name' in criteria:
        # prefer fast substring matching when pattern is plain
        pat = criteria['name']
        if any(c in pat for c in '^$.|*+?{}[]\\'):
            filters.append(RegexFilter('name', pat, flags=0))
        else:
            filters.append(lambda u, p=pat: p in u.get('name', ''))
    if 'email' in criteria:
        pat = criteria['email']
        if any(c in pat for c in '^$.|*+?{}[]\\'):
            filters.append(RegexFilter('email', pat))
        else:
            filters.append(lambda u, p=pat: p in u.get('email', ''))
    if 'role' in criteria:
        filters.append(lambda u, r=criteria['role']: u.get('role') == r)
    if 'status' in criteria:
        filters.append(lambda u, s=criteria['status']: u.get('status') == s)
    return CompositeFilter(filters)


@lru_cache(maxsize=1024)
def _cached_filter_result(store_id, criteria_key):
    # placeholder - real cache keyed by store identity + criteria
    return None


def filter_users(users, criteria, parallel=False):
    store = _ensure_store(users)
    snapshot = store.snapshot()
    f = _criteria_to_filter(criteria)
    incr('filter_calls')
    if parallel:
        res = store.parallel_filter(f, users=snapshot)
    else:
        res = [u for u in snapshot if f(u)]
    incr('filter_results', len(res))
    return res


def export_users_to_string(users, formatter='table'):
    store = _ensure_store(users)
    snapshot = store.snapshot()
    fmt = {'compact': CompactFormatter, 'json': JsonFormatter, 'table': TableFormatter}.get(formatter, TableFormatter)()
    incr('export_calls')
    return fmt.format(snapshot)
