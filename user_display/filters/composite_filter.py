from .base import Filter
from typing import List, Dict, Any


class CompositeFilter(Filter):
    def __init__(self, filters: List[Filter]):
        self.filters = filters

    def match(self, user: Dict[str, Any]) -> bool:
        return all(f.match(user) for f in self.filters)
