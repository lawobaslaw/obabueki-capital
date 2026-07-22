from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer

from app.exceptions.auth import InvalidCredentialsError
from app.models.user import User
from app.core.security import decode_access_token
from app.repositories.portfolio_repository import PortfolioRepository
from app.services.portfolio_service import PortfolioService
from app.repositories.account_repository import AccountRepository
from app.services.account_service import AccountService
from app.repositories.transaction_repository import TransactionRepository
from app.services.transaction_service import TransactionService
from app.services.holding_service import HoldingService
from app.services.price_service import PriceService
from app.services.valuation_service import ValuationService

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


def get_portfolio_repository(
    db: Session = Depends(get_db),
) -> PortfolioRepository:
    """Provide a PortfolioRepository instance."""

    return PortfolioRepository(db)


def get_portfolio_service(
    portfolio_repository: PortfolioRepository = Depends(
        get_portfolio_repository,
    ),
) -> PortfolioService:
    """Provide a PortfolioService instance."""

    return PortfolioService(portfolio_repository)


def get_account_repository(
    session: Session = Depends(get_db),
) -> AccountRepository:
    """Return an AccountRepository."""

    return AccountRepository(session)


def get_account_service(
    account_repository: AccountRepository = Depends(
        get_account_repository,
    ),
    portfolio_repository: PortfolioRepository = Depends(
        get_portfolio_repository,
    ),
) -> AccountService:
    """Return an AccountService."""

    return AccountService(
        account_repository=account_repository,
        portfolio_repository=portfolio_repository,
    )


def get_transaction_repository(
    session: Session = Depends(get_db),
) -> TransactionRepository:
    """Return a TransactionRepository."""

    return TransactionRepository(session)


def get_transaction_service(
    account_repository: AccountRepository = Depends(
        get_account_repository,
    ),
    transaction_repository: TransactionRepository = Depends(
        get_transaction_repository,
    ),
) -> TransactionService:
    """Return a TransactionService."""

    return TransactionService(
        account_repository=account_repository,
        transaction_repository=transaction_repository,
    )


def get_holding_service(
    transaction_repository: TransactionRepository = Depends(
        get_transaction_repository,
    ),
    account_repository: AccountRepository = Depends(
        get_account_repository,
    ),
) -> HoldingService:
    """Return a HoldingService."""

    return HoldingService(
        transaction_repository=transaction_repository,
        account_repository=account_repository,
    )


def get_price_service() -> PriceService:
    """Return a PriceService."""

    return PriceService()


def get_valuation_service(
    holding_service: HoldingService = Depends(
        get_holding_service,
    ),
    price_service: PriceService = Depends(
        get_price_service,
    ),
) -> ValuationService:
    """Return a ValuationService."""

    return ValuationService(
        holding_service=holding_service,
        price_service=price_service,
    )
