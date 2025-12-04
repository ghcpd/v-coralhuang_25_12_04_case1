"""
Plugin system for dynamic registration of formatters, filters, and validators.
"""

from typing import Dict, Any, Callable, Type, Optional
from .errors import PluginError


class PluginRegistry:
    """Registry for dynamic plugin registration."""

    def __init__(self):
        self._formatters: Dict[str, Any] = {}
        self._filters: Dict[str, Any] = {}
        self._validators: Dict[str, Any] = {}

    def register_formatter(self, name: str, formatter_class: Type) -> None:
        """Register a custom formatter."""
        if not hasattr(formatter_class, 'format'):
            raise PluginError(f"Formatter {name} must have a 'format' method")
        self._formatters[name] = formatter_class

    def register_filter(self, name: str, filter_class: Type) -> None:
        """Register a custom filter."""
        if not hasattr(filter_class, 'apply'):
            raise PluginError(f"Filter {name} must have an 'apply' method")
        self._filters[name] = filter_class

    def register_validator(self, name: str, validator_class: Type) -> None:
        """Register a custom validator."""
        if not hasattr(validator_class, 'validate'):
            raise PluginError(f"Validator {name} must have a 'validate' method")
        self._validators[name] = validator_class

    def get_formatter(self, name: str) -> Optional[Type]:
        """Get registered formatter."""
        return self._formatters.get(name)

    def get_filter(self, name: str) -> Optional[Type]:
        """Get registered filter."""
        return self._filters.get(name)

    def get_validator(self, name: str) -> Optional[Type]:
        """Get registered validator."""
        return self._validators.get(name)

    def list_formatters(self) -> Dict[str, Type]:
        """List all registered formatters."""
        return self._formatters.copy()

    def list_filters(self) -> Dict[str, Type]:
        """List all registered filters."""
        return self._filters.copy()

    def list_validators(self) -> Dict[str, Type]:
        """List all registered validators."""
        return self._validators.copy()

    def unregister_formatter(self, name: str) -> None:
        """Unregister a formatter."""
        self._formatters.pop(name, None)

    def unregister_filter(self, name: str) -> None:
        """Unregister a filter."""
        self._filters.pop(name, None)

    def unregister_validator(self, name: str) -> None:
        """Unregister a validator."""
        self._validators.pop(name, None)


# Global plugin registry
_plugin_registry = PluginRegistry()


def get_plugin_registry() -> PluginRegistry:
    """Get global plugin registry."""
    return _plugin_registry
