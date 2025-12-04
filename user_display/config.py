"""
Configuration management for user_display system.
Supports environment overrides and runtime configuration.
"""

import os
from typing import Any, Dict, Optional


class Config:
    """Configuration manager with environment override support."""

    # Default configuration
    DEFAULTS = {
        "max_users": 200000,
        "shard_count": 8,
        "enable_caching": True,
        "cache_max_size": 10000,
        "enable_parallel_filtering": True,
        "parallel_threshold": 1000,
        "thread_pool_size": 4,
        "enable_structured_logging": True,
        "log_level": "INFO",
        "validate_on_insert": True,
        "soft_fail_on_validation": True,
        "freeze_mode": False,  # Prevent modifications after initialization
    }

    def __init__(self):
        self._config: Dict[str, Any] = self.DEFAULTS.copy()
        self._frozen = False
        self._load_from_env()

    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        for key in self.DEFAULTS:
            env_key = f"USER_DISPLAY_{key.upper()}"
            if env_key in os.environ:
                value = os.environ[env_key]
                # Try to convert to appropriate type
                if key in ["enable_caching", "enable_parallel_filtering", 
                          "enable_structured_logging", "validate_on_insert",
                          "soft_fail_on_validation", "freeze_mode"]:
                    self._config[key] = value.lower() in ("true", "1", "yes")
                elif key in ["max_users", "shard_count", "cache_max_size",
                            "parallel_threshold", "thread_pool_size"]:
                    self._config[key] = int(value)
                else:
                    self._config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value. Raises error if frozen."""
        if self._frozen:
            raise RuntimeError("Configuration is frozen and cannot be modified.")
        self._config[key] = value

    def freeze(self) -> None:
        """Freeze configuration to prevent runtime modifications."""
        self._frozen = True

    def unfreeze(self) -> None:
        """Unfreeze configuration."""
        self._frozen = False

    def is_frozen(self) -> bool:
        """Check if configuration is frozen."""
        return self._frozen

    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary."""
        return self._config.copy()


# Global configuration instance
_global_config = Config()


def get_config() -> Config:
    """Get global configuration instance."""
    return _global_config
