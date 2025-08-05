from aiogram.types import Message
from aiogram import Router


router = Router()


@router.message()
async def fallback(message: Message) -> None:
    '''Handle any unmatched message'''
    await message.answer('🤖 Я не понял это сообщение.\nПожалуйста, используйте кнопки ниже 👇')
