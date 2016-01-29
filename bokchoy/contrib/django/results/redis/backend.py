from bokchoy.results import redis

from .helpers import get_redis_connection


class RedisResult(redis.RedisResult):
    def __init__(self, *args, **kwargs):
        client = get_redis_connection('bokchoy')

        super(RedisResult, self).__init__(client=client, *args, **kwargs)
