from datetime import UTC, datetime


from fastapi.testclient import TestClient

from app.main import app
from tests.helpers import auth_headers

client = TestClient(app)


def test_create_transaction():
    headers = auth_headers()

    portfolio_payload = {
        "name": "Retirement",
        "description": "Long-term investing",
        "base_currency": "GBP",
    }

    portfolio_response = client.post(
        "/portfolios",
        json=portfolio_payload,
        headers=headers,
    )

    assert portfolio_response.status_code == 201

    portfolio_id = portfolio_response.json()["id"]

    account_payload = {
        "name": "Trading 212",
        "broker": "Trading 212",
        "account_type": "BROKERAGE",
        "currency": "GBP",
        "is_default": True,
    }

    account_response = client.post(
        f"/accounts/portfolio/{portfolio_id}",
        json=account_payload,
        headers=headers,
    )

    assert account_response.status_code == 201

    account_id = account_response.json()["id"]

    transaction_payload = {
        "transaction_type": "BUY",
        "symbol": "AAPL",
        "quantity": "10",
        "price": "150.25",
        "fees": "1.50",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    transaction_response = client.post(
        f"/transactions/account/{account_id}",
        json=transaction_payload,
        headers=headers,
    )

    assert transaction_response.status_code == 201

    body = transaction_response.json()

    assert body["transaction_type"] == "BUY"
    assert body["symbol"] == "AAPL"
    assert body["currency"] == "GBP"
