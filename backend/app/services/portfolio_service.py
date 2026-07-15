from uuid import UUID

from app.models.portfolio import Portfolio
from app.models.user import User
from app.repositories.portfolio_repository import PortfolioRepository
from app.exceptions.portfolio import DuplicatePortfolioError, PortfolioNotFoundError


class PortfolioService:
    """Business logic for portfolio management."""

    def __init__(
        self,
        portfolio_repository: PortfolioRepository,
    ) -> None:
        self.portfolio_repository = portfolio_repository

    def create(
        self,
        current_user: User,
        name: str,
        description: str | None,
        base_currency: str,
    ) -> Portfolio:
        """Create a new portfolio."""

        existing_portfolios = self.portfolio_repository.list_by_user_id(
            current_user.id,
        )

        normalized_name = name.strip().lower()
        for portfolio in existing_portfolios:
            if portfolio.name.strip().lower() == normalized_name:
                raise DuplicatePortfolioError("Portfolio name already exists.")

        portfolio = Portfolio(
            user_id=current_user.id,
            name=name.strip(),
            description=description,
            base_currency=base_currency.upper(),
        )

        return self.portfolio_repository.create(portfolio)

    def get(
        self,
        portfolio_id: UUID,
        current_user: User,
    ) -> Portfolio:
        """Return a portfolio owned by the current user."""

        portfolio = self.portfolio_repository.get_by_id(portfolio_id)

        if portfolio is None:
            raise PortfolioNotFoundError("Portfolio not found.")

        if portfolio.user_id != current_user.id:
            raise PortfolioNotFoundError("Portfolio not found.")

        return portfolio

    def list(
        self,
        current_user: User,
    ) -> list[Portfolio]:
        """Return all portfolios owned by the current user."""

        return self.portfolio_repository.list_by_user_id(
            current_user.id,
        )

    def delete(
        self,
        portfolio_id: UUID,
        current_user: User,
    ) -> None:
        """Delete a portfolio."""

        portfolio = self.get(
            portfolio_id,
            current_user,
        )

        self.portfolio_repository.delete(portfolio)

    def update(
        self,
        portfolio_id: UUID,
        current_user: User,
        name: str | None,
        description: str | None,
        base_currency: str | None,
    ) -> Portfolio:
        """Update a portfolio."""

        portfolio = self.get(
            portfolio_id,
            current_user,
        )

        if name is not None:
            normalized_name = name.strip().lower()

            for existing in self.portfolio_repository.list_by_user_id(current_user.id):
                if (
                    existing.id != portfolio.id
                    and existing.name.strip().lower() == normalized_name
                ):
                    raise DuplicatePortfolioError("Portfolio name already exists.")

        portfolio.name = name.strip()

        if description is not None:
            portfolio.description = description

        if base_currency is not None:
            portfolio.base_currency = base_currency.upper()

        return self.portfolio_repository.save(portfolio)
