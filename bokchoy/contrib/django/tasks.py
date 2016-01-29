from bokchoy.contrib.django import defaults

from bokchoy import tasks as base

from .app import conductor


class task(base.task):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('topic', defaults.DEFAULT_TOPIC)
        kwargs.setdefault('max_retries', defaults.DEFAULT_MAX_RETRIES)
        kwargs.setdefault('retry_interval', defaults.DEFAULT_RETRY_INTERVAL)
        kwargs.setdefault('result_ttl', defaults.DEFAULT_RESULT_TTL)
        kwargs.setdefault('always_eager', defaults.ALWAYS_EAGER)
        kwargs.setdefault('conductor', conductor)

        super(task, self).__init__(*args, **kwargs)
