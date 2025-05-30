from aiogram.fsm.state import State, StatesGroup


class ParseStates(StatesGroup):
    name = State()
    city = State()
    salary = State()
    notification = State()