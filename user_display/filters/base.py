class BaseFilter:
    def match(self, user):
        raise NotImplementedError()

    def filter(self, users):
        return [u for u in users if self.match(u)]
