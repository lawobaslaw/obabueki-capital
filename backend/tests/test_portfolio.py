from uuid import uuid4

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


def test_create_portfolio():
    headers = auth_headers()

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

    data = response.json()

    assert data["name"] == "Retirement"
    assert data["description"] == "Long-term investing"
    assert data["base_currency"] == "GBP"
    assert "id" in data


def test_create_duplicate_portfolio():
    headers = auth_headers()

    payload = {
        "name": "Retirement",
        "description": "Long-term investing",
        "base_currency": "GBP",
    }

    response = client.post(
        "/portfolios",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 201

    response = client.post(
        "/portfolios",
        json=payload,
        headers=headers,
    )

    assert response.status_code == 400

    assert response.json()["detail"] == ("Portfolio name already exists.")


def test_list_portfolios():
    headers = auth_headers()

    client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    client.post(
        "/portfolios",
        json={
            "name": "Trading",
            "description": "Stocks",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    response = client.get(
        "/portfolios",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Retirement"
    assert data[1]["name"] == "Trading"


def test_get_portfolio():
    headers = auth_headers()

    response = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    portfolio_id = response.json()["id"]

    response = client.get(
        f"/portfolios/{portfolio_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == portfolio_id
    assert data["name"] == "Retirement"


def test_update_portfolio():
    headers = auth_headers()

    response = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    portfolio_id = response.json()["id"]

    response = client.patch(
        f"/portfolios/{portfolio_id}",
        json={
            "name": "Retirement Updated",
            "description": "Updated description",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Retirement Updated"
    assert data["description"] == "Updated description"


def test_delete_portfolio():
    headers = auth_headers()

    response = client.post(
        "/portfolios",
        json={
            "name": "Retirement",
            "description": "Long-term",
            "base_currency": "GBP",
        },
        headers=headers,
    )

    portfolio_id = response.json()["id"]

    response = client.delete(
        f"/portfolios/{portfolio_id}",
        headers=headers,
    )

    assert response.status_code == 204

    response = client.get(
        f"/portfolios/{portfolio_id}",
        headers=headers,
    )

    assert response.status_code == 404


def test_requires_authentication():
    response = client.get("/portfolios")

    assert response.status_code == 401


def test_get_missing_portfolio():
    headers = auth_headers()

    response = client.get(
        f"/portfolios/{uuid4()}",
        headers=headers,
    )

    assert response.status_code == 404
