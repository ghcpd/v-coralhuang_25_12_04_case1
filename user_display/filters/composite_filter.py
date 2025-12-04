from .base import BaseFilter

class CompositeFilter(BaseFilter):
    def __init__(self, filters):
        self.filters = list(filters)

    def __call__(self, user):
        return all(f(user) for f in self.filters)
