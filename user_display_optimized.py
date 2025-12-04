"""
Compatibility wrapper for user_display_original.py API.
Preserves the original public API while using the optimized backend.
"""

import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

from user_display import (
    UserStore,
    CompactFormatter,
    RegexFilter,
    DefaultValidator,
    get_config,
    get_metrics,
    get_logger,
)


logger = get_logger("CompatibilityLayer")
metrics = get_metrics()


class UserDisplayOptimized:
    """Optimized user display system with API compatibility."""

    def __init__(self, users: Optional[List[Dict[str, Any]]] = None):
        config = get_config()
        self.store = UserStore(
            shard_count=config.get("shard_count", 8),
            validator=DefaultValidator(),
        )
        self.formatter = CompactFormatter()
        self._cache: Dict[str, List[Dict[str, Any]]] = {}
        self._thread_pool = None

        if users:
            self.load_users(users)

    def load_users(self, users: List[Dict[str, Any]]) -> None:
        """Load users into the store."""
        for user in users:
            try:
                self.store.add_user(user)
            except Exception as e:
                logger.warning("Failed to add user", error=str(e))

    def display_users(
        self,
        show_all: bool = True,
        verbose: bool = False,
        format_type: str = "compact",
        **format_kwargs
    ) -> str:
        """
        Display all users.
        
        Args:
            show_all: Include count summary
            verbose: Verbose logging
            format_type: "compact", "json", or "table"
            **format_kwargs: Additional formatting options
            
        Returns:
            Formatted user display string
        """
        start_time = time.time()

        users = self.store.get_all_users()
        if verbose:
            logger.info("Displaying users", count=len(users))

        # Use appropriate formatter
        formatter = self._get_formatter(format_type)
        result = formatter.format(users, show_count=show_all, **format_kwargs)

        duration_ms = (time.time() - start_time) * 1000
        metrics.record_display_operation(duration_ms)

        return result

    def get_user_by_id(self, uid: Any) -> Optional[Dict[str, Any]]:
        """
        Get user by ID (O(1) operation).
        
        Args:
            uid: User ID
            
        Returns:
            User dict or None
        """
        return self.store.get_user(uid)

    def filter_users(
        self,
        criteria: Dict[str, Any],
        parallel: bool = False,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Filter users by criteria.
        
        Args:
            criteria: Filter criteria dict with field -> value/pattern
            parallel: Use parallel filtering for large datasets
            **kwargs: Additional filter options
            
        Returns:
            Filtered list of users
        """
        start_time = time.time()
        config = get_config()

        users = self.store.get_all_users()

        # Decide on parallel filtering
        use_parallel = (
            parallel
            and config.get("enable_parallel_filtering")
            and len(users) >= config.get("parallel_threshold")
        )

        if use_parallel:
            result = self._parallel_filter(users, criteria)
        else:
            result = self._serial_filter(users, criteria)

        duration_ms = (time.time() - start_time) * 1000
        metrics.record_filter_operation(duration_ms)

        logger.info(
            "Filter completed",
            input_count=len(users),
            output_count=len(result),
            duration_ms=duration_ms,
        )

        return result

    def _serial_filter(
        self, users: List[Dict[str, Any]], criteria: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Serial filtering."""
        result = []

        for user in users:
            if self._matches_criteria(user, criteria):
                result.append(user)

        return result

    def _parallel_filter(
        self, users: List[Dict[str, Any]], criteria: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Parallel filtering using thread pool."""
        config = get_config()
        thread_count = config.get("thread_pool_size", 4)

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            matches = list(
                executor.map(
                    lambda u: (u, self._matches_criteria(u, criteria)), users
                )
            )

        return [u for u, matched in matches if matched]

    def _matches_criteria(
        self, user: Dict[str, Any], criteria: Dict[str, Any]
    ) -> bool:
        """Check if user matches all criteria."""
        for field, value in criteria.items():
            user_value = user.get(field, "")

            if isinstance(value, str):
                # Case-insensitive substring match (default behavior)
                if value.lower() not in str(user_value).lower():
                    return False
            else:
                # Exact match for non-string values
                if user_value != value:
                    return False

        return True

    def export_users_to_string(
        self, format_type: str = "compact", **format_kwargs
    ) -> str:
        """
        Export all users as string.
        
        Args:
            format_type: "compact", "json", or "table"
            **format_kwargs: Additional formatting options
            
        Returns:
            Formatted export string
        """
        start_time = time.time()

        users = self.store.get_all_users()
        formatter = self._get_formatter(format_type)
        result = formatter.format(users, show_count=True, **format_kwargs)

        duration_ms = (time.time() - start_time) * 1000
        metrics.record_export_operation(duration_ms)

        return result

    def _get_formatter(self, format_type: str):
        """Get formatter by type."""
        if format_type == "compact":
            from user_display import CompactFormatter
            return CompactFormatter()
        elif format_type == "json":
            from user_display import JSONFormatter
            return JSONFormatter()
        elif format_type == "table":
            from user_display import TableFormatter
            return TableFormatter()
        else:
            raise ValueError(f"Unknown format type: {format_type}")

    def get_store(self) -> UserStore:
        """Get underlying UserStore for advanced operations."""
        return self.store

    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        return metrics.to_dict()

    def create_snapshot(self):
        """Create snapshot for concurrent reads."""
        return self.store.create_snapshot()

    def clone(self) -> "UserDisplayOptimized":
        """Create deep copy of system."""
        new_system = UserDisplayOptimized()
        new_system.store = self.store.clone()
        return new_system


# Module-level functions for backwards compatibility with original API

_global_instance: Optional[UserDisplayOptimized] = None


def _ensure_instance() -> UserDisplayOptimized:
    """Ensure global instance exists."""
    global _global_instance
    if _global_instance is None:
        _global_instance = UserDisplayOptimized()
    return _global_instance


def display_users(users: List[Dict[str, Any]], show_all: bool = True, verbose: bool = False) -> str:
    """Display users - API compatible with original."""
    instance = _ensure_instance()
    instance.load_users(users)
    return instance.display_users(show_all=show_all, verbose=verbose)


def get_user_by_id(users: List[Dict[str, Any]], uid: Any) -> Optional[Dict[str, Any]]:
    """Get user by ID - API compatible with original."""
    instance = _ensure_instance()
    instance.load_users(users)
    return instance.get_user_by_id(uid)


def filter_users(users: List[Dict[str, Any]], criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Filter users - API compatible with original."""
    instance = _ensure_instance()
    instance.load_users(users)
    return instance.filter_users(criteria)


def export_users_to_string(users: List[Dict[str, Any]]) -> str:
    """Export users to string - API compatible with original."""
    instance = _ensure_instance()
    instance.load_users(users)
    return instance.export_users_to_string()


if __name__ == "__main__":
    # Quick test
    sample_users = [
        {
            "id": i,
            "name": f"User{i}",
            "email": f"user{i}@example.com",
            "role": "User" if i % 3 != 0 else "Admin",
            "status": "Active" if i % 5 != 0 else "Inactive",
            "join_date": "2023-01-01",
            "last_login": "2025-11-26",
        }
        for i in range(1, 101)
    ]

    print("Testing UserDisplayOptimized...")
    result = display_users(sample_users)
    print(result[:500])

    print("\nTesting get_user_by_id...")
    user = get_user_by_id(sample_users, 50)
    print(user)

    print("\nTesting filter_users...")
    filtered = filter_users(sample_users, {"role": "Admin"})
    print(f"Filtered {len(filtered)} admins")
