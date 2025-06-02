import aio_pika

from config import rabbit_cfg, logger


TTL = 60000

async def get_conection():
    url = rabbit_cfg.get_url()
    connection =  await aio_pika.connect(url)
    logger.info("Successful connect to rabbit")
    return connection


async def setup_rabbit():
    global TTL
    connection = await get_conection()
    channel = await connection.channel()
    args = {"x-message-ttl" : TTL}
    await channel.declare_queue("parse", arguments=args)
    callback_queue = await channel.declare_queue(exclusive=True)
    return connection, channel, callback_queue