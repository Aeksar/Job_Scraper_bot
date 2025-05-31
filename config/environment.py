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
    
    @classmethod
    def get_url(cls) -> str:
        return f"amqp://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}"
        
        
class redis_cfg:
    PORT = os.getenv("REDIS_PORT")
    HOST = os.getenv("REDIS_HOST")
    PASSWORD = os.getenv("REDIS_PASSWORD")
    USERNAME = os.getenv("REDIS_USERNAME")
    DB = os.getenv("REDIS_HOST_DB")