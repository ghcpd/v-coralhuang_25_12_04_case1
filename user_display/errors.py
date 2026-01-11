class UserDisplayError(Exception):
    """Base package error."""


class ValidationError(UserDisplayError):
    """Raised when user validation fails but recovery may be possible."""


class NotFoundError(UserDisplayError):
    """Raised when a user was not found by id."""
