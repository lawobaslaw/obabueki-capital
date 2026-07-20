from uuid import UUID

from app.calculations.holding_calculator import HoldingCalculator
from app.exceptions.account import AccountNotFoundError
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import (
    TransactionRepository,
)
from app.schemas.holding import HoldingResponse


class HoldingService:
    """Business logic for account holdings."""

    def __init__(
        self,
        transaction_repository: TransactionRepository,
        account_repository: AccountRepository,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.account_repository = account_repository

    def list_by_account(
        self,
        account_id: UUID,
        current_user: User,
    ) -> list[HoldingResponse]:
        account = self.account_repository.get_by_id(account_id)

        if account is None:
            raise AccountNotFoundError("Account not found.")

        if account.portfolio.user_id != current_user.id:
            raise AccountNotFoundError("Account not found.")

        transactions = self.transaction_repository.list_by_account(
            account_id,
        )

        return HoldingCalculator.calculate(
            transactions,
        )
