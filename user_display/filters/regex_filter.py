import re
from typing import Dict, Pattern
from .base import UserFilter


class RegexFilter(UserFilter):
    def __init__(self, field_patterns: Dict[str, str], case_sensitive: bool = False):
        flags = 0 if case_sensitive else re.IGNORECASE
        self._patterns: Dict[str, Pattern] = {k: re.compile(v, flags) for k, v in field_patterns.items()}

    def match(self, user: Dict) -> bool:
        for field, pattern in self._patterns.items():
            val = user.get(field)
            if val is None:
                return False
            if not pattern.search(str(val)):
                return False
        return True
