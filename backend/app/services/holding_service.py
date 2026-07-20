from uuid import UUID
from decimal import Decimal


from app.repositories.transaction_repository import TransactionRepository
from app.repositories.account_repository import AccountRepository
from app.models.user import User
from app.schemas.holding import HoldingResponse
from app.exceptions.account import AccountNotFoundError


class HoldingService:
    """Business logic for calculating account holdings."""

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

        transactions = self.transaction_repository.list_by_account(account_id)

        holdings: dict[str, dict] = {}

        for transaction in transactions:
            if transaction.transaction_type.name != "BUY":
                continue

            symbol = transaction.symbol

            if symbol is None:
                continue

            quantity = transaction.quantity or Decimal("0")
            price = transaction.price or Decimal("0")

            total_cost = quantity * price + transaction.fees

            holdings[symbol] = {
                "symbol": symbol,
                "quantity": quantity,
                "total_cost": total_cost,
                "currency": transaction.currency,
            }

        results: list[HoldingResponse] = []

        for holding in holdings.values():
            average_cost = holding["total_cost"] / holding["quantity"]

            results.append(
                HoldingResponse(
                    symbol=holding["symbol"],
                    quantity=holding["quantity"],
                    average_cost=average_cost,
                    cost_basis=holding["total_cost"],
                    currency=holding["currency"],
                )
            )

        return results
