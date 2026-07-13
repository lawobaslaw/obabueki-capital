from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.account import Account


class Portfolio(UUIDMixin, TimestampMixin, Base):
    """Represents an investment portfolio."""

    __tablename__ = "portfolios"

    user_id: Mapped[str] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    base_currency: Mapped[str] = mapped_column(
        String(3),
        default="NGN",
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="portfolios",
    )

    accounts: Mapped[list["Account"]] = relationship(
        back_populates="portfolio",
        cascade="all, delete-orphan",
    )