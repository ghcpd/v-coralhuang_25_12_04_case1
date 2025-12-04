import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    """Runtime configuration with env overrides and optional freeze mode."""

    date_format: str = "%Y-%m-%d"
    parallel_filtering: bool = False
    max_workers: Optional[int] = None
    filter_cache_size: int = 64
    log_level: str = os.environ.get("USER_DISPLAY_LOG_LEVEL", "INFO")
    strict_validation: bool = False
    # formatter defaults
    default_formatter: str = "compact"
    json_pretty: bool = False
    table_trim_width: int = 40

    _frozen: bool = field(default=False, init=False, repr=False)

    def __post_init__(self):
        # env overrides
        self.parallel_filtering = _env_bool("USER_DISPLAY_PARALLEL", self.parallel_filtering)
        self.strict_validation = _env_bool("USER_DISPLAY_STRICT_VALIDATION", self.strict_validation)
        self.json_pretty = _env_bool("USER_DISPLAY_JSON_PRETTY", self.json_pretty)
        self.date_format = os.environ.get("USER_DISPLAY_DATE_FORMAT", self.date_format)
        mw = os.environ.get("USER_DISPLAY_MAX_WORKERS")
        if mw and mw.isdigit():
            self.max_workers = int(mw)
        cache = os.environ.get("USER_DISPLAY_FILTER_CACHE_SIZE")
        if cache and cache.isdigit():
            self.filter_cache_size = int(cache)

    def freeze(self):
        self._frozen = True

    def __setattr__(self, key, value):
        if getattr(self, "_frozen", False) and key != "_frozen":
            raise RuntimeError("Config is frozen")
        super().__setattr__(key, value)


def _env_bool(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.lower() in ("1", "true", "yes", "on")
