from enum import Enum


class AccountType(str, Enum):
    """Supported investment account types."""

    BROKERAGE = "BROKERAGE"
    ISA = "ISA"
    PENSION = "PENSION"
    SAVINGS = "SAVINGS"
    CRYPTO = "CRYPTO"
    CASH = "CASH"


class TransactionType(str, Enum):
    """Supported transaction types."""

    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    FEE = "FEE"
