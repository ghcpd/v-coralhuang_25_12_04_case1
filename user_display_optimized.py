"""Compatibility wrapper exposing the baseline API on top of the modular system."""
from typing import Any, Dict, List, Optional
from collections import OrderedDict

from user_display.store import UserStore
from user_display.config import Config

# Simple LRU cache for store instances keyed by id(users)
_store_cache: "OrderedDict[int, UserStore]" = OrderedDict()
_STORE_CACHE_LIMIT = 8


def _get_store(users: List[Dict[str, Any]], config: Optional[Config] = None) -> UserStore:
    key = id(users)
    if key in _store_cache:
        store = _store_cache.pop(key)
        _store_cache[key] = store
        return store
    store = UserStore(users, config=config)
    _store_cache[key] = store
    if len(_store_cache) > _STORE_CACHE_LIMIT:
        _store_cache.popitem(last=False)
    return store


# Public API (must match baseline signatures)

def display_users(
    users: List[Dict[str, Any]],
    show_all: bool = True,
    verbose: bool = False,
    formatter: str = "compact",
    fields: Optional[List[str]] = None,
    parallel: Optional[bool] = None,
    include_metrics: bool = False,
) -> str:
    store = _get_store(users)
    return store.display_users(
        formatter_name=formatter,
        fields=fields,
        show_all=show_all,
        verbose=verbose,
        parallel=parallel,
        include_metrics=include_metrics,
    )


def get_user_by_id(users: List[Dict[str, Any]], uid: Any):
    store = _get_store(users)
    return store.get_user_by_id(uid)


def filter_users(users: List[Dict[str, Any]], criteria: Dict[str, Any], parallel: Optional[bool] = None):
    store = _get_store(users)
    return store.filter_users(criteria, parallel=parallel)


def export_users_to_string(users: List[Dict[str, Any]]):
    store = _get_store(users)
    return store.export_users_to_string()


__all__ = [
    "display_users",
    "get_user_by_id",
    "filter_users",
    "export_users_to_string",
]
