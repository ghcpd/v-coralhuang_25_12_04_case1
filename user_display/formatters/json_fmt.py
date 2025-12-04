from .base import BaseFormatter
from typing import Iterable, Dict, Any
import json


class JSONFormatter(BaseFormatter):
    def format(self, users: Iterable[Dict[str, Any]], **options):
        # Ensure we convert generator/iterable into list only once
        users_list = list(users)
        return json.dumps({"users": users_list, "count": len(users_list)}, default=str)
