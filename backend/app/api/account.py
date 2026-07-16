from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_account_service,
    get_current_user,
)
from app.exceptions.account import (
    AccountNotFoundError,
    DuplicateAccountError,
)
from app.exceptions.portfolio import PortfolioNotFoundError
from app.models.user import User
from app.schemas.account import (
    AccountCreate,
    AccountResponse,
    AccountUpdate,
)
from app.services.account_service import AccountService

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


@router.post(
    "/portfolio/{portfolio_id}",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    portfolio_id: UUID,
    request: AccountCreate,
    current_user: User = Depends(get_current_user),
    account_service: AccountService = Depends(
        get_account_service,
    ),
):
    try:
        return account_service.create(
            current_user=current_user,
            portfolio_id=portfolio_id,
            name=request.name,
            broker=request.broker,
            account_type=request.account_type,
            currency=request.currency,
            is_default=request.is_default,
        )

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except DuplicateAccountError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/portfolio/{portfolio_id}",
    response_model=list[AccountResponse],
)
def list_accounts(
    portfolio_id: UUID,
    current_user: User = Depends(get_current_user),
    account_service: AccountService = Depends(
        get_account_service,
    ),
):
    try:
        return account_service.list(
            portfolio_id,
            current_user,
        )

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
)
def get_account(
    account_id: UUID,
    current_user: User = Depends(get_current_user),
    account_service: AccountService = Depends(
        get_account_service,
    ),
):
    try:
        return account_service.get(
            account_id,
            current_user,
        )

    except AccountNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{account_id}",
    response_model=AccountResponse,
)
def update_account(
    account_id: UUID,
    request: AccountUpdate,
    current_user: User = Depends(get_current_user),
    account_service: AccountService = Depends(
        get_account_service,
    ),
):
    try:
        return account_service.update(
            account_id=account_id,
            current_user=current_user,
            name=request.name,
            broker=request.broker,
            account_type=request.account_type,
            currency=request.currency,
            is_default=request.is_default,
        )

    except AccountNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except DuplicateAccountError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_account(
    account_id: UUID,
    current_user: User = Depends(get_current_user),
    account_service: AccountService = Depends(
        get_account_service,
    ),
):
    try:
        account_service.delete(
            account_id,
            current_user,
        )

    except AccountNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
