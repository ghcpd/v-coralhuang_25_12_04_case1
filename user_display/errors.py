class UserDisplayError(Exception):
    pass


class ValidationError(UserDisplayError):
    pass


class NotFoundError(UserDisplayError):
    pass
