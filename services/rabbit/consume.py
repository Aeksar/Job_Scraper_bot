from aiogram.types import BufferedInputFile
from datetime import datetime, timedelta
from aio_pika.abc import AbstractQueue
import aio_pika
import json
import io

from services.redis import redis
from services.rabbit.conf import TTL
from services.mongo import TaskCollection, HhCollection, SubscribeCollection, mongo_client
from handlers.parse_handlers import Bot
from config import TOKEN, logger
from utils.message import to_exel


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
        try:
            correlation_id = message.correlation_id
            payload: dict = json.loads(message.body.decode())
            title = payload.get("title")
            if title == "parse":
                chat_id = await redis.get(correlation_id)
                data = await TaskCollection(mongo_client).get_result(payload["result_id"])
                await send_response_to_user(chat_id, data, "Результат парсинга")
                await redis.delete(correlation_id)
            elif title == "new":
                params: dict = payload.get("params")
                city, text = params.get("city"), params.get("text")
                chat_ids = await SubscribeCollection(mongo_client).get_subscribers(text, city)
                jobs = await HhCollection(mongo_client).find_by_ids(payload.get("data"))
                print(jobs)
                for chat_id in chat_ids:
                    await send_response_to_user(chat_id, jobs, "Новые вакансии")
        except Exception as e:
            logger.error(f"Error with process answer: {e}")

async def send_response_to_user(chat_id: int, data: dict, caption: str):
    if data:
        file_bytes = to_exel(data)
        file = BufferedInputFile(file_bytes, "Results.xlsx")
        await Bot(token=TOKEN).send_document(chat_id, file, caption=caption)
    else:
        await Bot(token=TOKEN).send_message(chat_id, caption)

