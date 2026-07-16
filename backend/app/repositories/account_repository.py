from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account import Account


class AccountRepository:
    """Repository for account database operations."""

    def __init__(
        self,
        session: Session,
    ) -> None:
        self.session = session

    def create(
        self,
        account: Account,
    ) -> Account:
        """Create an account."""

        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)

        return account

    def get_by_id(
        self,
        account_id: UUID,
    ) -> Account | None:
        """Return an account by ID."""

        statement = select(Account).where(Account.id == account_id)

        return self.session.scalar(statement)

    def list_by_portfolio_id(
        self,
        portfolio_id: UUID,
    ) -> list[Account]:
        """Return all accounts in a portfolio."""

        statement = select(Account).where(Account.portfolio_id == portfolio_id)

        return self.session.scalars(statement).all()

    def save(
        self,
        account: Account,
    ) -> Account:
        """Save changes to an account."""

        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)

        return account

    def delete(
        self,
        account: Account,
    ) -> None:
        """Delete an account."""

        self.session.delete(account)
        self.session.commit()
