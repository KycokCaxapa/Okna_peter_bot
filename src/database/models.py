from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger
from typing import Annotated

from src.database.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id = mapped_column(BigInteger)
    name: Mapped[str]
    phone: Mapped[str] = mapped_column(nullable=True)
