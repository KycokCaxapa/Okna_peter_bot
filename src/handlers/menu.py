from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

from src.database.requests import (get_admins_tg_id, get_photos_by_category,
                                   update_user)
from src.texts import load_text

import src.keyboards as keyboards


router = Router()
NAVIGATION = load_text('navigation.txt')
FAQ = load_text('faq.txt')


@router.message(F.text == '🖼️ Фотогалерея')
async def btn_gallery(message: Message) -> None:
    '''Handle click on the gallery button'''
    await message.answer('Выберите категорию нашей продукции, которую хотите изучить',
                         reply_markup=keyboards.category_ikb())


@router.callback_query(F.data.startswith('gallery_'))
async def btn_gallery_category(callback: CallbackQuery) -> None:
    '''Handle click on the category from gallery menu'''
    await callback.answer()

    category = callback.data.split('_')[-1]
    photos = await get_photos_by_category(category)
    count = len(photos)
    page = 0

    if photos:
        caption = f'{photos[page].title}\n{photos[page].description}'
        await callback.message.answer_photo(
                photo=photos[page].photo_id,
                caption=caption,
                reply_markup=keyboards.pagination_ikb(category, page, count)
                )
    else:
        await callback.message.answer('Галерея пуста((')


@router.callback_query(F.data.startswith(('prev_', 'next_')))
async def pagination_callback(callback: CallbackQuery):
    '''Handle pagination buttons'''
    await callback.answer()

    action, category, page = callback.data.split('_')
    page = int(page) + 1 if action == 'next' else int(page) - 1
    photos = await get_photos_by_category(category)
    caption = f'{photos[page].title}\n{photos[page].description}'
    count = len(photos)


    await callback.message.edit_media(
        InputMediaPhoto(media=photos[page].photo_id,
                        caption=caption),
        reply_markup=keyboards.pagination_ikb(category, page, count)
    )


@router.callback_query(F.data == 'current_page')
async def btn_current_page(callback: CallbackQuery) -> None:
    '''Handle click on the current page button'''
    await callback.answer('Вы ничего этим не добьётесь')


@router.callback_query(F.data.startswith('want'))
async def btn_want(callback: CallbackQuery,
                   state: FSMContext) -> None:
    '''Handle click on the want ibutton'''
    await callback.answer()

    _, category, page = callback.data.split('_')
    await state.update_data(category=category,
                            page=page)
    await callback.message.answer('Отправьте свой номер телефона, нажав на кнопку ниже, чтобы менеджер смог с вами связаться',
                                  reply_markup=keyboards.phone_kb)


@router.callback_query(F.data == 'back_to_category')
async def btn_back_to_category(callback: CallbackQuery) -> None:
    '''Handle click on the back to category button'''
    await callback.answer()
    await callback.message.answer('Выберите категорию нашей продукции, которую хотите изучить',
                                  reply_markup=keyboards.category_ikb())


@router.message(F.text == '👋 Консультация')
async def btn_order(message: Message) -> None:
    '''Handle click on the order button'''
    await message.answer('Отправьте номер телефона для записи на консультацию',
                         reply_markup=keyboards.phone_kb)


@router.message(F.contact)
async def get_contact(message: Message,
                      state: FSMContext) -> None:
    '''Handle the phone number sent from user and send it to admins'''
    tg_id = message.from_user.id
    fullname = message.from_user.full_name
    phone = message.contact.phone_number
    admins = await get_admins_tg_id()
    chat_id = message.chat.id

    data = await state.get_data()
    

    if data:    #"or" because the page can be 0 (None) 😮🤯
        category = data.get('category')
        page = int(data.get('page') if data else None)

        photos = await get_photos_by_category(category)
        order = (
            f'Новая заявка по галерее:\n'
            f'Запрос: {photos[page].title}\n'
            f'Пользователь: <a href="tg://openmessage?user_id={chat_id}">{fullname}</a>\n'
            f'Номер: <code>+{phone}</code>'
        )
        await message.answer('✅ Ваш запрос по товару получен. Менеджер свяжется с вами!')
        await state.clear()
    else:
        order = f'Новая заявка: <a href="tg://openmessage?user_id={chat_id}">{fullname}</a>, <code>+{phone}</code>'
        await message.answer('✅ Спасибо! Мы свяжемся с вами.')

    await update_user(tg_id, phone=phone)
    await message.answer(f'Мы украли ваш номер телефона',
                         reply_markup=keyboards.main_kb)

    for admin in admins:
        await message.bot.send_message(admin, order, parse_mode='HTML')


@router.message(F.text == '◀️ Назад')
async def btn_back_from_phone(message: Message) -> None:
    '''Handle click on the back button in send phone action'''
    await message.answer('Выберите действие.',
                         reply_markup=keyboards.main_kb)


@router.message(F.text == '📍 Навигация')
async def btn_navigation(message: Message) -> None:
    '''Handle click on the navigation button'''
    await message.answer(NAVIGATION,
                         parse_mode='HTML')


@router.message(F.text == '❓ Ответы на часто задаваемые вопросы')
async def btn_faq(message: Message) -> None:
    '''Handle click on the FAQ button'''
    await message.answer(FAQ,
                         parse_mode='HTML',
                         disable_web_page_preview=True)
