from motor.motor_asyncio import AsyncIOMotorClient

from config import mongo_cfg, logger


def connect_to_mongo():
    try:
        client = AsyncIOMotorClient(mongo_cfg.url())
        logger.info("Successful connect to mongo")
        return client
    except Exception as e:
        logger.info(f"Error connecting to mongo: {e}")
        return None


mongo_client = connect_to_mongo()
