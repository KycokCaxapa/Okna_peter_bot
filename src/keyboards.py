from aiogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                           KeyboardButton, InlineKeyboardButton)


add_media_btn = KeyboardButton(text='🖼️ Пополнить галерею')
edit_media_btn = KeyboardButton(text='✏️ Редактировать галерею')
gallery_btn = KeyboardButton(text='🖼️ Галерея')
back_ibtn = InlineKeyboardButton(text='◀️ Назад к категориям',
                                     callback_data='back_to_category')
order_btn = KeyboardButton(text='👋 Консультация')
nav_btn = KeyboardButton(text='📍 Навигация')
faq_btn = KeyboardButton(text='❓ Ответы на часто задаваемые вопросы')
phone_btn = KeyboardButton(text='📞 Отправить мой номер телефона',
                           request_contact=True)
edit_title_ibtn = InlineKeyboardButton(text='Изменить название',
                                      callback_data='edit_title')
edit_description_ibtn = InlineKeyboardButton(text='Изменить описание',
                                             callback_data='edit_description')
edit_media_ibtn = InlineKeyboardButton(text='Изменить медиа',
                                       callback_data='edit_media')
delete_media_ibtn = InlineKeyboardButton(text='🗑️ Удалить медиа',
                                         callback_data='delete_media')
confirm_delete_ibtn = InlineKeyboardButton(text='✅ Удалить медиа',
                                           callback_data='confirm_delete_action')
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
        [add_media_btn],
        [edit_media_btn],
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

edit_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [edit_title_ibtn],
    [edit_description_ibtn],
    [edit_media_ibtn],
    [delete_media_ibtn],
    [back_ibtn]
])

confirm_delete_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [confirm_delete_ibtn],
    [cancel_ibtn]
])

spam_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [stocks_ibtn, vote_ibtn]
])

confirm_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [confirm_spam_ibtn],
    [cancel_ibtn]
])

cancel_ikb = InlineKeyboardMarkup(inline_keyboard=[[cancel_ibtn]])


def category_ikb(is_admin: bool = False,
                 flag: bool = False) -> None:
    prefix = f'{'admin_' if is_admin else ''}{'create_' if flag else 'edit_' if is_admin else ''}'

    return InlineKeyboardMarkup(
        # Использовать лишь одно слово после "gallery_", так как оно определяет категорию
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🪟 Окна', callback_data=f'{prefix}gallery_windows')
            ],
            [
                InlineKeyboardButton(text='🪟 Балконы', callback_data=f'{prefix}gallery_balconies')
            ],
            [
                InlineKeyboardButton(text='🔨 Реставрация', callback_data=f'{prefix}gallery_restoration')
            ],
            [
                InlineKeyboardButton(text='🏠 Потолки', callback_data=f'{prefix}gallery_ceilings'),
            ],
            [
                InlineKeyboardButton(text='🏠 Ремонт потолков', callback_data=f'{prefix}gallery_spp'),
            ],
            [
                InlineKeyboardButton(text='🦟 Москитные сетки', callback_data=f'{prefix}gallery_mosquito')
            ],
            [
                InlineKeyboardButton(text='🪟 Жалюзи', callback_data=f'{prefix}gallery_blinds'),
            ],
            [
                InlineKeyboardButton(text='🧵 Рулонные шторы', callback_data=f'{prefix}gallery_roller'),
            ],
            [cancel_ibtn] if is_admin else []
        ]
    )


def pagination_ikb(category: str,
                   page: int,
                   count: int,
                   is_admin: bool = False) -> InlineKeyboardMarkup:
    keyboard = []
    prefix = 'admin_' if is_admin else ''

    if page != 0:
        keyboard.append(InlineKeyboardButton(text='◀️',
                                            callback_data=f'{prefix}prev_{category}_{page}'))

    keyboard.append(InlineKeyboardButton(text=f'{page + 1}/{count}',
                                        callback_data='current_page'))

    if page + 1 != count:
        keyboard.append(InlineKeyboardButton(text='▶️',
                                            callback_data=f'{prefix}next_{category}_{page}'))
    want = InlineKeyboardButton(text='😮😮 Хочу!!',
                                 callback_data=f'want_{category}_{page}')
    edit = InlineKeyboardButton(text='✏️ Редактировать',
                                callback_data=f'edit_media_{category}_{page}')

    return InlineKeyboardMarkup(inline_keyboard=[keyboard, [edit if is_admin else want], [back_ibtn]])
