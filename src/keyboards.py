from aiogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                           KeyboardButton, InlineKeyboardButton)


add_photo_btn = KeyboardButton(text='🖼️ Добавить фото в галерею')
gallery_btn = KeyboardButton(text='🖼️ Фотогалерея')
order_btn = KeyboardButton(text='👋 Консультация')
nav_btn = KeyboardButton(text='📍 Навигация')
faq_btn = KeyboardButton(text='❓ Ответы на часто задаваемые вопросы')
phone_btn = KeyboardButton(text='📞 Отправить мой номер телефона',
                           request_contact=True)
spam_btn = KeyboardButton(text='📢 Запустить рассылку')
stocks_ibtn = InlineKeyboardButton(text='🎁 Акции и бонусы',
                                   callback_data='stocks')
vote_ibtn = InlineKeyboardButton(text='🙋‍♀️ Голосование',
                                   callback_data='vote')
back_btn = KeyboardButton(text='◀️ Назад')
confirm_spam_ibtn = InlineKeyboardButton(text='✅ Подтвердить действие',
                                    callback_data='confirm_spam_action')
cancel_ibtn = InlineKeyboardButton(text='❌ Отменить действие',
                                   callback_data='cancel_action')

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [add_photo_btn],
        [spam_btn],
        [back_btn]
    ],
    resize_keyboard=True
)

main_kb = ReplyKeyboardMarkup(
        keyboard=[
            [gallery_btn],
            [order_btn, nav_btn],
            [faq_btn]
        ],
        resize_keyboard=True
        )

phone_kb = ReplyKeyboardMarkup(
    keyboard=[[phone_btn],
              [back_btn]],
    resize_keyboard=True,
    one_time_keyboard=True
)

spam_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [stocks_ibtn, vote_ibtn]
])

confirm_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [confirm_spam_ibtn],
    [cancel_ibtn]
])

cancel_ikb = InlineKeyboardMarkup(inline_keyboard=[[cancel_ibtn]])


def category_ikb(is_admin: bool = False) -> None:
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
            ],
            [cancel_ibtn]
        ]
    )


def pagination_ikb(category: str,
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
