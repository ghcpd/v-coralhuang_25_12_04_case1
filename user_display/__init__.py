"""High-performance, modular user display system.

Exposes the main classes and factory functions for filters, formatters, validators, and the
thread-safe UserStore abstraction. See README.md for architecture and usage examples.
"""
from .config import Config
from .logging_utils import get_logger
from .metrics import Metrics
from .errors import ValidationError, PluginError, ConfigError
from .store import UserStore
from .plugins import (
    register_formatter,
    get_formatter,
    register_filter,
    get_filter,
    register_validator,
    get_validator,
    load_entrypoint_plugins,
)

__all__ = [
    "Config",
    "get_logger",
    "Metrics",
    "ValidationError",
    "PluginError",
    "ConfigError",
    "UserStore",
    "register_formatter",
    "get_formatter",
    "register_filter",
    "get_filter",
    "register_validator",
    "get_validator",
    "load_entrypoint_plugins",
]

__version__ = "1.0.0"
