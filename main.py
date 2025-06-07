from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
import asyncio

from handlers import rout
from config import TOKEN
from services import checkout
from services.redis import redis

async def main():
    await checkout()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.include_router(rout)
    await dp.start_polling(bot)
    
if __name__=="__main__":
    asyncio.run(main())