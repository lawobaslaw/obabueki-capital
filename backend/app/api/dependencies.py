from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer

from app.exceptions.auth import InvalidCredentialsError
from app.models.user import User
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_user_repository(
    db: Session = Depends(get_db),
) -> UserRepository:
    """Provide a UserRepository instance."""

    return UserRepository(db)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    """Provide an AuthService instance."""

    return AuthService(user_repository)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    """Return the authenticated user."""

    payload = decode_access_token(token)

    email = payload.get("sub")

    if not email:
        raise InvalidCredentialsError("Invalid token.")

    user = user_repository.get_by_email(email)

    if user is None:
        raise InvalidCredentialsError("User not found.")

    return user
