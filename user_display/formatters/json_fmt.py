import json
from .base import BaseFormatter


class JsonFormatter(BaseFormatter):
    def format_many(self, users, fields=None, show_all=True):
        # Optionally strip fields
        if fields:
            users = [{k: u.get(k) for k in fields} for u in users]
        out = {"users": users}
        if show_all:
            out["count"] = len(users)
        return json.dumps(out, default=str)

    def format_one(self, user, fields=None):
        return self.format_many([user], fields=fields, show_all=False)
