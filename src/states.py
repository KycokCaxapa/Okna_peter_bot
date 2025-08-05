from aiogram.fsm.state import State, StatesGroup


class GalleryState(StatesGroup):
    '''Photo state for gallery'''
    category = State()
    photo_id = State()
    title = State()
    description = State()


class StockState(StatesGroup):
    '''Stock state for spam'''
    content = State()
    confirm = State()


class VoteState(StatesGroup):
    '''Vote state for spam'''
    question = State()
    options = State()
    confirm = State()
