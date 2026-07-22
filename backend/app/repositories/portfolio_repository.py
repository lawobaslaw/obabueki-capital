from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.portfolio import Portfolio


class PortfolioRepository:
    """Repository for portfolio database operations."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, portfolio: Portfolio) -> Portfolio:
        self.session.add(portfolio)
        self.session.commit()
        self.session.refresh(portfolio)
        return portfolio

    def get_by_id(self, portfolio_id: UUID) -> Portfolio | None:
        statement = select(Portfolio).where(Portfolio.id == portfolio_id)
        return self.session.scalar(statement)

    def list_by_user_id(self, user_id: UUID) -> list[Portfolio]:
        statement = (
            select(Portfolio)
            .where(Portfolio.user_id == user_id)
            .order_by(Portfolio.created_at)
        )

        return self.session.scalars(statement).all()

    def save(
        self,
        portfolio: Portfolio,
    ) -> Portfolio:
        self.session.add(portfolio)
        self.session.commit()
        self.session.refresh(portfolio)
        return portfolio

    def delete(
        self,
        portfolio: Portfolio,
    ) -> None:
        self.session.delete(portfolio)
        self.session.commit()
