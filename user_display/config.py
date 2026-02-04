from dataclasses import dataclass


@dataclass
class Config:
    default_formatter: str = "compact"
    max_cache_size: int = 1024
    parallel_threshold: int = 1000


CONFIG = Config()
