import unittest
import redis
import socket
import pytest

from bokchoy.conductors.dummy import DummyConductor
from bokchoy.results.redis import RedisResult
from bokchoy.serializers.json import JSONSerializer

from exam import fixture

from .base import JobTests


def redis_is_available():
    try:
        socket.create_connection(('127.0.0.1', 6379), 1.0)
    except socket.error:
        return False
    else:
        return True

requires_redis = pytest.mark.skipif(
    not redis_is_available(),
    reason="requires elastic search server running")


@requires_redis
class RedisJobTests(JobTests, unittest.TestCase):
    @fixture
    def conductor(self):
        return DummyConductor(serializer=self.serializer, result=self.result)

    @fixture
    def serializer(self):
        return JSONSerializer()

    @fixture
    def result(self):
        return RedisResult(client=redis.StrictRedis())
