"""Simple metrics collection for user_display."""
from threading import Lock


class Metrics:
    def __init__(self):
        self._lock = Lock()
        self._counters = {
            "cache_hits": 0,
            "cache_misses": 0,
            "validation_failures": 0,
            "filter_calls": 0,
            "id_lookups": 0,
        }

    def incr(self, key, n=1):
        with self._lock:
            if key in self._counters:
                self._counters[key] += n
            else:
                self._counters[key] = n

    def get(self, key):
        with self._lock:
            return self._counters.get(key, 0)

    def snapshot(self):
        with self._lock:
            return dict(self._counters)


GLOBAL = Metrics()
