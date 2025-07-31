from aiogram.types import Message, CallbackQuery, PollAnswer
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Router, F

from src.database.requests import get_all_users, update_user
from src.handlers.admin.poll import clear_poll_options, load_poll_options, save_poll_options
from src.states import VoteState
from src.texts import load_text

import src.keyboards as keyboards


router = Router()
SPAM = load_text('spam.txt')


@router.callback_query(F.data == 'vote')
async def btn_vote(callback: CallbackQuery,
                   state: FSMContext) -> None:
    '''Handle click on the vote button'''
    await callback.answer()
    await state.set_state(VoteState.question)
    await callback.message.answer('Введите название голосования',
                                  reply_markup=keyboards.cancel_ikb)


@router.message(VoteState.question)
async def receive_vote_question(message: Message,
                                state: FSMContext) -> None:
    '''Save vote question and ask for options'''
    await state.update_data(message_id=message.message_id,
                            chat_id=message.chat.id,
                            question=message.text)
    await state.set_state(VoteState.options)
    await message.answer('Напишите через запятую варианты ответов')


@router.message(VoteState.options)
async def receive_vote_options(message: Message,
                               state: FSMContext) -> None:
    '''Save vote options and ask for confirm'''
    options = message.text.split(', ')
    await state.update_data(options=options)
    await state.set_state(VoteState.confirm)
    await message.answer('❓ Вы уверены, что хотите разослать это голосование всем пользователям?',
                         reply_markup=keyboards.confirm_ikb)


@router.message(VoteState.question)
async def receive_vote_confirm(message: Message,
                            state: FSMContext) -> None:
    '''Save vote and ask for confirm'''
    await state.update_data(message_id=message.message_id,
                            chat_id=message.chat.id)
    await state.set_state(VoteState.confirm)
    await message.answer('❓ Вы уверены, что хотите разослать это голосование всем пользователям?',
                         reply_markup=keyboards.confirm_ikb)
    

@router.callback_query(VoteState.confirm, F.data == 'confirm_spam_action')
async def confirm_spam_action(callback: CallbackQuery,
                              state: FSMContext,
                              bot: Bot) -> None:
    '''Confirm spam action'''
    await callback.answer()

    data = await state.get_data()
    question = data.get('question')
    options = data.get('options')
    users = await get_all_users()
    score = 0

    clear_poll_options()
    save_poll_options(options)

    for user in users:
        try:
            await update_user(tg_id=user.tg_id,
                              options=[])
            await bot.send_poll(
                chat_id=user.tg_id,
                question=question,
                options=options,
                is_anonymous=False,
                allows_multiple_answers=True
            )
            score += 1
        except Exception as e:
            print(f'[ERROR] Не удалось отправить сообщение пользователю {user.tg_id}: {e}')

    await callback.message.answer(f'👌 Рассылка завершена. Столько пользователей получили голосование: {score}')
    await state.clear()


@router.poll_answer()
async def poll_answer(poll: PollAnswer):
    tg_id = poll.user.id
    option_ids = poll.option_ids
    options = load_poll_options()
    selected = [options[i] for i in option_ids]

    await update_user(tg_id=tg_id,
                      options=selected)
