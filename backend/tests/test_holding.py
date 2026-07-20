from datetime import UTC, datetime
from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app
from tests.helpers import (
    auth_headers,
    create_account,
    create_transaction,
)

client = TestClient(app)


def test_list_holdings_returns_empty_list():
    headers = auth_headers()

    account_id = create_account(headers)

    response = client.get(
        f"/accounts/{account_id}/holdings",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json() == []


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

    holding = response.json()[0]

    assert holding["symbol"] == "AAPL"
    assert Decimal(holding["quantity"]) == Decimal("10")
    assert Decimal(holding["average_cost"]) == Decimal("150.15")
    assert Decimal(holding["cost_basis"]) == Decimal("1501.50")
    assert holding["currency"] == "GBP"


def test_multiple_buy_transactions_calculate_average_cost():
    headers = auth_headers()

    account_id = create_account(headers)

    create_transaction(
        headers=headers,
        account_id=account_id,
    )

    response = client.post(
        f"/transactions/account/{account_id}",
        headers=headers,
        json={
            "transaction_type": "BUY",
            "symbol": "AAPL",
            "quantity": "5",
            "price": "120",
            "fees": "0.00",
            "currency": "GBP",
            "transaction_date": datetime.now(UTC).isoformat(),
        },
    )

    assert response.status_code == 201

    response = client.get(
        f"/accounts/{account_id}/holdings",
        headers=headers,
    )

    holding = response.json()[0]

    assert Decimal(holding["quantity"]) == Decimal("15")
    assert Decimal(holding["average_cost"]) == Decimal("140.10")
    assert Decimal(holding["cost_basis"]) == Decimal("2101.50")


def test_sell_transaction_reduces_quantity():
    headers = auth_headers()

    account_id = create_account(headers)

    create_transaction(
        headers=headers,
        account_id=account_id,
    )

    response = client.post(
        f"/transactions/account/{account_id}",
        headers=headers,
        json={
            "transaction_type": "SELL",
            "symbol": "AAPL",
            "quantity": "4",
            "price": "160",
            "fees": "0.00",
            "currency": "GBP",
            "transaction_date": datetime.now(UTC).isoformat(),
        },
    )

    assert response.status_code == 201

    response = client.get(
        f"/accounts/{account_id}/holdings",
        headers=headers,
    )

    holding = response.json()[0]

    assert Decimal(holding["quantity"]) == Decimal("6")
    assert Decimal(holding["average_cost"]) == Decimal("150.15")
    assert Decimal(holding["cost_basis"]) == Decimal("900.90")


def test_sell_all_shares_removes_holding():
    headers = auth_headers()

    account_id = create_account(headers)

    create_transaction(
        headers=headers,
        account_id=account_id,
    )

    response = client.post(
        f"/transactions/account/{account_id}",
        headers=headers,
        json={
            "transaction_type": "SELL",
            "symbol": "AAPL",
            "quantity": "10",
            "price": "160",
            "fees": "0.00",
            "currency": "GBP",
            "transaction_date": datetime.now(UTC).isoformat(),
        },
    )

    assert response.status_code == 201

    response = client.get(
        f"/accounts/{account_id}/holdings",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json() == []
