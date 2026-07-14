from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)


def test_hash_password():
    password = "Password123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_create_access_token():
    token = create_access_token("test@example.com")

    assert isinstance(token, str)
    assert len(token) > 20
