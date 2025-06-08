from aiogram import Dispatcher, Router, F, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
)

from services.mongo import SubscribeCollection, mongo_client
from states import SubscribeStates


subscribe_router = Router()

UNSUB_MESSAGE = "Вы всегда можете подписаться с помощью команды /sub"

@subscribe_router.message(SubscribeStates.ask)
async def subscribe_ask(msg: Message, state: FSMContext):
    no_btn = InlineKeyboardButton(text="нет", callback_data="nosubscribe")
    yes_btn = InlineKeyboardButton(text="да", callback_data=f"subscribe")
    kb = InlineKeyboardMarkup(inline_keyboard=[[yes_btn], [no_btn]])
    await msg.answer("Присылать новые вакансии?", reply_markup=kb)
    
    
@subscribe_router.callback_query(F.data == "subscribe")
async def callback_subscribe(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SubscribeStates.yes)
    msg = callback.message
    data = await state.get_data()
    mongo = SubscribeCollection(client=mongo_client)
    print(data)
    await mongo.add(
        chat_id=msg.chat.id,
        text=data.get("text"),
        city=data.get("city"),
    )
    await msg.answer("Вы успешно подписались")


@subscribe_router.callback_query(F.data == "nosubscribe")
async def no_subscribe(callback: CallbackQuery):
    global UNSUB_MESSAGE
    await callback.answer()
    await callback.message.answer(UNSUB_MESSAGE)


@subscribe_router.message(Command("sub"))
async def subscribe(msg: Message,  command: CommandObject):
    global mongo_client
    args = command.args.split()
    mongo = SubscribeCollection(client=mongo_client)
    await mongo.add(
        chat_id=msg.chat.id,
        text=args[0],
        city=args[1],
    )
    await msg.answer("Вы успешно подписались") 
       
    
@subscribe_router.message(Command("unsub"))
async def unsubscribe(msg: Message):
    global UNSUB_MESSAGE, mongo_client
    await msg.answer("Рассылка удалена")
    await msg.answer(UNSUB_MESSAGE)
    await SubscribeCollection(mongo_client).remove(msg.chat.id)
