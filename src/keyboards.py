from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_order = KeyboardButton(text="Оставить заявку на замер")
button_ask = KeyboardButton(text="Задать вопрос менеджеру")
button_faq = KeyboardButton(text="Ответы на часто задаваемые вопросы")

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [button_order, button_ask],
        [button_faq]
    ],
    resize_keyboard=True
)
