"""Index utilities (placeholder for sharding/more advanced indexes)."""
from collections import defaultdict


class SimpleIndex:
    def __init__(self):
        self._map = {}

    def build(self, users, key="id"):
        self._map = {u.get(key): u for u in users}

    def get(self, k):
        return self._map.get(k)
