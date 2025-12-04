from datetime import datetime
from typing import Dict

from .base import Validator
from ..errors import ValidationError


class DefaultValidator(Validator):
    def __init__(self, strict: bool = False, metrics=None, date_format: str = "%Y-%m-%d"):
        self.strict = strict
        self.metrics = metrics
        self.date_format = date_format

    def validate(self, user: Dict) -> Dict:
        if not isinstance(user, dict):
            raise ValidationError("User must be a dict")

        required_fields = ["id", "name", "email", "role", "status", "join_date", "last_login"]
        sanitized = dict(user)  # shallow copy

        for field in required_fields:
            if field not in sanitized:
                if self.strict:
                    raise ValidationError(f"Missing required field: {field}")
                sanitized[field] = "" if field != "id" else None

        # Parse last_login to timestamp once
        last_login_val = sanitized.get("last_login")
        ts = None
        if last_login_val:
            try:
                # Try ISO fast-path first
                # datetime.fromisoformat handles many formats and is faster than strptime
                ts = datetime.fromisoformat(str(last_login_val)).timestamp()
            except Exception:
                try:
                    ts = datetime.strptime(str(last_login_val), self.date_format).timestamp()
                except Exception:
                    if self.strict:
                        raise ValidationError("Invalid last_login format")
        sanitized["_last_login_ts"] = ts

        if self.metrics:
            self.metrics.incr("validated_users")
        return sanitized
