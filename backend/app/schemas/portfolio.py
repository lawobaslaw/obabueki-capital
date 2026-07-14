from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PortfolioCreate(BaseModel):
    name: str
    description: str | None = None
    base_currency: str = "GBP"


class PortfolioUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    base_currency: str | None = None


class PortfolioResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    base_currency: str

    model_config = ConfigDict(from_attributes=True)