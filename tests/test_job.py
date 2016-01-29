import unittest

from bokchoy.tasks import task
from bokchoy.conductors.dummy import DummyConductor
from bokchoy.results.dummy import DummyResult
from bokchoy.serializers.json import JSONSerializer
from bokchoy.registry import registry
from bokchoy.job import Job

from exam import fixture, before, Exam


class JobTests(Exam, unittest.TestCase):
    @before
    def init_tasks(self):
        @task(self.conductor, name='kolkt.tasks.message', max_retries=3)
        def message(text, *args, **kwargs):
            print(text)

        self.message = message

        @task(self.conductor, name='kolkt.tasks.error', max_retries=3, topic='test')
        def error(text, *args, **kwargs):
            raise Exception('test')

        self.error = error

    @before
    def init_result(self):
        self.result.flush()

    @fixture
    def conductor(self):
        return DummyConductor(serializer=self.serializer, result=self.result)

    @fixture
    def serializer(self):
        return JSONSerializer()

    @fixture
    def result(self):
        return DummyResult()

    def test_registry(self):
        assert registry.get_registered('kolkt.tasks.message') is not None
        assert registry.get_registered('kolkt.tasks.error') is not None

    def test_execute_job(self):
        job = self.message.delay('test')

        assert job is not None

        assert self.result.exists(job.key) is True

        retrieved_job = Job.fetch(job.key, backend=self.result, serializer=self.serializer)

        assert job == retrieved_job
