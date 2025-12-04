"""
Metrics collection for user_display system.
Tracks cache performance, shard usage, filtering stats, and validation issues.
"""

from typing import Dict, Any
from collections import defaultdict


class Metrics:
    """Collects system metrics."""

    def __init__(self):
        self.cache_hits = 0
        self.cache_misses = 0
        self.shard_accesses: Dict[int, int] = defaultdict(int)
        self.filter_operations = 0
        self.filter_duration_ms = 0.0
        self.display_operations = 0
        self.display_duration_ms = 0.0
        self.lookup_operations = 0
        self.lookup_duration_ms = 0.0
        self.validation_errors = 0
        self.validation_warnings = 0
        self.export_operations = 0
        self.export_duration_ms = 0.0

    def record_cache_hit(self) -> None:
        """Record cache hit."""
        self.cache_hits += 1

    def record_cache_miss(self) -> None:
        """Record cache miss."""
        self.cache_misses += 1

    def record_shard_access(self, shard_id: int) -> None:
        """Record shard access."""
        self.shard_accesses[shard_id] += 1

    def record_filter_operation(self, duration_ms: float) -> None:
        """Record filter operation."""
        self.filter_operations += 1
        self.filter_duration_ms += duration_ms

    def record_display_operation(self, duration_ms: float) -> None:
        """Record display operation."""
        self.display_operations += 1
        self.display_duration_ms += duration_ms

    def record_lookup_operation(self, duration_ms: float) -> None:
        """Record ID lookup operation."""
        self.lookup_operations += 1
        self.lookup_duration_ms += duration_ms

    def record_validation_error(self) -> None:
        """Record validation error."""
        self.validation_errors += 1

    def record_validation_warning(self) -> None:
        """Record validation warning."""
        self.validation_warnings += 1

    def record_export_operation(self, duration_ms: float) -> None:
        """Record export operation."""
        self.export_operations += 1
        self.export_duration_ms += duration_ms

    def get_cache_hit_rate(self) -> float:
        """Get cache hit rate (0-1)."""
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total

    def get_avg_filter_duration_ms(self) -> float:
        """Get average filter duration."""
        if self.filter_operations == 0:
            return 0.0
        return self.filter_duration_ms / self.filter_operations

    def get_avg_display_duration_ms(self) -> float:
        """Get average display duration."""
        if self.display_operations == 0:
            return 0.0
        return self.display_duration_ms / self.display_operations

    def get_avg_lookup_duration_ms(self) -> float:
        """Get average lookup duration."""
        if self.lookup_operations == 0:
            return 0.0
        return self.lookup_duration_ms / self.lookup_operations

    def get_avg_export_duration_ms(self) -> float:
        """Get average export duration."""
        if self.export_operations == 0:
            return 0.0
        return self.export_duration_ms / self.export_operations

    def to_dict(self) -> Dict[str, Any]:
        """Export metrics as dictionary."""
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": self.get_cache_hit_rate(),
            "shard_accesses": dict(self.shard_accesses),
            "filter_operations": self.filter_operations,
            "filter_total_duration_ms": self.filter_duration_ms,
            "filter_avg_duration_ms": self.get_avg_filter_duration_ms(),
            "display_operations": self.display_operations,
            "display_total_duration_ms": self.display_duration_ms,
            "display_avg_duration_ms": self.get_avg_display_duration_ms(),
            "lookup_operations": self.lookup_operations,
            "lookup_total_duration_ms": self.lookup_duration_ms,
            "lookup_avg_duration_ms": self.get_avg_lookup_duration_ms(),
            "validation_errors": self.validation_errors,
            "validation_warnings": self.validation_warnings,
            "export_operations": self.export_operations,
            "export_total_duration_ms": self.export_duration_ms,
            "export_avg_duration_ms": self.get_avg_export_duration_ms(),
        }

    def reset(self) -> None:
        """Reset all metrics."""
        self.cache_hits = 0
        self.cache_misses = 0
        self.shard_accesses.clear()
        self.filter_operations = 0
        self.filter_duration_ms = 0.0
        self.display_operations = 0
        self.display_duration_ms = 0.0
        self.lookup_operations = 0
        self.lookup_duration_ms = 0.0
        self.validation_errors = 0
        self.validation_warnings = 0
        self.export_operations = 0
        self.export_duration_ms = 0.0


# Global metrics instance
_metrics = Metrics()


def get_metrics() -> Metrics:
    """Get global metrics instance."""
    return _metrics
