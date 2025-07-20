from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_gallery = KeyboardButton(text='🖼️ Фотогалерея')
button_order = KeyboardButton(text='👋 Консультация')
button_nav = KeyboardButton(text='📍 Навигация')
button_faq = KeyboardButton(text='❓ Ответы на часто задаваемые вопросы')
button_phone = KeyboardButton(
    text="Отправить мой номер телефона",
    request_contact=True
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [button_gallery],
        [button_order, button_nav],
        [button_faq]
    ],
    resize_keyboard=True
)

phone_kb = ReplyKeyboardMarkup(
    keyboard=[[button_phone]],
    resize_keyboard=True,
    one_time_keyboard=True
)
