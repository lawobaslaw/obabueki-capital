from decimal import Decimal
from uuid import UUID

from app.models.user import User
from app.schemas.portfolio_summary import PortfolioSummary
from app.services.account_service import AccountService
from app.services.valuation_service import ValuationService


class PortfolioSummaryService:
    """Builds portfolio summaries."""

    def __init__(
        self,
        account_service: AccountService,
        valuation_service: ValuationService,
    ) -> None:
        self.account_service = account_service
        self.valuation_service = valuation_service

    def get_summary(
        self,
        portfolio_id: UUID,
        current_user: User,
    ) -> PortfolioSummary:
        total_value = Decimal("0")

        accounts = self.account_service.list_by_portfolio(
            portfolio_id,
            current_user,
        )

        for account in accounts:
            valuation = self.valuation_service.get_account_valuation(
                account.id,
                current_user,
            )

            total_value += valuation.current_value

        return PortfolioSummary(
            total_value=total_value,
        )
