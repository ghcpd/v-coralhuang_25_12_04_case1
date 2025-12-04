"""
Composite filter - combine multiple filters with AND/OR logic.
"""

from typing import Any, Dict, List
from .base import Filter


class CompositeFilter(Filter):
    """Combines multiple filters with AND or OR logic."""

    def __init__(self, filters: List[Filter], combine_with: str = "AND"):
        """
        Initialize composite filter.
        
        Args:
            filters: List of filters to combine
            combine_with: "AND" or "OR"
        """
        if combine_with not in ("AND", "OR"):
            raise ValueError("combine_with must be 'AND' or 'OR'")
        
        self.filters = filters
        self.combine_with = combine_with

    def apply(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply composite filter."""
        if not self.filters:
            return users
        
        if self.combine_with == "AND":
            result = users
            for f in self.filters:
                result = f.apply(result)
            return result
        else:  # OR
            result_set = set()
            for f in self.filters:
                filtered = f.apply(users)
                result_set.update(id(user) for user in filtered)
            
            # Maintain original order
            return [u for u in users if id(u) in result_set]
