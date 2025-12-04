"""
Structured logging utilities for the user_display system.
Provides debug state dumps and audit trails.
"""

import json
from typing import Any, Dict, List, Optional
from enum import Enum


class LogLevel(Enum):
    """Log levels."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class StructuredLogger:
    """Structured logger for user_display operations."""

    def __init__(self, name: str, level: str = "INFO"):
        self.name = name
        self.level = LogLevel[level.upper()] if isinstance(level, str) else level
        self.records: List[Dict[str, Any]] = []
        self.enabled = True

    def _should_log(self, level: LogLevel) -> bool:
        """Check if message should be logged."""
        return self.enabled and level.value >= self.level.value

    def debug(self, msg: str, **kwargs) -> None:
        """Log debug message."""
        if self._should_log(LogLevel.DEBUG):
            self._add_record(LogLevel.DEBUG, msg, kwargs)

    def info(self, msg: str, **kwargs) -> None:
        """Log info message."""
        if self._should_log(LogLevel.INFO):
            self._add_record(LogLevel.INFO, msg, kwargs)

    def warning(self, msg: str, **kwargs) -> None:
        """Log warning message."""
        if self._should_log(LogLevel.WARNING):
            self._add_record(LogLevel.WARNING, msg, kwargs)

    def error(self, msg: str, **kwargs) -> None:
        """Log error message."""
        if self._should_log(LogLevel.ERROR):
            self._add_record(LogLevel.ERROR, msg, kwargs)

    def _add_record(self, level: LogLevel, msg: str, data: Dict[str, Any]) -> None:
        """Add log record."""
        record = {
            "logger": self.name,
            "level": level.name,
            "message": msg,
            **data
        }
        self.records.append(record)

    def get_records(self) -> List[Dict[str, Any]]:
        """Get all log records."""
        return self.records.copy()

    def clear_records(self) -> None:
        """Clear log records."""
        self.records.clear()

    def dump_records(self) -> str:
        """Dump records as JSON string."""
        return json.dumps(self.records, indent=2, default=str)


class DebugState:
    """Debug state dump for internal diagnostics."""

    def __init__(self):
        self.state: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """Set debug state."""
        self.state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get debug state."""
        return self.state.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Export state as dictionary."""
        return self.state.copy()

    def dump(self) -> str:
        """Dump state as JSON."""
        return json.dumps(self.state, indent=2, default=str)


# Global logger and debug state
_loggers: Dict[str, StructuredLogger] = {}
_debug_state = DebugState()


def get_logger(name: str, level: str = "INFO") -> StructuredLogger:
    """Get or create logger."""
    if name not in _loggers:
        _loggers[name] = StructuredLogger(name, level)
    return _loggers[name]


def get_debug_state() -> DebugState:
    """Get global debug state."""
    return _debug_state
