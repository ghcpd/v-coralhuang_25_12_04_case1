from .base import Formatter
from typing import List, Dict, Any, Optional


class TableFormatter(Formatter):
    def format(self, users: List[Dict[str, Any]], fields: Optional[List[str]] = None, **kwargs) -> str:
        if fields is None:
            fields = ["id", "name", "email", "role", "status"]

        # compute column widths
        cols = [str(h).upper() for h in fields]
        rows = []
        widths = [len(c) for c in cols]

        for u in users:
            row = [str(u.get(k, "") if isinstance(u, dict) else "") for k in fields]
            for i, v in enumerate(row):
                widths[i] = max(widths[i], len(v))
            rows.append(row)

        lines = []
        header = " | ".join(c.ljust(widths[i]) for i, c in enumerate(cols))
        lines.append(header)
        lines.append("-+-".join("-" * w for w in widths))

        for r in rows:
            lines.append(" | ".join(r[i].ljust(widths[i]) for i in range(len(r))))

        if kwargs.get("show_all", True):
            lines.append(f"PROCESSED={len(users)}")

        return "\n".join(lines) + ("\n" if lines else "")
