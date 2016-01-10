class Backend(object):
    def hset(self, name, key, value):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def hget(self, name, key):
        raise NotImplementedError

    def hset_many(self, key, items, ttl=None):
        raise NotImplementedError

    def hgetall(self, key):
        raise NotImplementedError

    def expire(self, key, ttl, pipe=None):
        raise NotImplementedError
