from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from src.database.requests import add_media, delete_media, get_medias_by_category, update_media
from src.states import EditState, GalleryState

import src.keyboards as keyboards


router = Router()


@router.message(F.text == '🖼️ Пополнить галерею')
async def btn_add_media(message: Message,
                        state: FSMContext) -> None:
    '''Handle add media button'''
    await state.set_state(GalleryState.category)
    await message.answer('Выберите категорию добавляемого продукта:',
                         reply_markup=keyboards.category_ikb(flag=True,
                                                             is_admin=True))


@router.callback_query(F.data.startswith('admin_create_gallery'))
async def choose_category(callback: CallbackQuery,
                          state: FSMContext) -> None:
    '''Save chosen category and ask for file'''
    category = callback.data.split('_')[-1]
    await callback.answer()
    await state.update_data(category=category)
    await state.set_state(GalleryState.media_id)
    await callback.message.answer('Теперь отправьте мне фото',
                                  reply_markup=keyboards.cancel_ikb)


@router.message(GalleryState.media_id, F.photo | F.video)
async def receive_media(message: Message,
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
    '''Save media title and ask for description'''
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
    print('-'*30, category)
    media_id = data.get('media_id')
    media_type = data.get('media_type')
    description = data.get('description')

    await add_media(title, media_id, media_type, category, description)

    await message.answer(f'{'Фото' if media_type == 'photo' else 'Видео'} успешно добавлено в галерею ✅',
                         reply_markup=keyboards.admin_kb)
    await state.clear()


@router.message(F.text == '✏️ Редактировать галерею')
async def btn_edit_gallery(message: Message,
                           state: FSMContext) -> None:
    '''Handle edit gallery button'''
    await state.set_state(GalleryState.category)
    await message.answer('Выберите категорию редактируемого продукта:',
                         reply_markup=keyboards.category_ikb(flag=False,
                                                             is_admin=True))


@router.callback_query(F.data.startswith('admin_edit_gallery'))
async def btn_gallery_category(callback: CallbackQuery) -> None:
    '''Handle click on the category from gallery menu'''
    await callback.answer()

    category = callback.data.split('_')[-1]
    medias = await get_medias_by_category(category)
    count = len(medias)
    page = 0

    if medias:
        caption = f'{medias[page].title}\n\n{medias[page].description}'
        if medias[page].media_type.value == 'photo':
            await callback.message.answer_photo(
                photo=medias[page].media_id,
                caption=caption,
                reply_markup=keyboards.pagination_ikb(category, page, count, is_admin=True)
            )
        if medias[page].media_type.value == 'video':
            await callback.message.answer_video(
                video=medias[page].media_id,
                caption=caption,
                reply_markup=keyboards.pagination_ikb(category, page, count, is_admin=True)
            )
    else:
        await callback.message.answer('Галерея пуста((')


@router.callback_query(F.data.startswith(('admin_prev', 'admin_next')))
async def pagination_callback(callback: CallbackQuery):
    '''Handle pagination buttons'''
    await callback.answer()

    _, action, category, page = callback.data.split('_')
    page = int(page) + 1 if action == 'next' else int(page) - 1
    medias = await get_medias_by_category(category)
    caption = f'{medias[page].title}\n\n{medias[page].description}'
    count = len(medias)

    if medias[page].media_type.value == 'photo':
        await callback.message.edit_media(
            InputMediaPhoto(media=medias[page].media_id,
                            caption=caption),
            reply_markup=keyboards.pagination_ikb(category, page, count, is_admin=True)
        )
    if medias[page].media_type.value == 'video':
        await callback.message.edit_media(
            InputMediaVideo(media=medias[page].media_id,
                            caption=caption),
            reply_markup=keyboards.pagination_ikb(category, page, count, is_admin=True)
        )


@router.message(F.text == '✏️ Редактировать')
async def btn_edit_media(message: Message) -> None:
    '''Handle edit media button'''
    await message.answer('Выберите категорию редактируемого продукта:',
                         reply_markup=keyboards.category_ikb(flag=False,
                                                             is_admin=True))


@router.callback_query(F.data.startswith('edit_media'))
async def ibtn_edit_media(callback: CallbackQuery,
                          state: FSMContext):
    '''Handle edit media ibutton'''
    _, _, category, page = callback.data.split('_')
    medias = await get_medias_by_category(category)
    caption = f'{medias[int(page)].title}\n\n{medias[int(page)].description}'

    await state.set_state()
    await state.update_data(media_id=medias[int(page)].media_id)

    if medias[int(page)].media_type.value == 'photo':
        media = InputMediaPhoto(media=medias[int(page)].media_id,
                                caption=caption)
    elif medias[int(page)].media_type.value == 'video':
        media = InputMediaVideo(media=medias[int(page)].media_id,
                                caption=caption)

    await callback.message.edit_media(media=media,
                                      reply_markup=keyboards.edit_ikb)


@router.callback_query(F.data == 'edit_title')
async def ibtn_edit_title(callback: CallbackQuery,
                          state: FSMContext):
    '''Handle edit title ibutton'''
    await callback.answer()
    await state.set_state(EditState.title)
    await callback.message.answer('Введите новый заголовок')


@router.message(EditState.title, F.text)
async def receive_new_title(message: Message,
                            state: FSMContext):
    '''Handle new title'''
    data = await state.get_data()
    media_id = data.get('media_id')

    await update_media(media_id, title=message.text)
    await message.answer('Заголовок обновлён')
    
    await state.clear()


@router.callback_query(F.data == 'edit_description')
async def ibtn_edit_description(callback: CallbackQuery,
                          state: FSMContext):
    '''Handle edit description ibutton'''
    await callback.answer()
    await state.set_state(EditState.description)
    await callback.message.answer('Введите новое описание')


@router.message(EditState.description, F.text)
async def receive_new_description(message: Message,
                            state: FSMContext):
    '''Handle new description'''
    data = await state.get_data()
    media_id = data.get('media_id')

    await update_media(media_id, description=message.text)
    await message.answer('Описание обновлено')
    
    await state.clear()


@router.callback_query(F.data == 'edit_media')
async def ibtn_edit_photo(callback: CallbackQuery,
                          state: FSMContext):
    '''Handle edit photo ibutton'''
    await callback.answer()
    await state.set_state(EditState.media)
    await callback.message.answer('Отправьте новый файл')


@router.message(EditState.media, F.photo | F.video)
async def receive_new_photo(message: Message,
                            state: FSMContext):
    '''Handle new photo'''
    data = await state.get_data()
    media_id = data.get('media_id')

    if message.photo:
        new_media_id = message.photo[-1].file_id
        new_media_type = 'photo'
    elif message.video:
        new_media_id = message.video.file_id
        new_media_type = 'video'

    await update_media(media_id,
                       media_id=new_media_id,
                       media_type=new_media_type)
    await message.answer('Файл обновлён')
    
    await state.clear()


@router.callback_query(F.data == 'delete_media')
async def ibtn_delete_media(callback: CallbackQuery,
                          state: FSMContext):
    '''Handle delete media ibutton'''
    await callback.answer()
    await state.set_state(EditState.delete)
    await callback.message.answer('Подтвердите действие',
                                  reply_markup=keyboards.confirm_delete_ikb)


@router.callback_query(EditState.delete, F.data == 'confirm_delete_action')
async def confirm_delete_action(callback: CallbackQuery,
                                state: FSMContext):
    '''Delete media'''
    data = await state.get_data()
    media_id = data.get('media_id')

    await callback.answer()
    await delete_media(media_id)
    await state.clear()
    await callback.message.answer('Медиа удалено',
                                  reply_markup=keyboards.admin_kb)
