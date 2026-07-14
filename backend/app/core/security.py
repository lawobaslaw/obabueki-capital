from datetime import datetime, timedelta, timezone


import bcrypt
from jose import JWTError, jwt

from app.core.config import settings
from app.exceptions.auth import InvalidCredentialsError

def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(),
    ).decode()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a hash."""
    return bcrypt.checkpw(
        password.encode(),
        password_hash.encode(),
    )


def create_access_token(subject: str) -> str:
    """Create a signed JWT access token."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token."""

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        return payload

    except JWTError as exc:
        raise InvalidCredentialsError("Invalid token.") from exc
