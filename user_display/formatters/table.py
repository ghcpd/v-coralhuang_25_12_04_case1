"""
Table formatter - formatted table output.
"""

from typing import Any, Dict, List
from .base import Formatter


class TableFormatter(Formatter):
    """Formats users as a table."""

    def format(self, users: List[Dict[str, Any]], **kwargs) -> str:
        """Format users as a table."""
        field_selection = kwargs.get("field_selection", ["id", "name", "email", "role", "status"])
        
        if not users:
            return "No users to display\n"
        
        # Build table
        lines = []
        
        # Header
        header = " | ".join(f"{field:20}" for field in field_selection)
        lines.append(header)
        lines.append("=" * len(header))
        
        # Rows
        for user in users:
            row = " | ".join(
                f"{str(user.get(field, 'N/A'))[:20]:20}"
                for field in field_selection
            )
            lines.append(row)
        
        result = "\n".join(lines)
        if kwargs.get("show_count", True):
            result += f"\n\nTotal: {len(users)} users\n"
        
        return result
