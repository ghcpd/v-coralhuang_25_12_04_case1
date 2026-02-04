import json
from typing import Dict, Iterable, List, Optional
from .base import UserFormatter


class JsonFormatter(UserFormatter):
    def __init__(self, fields: Optional[List[str]] = None, config=None):
        super().__init__(fields=fields, config=config)
        self.pretty = getattr(config, "json_pretty", False) if config else False

    def format_user(self, user: Dict) -> str:
        u = self._select_fields(user)
        return json.dumps(u, indent=2 if self.pretty else None)

    def format_many(self, users: Iterable[Dict], show_all: bool = False, metrics=None) -> str:
        # Return a JSON array for display
        arr = []
        count = 0
        for u in users:
            arr.append(self._select_fields(u))
            count += 1
        payload = json.dumps(arr, indent=2 if self.pretty else None)
        if show_all:
            # Append metadata as a small JSON object after a newline
            payload += "\n" + json.dumps({"processed": count})
        return payload

    def export(self, users: Iterable[Dict]) -> str:
        header = "EXPORT_BEGIN\n" + ("=" * 120) + "\n"
        body = self.format_many(users, show_all=False)
        footer = "\nEXPORT_END\n"
        return header + body + footer
