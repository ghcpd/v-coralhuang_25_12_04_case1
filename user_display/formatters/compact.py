"""
Compact formatter - single line per user.
"""

from typing import Any, Dict, List
from .base import Formatter


class CompactFormatter(Formatter):
    """Formats users in compact single-line format."""

    def format(self, users: List[Dict[str, Any]], **kwargs) -> str:
        """Format users in compact format."""
        field_selection = kwargs.get("field_selection", ["id", "name", "email", "status"])
        
        lines = []
        for user in users:
            parts = []
            for field in field_selection:
                value = user.get(field, "N/A")
                parts.append(f"{field}={value}")
            lines.append(" | ".join(parts))
        
        result = "\n".join(lines)
        if kwargs.get("show_count", True):
            result += f"\nPROCESSED={len(users)}\n"
        
        return result
