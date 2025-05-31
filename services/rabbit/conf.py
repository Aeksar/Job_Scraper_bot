import aio_pika

from config import rabbit_cfg


async def setup_rabbit():
    connection = await aio_pika.connect(url=rabbit_cfg.get_url())
    channel = await connection.channel()
    await channel.declare_queue("parse")
    callback_queue = await channel.declare_queue(exclusive=True)
    return connection, channel, callback_queue