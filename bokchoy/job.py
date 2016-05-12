import uuid

from datetime import datetime

from functools import partial

from bokchoy.utils.types import enum, utcformat, utcparse, safe_int
from bokchoy.compat import as_text
from bokchoy.exceptions import UnpickleError
from bokchoy.registry import registry

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
                 serializer=None, key=None, child=None,
                 parent=None, max_retries=None, timeout=None,
                 backend=None, args=None,
                 kwargs=None, task=None):
        self.task = task
        self.args = args
        self.kwargs = kwargs
        self.published_at = published_at or datetime.now()
        self.backend = backend
        self.key = key
        self.max_retries = max_retries
        self.timeout = timeout

        if task:
            if self.max_retries is None:
                self.max_retries = task.max_retries

            if self.timeout is None:
                self.timeout = task.timeout

        self.error = None
        self.serializer = serializer
        self.result = None
        self.parent = parent
        self.child = child
        self.exec_time = None

        self._name = None
        self._id = id
        self._status = JobStatus.QUEUED

    @property
    def name(self):
        if self._name is not None:
            return self._name

        if self.task:
            return self.task.name

        return None

    @name.setter
    def name(self, name):
        self._name = name

    @classmethod
    def fetch(cls, key, backend, serializer):
        job = cls(key=key,
                  backend=backend,
                  serializer=serializer)

        job.refresh()

        return job

    def __eq__(self, job):
        return self.to_dict() == job.to_dict()

    @property
    def id(self):
        if self._id is None:
            self._id = str(uuid.uuid4())

        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    def get_status(self):
        return int(self._status)

    def retry(self):
        job = Job(task=self.task,
                  args=self.args,
                  serializer=self.serializer,
                  max_retries=self.max_retries - 1,
                  backend=self.backend,
                  parent=self,
                  kwargs=self.kwargs)

        return job

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
        self.backend.set(self.key, key, value)

    def set_many(self, items, ttl=None):
        self.backend.set_many(self.key, items, ttl=ttl)

    def get(self, key):
        self.backend.get(self.key, key)

    def refresh(self):
        obj = self.backend.get(self.key)

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
        self._id = as_text(obj.get('id'))

        child_key = as_text(obj.get('child'))

        if child_key:
            self.child = Job.fetch(child_key, backend=self.backend, serializer=self.serializer)

        if not self.error:
            self.error = None

        self._status = safe_int(obj.get('status'))
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

        if self.name:
            self.task = registry.get_registered(self.name)

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
            'exec_time': self.exec_time,
            'result': dumps(self.result) if self.result else None,
            'parent': self.parent.key if self.parent else None,
            'child': self.child.key if self.child else None,
        }

    def save(self):
        result = self.to_dict()

        for k, v in result.items():
            if v is None:
                result[k] = ''

        self.set_many(result,
                      ttl=self.ttl if not self.is_queued() else None)

    def expire(self):
        self.backend.expire(self.key, self.ttl)

    @property
    def ttl(self):
        return self.task.ttl

    @property
    def retry_interval(self):
        return self.task.retry_interval

    @property
    def key(self):
        if self._key is None:
            self._key = '%s:%s' % (
                self.name,
                self.id
            )

        return self._key

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

    def can_retry(self):
        return self.max_retries > 0
