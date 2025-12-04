from typing import Dict, Callable

_plugins: Dict[str, Callable] = {}


def register(name: str, factory: Callable):
    _plugins[name] = factory


def get_plugin(name: str):
    return _plugins.get(name)


def list_plugins():
    return list(_plugins.keys())
