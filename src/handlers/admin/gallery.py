from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from src.database.requests import add_media
from src.states import GalleryState

import src.keyboards as keyboards


router = Router()


@router.message(F.text == '🖼️ Пополнить галерею')
async def btn_add_photo(message: Message,
                        state: FSMContext) -> None:
    '''Handle add photo button'''
    await state.set_state(GalleryState.category)
    await message.answer('Выберите категорию добавляемого продукта:',
                         reply_markup=keyboards.category_ikb(is_admin=True))


@router.callback_query(F.data.startswith('admin_gallery'))
async def choose_category(callback: CallbackQuery,
                          state: FSMContext) -> None:
    '''Save chosen category and ask for file'''
    category = callback.data.split('_')[2]
    await callback.answer()
    await state.update_data(category=category)
    await state.set_state(GalleryState.media_id)
    await callback.message.answer('Теперь отправьте мне фото',
                                  reply_markup=keyboards.cancel_ikb)


@router.message(GalleryState.media_id, F.photo | F.video)
async def receive_photo(message: Message,
                        state: FSMContext) -> None:
    '''Save media ID and ask for title'''
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        media_type = 'photo'
    if message.content_type == 'video':
        file_id = message.video.file_id
        media_type = 'video'
    await state.update_data(media_id=file_id)
    await state.update_data(media_type=media_type)
    await state.set_state(GalleryState.title)
    await message.answer('Теперь напиши название фото',
                         reply_markup=keyboards.cancel_ikb)


@router.message(GalleryState.title, F.text)
async def receive_title(message: Message,
                        state: FSMContext) -> None:
    '''Save photo title and ask for description'''
    title = message.text
    await state.update_data(title=title)
    await state.set_state(GalleryState.description)
    await message.answer('Теперь напиши описание для фото',
                         reply_markup=keyboards.cancel_ikb)


@router.message(GalleryState.description, F.text)
async def receive_description(message: Message,
                              state: FSMContext) -> None:
    '''Save description and insert to DB'''
    description = message.text
    await state.update_data(description=description)
    await state.set_state(GalleryState.description)

    data = await state.get_data()
    title = data.get('title')
    category = data.get('category')
    media_id = data.get('media_id')
    media_type = data.get('media_type')
    description = data.get('description')

    await add_media(title, media_id, media_type, category, description)

    await message.answer(f'{'Фото' if media_type == 'photo' else 'Видео'} успешно добавлено в галерею ✅',
                         reply_markup=keyboards.admin_kb)
    await state.clear()