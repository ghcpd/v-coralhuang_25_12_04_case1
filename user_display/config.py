"""Runtime configuration with sensible defaults."""
import os


DEFAULTS = {
    "FORMAT": "compact",
    "PARALLEL_FILTERING": False,
}


def get(key, default=None):
    return os.environ.get(key, DEFAULTS.get(key, default))
