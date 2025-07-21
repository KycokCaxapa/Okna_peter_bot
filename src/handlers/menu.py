from aiogram.types import Message
from aiogram import F, Router

from src.database.requests import update_user
from src.texts import load_text

import src.keyboards as keyboards


router = Router()
NAVIGATION = load_text('navigation.txt')
FAQ = load_text('faq.txt')


@router.message(F.text == '👋 Консультация')
async def btn_order(message: Message) -> None:
    '''Handle click on the "👋 Консультация"'''
    await message.answer('Отправьте номер телефона для записи на консультацию',
                         reply_markup=keyboards.phone_kb)


@router.message(F.text == '📍 Навигация')
async def btn_navigation(message: Message) -> None:
    '''Handle click on the "📍 Навигация"'''
    await message.answer(NAVIGATION,
                         parse_mode='HTML')


@router.message(F.text == '❓ Ответы на часто задаваемые вопросы')
async def btn_faq(message: Message) -> None:
    '''Handle click on the "❓ Ответы на часто задаваемые вопросы"'''
    await message.answer(FAQ,
                         parse_mode='HTML',
                         disable_web_page_preview=True)


@router.message(F.text == '◀️ Назад')
async def btn_back(message: Message) -> None:
    '''Handle click on the "◀️ Назад"'''
    await message.answer('Выберите действие.',
                         reply_markup=keyboards.main_kb)


@router.message()
async def get_contact(message: Message) -> None:
    '''Handle the phone number sent to user'''
    if message.contact:
        tg_id = message.from_user.id
        phone = message.contact.phone_number
        await update_user(tg_id, phone=phone)
        await message.answer(f'Мы украли ваш номер телефона')
