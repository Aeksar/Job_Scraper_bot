from aiogram.types import BufferedInputFile
import pandas as pd
import aio_pika
import json
import io

from services.redis import get_redis_client
from handlers.parse_handlers import Bot
from config import TOKEN


async def consume_message(message: aio_pika.IncomingMessage):
    async with message.process():
        correlation_id = message.correlation_id
        redis = get_redis_client()
        if chat_id := await redis.get(correlation_id):
            result: list[dict[str, str]] = json.loads(message.body.decode())
            if result:
                file_bytes = to_exel_buf(result)
                file = BufferedInputFile(file_bytes, "Results.xlsx")
                await Bot(token=TOKEN).send_document(chat_id, file, caption="Результат")
            else:
                await Bot(token=TOKEN).send_message(chat_id, "По вашему запросу ничего не найдено")
            await redis.delete(correlation_id)
            

def to_exel_buf(data: dict):
    df = pd.DataFrame(data)
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    excel_file.seek(0)
    return excel_file.read()