"""
Default validator with field validation and soft-failure recovery.
"""

from typing import Any, Dict, Optional, Tuple
from .base import Validator


class DefaultValidator(Validator):
    """Default validator with schema-based validation and repair."""

    # Default schema
    DEFAULT_SCHEMA = {
        "id": (int, "N/A"),
        "name": (str, ""),
        "email": (str, ""),
        "role": (str, "User"),
        "status": (str, "Active"),
        "join_date": (str, "2000-01-01"),
        "last_login": (str, "2000-01-01"),
    }

    def __init__(self, schema: Optional[Dict[str, Any]] = None):
        self.schema = schema or self.DEFAULT_SCHEMA

    def validate(self, user: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate user against schema."""
        errors = []
        
        for field, (expected_type, _) in self.schema.items():
            if field not in user:
                errors.append(f"Missing field: {field}")
            elif not isinstance(user[field], expected_type):
                errors.append(f"Field {field} has wrong type: expected {expected_type.__name__}, got {type(user[field]).__name__}")

        if errors:
            return False, "; ".join(errors)
        return True, None

    def repair(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Repair user with missing/invalid fields."""
        repaired = user.copy()
        
        for field, (expected_type, default) in self.schema.items():
            if field not in repaired:
                repaired[field] = default
            elif not isinstance(repaired[field], expected_type):
                # Try type conversion
                try:
                    if expected_type == int:
                        repaired[field] = int(repaired[field])
                    elif expected_type == str:
                        repaired[field] = str(repaired[field])
                    elif expected_type == float:
                        repaired[field] = float(repaired[field])
                except (ValueError, TypeError):
                    repaired[field] = default

        return repaired


__all__ = ["DefaultValidator"]
