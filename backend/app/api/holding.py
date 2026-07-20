from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_current_user,
    get_holding_service,
)
from app.exceptions.account import AccountNotFoundError
from app.models.user import User
from app.schemas.holding import HoldingResponse
from app.services.holding_service import HoldingService

router = APIRouter(
    prefix="/accounts",
    tags=["Holdings"],
)


@router.get(
    "/{account_id}/holdings",
    response_model=list[HoldingResponse],
    status_code=status.HTTP_200_OK,
)
def list_holdings(
    account_id: UUID,
    current_user: User = Depends(get_current_user),
    holding_service: HoldingService = Depends(
        get_holding_service,
    ),
) -> list[HoldingResponse]:
    """Return calculated holdings for an account."""

    try:
        return holding_service.list_by_account(
            account_id,
            current_user,
        )

    except AccountNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
