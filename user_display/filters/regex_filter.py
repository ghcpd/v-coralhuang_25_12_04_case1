import re
from .base import Filter
from typing import Dict, Any


class RegexFilter(Filter):
    def __init__(self, field: str, pattern: str, flags=0):
        self.field = field
        self.regex = re.compile(pattern, flags)

    def match(self, user: Dict[str, Any]) -> bool:
        v = user.get(self.field)
        if v is None:
            return False
        return bool(self.regex.search(str(v)))
