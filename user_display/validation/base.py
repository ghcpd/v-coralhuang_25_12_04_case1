"""
Base classes for validation system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class Validator(ABC):
    """Base class for validators."""

    @abstractmethod
    def validate(self, user: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate a user record.
        
        Returns:
            (is_valid, error_message)
        """
        pass

    @abstractmethod
    def repair(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempt to repair a user record with missing/invalid fields.
        
        Returns:
            Repaired user record
        """
        pass
