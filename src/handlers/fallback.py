from aiogram.types import Message
from aiogram import Router

import src.keyboards as keyboards


router = Router()


@router.message()
async def fallback(message: Message) -> None:
    '''Handle any unmatched message'''
    await message.answer('🤖 Я не понял это сообщение.\nПожалуйста, используйте кнопки ниже 👇',
                         reply_markup=keyboards.main_kb)
