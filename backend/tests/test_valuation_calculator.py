from decimal import Decimal

import pytest

from app.calculations.valuation_calculator import ValuationCalculator
from app.exceptions.valuation import MissingPriceError
from app.schemas.holding import HoldingResponse


def test_calculate_summary_returns_correct_portfolio_values():
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

    current_prices = {
        "AAPL": Decimal("180"),
        "MSFT": Decimal("450"),
    }

    valuation = ValuationCalculator.calculate_summary(
        holdings,
        current_prices,
    )

    assert valuation.total_invested == Decimal("3500")
    assert valuation.current_value == Decimal("4050")
    assert valuation.total_gain == Decimal("550")
    assert valuation.return_percentage == Decimal("15.71")


def test_raises_missing_price_error_when_price_is_unavailable():
    holdings = [
        HoldingResponse(
            symbol="AAPL",
            quantity=Decimal("10"),
            average_cost=Decimal("150"),
            cost_basis=Decimal("1500"),
            currency="USD",
        )
    ]

    current_prices = {}

    with pytest.raises(MissingPriceError):
        ValuationCalculator.calculate_summary(
            holdings,
            current_prices,
        )
