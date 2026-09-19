import json
import redis
from django.conf import settings

redis_host = settings.REDIS_HOST
redis_port = settings.REDIS_PORT
redis_select_db = settings.REDIS_SELECT_DB

class RedisCache:
    def __init__(self):
        self.client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_select_db,
            decode_responses=True
        )

    def get_data(self, cache_key):
        data = self.client.get(cache_key)
        return json.loads(data) if data else None

    def set_data(self, cache_key, data, timeout=3600):
        self.client.set(
            cache_key,
            json.dumps(data),
            ex=timeout
        )
