from decimal import Decimal

from app.schemas.holding import HoldingResponse
from app.services.price_service import PriceService
from app.exceptions.valuation import MissingPriceError
import pytest


def test_get_current_prices_returns_prices_for_holdings():
    # Arrange
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

    service = PriceService()

    # Act
    prices = service.get_current_prices(
        holdings,
    )

    # Assert
    assert prices == {
        "AAPL": Decimal("180"),
        "MSFT": Decimal("450"),
    }


def test_get_current_prices_raises_missing_price_error():
    # Arrange
    holdings = [
        HoldingResponse(
            symbol="GOOG",
            quantity=Decimal("5"),
            average_cost=Decimal("100"),
            cost_basis=Decimal("500"),
            currency="USD",
        ),
    ]

    service = PriceService()

    # Act / Assert
    with pytest.raises(MissingPriceError):
        service.get_current_prices(
            holdings,
        )
