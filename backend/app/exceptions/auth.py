class AuthenticationError(Exception):
    """Base authentication exception."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when authentication fails."""


class DuplicateEmailError(AuthenticationError):
    """Raised when email already exists."""
