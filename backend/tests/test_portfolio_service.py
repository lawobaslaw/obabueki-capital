from decimal import Decimal
from unittest.mock import Mock
from uuid import uuid4

from app.schemas.portfolio_summary import PortfolioSummary
from app.schemas.valuation import PortfolioValuation
from app.services.portfolio_summary_service import PortfolioSummaryService


def test_get_portfolio_summary_returns_total_value():
    # Arrange
    portfolio_id = uuid4()
    current_user = Mock()

    account_service = Mock()
    valuation_service = Mock()

    accounts = [
        Mock(id=uuid4()),
        Mock(id=uuid4()),
        Mock(id=uuid4()),
    ]

    account_service.list_by_portfolio.return_value = accounts

    valuation_service.get_account_valuation.side_effect = [
        PortfolioValuation(
            total_invested=Decimal("3500"),
            current_value=Decimal("4050"),
            total_gain=Decimal("550"),
            return_percentage=Decimal("15.71"),
        ),
        PortfolioValuation(
            total_invested=Decimal("1000"),
            current_value=Decimal("1200"),
            total_gain=Decimal("200"),
            return_percentage=Decimal("20.00"),
        ),
        PortfolioValuation(
            total_invested=Decimal("800"),
            current_value=Decimal("900"),
            total_gain=Decimal("100"),
            return_percentage=Decimal("12.50"),
        ),
    ]

    service = PortfolioSummaryService(
        account_service=account_service,
        valuation_service=valuation_service,
    )

    # Act
    summary = service.get_summary(
        portfolio_id,
        current_user,
    )

    # Assert
    assert isinstance(summary, PortfolioSummary)
    assert summary.total_value == Decimal("6150")
    assert valuation_service.get_account_valuation.call_count == 3
