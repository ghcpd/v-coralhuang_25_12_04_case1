class UserDisplayError(Exception):
    pass


class ValidationError(UserDisplayError):
    pass


class FormatError(UserDisplayError):
    pass
