class BaseFilter:
    def __call__(self, user):
        raise NotImplementedError()
