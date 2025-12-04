"""
JSON formatter - structured JSON output.
"""

import json
from typing import Any, Dict, List
from .base import Formatter


class JSONFormatter(Formatter):
    """Formats users as JSON."""

    def format(self, users: List[Dict[str, Any]], **kwargs) -> str:
        """Format users as JSON."""
        field_selection = kwargs.get("field_selection", None)
        indent = kwargs.get("indent", 2)
        
        # If field selection specified, extract only those fields
        if field_selection:
            filtered_users = []
            for user in users:
                filtered = {k: user.get(k) for k in field_selection}
                filtered_users.append(filtered)
        else:
            filtered_users = users
        
        return json.dumps(filtered_users, indent=indent, default=str)
