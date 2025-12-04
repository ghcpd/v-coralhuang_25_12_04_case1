from .base import Formatter
from typing import List, Dict, Any, Optional
import json


class JsonFormatter(Formatter):
    def format(self, users: List[Dict[str, Any]], fields: Optional[List[str]] = None, **kwargs) -> str:
        # Select fields if provided, else include full user objects
        if fields:
            out = [{k: (u.get(k) if isinstance(u, dict) else None) for k in fields} for u in users]
        else:
            # omit non-dict entries when returning full users list
            out = [u for u in users if isinstance(u, dict)]
        return json.dumps({"count": len(users), "users": out}, default=str)
