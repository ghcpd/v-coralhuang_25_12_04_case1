from .base import BaseFormatter
from io import StringIO

class CompactFormatter(BaseFormatter):
    def format(self, users, show_all=True, fields=None, **opts):
        buf = StringIO()
        count = 0
        fields = fields or ["id","name","email","role","status","join_date","last_login"]
        for u in users:
            parts = []
            for f in fields:
                parts.append(f.upper()+"="+str(u.get(f,"")))
            buf.write(" | ".join(parts))
            buf.write("\n")
            count += 1
        if show_all:
            buf.write("PROCESSED="+str(count)+"\n")
        return buf.getvalue()
