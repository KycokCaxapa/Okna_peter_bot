from sqlalchemy import ARRAY, BigInteger, Enum, String
from sqlalchemy.orm import Mapped, mapped_column
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
    options: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)


class GalleryCategory(enum.Enum):
    windows = 'windows'
    balconies = 'balconies'
    restoration = 'restoration'
    ceilings = 'ceilings'
    spp = 'spp'
    mosquito = 'mosquito'
    blinds = 'blinds'
    roller = 'roller'


class MediaType(enum.Enum):
    photo = 'photo'
    video = 'video'


class Gallery(Base):
    __tablename__ = 'gallery'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(nullable=False)
    media_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    media_type: Mapped[str] = mapped_column(Enum(MediaType), name='media_type')
    category: Mapped[str] = mapped_column(Enum(GalleryCategory), name='category')
    description: Mapped[str]
