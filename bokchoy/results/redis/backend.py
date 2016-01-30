from bokchoy.results import base

from .utils import decode_hash


class RedisResult(base.Result):
    def __init__(self, client):
        self.client = client

    def set(self, name, key, value):
        return self.client.hset(name, key, value)

    def set_many(self, key, items, ttl=None):
        with self.client.pipeline() as pipe:
            for k, v in items.items():
                pipe.hset(key, k, v)

            if ttl is not None:
                self.expire(key, ttl)

            pipe.execute()

    def get(self, name, key=None):
        if key is not None:
            return self.client.hget(name, key)

        return decode_hash(self.client.hgetall(name))

    def expire(self, key, ttl, pipe=None):
        pipe = pipe or self.client

        return pipe.expire(key, ttl)

    def flush(self):
        self.client.flushdb()

    def exists(self, key):
        return self.client.exists(key)
