from sqlalchemy import select, update

from src.database.database import async_session
from src.database.models import User


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


async def update_user(tg_id: int, **kwargs) -> None:
    '''Update user fields by tg ID'''
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(kwargs))
        await session.commit()
