from enum import Enum


class AccountType(str, Enum):
    """Supported investment account types."""

    BROKERAGE = "BROKERAGE"
    ISA = "ISA"
    PENSION = "PENSION"
    SAVINGS = "SAVINGS"
    CRYPTO = "CRYPTO"
    CASH = "CASH"
