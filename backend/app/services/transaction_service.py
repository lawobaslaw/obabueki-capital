from uuid import UUID
from decimal import Decimal

from app.exceptions.account import AccountNotFoundError
from app.exceptions.transaction import (
    InvalidTransactionError,
    TransactionNotFoundError,
)
from app.models.enums import TransactionType
from app.models.transaction import Transaction
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionService:
    """Business logic for account transactions."""

    def __init__(
        self,
        account_repository: AccountRepository,
        transaction_repository: TransactionRepository,
    ) -> None:
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def create(
        self,
        account_id: UUID,
        transaction_data: TransactionCreate,
    ) -> Transaction:
        """Create a new transaction."""

        account = self.account_repository.get_by_id(account_id)

        if account is None:
            raise AccountNotFoundError("Account not found.")

        self._validate_transaction(transaction_data)

        self._validate_sell_quantity(account_id, transaction_data)

        transaction = Transaction(
            account_id=account_id,
            **transaction_data.model_dump(),
        )

        return self.transaction_repository.create(transaction)

    def get_by_id(
        self,
        transaction_id: UUID,
    ) -> Transaction:
        """Retrieve a transaction by ID."""

        transaction = self.transaction_repository.get_by_id(transaction_id)

        if transaction is None:
            raise TransactionNotFoundError("Transaction not found.")

        return transaction

    def list_by_account(
        self,
        account_id: UUID,
    ) -> list[Transaction]:
        """List all transactions for an account."""

        account = self.account_repository.get_by_id(account_id)

        if account is None:
            raise AccountNotFoundError("Account not found.")

        return self.transaction_repository.list_by_account(account_id)

    def update(
        self,
        transaction_id: UUID,
        transaction_data: TransactionUpdate,
    ) -> Transaction:
        """Update an existing transaction."""

        transaction = self.get_by_id(transaction_id)

        update_data = transaction_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(transaction, field, value)

        return self.transaction_repository.save(transaction)

    def delete(
        self,
        transaction_id: UUID,
    ) -> None:
        """Delete a transaction."""

        transaction = self.get_by_id(transaction_id)

        self.transaction_repository.delete(transaction)

    def _validate_transaction(
        self,
        transaction_data: TransactionCreate,
    ) -> None:
        """Validate transaction data based on the transaction type."""

        if transaction_data.transaction_type in (
            TransactionType.BUY,
            TransactionType.SELL,
        ):
            if not transaction_data.symbol:
                raise InvalidTransactionError(
                    "Symbol is required for BUY and SELL transactions."
                )

            if transaction_data.quantity is None:
                raise InvalidTransactionError(
                    "Quantity is required for BUY and SELL transactions."
                )

            if transaction_data.quantity <= 0:
                raise InvalidTransactionError("Quantity must be greater than zero.")

            if transaction_data.price is None:
                raise InvalidTransactionError(
                    "Price is required for BUY and SELL transactions."
                )

            if transaction_data.price <= 0:
                raise InvalidTransactionError("Price must be greater than zero.")

        elif transaction_data.transaction_type == TransactionType.DIVIDEND:
            if not transaction_data.symbol:
                raise InvalidTransactionError(
                    "Symbol is required for DIVIDEND transactions."
                )

            if transaction_data.amount is None:
                raise InvalidTransactionError(
                    "Amount is required for DIVIDEND transactions."
                )

            if transaction_data.amount <= 0:
                raise InvalidTransactionError("Amount must be greater than zero.")

        elif transaction_data.transaction_type in (
            TransactionType.DEPOSIT,
            TransactionType.WITHDRAWAL,
            TransactionType.FEE,
        ):
            if transaction_data.amount is None:
                raise InvalidTransactionError(
                    "Amount is required for this transaction type."
                )

            if transaction_data.amount <= 0:
                raise InvalidTransactionError("Amount must be greater than zero.")

        if transaction_data.fees is not None and transaction_data.fees < 0:
            raise InvalidTransactionError("Fees cannot be negative.")

    def _validate_sell_quantity(
        self,
        account_id: UUID,
        transaction_data: TransactionCreate,
    ) -> None:
        """Ensure a SELL transaction does not exceed current holdings."""

        if transaction_data.transaction_type != TransactionType.SELL:
            return

        transactions = self.transaction_repository.list_by_account(account_id)

        owned_quantity = Decimal("0")

        for transaction in transactions:
            if transaction.symbol != transaction_data.symbol:
                continue

            quantity = transaction.quantity or Decimal("0")

            if transaction.transaction_type == TransactionType.BUY:
                owned_quantity += quantity
            elif transaction.transaction_type == TransactionType.SELL:
                owned_quantity -= quantity

        sell_quantity = transaction_data.quantity or Decimal("0")

        if sell_quantity > owned_quantity:
            raise InvalidTransactionError(
                "Cannot sell more shares than currently held."
            )
