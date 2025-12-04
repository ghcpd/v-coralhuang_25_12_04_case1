"""Plugin registry and loader.

Provides simple in-process registries plus optional loading from entry points
(`user_display.formatters`, `user_display.filters`, `user_display.validators`).
"""
import importlib
from typing import Callable, Dict, Type

try:
    # Python 3.8+
    from importlib.metadata import entry_points
except ImportError:  # pragma: no cover
    from importlib_metadata import entry_points  # type: ignore

from .errors import PluginError

_formatter_registry: Dict[str, Callable] = {}
_filter_registry: Dict[str, Callable] = {}
_validator_registry: Dict[str, Callable] = {}


def register_formatter(name: str, factory: Callable):
    _formatter_registry[name] = factory


def get_formatter(name: str) -> Callable:
    if name not in _formatter_registry:
        raise PluginError(f"Unknown formatter: {name}")
    return _formatter_registry[name]


def register_filter(name: str, factory: Callable):
    _filter_registry[name] = factory


def get_filter(name: str) -> Callable:
    if name not in _filter_registry:
        raise PluginError(f"Unknown filter: {name}")
    return _filter_registry[name]


def register_validator(name: str, factory: Callable):
    _validator_registry[name] = factory


def get_validator(name: str) -> Callable:
    if name not in _validator_registry:
        raise PluginError(f"Unknown validator: {name}")
    return _validator_registry[name]


_ENTRYPOINT_GROUPS = {
    "user_display.formatters": register_formatter,
    "user_display.filters": register_filter,
    "user_display.validators": register_validator,
}


def load_entrypoint_plugins():
    try:
        eps = entry_points()
    except Exception as exc:  # pragma: no cover - defensive
        raise PluginError(f"Failed to load entry points: {exc}")

    # entry_points API varies across Python versions
    for group, registrar in _ENTRYPOINT_GROUPS.items():
        if hasattr(eps, "select"):
            selected = eps.select(group=group)
        else:  # pragma: no cover
            # Older importlib_metadata returns a dict-like object
            selected = getattr(eps, "get", lambda *_: [])(group, [])  # type: ignore[attr-defined]
        for ep in selected:
            try:
                obj = ep.load()
                registrar(ep.name, obj)
            except Exception as exc:
                raise PluginError(f"Failed to load plugin {ep.name} from {group}: {exc}")
