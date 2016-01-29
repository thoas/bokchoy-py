from bokchoy.results import base

from .utils import decode_hash


class RedisResult(base.Result):
    def __init__(self, client):
        self.client = client

    def hset(self, name, key, value):
        return self.client.hset(name, key, value)

    def hgetall(self, key):
        return decode_hash(self.client.hgetall(key))

    def hset_many(self, key, items, ttl=None):
        with self.client.pipeline() as pipe:
            for k, v in items.items():
                pipe.hset(key, k, v)

            if ttl is not None:
                self.expire(key, ttl)

            pipe.execute()

    def set(self, key, value):
        return self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)

    def hget(self, name, key):
        return self.client.hget(name, key)

    def expire(self, key, ttl, pipe=None):
        pipe = pipe or self.client

        return pipe.expire(key, ttl)

    def flush(self):
        self.client.flushdb()

    def exists(self, key):
        return self.client.exists(key)
