from .base import BaseFormatter
import json

class JsonFormatter(BaseFormatter):
    def format(self, users, **opts):
        return json.dumps(list(users), default=str)
