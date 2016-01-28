from bokchoy.results import redis

from .helpers import get_redis_connection


class RedisBackend(redis.RedisBackend):
    def __init__(self, *args, **kwargs):
        client = get_redis_connection('bokchoy')

        super(RedisBackend, self).__init__(client=client, *args, **kwargs)
