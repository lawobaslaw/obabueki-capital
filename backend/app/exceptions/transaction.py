class TransactionNotFoundError(Exception):
    """Raised when a transaction cannot be found."""


class InvalidTransactionError(Exception):
    """Raised when a transaction fails business validation."""
