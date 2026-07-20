from fastapi.testclient import TestClient

from app.main import app
from tests.helpers import (
    auth_headers,
    create_account,
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
