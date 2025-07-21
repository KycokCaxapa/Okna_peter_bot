from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

gallery = KeyboardButton(text='🖼️ Фотогалерея')
order = KeyboardButton(text='👋 Консультация')
nav = KeyboardButton(text='📍 Навигация')
faq = KeyboardButton(text='❓ Ответы на часто задаваемые вопросы')
phone = KeyboardButton(
    text="📞 Отправить мой номер телефона",
    request_contact=True
)
back = KeyboardButton(text='◀️ Назад')

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [gallery],
        [order, nav],
        [faq]
    ],
    resize_keyboard=True
)

phone_kb = ReplyKeyboardMarkup(
    keyboard=[[phone],
              [back]],
    resize_keyboard=True,
    one_time_keyboard=True
)
