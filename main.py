from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
import asyncio

from handlers import rout, subscribe_router
from config import TOKEN
from services import checkout
from services.redis import redis
from services.rabbit.conf import setup_rabbit, get_conection
from services.rabbit.consume import consume_message

async def main():
    await checkout()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.include_router(rout)
    dp.include_router(subscribe_router)
    conn = await get_conection()
    _, callback_queue = await setup_rabbit(conn)
    await callback_queue.consume(consume_message)
    await dp.start_polling(bot)
    
if __name__=="__main__":
    asyncio.run(main())