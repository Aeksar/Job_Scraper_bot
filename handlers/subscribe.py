from aiogram import Dispatcher, Router, F, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
)
from typing import Optional

from services.mongo import SubscribeCollection, mongo_client
from states import SubscribeStates


subscribe_router = Router()

SUB_OFFER_MESSAGE = "Вы всегда можете подписаться с помощью команды /sub"
UNSUB_MESSAGE = "Вы успешно отписались от рассылки для {text} в городе {city}"
SUB_MESSAGE = "Вы успешно подписались на рассылку для {text} в городе {city}"
WRONG_MESSAGE = "Укажите должность и город\nПример:  /{command}  <должность>  <город>"

def validate_args(args: Optional[str]):
    if args:
        args_list = args.split()
        if len(args_list) == 2:
            return args_list


@subscribe_router.message(SubscribeStates.ask)
async def subscribe_ask(msg: Message):
    no_btn = InlineKeyboardButton(text="нет", callback_data="nosubscribe")
    yes_btn = InlineKeyboardButton(text="да", callback_data=f"subscribe")
    kb = InlineKeyboardMarkup(inline_keyboard=[[yes_btn], [no_btn]])
    await msg.answer("Присылать новые вакансии?", reply_markup=kb)
    
    
@subscribe_router.callback_query(F.data == "subscribe")
async def callback_subscribe(callback: CallbackQuery, state: FSMContext):
    global SUB_MESSAGE, WRONG_MESSAGE, mongo_client
    await callback.answer()
    msg = callback.message
    data = await state.get_data()
    mongo = SubscribeCollection(client=mongo_client)
    text = data.get("text")
    city = data.get("city")
    if not (text and city):
        msg.answer(WRONG_MESSAGE.format(command="sub"))
    await mongo.add(
        chat_id=msg.chat.id,
        text=text,
        city=city,
    )
    await state.clear()
    await msg.answer(SUB_MESSAGE.format(text=text, city=city))


@subscribe_router.callback_query(F.data == "nosubscribe")
async def no_subscribe(callback: CallbackQuery):
    global SUB_OFFER_MESSAGE
    await callback.answer()
    await callback.message.answer(SUB_OFFER_MESSAGE)


@subscribe_router.message(Command("sub"))
async def subscribe(msg: Message,  command: CommandObject):
    global SUB_MESSAGE, WRONG_MESSAGE, mongo_client
    args = validate_args(command.args)
    if not args:
        await msg.answer(WRONG_MESSAGE.format(command="sub"))
        return
    mongo = SubscribeCollection(client=mongo_client)
    added = await mongo.add(
        chat_id=msg.chat.id,
        text=args[0],
        city=args[1],
    )
    if not added:
        await msg.answer("Вы уже подписаны на эту рассылку")
        return
    await msg.answer(SUB_MESSAGE.format(text=args[0], city=args[1])) 
       
    
@subscribe_router.message(Command("unsub"))
async def unsubscribe(msg: Message, command: CommandObject):
    global UNSUB_MESSAGE, SUB_OFFER_MESSAGE, WRONG_MESSAGE, mongo_client
    args = validate_args(command.args)
    if not args:
        await msg.answer(WRONG_MESSAGE.format(command="unsub"))
        return
    mongo = SubscribeCollection(client=mongo_client)
    await mongo.remove(
        chat_id=msg.chat.id,
        text=args[0],
        city=args[1],
    )
    await msg.answer(UNSUB_MESSAGE.format(text=args[0], city=args[1]))


@subscribe_router.message(Command("my_sub"))
async def get_subscribes(msg: Message):
    global mongo_client
    mongo = SubscribeCollection(mongo_client)
    subs = await mongo.find(msg.chat.id)
    ans = "Ваши подписки:\nДолжность   Город\n"
    for sub in subs:
        ans += f"{sub["text"]}  {sub["city"]}\n"
    await msg.answer(ans)
    
    
