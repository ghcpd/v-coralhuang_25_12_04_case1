from .base import BaseValidator
from datetime import datetime

class DefaultValidator(BaseValidator):
    def validate(self, user):
        # ensure required fields with defaults
        u = dict(user) if user else {}
        u.setdefault('id', None)
        u.setdefault('name', '')
        u.setdefault('email', '')
        u.setdefault('role', 'User')
        u.setdefault('status', 'Inactive')
        u.setdefault('join_date', '1970-01-01')
        u.setdefault('last_login', '1970-01-01')
        # normalize date format
        try:
            datetime.strptime(u['last_login'], '%Y-%m-%d')
        except Exception:
            u['last_login'] = '1970-01-01'
        return u
