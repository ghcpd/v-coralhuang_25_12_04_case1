from .base import BaseFormatter
from typing import Iterable, Dict, Any
from io import StringIO


class TableFormatter(BaseFormatter):
    def format(self, users: Iterable[Dict[str, Any]], headers=None, **_):
        headers = headers or ["id", "name", "email", "role", "status", "last_login"]
        rows = [headers]
        for u in users:
            rows.append([str(u.get(h, "")) for h in headers])

        # simple column width
        widths = [max(len(str(row[i])) for row in rows) for i in range(len(headers))]
        out = StringIO()
        # header
        out.write(" | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + "\n")
        out.write("-+-".join("-" * w for w in widths) + "\n")
        for r in rows[1:]:
            out.write(" | ".join(r[i].ljust(widths[i]) for i in range(len(headers))) + "\n")
        return out.getvalue()
