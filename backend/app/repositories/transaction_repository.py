from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TransactionRepository:
    """Repository for transaction database operations."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def get_by_id(self, transaction_id: UUID) -> Transaction | None:
        statement = select(Transaction).where(Transaction.id == transaction_id)
        return self.session.scalar(statement)

    def list_by_account(self, account_id: UUID) -> list[Transaction]:
        statement = (
            select(Transaction)
            .where(Transaction.account_id == account_id)
            .order_by(Transaction.transaction_date)
        )
        return self.session.scalars(statement).all()

    def save(
        self,
        transaction: Transaction,
    ) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def delete(
        self,
        transaction: Transaction,
    ) -> None:
        self.session.delete(transaction)
        self.session.commit()
