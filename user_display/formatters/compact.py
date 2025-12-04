from .base import BaseFormatter
from typing import Iterable, Dict, Any
from io import StringIO


class CompactFormatter(BaseFormatter):
    """Compact single-line per user formatter.

    Uses join and StringIO for efficient construction.
    """

    def format(self, users: Iterable[Dict[str, Any]], show_all=True, fields=None, **_):
        fields = fields or ["id", "name", "email", "role", "status", "join_date", "last_login"]
        out = StringIO()
        count = 0
        for u in users:
            parts = []
            for f in fields:
                parts.append(f + "=" + str(u.get(f, "")))
            out.write(" | ".join(parts))
            out.write("\n")
            count += 1
        if show_all:
            out.write("PROCESSED=" + str(count) + "\n")
        return out.getvalue()
