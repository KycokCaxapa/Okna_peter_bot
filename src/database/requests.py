from sqlalchemy import select, update

from src.database.database import async_session
from src.database.models import User, Photo


async def user_in_db(tg_id: int) -> bool:
    '''Check if user exists in the DB by tg ID'''
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return True if user else False


async def is_admin(tg_id: int) -> bool:
    '''Check admin by tg ID'''
    async with async_session() as session:
        admin = await session.scalar(select(User.is_admin).where(User.tg_id == tg_id))
        return admin


async def get_admins_tg_id() -> list[int]:
    '''Get all tg IDs of admins'''
    async with async_session() as session:
        admins = await session.scalars(select(User.tg_id).where(User.is_admin))
        return admins


async def add_user(tg_id: int, name: str) -> None:
    '''Add new user to the DB'''
    async with async_session() as session:
        session.add(User(tg_id=tg_id,
                         name=name,
                         phone=None))
        await session.commit()


async def update_user(tg_id: int, **kwargs) -> None:
    '''Update user fields by tg ID'''
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(kwargs))
        await session.commit()


async def add_photo(photo_id: str,
                    category: str,
                    description: str) -> None:
    '''Add new photo to the DB'''
    async with async_session() as session:
        session.add(Photo(photo_id=photo_id,
                            category=category,
                            description=description))
        await session.commit()


async def get_photos_by_category(category: str) -> list[Photo]:
    '''Get list of photos by category'''
    async with async_session() as session:
        photos = await session.scalars(select(Photo).where(Photo.category == category))
        return list(photos)
