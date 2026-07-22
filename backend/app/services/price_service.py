from decimal import Decimal
from app.schemas.holding import HoldingResponse
from app.exceptions.valuation import MissingPriceError


class PriceService:
    """Provides current market prices."""

    def get_current_prices(
        self,
        holdings: list[HoldingResponse],
    ) -> dict[str, Decimal]:

        prices = {
            "AAPL": Decimal("180"),
            "MSFT": Decimal("450"),
        }
        for holding in holdings:
            if holding.symbol not in prices:
                raise MissingPriceError(f"No current price found for {holding.symbol}")
        return {holding.symbol: prices[holding.symbol] for holding in holdings}
