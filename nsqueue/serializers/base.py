class Serializer(object):
    def dumps(self, value):
        raise NotImplementedError

    def loads(self, value):
        raise NotImplementedError
