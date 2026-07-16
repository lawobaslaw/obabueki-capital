from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import AccountType


class AccountCreate(BaseModel):
    name: str
    broker: str
    account_type: AccountType
    currency: str = "GBP"
    is_default: bool = False


class AccountUpdate(BaseModel):
    name: str | None = None
    broker: str | None = None
    account_type: AccountType | None = None
    currency: str | None = None
    is_default: bool | None = None


class AccountResponse(BaseModel):
    id: UUID
    name: str
    broker: str
    account_type: AccountType
    currency: str
    is_default: bool

    model_config = ConfigDict(from_attributes=True)
