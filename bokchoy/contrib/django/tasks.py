from bokchoy.contrib.django.app import conductor
from bokchoy.contrib.django import defaults
from bokchoy.utils.log import get_task_logger

from functools import wraps


class task(object):
    def __init__(self, name=None, timeout=None,
                 topic=defaults.DEFAULT_TOPIC,
                 max_retries=defaults.DEFAULT_MAX_RETRIES,
                 retry_interval=defaults.DEFAULT_RETRY_INTERVAL,
                 result_ttl=defaults.DEFAULT_RESULT_TTL):
        self.name = name
        self.timeout = timeout
        self.topic = topic
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.result_ttl = result_ttl
        self.func = None

    def __call__(self, f):
        name = self.name or '%s.%s' % (f.__module__, f.__name__)

        self.name = name

        self.func = f

        @wraps(f)
        def delay(*args, **kwargs):
            if defaults.ALWAYS_EAGER:
                return f(*args, **kwargs)

            return conductor.publish(self, *args, **kwargs)

        f.delay = delay
        f.get_logger = lambda: get_task_logger(self.name)

        conductor.register_task(self)

        return f
