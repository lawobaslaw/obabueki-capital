from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_current_user,
    get_valuation_service,
)

from app.models.user import User
from app.schemas.valuation import PortfolioValuation
from app.services.valuation_service import ValuationService

router = APIRouter(
    prefix="/valuations",
    tags=["Valuations"],
)


@router.get(
    "/account/{account_id}",
    response_model=PortfolioValuation,
)
def get_account_valuation(
    account_id: UUID,
    current_user: User = Depends(get_current_user),
    valuation_service: ValuationService = Depends(
        get_valuation_service,
    ),
) -> PortfolioValuation:
    """Return the current valuation for an account."""
    return valuation_service.get_account_valuation(
        account_id,
        current_user,
    )
