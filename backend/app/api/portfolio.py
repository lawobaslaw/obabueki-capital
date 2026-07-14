from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_current_user,
    get_portfolio_service,
)
from app.exceptions.portfolio import DuplicatePortfolioError
from app.models.user import User
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse,
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
