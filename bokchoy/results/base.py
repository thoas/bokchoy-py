class Result(object):
    def set(self, name, key, value):
        raise NotImplementedError

    def get(self, name, key=None):
        raise NotImplementedError

    def set_many(self, key, items, ttl=None):
        raise NotImplementedError

    def expire(self, key, ttl):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError

    def exists(self, key):
        raise NotImplementedError
