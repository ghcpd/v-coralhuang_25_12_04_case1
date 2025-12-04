from .base import BaseFormatter
from io import StringIO


class TableFormatter(BaseFormatter):
    def format_many(self, users, fields=None, show_all=True):
        fields = fields or ["id", "name", "email", "role"]
        out = StringIO()
        # compute widths
        widths = {f: max(len(str(u.get(f, ""))) for u in users) if users else len(f) for f in fields}
        # header
        out.write(" | ".join(f.ljust(widths[f]) for f in fields) + "\n")
        out.write("-" * (sum(widths.values()) + 3 * (len(fields) - 1)) + "\n")
        for u in users:
            out.write(" | ".join(str(u.get(f, "")).ljust(widths[f]) for f in fields) + "\n")
        if show_all:
            out.write("PROCESSED=" + str(len(users)) + "\n")
        return out.getvalue()

    def format_one(self, user, fields=None):
        return self.format_many([user], fields=fields, show_all=False)
