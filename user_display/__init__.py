"""
User Display System - High-performance, modular, concurrent, and fault-tolerant.

A refactored and extended user display module that combines:
- High-performance storage with O(1) ID lookups and sharding
- Modular formatters and filters with plugin support
- Validation with soft-failure recovery
- Structured logging and metrics collection
- Thread-safe MVCC-like snapshotting
- Optional parallel filtering
"""

from .store import UserStore, UserSnapshot
from .config import get_config, Config
from .logging_utils import get_logger, get_debug_state
from .metrics import get_metrics
from .plugins import get_plugin_registry
from .errors import (
    UserDisplayError,
    ValidationError,
    FilterError,
    FormatterError,
    StorageError,
    PluginError,
)
from .formatters import (
    Formatter,
    CompactFormatter,
    JSONFormatter,
    TableFormatter,
)
from .filters import (
    Filter,
    RegexFilter,
    CompositeFilter,
)
from .validation import DefaultValidator

__all__ = [
    "UserStore",
    "UserSnapshot",
    "get_config",
    "Config",
    "get_logger",
    "get_debug_state",
    "get_metrics",
    "get_plugin_registry",
    "UserDisplayError",
    "ValidationError",
    "FilterError",
    "FormatterError",
    "StorageError",
    "PluginError",
    "Formatter",
    "CompactFormatter",
    "JSONFormatter",
    "TableFormatter",
    "Filter",
    "RegexFilter",
    "CompositeFilter",
    "DefaultValidator",
]
