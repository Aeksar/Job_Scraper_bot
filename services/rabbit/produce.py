import aio_pika
from aio_pika.channel import AbstractChannel
from aio_pika.exchange import Exchange
import json
import uuid

from services.rabbit.conf import setup_rabbit
from config import logger, rabbit_cfg
from services.rabbit.consume import consume_message

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
    await ch.default_exchange.publish(
        message=body,
        routing_key=rabbit_cfg.PRODUCE_ROUTING_KEY,
    )
    await callback_queue.consume(consume_message)
    logger.info(f"Send message to MQ -> {payload}")
    


