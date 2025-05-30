from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.getenv("TOKEN")

class rabbit_cfg:
    RMQ_HOST = os.getenv("RMQ_HOST")
    RMQ_PORT = os.getenv("RMG_PORT")
    RMQ_PWD = os.getenv("RMQ_PWD")
    RMQ_USER = os.getenv("RMQ_USER")
    
    MQ_EXCHANGE = os.getenv("MQ_EXCHANGE")
    MQ_RK = os.getenv("MQ_RK")
    
    @classmethod
    def get_url(cls) -> str:
        return f"amqp://{cls.RMQ_USER}:{cls.RMQ_PWD}@{cls.RMQ_HOST}:{cls.RMQ_PORT}"
        