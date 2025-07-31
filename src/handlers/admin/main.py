from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F, Router

from src.database.requests import is_admin

import src.keyboards as keyboards


router = Router()


@router.message(Command('admin'))
async def cmd_admin(message: Message) -> None:
    '''Handle /admin command'''
    tg_id = message.from_user.id

    if await is_admin(tg_id):
        await message.answer('Вы вошли в админ-панель 🤯',
                             reply_markup=keyboards.admin_kb)
    else:
        await message.answer('Не дорос ещё((')


@router.callback_query(F.data == 'cancel_action')
async def cancel_action(callback: CallbackQuery,
                          state: FSMContext) -> None:
    '''Cancel add photo action'''
    await callback.answer()
    await state.clear()
    await callback.message.answer('👌 Действие отменено')
