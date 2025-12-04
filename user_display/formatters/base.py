from typing import Iterable, Dict, Any


class BaseFormatter:
    def format(self, users: Iterable[Dict[str, Any]], **options) -> str:
        raise NotImplementedError()
