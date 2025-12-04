from .base import Formatter
from typing import List, Dict, Any, Optional


class CompactFormatter(Formatter):
    def format(self, users: List[Dict[str, Any]], fields: Optional[List[str]] = None, **kwargs) -> str:
        # default fields if none provided
        if fields is None:
            fields = ["id", "name", "email", "role", "status", "join_date", "last_login"]

        rows = []
        for u in users:
            parts = [f"{k.upper()}={(u.get(k, '') if isinstance(u, dict) else '')}" for k in fields]
            rows.append(" | ".join(parts))

        if kwargs.get("show_all", True):
            rows.append(f"PROCESSED={len(users)}")

        return "\n".join(rows) + ("\n" if rows else "")
