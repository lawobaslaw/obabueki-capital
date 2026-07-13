from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    portfolio_id: Mapped[str]

    name: Mapped[str]

    broker: Mapped[str]
    currency: Mapped[str]
    account_type: Mapped[str]

   


