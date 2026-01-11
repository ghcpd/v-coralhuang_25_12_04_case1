from .base import BaseFilter


class CompositeFilter(BaseFilter):
    def __init__(self, filters=None):
        self.filters = filters or []

    def match(self, user):
        return all(f.match(user) for f in self.filters)
