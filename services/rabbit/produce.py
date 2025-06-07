from datetime import datetime, timedelta
from aio_pika.abc import AbstractConnection, AbstractChannel
import aio_pika
import json
import asyncio
import uuid

from services.rabbit.conf import setup_rabbit, TTL, get_conection
from services.rabbit.consume import wait_consume
from services.redis import redis
from config import logger, rabbit_cfg


async def process_message(chat_id: int, message: dict[str, str]):
    global TTL
    conn = await get_conection()
    corelation_id = str(uuid.uuid4())
    await redis.set(corelation_id, chat_id, ex=int(TTL/1000+3))
    callback_queue = await produce_message(corelation_id, message, conn)
    await wait_consume(callback_queue, chat_id)
    await conn.close()
    
    
async def produce_message(corelation_id: str, data: dict[str, str], connection: AbstractConnection):
    ch, callback_queue  = await setup_rabbit(connection)
    payload = {
        "title": "hh",
        "data": data
    }
    message = aio_pika.Message(
        body=json.dumps(payload).encode(),
        correlation_id=corelation_id,
        reply_to=callback_queue.name,
    )
    await ch.default_exchange.publish(
        message=message,
        routing_key=rabbit_cfg.PRODUCE_ROUTING_KEY,
    )
    logger.info(f"Send message to MQ -> {payload}")
    
    return callback_queue
    


