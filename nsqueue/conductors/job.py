import uuid

from datetime import datetime

from functools import partial

from nsqueue.utils.types import enum, utcformat, utcparse, safe_int
from nsqueue.compat import as_text
from nsqueue.exceptions import UnpickleError

try:
    import cPickle as pickle
except ImportError:  # noqa
    import pickle

dumps = partial(pickle.dumps, protocol=pickle.HIGHEST_PROTOCOL)
loads = pickle.loads


def unpickle(pickled_string):
    try:
        obj = loads(pickled_string)
    except Exception as e:
        raise UnpickleError('Could not unpickle', pickled_string, e)
    return obj


JobStatus = enum(
    'JobStatus',
    QUEUED=0,
    FAILED=1,
    SUCCEEDED=2
)


class Job(object):
    def __init__(self, id=None, published_at=None,
                 serializer=None, key=None,
                 backend=None, args=None,
                 kwargs=None, task=None):
        self.task = task
        self.args = args
        self.kwargs = kwargs
        self.published_at = published_at or datetime.now()
        self.backend = backend
        self.key = key

        if task:
            self.max_retries = task.max_retries

        self.error = None
        self.serializer = serializer
        self.result = None

        self._name = None
        self._id = id or str(uuid.uuid4())
        self._status = JobStatus.QUEUED

    @property
    def name(self):
        if self._name is not None:
            return self._name

        return self.task.name

    @name.setter
    def name(self, name):
        self._name = name

    @classmethod
    def fetch(cls, key, backend=None, serializer=None):
        job = cls(key=key,
                  backend=backend,
                  serializer=serializer)

        job.refresh()
        return job

    @property
    def id(self):
        return self._id

    def get_status(self):
        return int(self._status)

    def is_failed(self):
        return self.get_status() == JobStatus.FAILED

    def is_succeeded(self):
        return self.get_status() == JobStatus.SUCCEEDED

    def is_queued(self):
        return self.get_status() == JobStatus.QUEUED

    def set_status(self, status, commit=True):
        self._status = status

        if commit is True:
            self.set('status', status)

    def set_status_failed(self, commit=True):
        return self.set_status(JobStatus.FAILED, commit=commit)

    def set_status_succeeded(self, commit=True):
        return self.set_status(JobStatus.SUCCEEDED, commit=commit)

    def set(self, key, value):
        self.backend.hset(self.key, key, value)

    def set_many(self, items, ttl=None):
        self.backend.hset_many(self.key, items, ttl=ttl)

    def get(self, key):
        self.backend.hget(self.key, key)

    def refresh(self):
        obj = self.backend.hgetall(self.key)

        if len(obj) == 0:
            return None

        def to_date(date_str):
            if date_str is None:
                return
            else:
                return utcparse(date_str)

        self.published_at = to_date(obj.get('published_at'))
        self.max_retries = safe_int(obj.get('max_retries'))
        self.error = as_text(obj.get('error'))
        self.status = safe_int(obj.get('status'))
        self.name = as_text(obj.get('name'))

        result = obj.get('result')

        if result:
            self.result = unpickle(result)
        else:
            self.result = None

        kwargs = obj.get('kwargs')

        if kwargs:
            self.kwargs = self.serializer.loads(as_text(kwargs))

        args = obj.get('args')

        if args:
            self.args = self.serializer.loads(as_text(args))

    def to_dict(self):
        return {
            'id': self.id,
            'status': int(self.get_status()),
            'error': self.error,
            'max_retries': self.max_retries,
            'published_at': utcformat(self.published_at),
            'kwargs': self.serializer.dumps(self.kwargs),
            'name': self.name,
            'args': self.serializer.dumps(self.args),
            'result': dumps(self.result) if self.result else None,
        }

    def save(self):
        result = self.to_dict()

        for k, v in result.items():
            if v is None:
                result[k] = ''

        self.set_many(result,
                      ttl=self.result_ttl if not self.is_queued() else None)

    def expire(self):
        self.backend.expire(self.key, self.result_ttl)

    @property
    def result_ttl(self):
        return self.task.result_ttl

    @property
    def key(self):
        if self._key is not None:
            return self._key

        return '%s:%s' % (
            self.name,
            self.id
        )

    @key.setter
    def key(self, key):
        self._key = key

    def __call__(self, *args, **kwargs):
        self.args = args or self.args
        self.kwargs = kwargs or self.kwargs

        return self.task.func(*self.args, **self.kwargs)

    def __str__(self):
        return '<Job {0}>'.format(self.id)

    def __repr__(self):  # noqa
        return 'Job({0!r}, published_at={1!r})'.format(self.key, self.published_at)
