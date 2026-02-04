from typing import Dict, Iterable, List, Optional
from .base import UserFormatter

try:
    from tabulate import tabulate
except ImportError:  # pragma: no cover
    tabulate = None


class TableFormatter(UserFormatter):
    def __init__(self, fields: Optional[List[str]] = None, config=None):
        super().__init__(fields=fields, config=config)
        self.trim_width = getattr(config, "table_trim_width", None) if config else None

    def format_user(self, user: Dict) -> str:
        # Not used directly; we override format_many to produce a table at once
        return ""

    def format_many(self, users: Iterable[Dict], show_all: bool = False, metrics=None) -> str:
        data = []
        headers = self.fields or list(next(iter(users), {}).keys())
        count = 0
        for u in users:
            row = []
            for h in headers:
                val = u.get(h)
                s = str(val) if val is not None else ""
                if self.trim_width and len(s) > self.trim_width:
                    s = s[: self.trim_width - 3] + "..."
                row.append(s)
            data.append(row)
            count += 1
        if tabulate:
            table = tabulate(data, headers=headers, tablefmt="github")
        else:
            # Minimal fallback
            table = "\n".join([" | ".join(headers)] + [" | ".join(r) for r in data])
        if show_all:
            table += f"\nPROCESSED={count}"
        return table
