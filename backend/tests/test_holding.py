from fastapi.testclient import TestClient
from decimal import Decimal

from app.main import app
from tests.helpers import (
    auth_headers,
    create_account,
    create_transaction,
)

client = TestClient(app)


def test_buy_transaction_creates_holding():
    headers = auth_headers()

    account_id = create_account(headers)

    create_transaction(
        headers=headers,
        account_id=account_id,
    )

    response = client.get(
        f"/accounts/{account_id}/holdings",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    holding = data[0]

    assert holding["symbol"] == "AAPL"
    assert Decimal(holding["quantity"]) == Decimal("10")
    assert Decimal(holding["average_cost"]) == Decimal("150.15")
    assert Decimal(holding["cost_basis"]) == Decimal("1501.50000000")
    assert holding["currency"] == "GBP"
