from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Enum
from typing import Annotated

import enum

from src.database.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id = mapped_column(BigInteger, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(default='', nullable=False)
    phone: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)


class PhotoCategory(enum.Enum):
    windows = 'windows'
    ceilings = 'ceilings'
    mosquito = 'mosquito'
    blinds = 'blinds'
    roller = 'roller'


class Photo(Base):
    __tablename__ = 'photos'

    id: Mapped[intpk]
    photo_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    category: Mapped[str] = mapped_column(Enum(PhotoCategory))
    description: Mapped[str]
