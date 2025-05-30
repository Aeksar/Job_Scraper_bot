import aio_pika

from config import rabbit_cfg


async def get_rmq_conn() -> aio_pika.connection.AbstractConnection:
    return await aio_pika.connect(url=rabbit_cfg.get_url())