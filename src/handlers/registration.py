from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router

from src.database.requests import add_user, user_in_db
import src.keyboards as keyboards


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    tg_id = message.from_user.id
    if not await user_in_db(tg_id):
        await add_user(tg_id, message.from_user.full_name)
        await message.answer(f'Приветствую...\nБлаблабла\nБимбимбамбам',
                             reply_markup=keyboards.main_kb)
    else:
        await message.answer('Выберите действие.',
                             reply_markup=keyboards.main_kb)
