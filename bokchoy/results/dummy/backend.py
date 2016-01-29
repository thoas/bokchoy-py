from bokchoy.results import base

from collections import defaultdict


class DummyResult(base.Result):
    def __init__(self):
        self.data = defaultdict(dict)

    def hset(self, name, key, value):
        self.data[name][key] = value

    def hgetall(self, key):
        return self.data[key]

    def hset_many(self, key, items, ttl=None):
        self.data[key].update(items)

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def hget(self, name, key):
        return (self.data.get(key) or {}).get(key)

    def expire(self, key, ttl, pipe=None):
        pass
