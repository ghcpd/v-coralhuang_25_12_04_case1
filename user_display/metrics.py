import time
import threading
from collections import Counter
from contextlib import contextmanager
from typing import Dict, Optional


class Metrics:
    """Thread-safe metrics collector for counters and timers."""

    def __init__(self):
        self._counters = Counter()
        self._timings: Dict[str, float] = {}
        self._lock = threading.RLock()

    def incr(self, key: str, value: int = 1):
        with self._lock:
            self._counters[key] += value

    def timing(self, key: str, duration: float):
        with self._lock:
            self._timings[key] = self._timings.get(key, 0.0) + duration

    @contextmanager
    def timer(self, key: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            end = time.perf_counter()
            self.timing(key, end - start)

    def snapshot(self) -> Dict[str, Dict[str, float]]:
        with self._lock:
            return {
                "counters": dict(self._counters),
                "timings": dict(self._timings),
            }

    def reset(self):
        with self._lock:
            self._counters.clear()
            self._timings.clear()
