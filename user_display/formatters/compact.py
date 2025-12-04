from io import StringIO
from .base import BaseFormatter


class CompactFormatter(BaseFormatter):
    def format_many(self, users, fields=None, show_all=True):
        out = StringIO()
        count = 0
        fields = fields or ["id", "name", "email", "role", "status", "join_date", "last_login"]
        for u in users:
            parts = []
            for f in fields:
                parts.append(f.upper() + "=" + str(u.get(f, "")))
            out.write(" | ".join(parts) + "\n")
            count += 1
        if show_all:
            out.write("PROCESSED=" + str(count) + "\n")
        return out.getvalue()

    def format_one(self, user, fields=None):
        return self.format_many([user], fields=fields, show_all=False)
