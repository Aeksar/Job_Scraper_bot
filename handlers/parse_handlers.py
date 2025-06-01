from aiogram import Dispatcher, Router, F, Bot
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext

from states import ParseStates
from services.rabbit import send_message


rout = Router()

def create_skip_keyboard(state: str):
    skip_button = InlineKeyboardButton(text="Пропустить", callback_data=f"skip:{state}")
    return InlineKeyboardMarkup(inline_keyboard=[[skip_button]])

state_actions = {
    "text": {
        "state": ParseStates.city,
        "question": "Город",
        "keyboard_arg": "city"
    },
    "city": {
        "state": ParseStates.salary,
        "question": "Зарплата",
        "keyboard_arg": "salary"
    },
    "salary": {
        "state": None, 
        "question": None,
        "keyboard_arg": None
    }
}
    
async def process_answer(msg: Message, state: FSMContext, current_state: str, data_key: str):
    await state.update_data({data_key: msg.text.replace(" ", "")})
    if current_state in state_actions:
        action = state_actions[current_state]
        if action["state"] is not None:
            kb = create_skip_keyboard(action["keyboard_arg"])
            await msg.answer(action["question"], reply_markup=kb)
            await state.set_state(action["state"])
        else:
            await msg.answer("Поиск вакансий\nЭто может занять 10-15 секунд")
            data = await state.get_data()
            chat_id = msg.chat.id
            await state.clear()
            await send_message(chat_id, data)

    
    
@rout.message(Command("parse"))
async def start_parse(msg: Message, state: FSMContext):
    kb = create_skip_keyboard("text")
    await msg.answer("должность", reply_markup=kb)
    await state.set_state(ParseStates.text)
    
    
@rout.message(ParseStates.text)
async def input_name(msg: Message, state: FSMContext):
    await process_answer(msg, state, "text", "text")
    
    
@rout.message(ParseStates.city)
async def input_city(msg: Message, state: FSMContext):
    await process_answer(msg, state, "city", "city")
    
    
@rout.message(ParseStates.salary)
async def input_salary(msg: Message, state: FSMContext):
    await process_answer(msg, state, "salary", "salary")
    

@rout.callback_query(F.data.startswith("skip:"))
async def skip_question(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    skip_to = callback.data.removeprefix("skip:")
    
    if skip_to in state_actions:
        await state.update_data({skip_to: None})
        action = state_actions[skip_to]
        if action["state"] is not None:
            await state.set_state(action["state"])
            kb = create_skip_keyboard(action["keyboard_arg"])
            await callback.message.answer(action["question"], reply_markup=kb)
        else:
            await callback.message.answer("Поиск вакансий\nЭто может занять 10-15 секунд")
            data = await state.get_data()
            chat_id = callback.message.chat.id
            await state.clear()
            await send_message(chat_id, data)
               