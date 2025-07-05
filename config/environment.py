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
    def url(cls) -> str:
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
    USERNAME=os.getenv("MONGO_INITDB_ROOT_USERNAME")
    PASSWORD=os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    DATABASE=os.getenv("MONGO_INITDB_DATABASE")
    HOST=os.getenv("MONGO_HOST")
    PORT=os.getenv("MONGO_PORT")
    
    @classmethod
    def url(cls) -> str:
        return f"mongodb://{cls.USERNAME}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/"