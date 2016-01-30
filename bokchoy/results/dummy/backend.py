from bokchoy.results import base

from collections import defaultdict


class DummyResult(base.Result):
    def __init__(self):
        self.flush()

    def set(self, name, key, value):
        self.data[name][key] = value

    def set_many(self, key, items, ttl=None):
        self.data[key].update(items)

    def get(self, name, key=None):
        if key is not None:
            return (self.data.get(name) or {}).get(key)

        return self.data.get(name)

    def expire(self, key, ttl, pipe=None):
        pass

    def flush(self):
        self.data = defaultdict(dict)

    def exists(self, key):
        return key in self.data
