from redis.asyncio.client import Redis
from datetime import timedelta

from config import redis_cfg, logger


def get_redis_client() -> Redis:
    
    try:
        redis_conn = Redis(
            username=redis_cfg.USERNAME,
            password=redis_cfg.PASSWORD,            
            host=redis_cfg.HOST,
            port=redis_cfg.PORT,
            db=redis_cfg.DB,
            decode_responses=True
        ) 
        logger.debug(f'Successful connect to redis')
        return redis_conn
    
    except Exception as e:
        logger.error(f'Error with connect to redis: {e}')
        raise
    
redis = get_redis_client()