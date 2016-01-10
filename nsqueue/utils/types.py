import datetime

from nsqueue.compat import as_text


def enum(name, *sequential, **named):
    values = dict(zip(sequential, range(len(sequential))), **named)

    # NOTE: Yes, we *really* want to cast using str() here.
    # On Python 2 type() requires a byte string (which is str() on Python 2).
    # On Python 3 it does not matter, so we'll use str(), which acts as
    # a no-op.
    return type(str(name), (), values)


def utcformat(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


def utcparse(string):
    return datetime.datetime.strptime(as_text(string), '%Y-%m-%dT%H:%M:%SZ')


def safe_int(value):
    if value is not None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    return None
