from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PortfolioSummary(BaseModel):
    total_value: Decimal

    model_config = ConfigDict(from_attributes=True)
