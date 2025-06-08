import aio_pika
from aio_pika.abc import AbstractConnection
from config import rabbit_cfg, logger


TTL = 60000

async def get_conection():
    url = rabbit_cfg.get_url()
    connection =  await aio_pika.connect_robust(url)
    logger.info("Successful connect to rabbit")
    return connection


async def setup_rabbit(connection: AbstractConnection):
    global TTL
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    args = {"x-message-ttl" : TTL}
    await channel.declare_queue(rabbit_cfg.PRODUCE_ROUTING_KEY, arguments=args)
    callback_queue = await channel.declare_queue(rabbit_cfg.MQ_CONSUME_QUEUE)
    return channel, callback_queue