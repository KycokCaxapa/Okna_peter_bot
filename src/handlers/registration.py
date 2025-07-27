from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router

from src.database.requests import add_user, is_admin, user_in_db

import src.keyboards as keyboards


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    '''Handle click on the gallery button for users'''
    tg_id = message.from_user.id
    full_name = message.from_user.full_name
    if not await user_in_db(tg_id):
        await add_user(tg_id, full_name)
        await message.answer(f'Приветствую...\nБлаблабла\nБимбимбамбам',
                             reply_markup=keyboards.main_kb)
    else:
        await message.answer('Выберите действие',
                             reply_markup=keyboards.main_kb)
