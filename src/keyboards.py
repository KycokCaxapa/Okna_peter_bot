from aiogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                           KeyboardButton, InlineKeyboardButton)


add_photo = KeyboardButton(text='🖼️ Добавить фото в галерею')
gallery = KeyboardButton(text='🖼️ Фотогалерея')
order = KeyboardButton(text='👋 Консультация')
nav = KeyboardButton(text='📍 Навигация')
faq = KeyboardButton(text='❓ Ответы на часто задаваемые вопросы')
phone = KeyboardButton(text='📞 Отправить мой номер телефона', request_contact=True)
back = KeyboardButton(text='◀️ Назад')

phone_kb = ReplyKeyboardMarkup(
    keyboard=[[phone],
              [back]],
    resize_keyboard=True,
    one_time_keyboard=True
)


def main_kb(is_admin: bool = False) -> None:
    keyboard=[
            [gallery],
            [order, nav],
            [faq]
    ]
    if is_admin:
        keyboard.append([add_photo])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


def category_kb(is_admin: bool = False) -> None:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🪟 Окна', callback_data=f'{'admin_' if is_admin else ''}gallery_windows')
            ],
            [
                InlineKeyboardButton(text='🏠 Потолки', callback_data=f'{'admin_' if is_admin else ''}gallery_ceilings'),
            ],
            [
                InlineKeyboardButton(text='🦟 Москитные сетки', callback_data=f'{'admin_' if is_admin else ''}gallery_mosquito')
            ],
            [
                InlineKeyboardButton(text='🪟 Жалюзи', callback_data=f'{'admin_' if is_admin else ''}gallery_blinds'),
            ],
            [
                InlineKeyboardButton(text='🧵 Рулонные шторы', callback_data=f'{'admin_' if is_admin else ''}gallery_roller'),
            ]
        ]
    )


def pagination_kb(category: str,
                  page: int,
                  count: int) -> InlineKeyboardMarkup:
    keyboard = []

    if page != 0:
        keyboard.append(InlineKeyboardButton(text='◀️',
                                            callback_data=f'prev_{category}_{page}'))

    keyboard.append(InlineKeyboardButton(text=f'{page + 1}/{count}',
                                        callback_data='current_page'))

    if page + 1 != count:
        keyboard.append(InlineKeyboardButton(text='▶️',
                                            callback_data=f'next_{category}_{page}'))
    
    back = InlineKeyboardButton(text='◀️ Назад к категориям',
                                        callback_data='back_to_category')

    return InlineKeyboardMarkup(inline_keyboard=[keyboard, [back]])
