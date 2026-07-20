from datetime import UTC, datetime
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from tests.helpers import auth_headers, create_account, create_transaction

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


def test_list_transactions():
    headers = auth_headers()

    # Create portfolio
    portfolio_payload = {
        "name": "Retirement",
        "description": "Long-term investing",
        "base_currency": "GBP",
    }

    portfolio = client.post(
        "/portfolios",
        json=portfolio_payload,
        headers=headers,
    )

    assert portfolio.status_code == 201

    portfolio_id = portfolio.json()["id"]

    # Create account
    account_payload = {
        "name": "Trading 212",
        "broker": "Trading 212",
        "account_type": "BROKERAGE",
        "currency": "GBP",
        "is_default": True,
    }

    account = client.post(
        f"/accounts/portfolio/{portfolio_id}",
        json=account_payload,
        headers=headers,
    )

    assert account.status_code == 201

    account_id = account.json()["id"]

    # Create two transactions
    payload = {
        "transaction_type": "BUY",
        "symbol": "AAPL",
        "quantity": "10",
        "price": "150",
        "fees": "1.50",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    payload["symbol"] = "MSFT"

    client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    # List transactions
    response = client.get(
        f"/transactions/account/{account_id}",
        headers=headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 2

    assert body[0]["symbol"] == "AAPL"
    assert body[1]["symbol"] == "MSFT"


def test_get_transaction():
    headers = auth_headers()

    # Create portfolio
    portfolio = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term investing",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    assert portfolio.status_code == 201
    portfolio_id = portfolio.json()["id"]

    # Create account
    account = client.post(
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

    assert account.status_code == 201
    account_id = account.json()["id"]

    # Create transaction
    transaction = client.post(
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

    assert transaction.status_code == 201

    transaction_id = transaction.json()["id"]

    # Retrieve transaction
    response = client.get(
        f"/transactions/{transaction_id}",
        headers=headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == transaction_id
    assert body["symbol"] == "AAPL"
    assert body["transaction_type"] == "BUY"


def test_update_transaction():
    headers = auth_headers()

    # Create portfolio
    portfolio = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term investing",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    assert portfolio.status_code == 201
    portfolio_id = portfolio.json()["id"]

    # Create account
    account = client.post(
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

    assert account.status_code == 201
    account_id = account.json()["id"]

    # Create transaction
    transaction = client.post(
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

    assert transaction.status_code == 201

    transaction_id = transaction.json()["id"]

    # Update transaction
    response = client.patch(
        f"/transactions/{transaction_id}",
        json={
            "notes": "Monthly investment",
        },
        headers=headers,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == transaction_id
    assert body["notes"] == "Monthly investment"


def test_delete_transaction():
    headers = auth_headers()

    # Create portfolio
    portfolio = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term investing",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    assert portfolio.status_code == 201
    portfolio_id = portfolio.json()["id"]

    # Create account
    account = client.post(
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

    assert account.status_code == 201
    account_id = account.json()["id"]

    # Create transaction
    transaction = client.post(
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

    assert transaction.status_code == 201

    transaction_id = transaction.json()["id"]

    # Delete transaction
    response = client.delete(
        f"/transactions/{transaction_id}",
        headers=headers,
    )

    assert response.status_code == 204

    # Verify it no longer exists
    response = client.get(
        f"/transactions/{transaction_id}",
        headers=headers,
    )

    assert response.status_code == 404


def test_get_missing_transaction():
    headers = auth_headers()

    response = client.get(
        f"/transactions/{uuid4()}",
        headers=headers,
    )

    assert response.status_code == 404


def test_create_transaction_invalid_account():
    headers = auth_headers()

    payload = {
        "transaction_type": "BUY",
        "symbol": "AAPL",
        "quantity": "10",
        "price": "150",
        "fees": "1.50",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{uuid4()}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 404


def test_buy_requires_symbol():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "BUY",
        "quantity": "10",
        "price": "150",
        "fees": "1.50",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_buy_requires_quantity():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "BUY",
        "symbol": "AAPL",
        "price": "150",
        "fees": "1.50",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_buy_requires_price():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "BUY",
        "symbol": "AAPL",
        "quantity": "10",
        "fees": "1.50",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_buy_quantity_must_be_positive():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "BUY",
        "symbol": "AAPL",
        "quantity": "0",
        "price": "150",
        "fees": "1.50",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_buy_price_must_be_positive():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "BUY",
        "symbol": "AAPL",
        "quantity": "10",
        "price": "0",
        "fees": "1.50",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_dividend_requires_symbol():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "DIVIDEND",
        "amount": "50",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_dividend_requires_amount():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "DIVIDEND",
        "symbol": "AAPL",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_dividend_amount_must_be_positive():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "DIVIDEND",
        "symbol": "AAPL",
        "amount": "0",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_deposit_requires_amount():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "DEPOSIT",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_withdrawal_requires_amount():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "WITHDRAWAL",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_fee_requires_amount():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "FEE",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_amount_must_be_positive():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "DEPOSIT",
        "amount": "0",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_fee_cannot_be_negative():
    headers = auth_headers()

    account_id = create_account(headers)

    payload = {
        "transaction_type": "BUY",
        "symbol": "AAPL",
        "quantity": "10",
        "price": "150",
        "amount": "1500",
        "fees": "-1.00",
        "currency": "GBP",
        "transaction_date": datetime.now(UTC).isoformat(),
    }

    response = client.post(
        f"/transactions/account/{account_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400


def test_cannot_sell_more_than_owned():
    headers = auth_headers()

    account_id = create_account(headers)

    # Buy 10 shares
    create_transaction(
        headers=headers,
        account_id=account_id,
    )

    # Attempt to sell 20 shares
    response = client.post(
        f"/transactions/account/{account_id}",
        headers=headers,
        json={
            "transaction_type": "SELL",
            "symbol": "AAPL",
            "quantity": "20",
            "price": "160",
            "fees": "0.00",
            "currency": "GBP",
            "transaction_date": datetime.now(UTC).isoformat(),
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == ("Cannot sell more shares than currently held.")
