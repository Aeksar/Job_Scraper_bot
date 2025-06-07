from aiogram import Dispatcher, Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext
from typing import Optional

from states import ParseStates
from services.rabbit import process_message
from config import logger

rout = Router()

def create_skip_keyboard(state: str):
    skip_button = InlineKeyboardButton(text="Пропустить", callback_data=f"skip:ParseStates:{state}")
    return InlineKeyboardMarkup(inline_keyboard=[[skip_button]])

state_actions = {
    None: {
        "state": ParseStates.text,
        "question": "Должность",
        "keyboard_arg": "text",
        "data_key": None,
    },
    "ParseStates:text": {
        "state": ParseStates.city,
        "question": "Город",
        "keyboard_arg": "city",
        "data_key": "text",
    },
    "ParseStates:city": {
        "state": ParseStates.experience,
        "question": "Опыт",
        "keyboard_arg": "experience",
        "data_key": "city"
    },
    "ParseStates:experience": {
        "state": ParseStates.salary,
        "question": "Зарплата",
        "keyboard_arg": "salary",
        "data_key": "experience"
    },
    "ParseStates:salary": {
        "state": None, 
        "question": "Поиск вакансий\nЭто может занять 10-15 секунд\n60 край брат",
        "keyboard_arg": None,
        "data_key": "salary"
    }
}

@rout.message(Command("parse"))
async def start_ask(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        current_state = None
    action = state_actions[current_state]
    await process_action(msg, state, action)


@rout.message(StateFilter(ParseStates))
async def answer_question(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    action = state_actions[current_state]
    data_key = action["data_key"]
    await state.update_data({data_key: msg.text})
    await process_action(msg, state, action)


@rout.callback_query(F.data.startswith("skip:"))
async def skip_question(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    skip_to = callback.data.removeprefix("skip:")
    action = state_actions[skip_to]
    await state.update_data({action["data_key"]: None})
    await process_action(callback.message, state, action)
            

async def process_action(msg: Message, state: FSMContext, action: dict[Optional[str], Optional[str]]):
    if action["state"] is not None:
        kb = create_skip_keyboard(action["keyboard_arg"])
        await msg.answer(action["question"], reply_markup=kb)
        await state.set_state(action["state"])
    else:
        await msg.answer(action["question"])
        data = await state.get_data()
        chat_id = msg.chat.id
        await state.clear()
        await process_message(chat_id, data)