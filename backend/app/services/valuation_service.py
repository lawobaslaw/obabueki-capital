from uuid import UUID

from app.calculations.valuation_calculator import ValuationCalculator
from app.schemas.valuation import PortfolioValuation
from app.services.holding_service import HoldingService
from app.services.price_service import PriceService
from app.models.user import User


class ValuationService:
    """Orchestrates portfolio valuation."""

    def __init__(
        self,
        holding_service: HoldingService,
        price_service: PriceService,
    ) -> None:
        self.holding_service = holding_service
        self.price_service = price_service

    def get_account_valuation(
        self,
        account_id: UUID,
        current_user: User,
    ) -> PortfolioValuation:
        holdings = self.holding_service.list_by_account(
            account_id,
            current_user,
        )

        current_prices = self.price_service.get_current_prices(
            holdings,
        )

        return ValuationCalculator.calculate_summary(
            holdings,
            current_prices,
        )
