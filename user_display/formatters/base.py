from abc import ABC, abstractmethod
from io import StringIO
from typing import Dict, Iterable, List, Optional


class UserFormatter(ABC):
    def __init__(self, fields: Optional[List[str]] = None, config=None):
        self.fields = fields
        self.config = config

    @abstractmethod
    def format_user(self, user: Dict) -> str:
        ...

    def _select_fields(self, user: Dict) -> Dict:
        if self.fields is None:
            return user
        return {k: user.get(k) for k in self.fields}

    def format_many(self, users: Iterable[Dict], show_all: bool = False, metrics=None) -> str:
        buf = StringIO()
        count = 0
        for u in users:
            buf.write(self.format_user(u))
            buf.write("\n")
            count += 1
        if show_all:
            buf.write(f"PROCESSED={count}\n")
        return buf.getvalue()
