import re
from .base import BaseFilter
from typing import Dict, Any


class RegexFilter(BaseFilter):
    def matches(self, user: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        # criteria keys: field->pattern (string)
        for field, patt in criteria.items():
            if patt is None:
                continue
            val = str(user.get(field, ""))
            try:
                if not re.search(patt, val):
                    return False
            except re.error:
                # invalid regex; treat as no-match
                return False
        return True
