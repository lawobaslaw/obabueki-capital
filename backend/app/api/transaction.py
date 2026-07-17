from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_current_user,
    get_transaction_service,
)
from app.exceptions.account import AccountNotFoundError
from app.exceptions.transaction import InvalidTransactionError, TransactionNotFoundError
from app.models.user import User
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    "/account/{account_id}",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    account_id: UUID,
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    transaction_service: TransactionService = Depends(
        get_transaction_service,
    ),
) -> TransactionResponse:
    """Create a new transaction."""

    try:
        transaction = transaction_service.create(
            account_id,
            transaction_data,
        )
        return transaction

    except AccountNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except InvalidTransactionError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "/account/{account_id}",
    response_model=list[TransactionResponse],
)
def list_transactions(
    account_id: UUID,
    current_user: User = Depends(get_current_user),
    transaction_service: TransactionService = Depends(
        get_transaction_service,
    ),
) -> list[TransactionResponse]:
    """List all transactions for an account."""

    try:
        return transaction_service.list_by_account(account_id)

    except AccountNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def get_transaction(
    transaction_id: UUID,
    current_user: User = Depends(get_current_user),
    transaction_service: TransactionService = Depends(
        get_transaction_service,
    ),
) -> TransactionResponse:
    """Retrieve a transaction."""

    try:
        return transaction_service.get_by_id(transaction_id)

    except TransactionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def update_transaction(
    transaction_id: UUID,
    transaction_data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    transaction_service: TransactionService = Depends(
        get_transaction_service,
    ),
) -> TransactionResponse:
    """Update a transaction."""

    try:
        return transaction_service.update(
            transaction_id,
            transaction_data,
        )

    except TransactionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_transaction(
    transaction_id: UUID,
    current_user: User = Depends(get_current_user),
    transaction_service: TransactionService = Depends(
        get_transaction_service,
    ),
) -> None:
    """Delete a transaction."""

    try:
        transaction_service.delete(transaction_id)

    except TransactionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
