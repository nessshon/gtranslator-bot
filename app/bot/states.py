from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    TRANSLATE = State()
    TRANSLATE_TO = State()
    TRANSLATE_FROM = State()
