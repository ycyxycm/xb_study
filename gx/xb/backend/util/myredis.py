import redis
from conf.config import *

expire_time = 60 * 60


class RedisClient():
    def __init__(self):
        self.host = REDIS_HOST
        self.port = REDIS_PORT
        self.password = REDIS_PASSWORD
        self.db = REDIS_DB

        self.pool = redis.ConnectionPool(
            host=self.host,
            port=self.port,
            password=self.password,
            db=self.db,
            max_connections=300,
            decode_responses=True#设置返回值是否字符串类型 True为字符串 False为字节类型bytes
        )
        self.client = redis.Redis(
            connection_pool=self.pool,
            decode_responses=True,
            socket_connect_timeout=1
        )

    def get(self, key):
        try:
            redis_instance = self.client.get(key)
            if not redis_instance:
                return None
            try:
                if isinstance(redis_instance, bytes):
                    redis_instance = str(redis_instance, encoding="utf-8")
                redis_instance = eval(redis_instance)
            except Exception as e:
                pass
            return redis_instance
        except Exception as e:
            return None

    def set(self, key, value):
        try:
            self.client.set(key, value)
            return True
        except Exception as e:
            return False
# redis_cli = RedisClient()
