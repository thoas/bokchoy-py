from nsqueue.serializers import base

try:
    import simplejson as json
except ImportError:
    import json


class Serializer(base.Serializer):
    def dumps(self, value):
        return json.dumps(value)

    def loads(self, value):
        return json.loads(value)
