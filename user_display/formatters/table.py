from .base import BaseFormatter
from io import StringIO

class TableFormatter(BaseFormatter):
    def format(self, users, fields=None, **opts):
        fields = fields or ["id","name","email","role","status"]
        buf = StringIO()
        widths = {f: max(len(str(f)), *(len(str(u.get(f, ''))) for u in users)) for f in fields}
        header = " | ".join(f.upper().ljust(widths[f]) for f in fields)
        buf.write(header+"\n")
        buf.write("-"*len(header)+"\n")
        for u in users:
            row = " | ".join(str(u.get(f, '')).ljust(widths[f]) for f in fields)
            buf.write(row+"\n")
        return buf.getvalue()
