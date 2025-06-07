from aiogram.types import BufferedInputFile
from datetime import datetime, timedelta
from aio_pika.abc import AbstractQueue
from typing import Optional
import pandas as pd
import aio_pika
import json
import io

from services.redis import redis
from services.rabbit.conf import TTL
from handlers.parse_handlers import Bot
from config import TOKEN, logger


async def wait_consume(callback_queue: AbstractQueue, chat_id: int):
    global TTL
    wait_until = datetime.now() + timedelta(milliseconds=TTL)
    while datetime.now() < wait_until:
        try:
            message = await callback_queue.get()
        except aio_pika.exceptions.QueueEmpty:
            continue
        else:
            await consume_message(message)
            return
    await send_response_to_user(chat_id)


async def consume_message(message: aio_pika.IncomingMessage):
    async with message.process():
        correlation_id = message.correlation_id
        logger.info(f"Take response for {correlation_id}")
        if chat_id := await redis.get(correlation_id):
            result: list[dict[str, str]] = json.loads(message.body.decode())   
            await send_response_to_user(chat_id, result)
            await redis.delete(correlation_id)
    

async def send_response_to_user(chat_id: int, result: Optional[list[dict]]):
    if result:
        file_bytes = to_exel_buf(result)
        file = BufferedInputFile(file_bytes, "Results.xlsx")
        await Bot(token=TOKEN).send_document(chat_id, file, caption="Результат")
    else:
        await Bot(token=TOKEN).send_message(chat_id, "По вашему запросу ничего не найдено")
          
                
def to_exel_buf(data: dict):
    df = pd.DataFrame(data)
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    excel_file.seek(0)
    return excel_file.read()