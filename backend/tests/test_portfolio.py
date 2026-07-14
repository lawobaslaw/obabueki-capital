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
