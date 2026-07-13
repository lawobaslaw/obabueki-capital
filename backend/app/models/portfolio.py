from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int]

    name: Mapped[str]

    base_currency: Mapped[str]

   

