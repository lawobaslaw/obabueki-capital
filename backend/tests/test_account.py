from uuid import uuid4
from fastapi.testclient import TestClient

from app.main import app
from tests.helpers import auth_headers

client = TestClient(app)


def test_create_account():
    headers = auth_headers()

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

    payload = {
        "name": "Trading 212",
        "broker": "Trading 212",
        "account_type": "BROKERAGE",
        "currency": "GBP",
        "is_default": True,
    }

    response = client.post(
        f"/accounts/portfolio/{portfolio_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == payload["name"]
    assert body["broker"] == payload["broker"]
    assert body["account_type"] == payload["account_type"]
    assert body["currency"] == payload["currency"]
    assert body["is_default"] is True


def test_create_duplicate_account():
    headers = auth_headers()

    portfolio = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    portfolio_id = portfolio.json()["id"]

    payload = {
        "name": "Trading 212",
        "broker": "Trading 212",
        "account_type": "BROKERAGE",
        "currency": "GBP",
        "is_default": True,
    }

    response = client.post(
        f"/accounts/portfolio/{portfolio_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 201

    response = client.post(
        f"/accounts/portfolio/{portfolio_id}",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Account name already exists."


def test_list_accounts():
    headers = auth_headers()

    portfolio = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    portfolio_id = portfolio.json()["id"]

    client.post(
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

    client.post(
        f"/accounts/portfolio/{portfolio_id}",
        json={
            "name": "Interactive Brokers",
            "broker": "Interactive Brokers",
            "account_type": "BROKERAGE",
            "currency": "USD",
            "is_default": False,
        },
        headers=headers,
    )

    response = client.get(
        f"/accounts/portfolio/{portfolio_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Trading 212"
    assert data[1]["name"] == "Interactive Brokers"


def test_get_account():
    headers = auth_headers()

    portfolio = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    portfolio_id = portfolio.json()["id"]

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

    account_id = response.json()["id"]

    response = client.get(
        f"/accounts/{account_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == account_id
    assert data["name"] == "Trading 212"


def test_update_account():
    headers = auth_headers()

    portfolio = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    portfolio_id = portfolio.json()["id"]

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

    account_id = response.json()["id"]

    response = client.patch(
        f"/accounts/{account_id}",
        json={
            "name": "Interactive Brokers",
            "broker": "IBKR",
            "currency": "USD",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Interactive Brokers"
    assert data["broker"] == "IBKR"
    assert data["currency"] == "USD"


def test_delete_account():
    headers = auth_headers()

    portfolio = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    portfolio_id = portfolio.json()["id"]

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

    account_id = response.json()["id"]

    response = client.delete(
        f"/accounts/{account_id}",
        headers=headers,
    )

    assert response.status_code == 204

    response = client.get(
        f"/accounts/{account_id}",
        headers=headers,
    )

    assert response.status_code == 404


def test_get_missing_account():
    headers = auth_headers()

    response = client.get(
        f"/accounts/{uuid4()}",
        headers=headers,
    )

    assert response.status_code == 404


def test_switch_default_account():
    headers = auth_headers()

    portfolio = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    portfolio_id = portfolio.json()["id"]

    first = client.post(
        f"/accounts/portfolio/{portfolio_id}",
        json={
            "name": "Trading 212",
            "broker": "Trading 212",
            "account_type": "BROKERAGE",
            "currency": "GBP",
            "is_default": True,
        },
        headers=headers,
    ).json()

    second = client.post(
        f"/accounts/portfolio/{portfolio_id}",
        json={
            "name": "Interactive Brokers",
            "broker": "IBKR",
            "account_type": "BROKERAGE",
            "currency": "USD",
            "is_default": False,
        },
        headers=headers,
    ).json()

    response = client.patch(
        f"/accounts/{second['id']}",
        json={
            "is_default": True,
        },
        headers=headers,
    )

    assert response.status_code == 200

    first_account = client.get(
        f"/accounts/{first['id']}",
        headers=headers,
    ).json()

    second_account = client.get(
        f"/accounts/{second['id']}",
        headers=headers,
    ).json()

    assert first_account["is_default"] is False
    assert second_account["is_default"] is True
