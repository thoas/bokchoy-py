from bokchoy.serializers import base

try:
    import simplejson as json
except ImportError:
    import json


import uuid


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)

        return super(JSONEncoder, self).default(obj)


class JSONSerializer(base.Serializer):
    def dumps(self, value):
        return json.dumps(value, cls=JSONEncoder)

    def loads(self, value):
        return json.loads(value)
