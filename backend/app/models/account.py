from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.portfolio import Portfolio


class Account(UUIDMixin, TimestampMixin, Base):
    """Represents an investment account."""

    __tablename__ = "accounts"

    portfolio_id: Mapped[str] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("portfolios.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    institution: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    account_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    portfolio: Mapped["Portfolio"] = relationship(
        back_populates="accounts",
    )