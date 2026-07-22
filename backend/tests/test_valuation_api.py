from uuid import uuid4
from unittest.mock import Mock
from decimal import Decimal
from unittest.mock import ANY

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.valuation import PortfolioValuation
from tests.helpers import auth_headers
from app.api.dependencies import get_valuation_service

client = TestClient(app)


def test_get_account_valuation_returns_200():
    account_id = uuid4()

    valuation = PortfolioValuation(
        total_invested=Decimal("3500"),
        current_value=Decimal("4050"),
        total_gain=Decimal("550"),
        return_percentage=Decimal("15.71"),
    )

    mock_service = Mock()
    mock_service.get_account_valuation.return_value = valuation

    app.dependency_overrides[get_valuation_service] = lambda: mock_service

    try:
        response = client.get(
            f"/valuations/account/{account_id}",
            headers=auth_headers(),
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    assert response.json() == {
        "total_invested": "3500",
        "current_value": "4050",
        "total_gain": "550",
        "return_percentage": "15.71",
    }

    mock_service.get_account_valuation.assert_called_once_with(
        account_id,
        ANY,
    )
