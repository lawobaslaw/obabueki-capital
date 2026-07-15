class PortfolioError(Exception):
    """Base portfolio exception."""


class DuplicatePortfolioError(PortfolioError):
    """Raised when a portfolio name already exists."""


class PortfolioNotFoundError(PortfolioError):
    """Raised when a portfolio cannot be found."""
