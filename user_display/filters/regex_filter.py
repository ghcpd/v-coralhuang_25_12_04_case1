import re
from .base import BaseFilter

class RegexFilter(BaseFilter):
    def __init__(self, field, pattern, flags=0):
        self.field = field
        self.re = re.compile(pattern, flags)

    def __call__(self, user):
        return bool(self.re.search(str(user.get(self.field, ''))))
