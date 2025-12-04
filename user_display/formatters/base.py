class BaseFormatter:
    def format_many(self, users, **opts):
        raise NotImplementedError()

    def format_one(self, user, **opts):
        raise NotImplementedError()
