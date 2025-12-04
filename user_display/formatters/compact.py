from typing import Dict, List, Optional
from .base import UserFormatter


DEFAULT_FIELDS = [
    "id",
    "name",
    "email",
    "role",
    "status",
    "join_date",
    "last_login",
]


class CompactFormatter(UserFormatter):
    def __init__(self, fields: Optional[List[str]] = None, config=None):
        super().__init__(fields=fields or DEFAULT_FIELDS, config=config)

    def format_user(self, user: Dict) -> str:
        u = self._select_fields(user)
        parts = []
        for k, v in u.items():
            parts.append(f"{k.upper()}={v if v is not None else 'N/A'}")
        return " | ".join(parts)
