from datetime import datetime, timedelta
import aio_pika
import json
import asyncio
import uuid

from services.rabbit.conf import setup_rabbit, TTL
from services.rabbit.consume import process_message, send_response_to_user
from services.redis import get_redis_client
from config import logger, rabbit_cfg


async def send_message(chat_id: int, message: dict[str, str]):
    global TTL
    wait_until = datetime.now() + timedelta(milliseconds=TTL)
    redis = await get_redis_client()
    corelation_id = str(uuid.uuid4())
    await redis.set(corelation_id, chat_id, ex=int(TTL/1000+3))
    callback_queue = await _send_message(corelation_id, message)
    while datetime.now() < wait_until:
        try:
            message = await callback_queue.get()
        except aio_pika.exceptions.QueueEmpty:
            continue
        else:
            await process_message(message)
            return
    await send_response_to_user(chat_id)



async def _send_message(corelation_id: str, message: dict[str, str]):
    conn, ch, callback_queue = await setup_rabbit()
    payload = {
        "title": "hh",
        "data": message
    }
    body = aio_pika.Message(
        json.dumps(payload).encode(),
        correlation_id=corelation_id,
        reply_to=callback_queue.name,
    )
    
    await ch.default_exchange.publish(
        message=body,
        routing_key=rabbit_cfg.PRODUCE_ROUTING_KEY,
    )
    logger.info(f"Send message to MQ -> {payload}")
    
    return callback_queue
    


