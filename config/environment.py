from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.getenv("TOKEN")

class rabbit_cfg:
    HOST = os.getenv("RMQ_HOST")
    PORT = os.getenv("RMG_PORT")
    PASSWORD = os.getenv("RMQ_PWD")
    USER = os.getenv("RMQ_USER")
    PRODUCE_ROUTING_KEY = os.getenv("MQ_PRODUCE_RK")
    MQ_CONSUME_QUEUE = os.getenv("MQ_CONSUME_QUEUE")
    
    @classmethod
    def get_url(cls) -> str:
        return f"amqp://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}"
        
        
class redis_cfg:
    PORT = os.getenv("REDIS_PORT")
    HOST = os.getenv("REDIS_HOST")
    PASSWORD = os.getenv("REDIS_PASSWORD")
    USERNAME = os.getenv("REDIS_USERNAME")
    DB = os.getenv("REDIS_HOST_DB")
    
    @classmethod
    def url(cls) -> str:
        return f"redis://{cls.USERNAME}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DB}"
    

class mongo_cfg:
    MONGO_USERNAME=os.getenv("MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD=os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    MONGO_DATABASE=os.getenv("MONGO_INITDB_DATABASE")
    MONGO_HOST=os.getenv("MONGO_HOST")
    MONGO_PORT=os.getenv("MONGO_PORT")
    
    @classmethod
    def url(cls) -> str:
        return f"mongodb://{cls.MONGO_USERNAME}:{cls.MONGO_PASSWORD}@{cls.MONGO_HOST}:{cls.MONGO_PORT}/"