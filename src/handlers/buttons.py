from aiogram.types import Message
from aiogram import F, Router

from src.database.requests import update_user
import src.keyboards as keyboards


router = Router()


@router.message(F.text == '👋 Консультация')
async def btn_order(message: Message) -> None:
    await message.answer('Отправьте номер телефона для записи на консультацию',
                         reply_markup=keyboards.phone_kb)

@router.message()
async def get_contact(message: Message) -> None:
    if message.contact:
        tg_id = message.from_user.id
        phone = message.contact.phone_number
        await update_user(tg_id, phone=phone)
        await message.answer(f'Мы украли ваш номер телефона')
