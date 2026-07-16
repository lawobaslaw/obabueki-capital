from uuid import UUID

from app.exceptions.account import (
    AccountNotFoundError,
    DuplicateAccountError,
)
from app.exceptions.portfolio import PortfolioNotFoundError
from app.models.account import Account
from app.models.enums import AccountType
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.repositories.portfolio_repository import PortfolioRepository


class AccountService:
    """Business logic for investment accounts."""

    def __init__(
        self,
        account_repository: AccountRepository,
        portfolio_repository: PortfolioRepository,
    ) -> None:
        self.account_repository = account_repository
        self.portfolio_repository = portfolio_repository

    def create(
        self,
        current_user: User,
        portfolio_id: UUID,
        name: str,
        broker: str,
        account_type: AccountType,
        currency: str,
        is_default: bool,
    ) -> Account:
        """Create an account."""

        portfolio = self.portfolio_repository.get_by_id(
            portfolio_id,
        )

        if portfolio is None:
            raise PortfolioNotFoundError("Portfolio not found.")

        if portfolio.user_id != current_user.id:
            raise PortfolioNotFoundError("Portfolio not found.")

        existing_accounts = self.account_repository.list_by_portfolio_id(
            portfolio_id,
        )

        normalized_name = name.strip().lower()

        for account in existing_accounts:
            if account.name.strip().lower() == normalized_name:
                raise DuplicateAccountError("Account name already exists.")

        if is_default:
            for account in existing_accounts:
                if account.is_default:
                    account.is_default = False
                    self.account_repository.save(account)

        account = Account(
            portfolio_id=portfolio_id,
            name=name.strip(),
            broker=broker.strip(),
            account_type=account_type,
            currency=currency.upper(),
            is_default=is_default,
        )

        return self.account_repository.create(account)

    def get(
        self,
        account_id: UUID,
        current_user: User,
    ) -> Account:
        """Return an account."""

        account = self.account_repository.get_by_id(
            account_id,
        )

        if account is None:
            raise AccountNotFoundError("Account not found.")

        portfolio = self.portfolio_repository.get_by_id(
            account.portfolio_id,
        )

        if portfolio is None or portfolio.user_id != current_user.id:
            raise AccountNotFoundError("Account not found.")

        return account

    def list(
        self,
        portfolio_id: UUID,
        current_user: User,
    ) -> list[Account]:
        """Return all accounts in a portfolio."""

        portfolio = self.portfolio_repository.get_by_id(
            portfolio_id,
        )

        if portfolio is None or portfolio.user_id != current_user.id:
            raise PortfolioNotFoundError("Portfolio not found.")

        return self.account_repository.list_by_portfolio_id(
            portfolio_id,
        )

    def delete(
        self,
        account_id: UUID,
        current_user: User,
    ) -> None:
        """Delete an account."""

        account = self.get(
            account_id,
            current_user,
        )

        self.account_repository.delete(account)

    def update(
        self,
        account_id: UUID,
        current_user: User,
        name: str | None,
        broker: str | None,
        account_type: AccountType | None,
        currency: str | None,
        is_default: bool | None,
    ) -> Account:
        """Update an account."""

        account = self.get(
            account_id,
            current_user,
        )

        if name is not None:
            normalized_name = name.strip().lower()

            for existing in self.account_repository.list_by_portfolio_id(
                account.portfolio_id,
            ):
                if (
                    existing.id != account.id
                    and existing.name.strip().lower() == normalized_name
                ):
                    raise DuplicateAccountError("Account name already exists.")

            account.name = name.strip()

        if broker is not None:
            account.broker = broker.strip()

        if account_type is not None:
            account.account_type = account_type

        if currency is not None:
            account.currency = currency.upper()

        if is_default is not None:
            if is_default:
                for existing in self.account_repository.list_by_portfolio_id(
                    account.portfolio_id,
                ):
                    if existing.id != account.id and existing.is_default:
                        existing.is_default = False
                        self.account_repository.save(existing)

            account.is_default = is_default

        return self.account_repository.save(account)
