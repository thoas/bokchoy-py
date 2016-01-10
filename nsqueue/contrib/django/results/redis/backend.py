from nsqueue.results import redis

from .helpers import get_redis_connection


class RedisBackend(redis.RedisBackend):
    def __init__(self, *args, **kwargs):
        client = get_redis_connection('nsqueue')

        super(RedisBackend, self).__init__(client=client, *args, **kwargs)
