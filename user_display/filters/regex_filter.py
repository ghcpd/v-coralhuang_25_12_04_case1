import re
from .base import BaseFilter


class RegexFilter(BaseFilter):
    def __init__(self, field, pattern, flags=0):
        self.field = field
        self.re = re.compile(pattern, flags)

    def match(self, user):
        v = user.get(self.field, "")
        return bool(self.re.search(str(v)))
