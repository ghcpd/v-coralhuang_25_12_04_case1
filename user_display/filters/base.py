"""
Base classes for filters.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Filter(ABC):
    """Base class for user filters."""

    @abstractmethod
    def apply(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply filter to users.
        
        Args:
            users: List of user dictionaries
            
        Returns:
            Filtered list of users
        """
        pass
