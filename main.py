from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
import asyncio

from handlers import rout
from config import TOKEN
from services import checkout
from services.redis import get_redis_client

async def main():
    await checkout()
    redis = await get_redis_client()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.include_router(rout)
    await dp.start_polling(bot)
    
if __name__=="__main__":
    asyncio.run(main())