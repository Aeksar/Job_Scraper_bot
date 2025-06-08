from motor.motor_asyncio import  AsyncIOMotorClient
from config import logger
    
    
class SubscribeCollection:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db = self.client["job_name"]
        self.collection = self.db["subscribe"]
    
    async def add(self, chat_id: int, text: str, city: str):
        filter = {"text": text, "city": city}
        update =  {"$push": {"subscriber_ids": chat_id}}
        res = await self.collection.update_one(filter, update, upsert=True)
        logger.debug(f"Add new user to {res["text"]}, {res["city"]}")
        
    async def remove(self, chat_id: int):
        filter = {"subscriber_ids": chat_id}
        update = {"$pull": chat_id}
        await self.collection.update_one(filter, update)