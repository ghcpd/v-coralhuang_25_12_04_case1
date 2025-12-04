"""
Custom error types for the user_display system.
"""


class UserDisplayError(Exception):
    """Base exception for user_display module."""
    pass


class ValidationError(UserDisplayError):
    """Raised when user data validation fails."""
    pass


class FilterError(UserDisplayError):
    """Raised when filter application fails."""
    pass


class FormatterError(UserDisplayError):
    """Raised when formatting fails."""
    pass


class StorageError(UserDisplayError):
    """Raised when storage operation fails."""
    pass


class PluginError(UserDisplayError):
    """Raised when plugin operation fails."""
    pass
