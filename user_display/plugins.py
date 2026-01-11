"""Plugin registry for formatters, filters, and validators."""
from typing import Dict, Type

_formatters: Dict[str, Type] = {}
_filters: Dict[str, Type] = {}
_validators: Dict[str, Type] = {}


def register_formatter(name: str, cls: Type):
    _formatters[name] = cls


def get_formatter(name: str):
    return _formatters.get(name)


def register_filter(name: str, cls: Type):
    _filters[name] = cls


def get_filter(name: str):
    return _filters.get(name)


def register_validator(name: str, cls: Type):
    _validators[name] = cls


def get_validator(name: str):
    return _validators.get(name)
