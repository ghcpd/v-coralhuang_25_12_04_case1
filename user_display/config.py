"""Configuration for user_display package."""
import os


DEFAULTS = {
    "snapshot_freeze": True,
    "shard_count": int(os.environ.get("USRDS_SHARD_COUNT", 8)),
    "parallel_filtering": False,
}


def get(name, default=None):
    return DEFAULTS.get(name, default)
