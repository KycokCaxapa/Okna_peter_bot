from sqlalchemy import select, update

from src.database.database import async_session
from src.database.models import User


async def user_in_db(tg_id: int) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return True if user else False

async def add_user(tg_id: int, name: str) -> None:
    async with async_session() as session:
        session.add(User(tg_id=tg_id, name=name))
        await session.commit()
