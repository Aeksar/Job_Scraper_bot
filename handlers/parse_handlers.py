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
from aio_pika.patterns import RPC
import uuid

from config import logger
from states import ParseStates
from services.rabbit import send_message
from services.redis import get_redis_client


rout = Router()

def create_skip_keyboard(state: str):
    skip_button = InlineKeyboardButton(text="Пропустить", callback_data=f"skip:{state}")
    return InlineKeyboardMarkup(inline_keyboard=[[skip_button]])

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
    await state.update_data({"city": msg.text})
    await msg.answer("Зарплата")
    await state.set_state(ParseStates.salary)
    
    
@rout.message(ParseStates.salary)
async def input_salary(msg: Message, state: FSMContext):
    data = await state.get_data()
    if salary := msg.text.isdigit() or msg.text is "скип":
        data["salary"] = salary if int(salary) < 10**9 else 10**9
    else:
        msg.answer("Введите сумму в рублях, состаящую из цифр")
    
    await msg.answer("Поиск вакансий\nЭто может занять 10-15 секунд")
    chat_id = msg.chat.id
    corelation_id = uuid.uuid4()
    redis = get_redis_client()
    await redis.set(str(corelation_id), chat_id)
    await send_message(corelation_id, data)
    
    await state.clear()
    

    