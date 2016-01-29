import unittest

from bokchoy.conductors.dummy import DummyConductor
from bokchoy.results.dummy import DummyResult
from bokchoy.serializers.json import JSONSerializer

from exam import fixture

from .base import JobTests


class DummyJobTests(JobTests, unittest.TestCase):
    @fixture
    def conductor(self):
        return DummyConductor(serializer=self.serializer, result=self.result)

    @fixture
    def serializer(self):
        return JSONSerializer()

    @fixture
    def result(self):
        return DummyResult()
