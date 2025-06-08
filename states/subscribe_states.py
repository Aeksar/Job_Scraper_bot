from aiogram.fsm.state import State, StatesGroup


class SubscribeStates(StatesGroup):
    ask = State()
    yes = State()
    no = State()
    