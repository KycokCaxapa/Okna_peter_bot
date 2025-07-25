from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

from src.database.requests import add_photo
from src.states import GalleryState
import src.keyboards as keyboards


router = Router()


@router.message(F.text == '🖼️ Добавить фото в галерею')
async def btn_add_photo(message: Message,
                        state: FSMContext) -> None:
    '''Handle add photo button'''
    await state.set_state(GalleryState.category)
    await message.answer('Выберите категорию для добавления фото:',
                         reply_markup=keyboards.category_kb(is_admin=True))


@router.callback_query(F.data.startswith('admin_gallery'))
async def choose_category(callback: CallbackQuery,
                          state: FSMContext) -> None:
    '''Save chosen category and ask for photo'''
    category = callback.data.split('_')[2]
    await callback.answer()
    await state.update_data(category=category)
    await state.set_state(GalleryState.photo_id)
    await callback.message.answer('Теперь отправьте мне фото')


@router.message(GalleryState.photo_id, F.photo)
async def receive_photo(message: Message,
                        state: FSMContext) -> None:
    '''Save photo ID and ask for description'''
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await state.set_state(GalleryState.description)
    await message.answer('Теперь напиши описание для фото')


@router.message(GalleryState.description, F.text)
async def receive_description(message: Message,
                              state: FSMContext) -> None:
    '''Save description and insert to DB'''
    description = message.text
    await state.update_data(description=description)
    await state.set_state(GalleryState.description)

    data = await state.get_data()
    category = data.get('category')
    photo_id = data.get('photo_id')
    description = data.get('description')

    await add_photo(photo_id, category, description)

    await message.answer('Фото успешно добавлено в галерею ✅')
    await state.clear()
