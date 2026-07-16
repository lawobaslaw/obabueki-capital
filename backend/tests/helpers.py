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
