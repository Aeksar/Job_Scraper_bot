from aiogram import Bot, Dispatcher
import asyncio

from handlers import rout
from config import TOKEN


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(rout)
    await dp.start_polling(bot)
    
if __name__=="__main__":
    asyncio.run(main())