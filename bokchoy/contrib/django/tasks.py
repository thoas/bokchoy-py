from bokchoy.contrib.django import defaults

from bokchoy import tasks as base

from .app import conductor


class task(base.task):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('topic', defaults.TOPIC)
        kwargs.setdefault('max_retries', defaults.MAX_RETRIES)
        kwargs.setdefault('retry_interval', defaults.RETRY_INTERVAL)
        kwargs.setdefault('ttl', defaults.TTL)
        kwargs.setdefault('always_eager', defaults.ALWAYS_EAGER)
        kwargs.setdefault('conductor', conductor)
        kwargs.setdefault('timeout', defaults.TIMEOUT)

        super(task, self).__init__(*args, **kwargs)
