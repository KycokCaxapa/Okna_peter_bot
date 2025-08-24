from aiogram.fsm.state import State, StatesGroup


class GalleryState(StatesGroup):
    '''Media state for gallery'''
    category = State()
    media_id = State()
    title = State()
    description = State()


class EditState(StatesGroup):
    '''Edit media state for gallery'''
    title = State()
    description = State()
    media = State()
    delete = State()


class StockState(StatesGroup):
    '''Stock state for spam'''
    content = State()
    confirm = State()


class VoteState(StatesGroup):
    '''Vote state for spam'''
    question = State()
    options = State()
    confirm = State()
