import aio_pika
from aio_pika.channel import AbstractChannel
from aio_pika.exchange import Exchange

import json

from rabbit.conf import get_rmq_conn
from config import logger, rabbit_cfg


async def send_message(channel: AbstractChannel, message: dict[str, str]):
    exchange: Exchange = await channel.declare_exchange(
        name=rabbit_cfg.MQ_EXCHANGE, 
        type=aio_pika.ExchangeType.FANOUT
    )
    payload = {
        "title": "hh",
        "data": message
    }
    body = aio_pika.Message(json.dumps(payload).encode())
    await exchange.publish(message=body, routing_key="")
    logger.info(f"Send message to MQ -> {payload}")
    
async def produce_message(message: dict[str, str]):
    conn = await get_rmq_conn()
    async with conn.channel() as ch:
        await send_message(ch, message)

