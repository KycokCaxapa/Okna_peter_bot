from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger
from typing import Annotated

from src.database.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id = mapped_column(BigInteger, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(default='', nullable=False)
    phone: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[intpk]
    tg_id = mapped_column(BigInteger, nullable=False, unique=True)
