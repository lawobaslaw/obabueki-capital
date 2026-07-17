from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TransactionType


class TransactionCreate(BaseModel):
    transaction_type: TransactionType
    symbol: str | None = None
    quantity: Decimal | None = None
    price: Decimal | None = None
    amount: Decimal | None = None
    fees: Decimal = Decimal("0.00")
    currency: str = Field(default="GBP", min_length=3, max_length=3)
    transaction_date: datetime
    notes: str | None = Field(default=None, max_length=500)


class TransactionUpdate(BaseModel):
    transaction_type: TransactionType | None = None
    symbol: str | None = None
    quantity: Decimal | None = None
    price: Decimal | None = None
    amount: Decimal | None = None
    fees: Decimal | None = None
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    transaction_date: datetime | None = None
    notes: str | None = Field(default=None, max_length=500)


class TransactionResponse(BaseModel):
    id: UUID
    account_id: UUID
    transaction_type: TransactionType
    symbol: str | None
    quantity: Decimal | None
    price: Decimal | None
    amount: Decimal | None
    fees: Decimal
    currency: str
    transaction_date: datetime
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
