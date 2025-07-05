from motor.motor_asyncio import  AsyncIOMotorClient
from pymongo import ReturnDocument
from bson.objectid import ObjectId

from config import logger, mongo_cfg
    
    
class SubscribeCollection:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db = self.client[mongo_cfg.DATABASE]
        self.collection = self.db["subscribe"]
    
    async def add(self, chat_id: int, text: str, city: str) -> bool:
        filter = {"text": text, "city": city}
        exist = await self.collection.find_one(filter)
        if chat_id in exist["subscriber_ids"]:
            return False
        update =  {"$push": {"subscriber_ids": chat_id}}
        await self.collection.update_one(filter, update, upsert=True)
        logger.debug(f"Add new user in {text}, {city}")
        return True
        
    async def remove(self, chat_id: int, text: str, city: str):
        filter = {"text": text, "city": city}
        update = {"$pull": {"subscriber_ids": chat_id}}
        doc = await self.collection.find_one_and_update(
            filter=filter, 
            update=update, 
            return_document=ReturnDocument.AFTER
        )
        logger.debug(f"Remove sub for user in {text}, {city}")
        if len(doc["subscriber_ids"]) == 0:
            await self.collection.delete_one(filter)
            logger.debug(f"Remove document, subscriber_ids is empty")
        
    async def find(self, chat_id: int) -> list:
        filter = {"subscriber_ids": chat_id}
        include = {"text": 1, "city": 1, "_id": 0}
        res = await self.collection.find(filter, include).to_list()
        logger.debug(f"Find {len(res)} subs")
        return res
    
    async def get_subscribers(self, text: str, city: str) -> list:
        filter = {"text": text, "city": city}
        doc = await self.collection.find_one(filter)
        if doc:
            return doc["subscriber_ids"]
        
    
class HhCollection:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db = self.client[mongo_cfg.DATABASE]
        self.collection = self.db["hh"]
        
    async def find_by_ids(self, ids: list[str]) -> list[dict]:
        valid_ids = []
        for id in ids:
            valid_ids.append(ObjectId(id))
        res = await self.collection.find({"_id": {"$in": valid_ids}}, {"_id": 0}).to_list()
        return res
    
class TaskCollection:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db = self.client[mongo_cfg.DATABASE]
        self.collection = self.db["search_result"]
        self.jobs_col = HhCollection(self.client)
        
    async def get_result(self, task_id: str) -> dict:
        document = await  self.collection.find_one({"_id": ObjectId(task_id)})
        job_ids = document["jobs"]
        return await self.jobs_col.find_by_ids(job_ids)
    
    async def add(self, params: dict) -> ObjectId:
        res = await self.collection.insert_one({
            "status": "pending",
            "parameters": params
        })
        return res.inserted_id
        
        