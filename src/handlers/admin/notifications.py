from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Router, F

from src.database.requests import get_all_users
from src.states import StockState
from src.texts import load_text

import src.keyboards as keyboards


router = Router()
SPAM = load_text('spam.txt')


@router.message(F.text == '📢 Запустить рассылку')
async def btn_start_spam(message: Message) -> None:
    '''Handle start spam button'''
    await message.answer(SPAM,
                         parse_mode='HTML',
                         reply_markup=keyboards.spam_ikb)


@router.callback_query(F.data == 'stocks')
async def btn_stocks(callback: CallbackQuery,
                     state: FSMContext) -> None:
    '''Handle click on the stocks button'''
    await callback.answer()
    await state.set_state(StockState.content)
    await callback.message.answer('Теперь отправьте сообщение для рассылки',
                                  reply_markup=keyboards.cancel_ikb)


@router.message(StockState.content)
async def receive_stock_text(message: Message,
                             state: FSMContext) -> None:
    '''Save stock description and ask for confirm'''
    await state.update_data(message_id=message.message_id,
                            chat_id=message.chat.id)
    await message.answer('❓ Вы уверены, что хотите разослать это сообщение всем пользователям?',
                         reply_markup=keyboards.confirm_ikb)
    

@router.callback_query(F.data == 'confirm_spam_action')
async def confirm_spam_action(callback: CallbackQuery,
                              state: FSMContext,
                              bot: Bot) -> None:
    '''Confirm spam action'''
    await callback.answer()

    data = await state.get_data()
    chat_id = data.get('chat_id')
    message_id = data.get('message_id')
    users = await get_all_users()
    score = 0

    for user in users:
        try:
            await bot.copy_message(
                chat_id=user.tg_id,
                from_chat_id=chat_id,
                message_id=message_id
            )
            score += 1
        except Exception as e:
            print(f'[ERROR] Не удалось отправить сообщение пользователю {user.tg_id}: {e}')

    await callback.message.answer(f'👌 Рассылка завершена. Столько пользователей получили сообщение: {score}')
    await state.clear()

