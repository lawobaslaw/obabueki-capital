from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PortfolioValuation(BaseModel):
    total_invested: Decimal
    current_value: Decimal
    total_gain: Decimal
    return_percentage: Decimal

    model_config = ConfigDict(from_attributes=True)
