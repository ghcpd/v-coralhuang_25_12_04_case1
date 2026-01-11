from .base import BaseValidator


class DefaultValidator(BaseValidator):
    def validate_and_recover(self, user):
        # Ensure required fields exist and have sane defaults
        if not isinstance(user, dict):
            return False, {}
        u = dict(user)
        if "id" not in u:
            return False, u
        # normalize simple fields
        for f in ["name", "email", "role", "status", "join_date", "last_login"]:
            u.setdefault(f, "")
        return True, u
