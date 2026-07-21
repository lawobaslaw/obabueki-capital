from decimal import Decimal

from app.exceptions.valuation import MissingPriceError
from app.schemas.holding import HoldingResponse
from app.schemas.valuation import PortfolioValuation


class ValuationCalculator:
    """Calculates portfolio valuation from holdings and market prices."""

    @staticmethod
    def calculate_summary(
        holdings: list[HoldingResponse],
        current_prices: dict[str, Decimal],
    ) -> PortfolioValuation:
        total_invested = Decimal("0")
        current_value = Decimal("0")

        for holding in holdings:
            if holding.symbol not in current_prices:
                raise MissingPriceError(
                    f"Market price unavailable for {holding.symbol}."
                )

            current_price = current_prices[holding.symbol]

            total_invested += holding.cost_basis

            current_value += holding.quantity * current_price

        total_gain = current_value - total_invested

        return_percentage = (
            (total_gain / total_invested) * Decimal("100")
            if total_invested > 0
            else Decimal("0")
        ).quantize(Decimal("0.01"))

        return PortfolioValuation(
            total_invested=total_invested,
            current_value=current_value,
            total_gain=total_gain,
            return_percentage=return_percentage,
        )
