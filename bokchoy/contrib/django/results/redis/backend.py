from bokchoy.results import redis

from .helpers import get_redis_connection
from . import defaults


class RedisResult(redis.RedisResult):
    def __init__(self, *args, **kwargs):
        client = get_redis_connection(defaults.CACHE_ALIAS)

        super(RedisResult, self).__init__(client=client, *args, **kwargs)
