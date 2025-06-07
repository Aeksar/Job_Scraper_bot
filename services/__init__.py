from .redis.conf import redis
from .rabbit.conf import get_conection
from redis.exceptions import ConnectionError
from aiormq.exceptions import AMQPConnectionError
from config import logger


async def checkout():
    try:
        await redis.ping()
        _ = await get_conection()
    except ConnectionError as e:
        logger.error(f"Cann't connect to redis {e}")
        raise
    except AMQPConnectionError as e:
        logger.error(f"Cann't connect to rabbit {e}")
        raise