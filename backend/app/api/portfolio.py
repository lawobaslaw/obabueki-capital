from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_current_user,
    get_portfolio_service,
)
from app.exceptions.portfolio import (
    DuplicatePortfolioError,
    PortfolioNotFoundError,
)
from app.models.user import User
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse,
    PortfolioUpdate,
)
from app.services.portfolio_service import PortfolioService

router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolios"],
)


@router.post(
    "",
    response_model=PortfolioResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_portfolio(
    request: PortfolioCreate,
    current_user: User = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(
        get_portfolio_service,
    ),
):
    try:
        return portfolio_service.create(
            current_user=current_user,
            name=request.name,
            description=request.description,
            base_currency=request.base_currency,
        )

    except DuplicatePortfolioError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[PortfolioResponse],
)
def list_portfolios(
    current_user: User = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(
        get_portfolio_service,
    ),
):
    return portfolio_service.list(current_user)


@router.get(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
)
def get_portfolio(
    portfolio_id: UUID,
    current_user: User = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(
        get_portfolio_service,
    ),
):
    """Return a single portfolio."""

    try:
        return portfolio_service.get(
            portfolio_id,
            current_user,
        )

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
)
def update_portfolio(
    portfolio_id: UUID,
    request: PortfolioUpdate,
    current_user: User = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(
        get_portfolio_service,
    ),
):
    """Update a portfolio."""

    try:
        return portfolio_service.update(
            portfolio_id=portfolio_id,
            current_user=current_user,
            name=request.name,
            description=request.description,
            base_currency=request.base_currency,
        )

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except DuplicatePortfolioError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_portfolio(
    portfolio_id: UUID,
    current_user: User = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(
        get_portfolio_service,
    ),
):
    """Delete a portfolio."""

    try:
        portfolio_service.delete(
            portfolio_id,
            current_user,
        )

    except PortfolioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
