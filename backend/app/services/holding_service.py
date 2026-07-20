from decimal import Decimal
from uuid import UUID

from app.exceptions.account import AccountNotFoundError
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.holding import HoldingResponse


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

        holdings: dict[str, dict[str, Decimal | str]] = {}

        for transaction in transactions:
            if transaction.symbol is None:
                continue

            symbol = transaction.symbol

            if symbol not in holdings:
                holdings[symbol] = {
                    "quantity": Decimal("0"),
                    "total_cost": Decimal("0"),
                    "currency": transaction.currency,
                }

            quantity = transaction.quantity or Decimal("0")
            price = transaction.price or Decimal("0")
            fees = transaction.fees or Decimal("0")

            if transaction.transaction_type.name == "BUY":
                holdings[symbol]["quantity"] += quantity
                holdings[symbol]["total_cost"] += (quantity * price) + fees

            elif transaction.transaction_type.name == "SELL":
                current_quantity = holdings[symbol]["quantity"]

                if current_quantity == 0:
                    continue

                average_cost = holdings[symbol]["total_cost"] / current_quantity

                holdings[symbol]["quantity"] -= quantity
                holdings[symbol]["total_cost"] -= average_cost * quantity

        results: list[HoldingResponse] = []

        for symbol, holding in holdings.items():
            quantity = holding["quantity"]

            if quantity <= 0:
                continue

            total_cost = holding["total_cost"]
            average_cost = total_cost / quantity

            results.append(
                HoldingResponse(
                    symbol=symbol,
                    quantity=quantity,
                    average_cost=average_cost,
                    cost_basis=total_cost,
                    currency=holding["currency"],
                )
            )

        return results
