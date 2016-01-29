from bokchoy.results import base
from bokchoy.compat import as_text


def decode_redis_hash(h):
    return dict((as_text(k), h[k]) for k in h)


class RedisResult(base.Result):
    def __init__(self, client):
        self.client = client

    def hset(self, name, key, value):
        return self.client.hset(name, key, value)

    def hgetall(self, key):
        return decode_redis_hash(self.client.hgetall(key))

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
        self.client.flush()

    def exists(self, key):
        return self.client.exists(key)
