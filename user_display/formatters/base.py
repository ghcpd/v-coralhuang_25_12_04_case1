"""
Base classes for formatters.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class Formatter(ABC):
    """Base class for output formatters."""

    @abstractmethod
    def format(self, users: List[Dict[str, Any]], **kwargs) -> str:
        """
        Format users for output.
        
        Args:
            users: List of user dictionaries
            **kwargs: Format-specific options (field_selection, conditional_rules, etc.)
            
        Returns:
            Formatted string
        """
        pass
