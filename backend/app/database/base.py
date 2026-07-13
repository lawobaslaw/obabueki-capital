from sqlalchemy.orm import DeclarativeBase

from app.database.naming import metadata


class Base(DeclarativeBase):
    metadata = metadata