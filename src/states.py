from aiogram.fsm.state import State, StatesGroup


class GalleryState(StatesGroup):
    '''Photo state for gallery'''
    category = State()
    photo_id = State()
    description = State()

class StockState(StatesGroup):
    '''Stock state for spam'''
    content = State()
