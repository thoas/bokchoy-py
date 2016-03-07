from bokchoy.results import redis
from bokchoy.utils.imports import get_instance


class RedisResult(redis.RedisResult):
    def __init__(self, *args, **kwargs):

        client_class = kwargs.pop('client_class')
        options = kwargs.pop('options')

        client = get_instance(client_class, **options)

        super(RedisResult, self).__init__(client=client, *args, **kwargs)
