from sqlalchemy import select, update

from src.database.database import async_session
from src.database.models import User, Gallery


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


async def user_in_db(tg_id: int) -> bool:
    '''Check if user exists in the DB by tg ID'''
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return True if user else False


async def add_user(tg_id: int, name: str) -> None:
    '''Add new user to the DB'''
    async with async_session() as session:
        session.add(User(tg_id=tg_id,
                         name=name,
                         phone=None))
        await session.commit()


async def get_all_users() -> list[User]:
    '''Get all users'''
    async with async_session() as session:
        users = await session.scalars(select(User))
        return list(users)


async def update_user(tg_id: int, **kwargs) -> None:
    '''Update user fields by tg ID'''
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(kwargs))
        await session.commit()


async def add_media(title:str,
                    media_id: str,
                    media_type: str,
                    category: str,
                    description: str) -> None:
    '''Add new photo to the DB'''
    async with async_session() as session:
        session.add(Gallery(title=title,
                            media_id=media_id,
                            media_type=media_type,
                            category=category,
                            description=description))
        await session.commit()


async def update_media(id: str, **kwargs) -> None:
    '''Update media fields by media ID'''
    async with async_session() as session:
        await session.execute(update(Gallery).where(Gallery.media_id == id).values(kwargs))
        await session.commit()


async def delete_media(id: str) -> None:
    '''Delete media by media ID'''
    async with async_session() as session:
        media = await session.scalar(select(Gallery).where(Gallery.media_id == id))
        await session.delete(media)
        await session.commit()


async def get_medias_by_category(category: str) -> list[Gallery]:
    '''Get list of media by category'''
    async with async_session() as session:
        medias = await session.scalars(select(Gallery).where(Gallery.category == category))
        return list(medias)
