from bokchoy.utils.log import get_task_logger
from bokchoy.registry import registry

from functools import wraps


class task(object):
    def __init__(self, conductor=None, name=None, timeout=None,
                 topic=None, max_retries=None,
                 always_eager=False,
                 retry_interval=None, result_ttl=None):
        self.conductor = conductor
        self.name = name
        self.timeout = timeout
        self.topic = topic
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.result_ttl = result_ttl
        self.func = None
        self.always_eager = always_eager

    def __call__(self, f):
        name = self.name or '%s.%s' % (f.__module__, f.__name__)

        self.name = name

        self.func = f

        @wraps(f)
        def delay(*args, **kwargs):
            if self.always_eager:
                return f(*args, **kwargs)

            return self.conductor.publish(self, *args, **kwargs)

        f.delay = delay
        f.get_logger = lambda: get_task_logger(self.name)

        registry.register(self)

        return f
