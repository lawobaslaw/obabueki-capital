from uuid import uuid4
from datetime import UTC, datetime
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def register_user(email: str) -> None:
    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "Password123!",
            "first_name": "Larry",
            "last_name": "Obabueki",
        },
    )

    assert response.status_code == 201


def auth_headers() -> dict[str, str]:
    email = f"{uuid4()}@example.com"

    register_user(email)

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


def create_portfolio(headers: dict) -> str:
    response = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term investing",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_account(headers: dict) -> str:
    portfolio_id = create_portfolio(headers)

    response = client.post(
        f"/accounts/portfolio/{portfolio_id}",
        json={
            "name": "Trading 212",
            "broker": "Trading 212",
            "account_type": "BROKERAGE",
            "currency": "GBP",
            "is_default": True,
        },
        headers=headers,
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_transaction(headers: dict, account_id: str) -> dict:
    response = client.post(
        f"/transactions/account/{account_id}",
        json={
            "transaction_type": "BUY",
            "symbol": "AAPL",
            "quantity": "10",
            "price": "150",
            "fees": "1.50",
            "currency": "GBP",
            "transaction_date": datetime.now(UTC).isoformat(),
        },
        headers=headers,
    )

    assert response.status_code == 201

    return response.json()
