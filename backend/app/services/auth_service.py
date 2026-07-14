from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    """Authentication business logic."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
    ) -> User:

        existing_user = self.user_repository.get_by_email(email)

        if existing_user:
            raise ValueError("Email already registered.")

        user = User(
            email=email,
            password_hash=hash_password(password),
            first_name=first_name,
            last_name=last_name,
        )

        return self.user_repository.create(user)

    def login(
        self,
        email: str,
        password: str,
    ) -> str:

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid credentials.")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials.")

        return create_access_token(user.email)
