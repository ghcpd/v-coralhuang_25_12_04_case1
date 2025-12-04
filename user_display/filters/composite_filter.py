from typing import Dict, List, Optional
from .base import UserFilter
from .regex_filter import RegexFilter


class CompositeFilter(UserFilter):
    def __init__(self, filters: Optional[List[UserFilter]] = None):
        self.filters = filters or []

    def match(self, user: Dict) -> bool:
        return all(f.match(user) for f in self.filters)

    @classmethod
    def from_criteria(cls, criteria: Dict[str, object]):
        filters: List[UserFilter] = []
        regex_patterns = {}

        for key, val in criteria.items():
            if key.startswith("regex:"):
                field = key.split(":", 1)[1]
                regex_patterns[field] = val
                continue

            # if value looks like a regex pattern /.../ we can treat it as regex
            if isinstance(val, str) and len(val) > 2 and val[0] == "/" and val[-1] == "/":
                regex_patterns[key] = val[1:-1]
                continue

            filters.append(SimpleFieldFilter(key, val))

        if regex_patterns:
            filters.append(RegexFilter(regex_patterns, case_sensitive=False))

        return cls(filters)


class SimpleFieldFilter(UserFilter):
    def __init__(self, field: str, value):
        self.field = field
        self.value = value

    def match(self, user: Dict) -> bool:
        val = user.get(self.field)
        if val is None:
            return False
        if isinstance(self.value, str) and isinstance(val, str):
            # contains for name/email; exact match otherwise
            if self.field in {"name", "email"}:
                return self.value.lower() in val.lower()
            return self.value.lower() == val.lower()
        return val == self.value
