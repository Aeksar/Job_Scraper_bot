from aiogram.fsm.state import State, StatesGroup


class ParseStates(StatesGroup):
    text = State()
    city = State()
    salary = State()
    experience = State()