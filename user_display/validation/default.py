from .base import Validator
from typing import Dict, Any


class DefaultValidator(Validator):
    def validate(self, user: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(user, dict):
            return {}
        # provide safe defaults
        return {
            "id": user.get("id"),
            "name": user.get("name") or "",
            "email": user.get("email") or "",
            "role": user.get("role") or "",
            "status": user.get("status") or "",
            "join_date": user.get("join_date") or "",
            "last_login": user.get("last_login") or "",
        }
