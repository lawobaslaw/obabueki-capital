from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.exceptions.auth import DuplicateEmailError, InvalidCredentialsError

class AuthService:
    """Business logic for authentication."""

    def __init__(
    self,
    user_repository: UserRepository,
) -> None:
        self.user_repository = user_repository

    def register(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
    ) -> User:
        """Register a new user."""
        email = email.strip().lower()
        if self.user_repository.get_by_email(email):
            raise DuplicateEmailError("Email already registered.")

        
        user = User(
            email=email,
            password_hash=hash_password(password),
            first_name=first_name,
            last_name=last_name,
        )

        return self.user_repository.create(user)

    def authenticate(
        self,
        email: str,
        password: str,
    ) -> User:
        """Authenticate a user."""
        email = email.strip().lower()
        user = self.user_repository.get_by_email(email)

        if user is None:
            raise InvalidCredentialsError("Invalid credentials.")

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid credentials.")

        return user

    def login(
        self,
        email: str,
        password: str,
    ) -> str:
        """Authenticate a user and return an access token."""

        user = self.authenticate(email, password)

        return create_access_token(user.email)