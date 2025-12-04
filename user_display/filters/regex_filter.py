"""
Regex filter for pattern matching on user fields.
"""

import re
from typing import Any, Dict, List, Optional, Pattern
from .base import Filter


class RegexFilter(Filter):
    """Filters users based on regex patterns on specified fields."""

    def __init__(self, patterns: Dict[str, str], case_sensitive: bool = False):
        """
        Initialize regex filter.
        
        Args:
            patterns: Dict of field -> regex pattern
            case_sensitive: Whether patterns are case-sensitive
        """
        self.patterns = patterns
        self.case_sensitive = case_sensitive
        self.compiled_patterns: Dict[str, Pattern] = {}
        
        for field, pattern in patterns.items():
            flags = 0 if case_sensitive else re.IGNORECASE
            self.compiled_patterns[field] = re.compile(pattern, flags)

    def apply(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply regex filters to users."""
        result = []
        
        for user in users:
            if self._matches(user):
                result.append(user)
        
        return result

    def _matches(self, user: Dict[str, Any]) -> bool:
        """Check if user matches all patterns."""
        for field, regex in self.compiled_patterns.items():
            value = user.get(field, "")
            if not regex.search(str(value)):
                return False
        return True
