from bokchoy.tasks import task
from bokchoy.registry import registry
from bokchoy.job import Job

from exam import before, Exam

_state = {}


class JobTests(Exam):
    @before
    def init_tasks(self):
        @task(self.conductor, name='kolkt.tasks.message', max_retries=3, retry_interval=60)
        def message(text, *args, **kwargs):
            _state['message'] = text

        self.message = message

        @task(self.conductor, name='kolkt.tasks.error', max_retries=3, retry_interval=60, topic='test')
        def error(text, *args, **kwargs):
            raise Exception('test')

        self.error = error

    @before
    def init_result(self):
        self.result.flush()

    def test_registry(self):
        assert registry.get_registered('kolkt.tasks.message') is not None
        assert registry.get_registered('kolkt.tasks.error') is not None

    def test_execute_job(self):
        job = self.message.delay('test')

        assert job is not None
        assert job.is_queued() is True

        assert self.result.exists(job.key) is True

    def test_fetch_job(self):
        job = self.message.delay('test')

        retrieved_job = Job.fetch(job.key, backend=self.result, serializer=self.serializer)

        assert job == retrieved_job

    def test_retry_job(self):
        job = self.error.delay('test')

        assert self.conductor.handle(job) is False
        assert job.is_failed() is True
        assert job.child is not None
        assert job.child.is_queued() is True

    def test_consume_job(self):
        job = self.message.delay('test')

        assert self.conductor.handle(job) is True

        assert 'test' not in _state
