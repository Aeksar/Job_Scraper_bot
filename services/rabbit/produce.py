import aio_pika
import json
import asyncio

from services.rabbit.conf import setup_rabbit
from services.rabbit.consume import consume_message, send_answer_to_user
from services.redis import get_redis_client
from config import logger, rabbit_cfg


async def send_message(corelation_id: str, message: dict[str, str]):
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
    TIMEOUT = 30 * 1000
    await ch.default_exchange.publish(
        message=body,
        routing_key=rabbit_cfg.PRODUCE_ROUTING_KEY,
        timeout=TIMEOUT
    )

    try:
        await callback_queue.consume(consume_message, timeout=TIMEOUT)
    except asyncio.TimeoutError:
        redis = await get_redis_client()
        chat_id = await redis.get(corelation_id)
        await send_answer_to_user(chat_id)
        
    logger.info(f"Send message to MQ -> {payload}")
    


