from aiogram import Dispatcher, Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext

from config import logger
from states import ParseStates
from rabbit import produce_message

rout = Router()

@rout.message(Command("start"))
async def start_command(msg: Message):
    await msg.answer("qq")
    
    
@rout.message(Command("parse"))
async def proccess_parse(msg: Message, state: FSMContext):
    await msg.answer("Введите название желаемой должности")
    await state.set_state(ParseStates.name)
    
@rout.message(ParseStates.name)
async def input_name(msg: Message, state: FSMContext):
    await state.set_data({"text": msg.text})
    await msg.answer("Город")
    await state.set_state(ParseStates.city)
    
@rout.message(ParseStates.city)
async def input_city(msg: Message, state: FSMContext):
    data = await state.get_data()
    data["city"] = msg.text
    await state.set_data(data)
    await msg.answer("ZP?")
    await state.set_state(ParseStates.salary)
    
@rout.message(ParseStates.salary)
async def input_salary(msg: Message, state: FSMContext):
    data = await state.get_data()
    data["salary"] = msg.text
    await state.set_data(data)
    await state.set_data(data)
    await msg.answer("DAUN?")
    await state.set_state(ParseStates.notification)
    
@rout.message(ParseStates.notification)
async def get_to_parser(msg: Message, state: FSMContext):
    data = await state.get_data()
    await msg.answer(f"{data}")
    await produce_message(data)
    await state.clear()
    