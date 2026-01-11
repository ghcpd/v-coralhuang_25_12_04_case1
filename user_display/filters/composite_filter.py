from .base import BaseFilter
from typing import Dict, Any


class CompositeFilter(BaseFilter):
    """Simple composite filter supporting substring or exact match per field.

    Criteria format:
      {"name": {"type": "contains", "value": "alice"},
       "status": {"type": "exact", "value": "Active"}}
    """

    def matches(self, user: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        for field, rule in criteria.items():
            if isinstance(rule, dict):
                typ = rule.get("type", "contains")
                value = rule.get("value")
            else:
                typ = "contains"
                value = rule

            if value is None:
                continue

            text = str(user.get(field, ""))
            if typ == "contains":
                if str(value).lower() not in text.lower():
                    return False
            elif typ == "exact":
                if text != str(value):
                    return False
            elif typ == "prefix":
                if not text.startswith(str(value)):
                    return False
            elif typ == "suffix":
                if not text.endswith(str(value)):
                    return False
            else:
                # unknown rule, skip strict matching
                return False

        return True
