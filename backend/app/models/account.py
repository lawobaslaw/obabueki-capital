from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.mixins import TimestampMixin, UUIDMixin
from app.models.enums import AccountType

if TYPE_CHECKING:
    from app.models.portfolio import Portfolio
    from app.models.transaction import Transaction


class Account(UUIDMixin, TimestampMixin, Base):
    """Represents an investment account."""

    __tablename__ = "accounts"

    portfolio_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("portfolios.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    broker: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    account_type: Mapped[AccountType] = mapped_column(
        Enum(AccountType, name="account_type_enum"),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        default="GBP",
        nullable=False,
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    portfolio: Mapped["Portfolio"] = relationship(
        back_populates="accounts",
        lazy="selectin",
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"Account("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"broker='{self.broker}', "
            f"account_type={self.account_type}, "
            f"currency='{self.currency}', "
            f"is_default={self.is_default})"
        )
