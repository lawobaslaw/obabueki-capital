class AccountNotFoundError(Exception):
    """Raised when an account cannot be found."""


class DuplicateAccountError(Exception):
    """Raised when an account name already exists."""
