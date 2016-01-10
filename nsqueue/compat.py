import six


if not six.PY2:
    # Python 3.x and up
    text_type = str
    string_types = (str,)

    def as_text(v):
        if v is None:
            return None
        elif isinstance(v, bytes):
            return v.decode('utf-8')
        elif isinstance(v, str):
            return v
        else:
            raise ValueError('Unknown type %r' % type(v))
else:
    # Python 2.x
    text_type = unicode
    string_types = (str, unicode)

    def as_text(v):
        if v is None:
            return None
        return v.decode('utf-8')

    def decode_redis_hash(h):
        return h
