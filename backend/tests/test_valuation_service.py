from decimal import Decimal
from unittest.mock import Mock
from uuid import uuid4

from app.schemas.holding import HoldingResponse
from app.schemas.valuation import PortfolioValuation
from app.services.valuation_service import ValuationService


def test_get_account_valuation_returns_portfolio_valuation():
    # Arrange
    account_id = uuid4()
    current_user = Mock()

    holding_service = Mock()
    price_service = Mock()

    holdings = [
        HoldingResponse(
            symbol="AAPL",
            quantity=Decimal("10"),
            average_cost=Decimal("150"),
            cost_basis=Decimal("1500"),
            currency="USD",
        ),
        HoldingResponse(
            symbol="MSFT",
            quantity=Decimal("5"),
            average_cost=Decimal("400"),
            cost_basis=Decimal("2000"),
            currency="USD",
        ),
    ]

    holding_service.list_by_account.return_value = holdings

    price_service.get_current_prices.return_value = {
        "AAPL": Decimal("180"),
        "MSFT": Decimal("450"),
    }

    service = ValuationService(
        holding_service=holding_service,
        price_service=price_service,
    )

    # Act
    valuation = service.get_account_valuation(
        account_id,
        current_user,
    )

    # Assert
    assert isinstance(valuation, PortfolioValuation)
    assert valuation.current_value == Decimal("4050")

    holding_service.list_by_account.assert_called_once_with(
        account_id,
        current_user,
    )

    price_service.get_current_prices.assert_called_once_with(
        holdings,
    )
