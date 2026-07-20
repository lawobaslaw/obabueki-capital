from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class HoldingResponse(BaseModel):
    symbol: str
    quantity: Decimal
    average_cost: Decimal
    cost_basis: Decimal
    currency: str = Field(
        min_length=3,
        max_length=3,
    )

    model_config = ConfigDict(from_attributes=True)
