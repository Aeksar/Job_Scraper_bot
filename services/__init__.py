from .redis.conf import get_redis_client
from .rabbit.conf import get_conection
from redis.exceptions import ConnectionError
from aiormq.exceptions import AMQPConnectionError
from config import logger


async def checkout():
    try:
        _ = await get_redis_client()
        _ = await get_conection()
    except ConnectionError as e:
        logger.error(f"Cann't connect to redis {e}")
        raise
    except AMQPConnectionError as e:
        logger.error(f"Cann't connect to rabbit {e}")
        raise