from bokchoy.tasks import task
from bokchoy.job import Job

from exam import before, Exam

_state = {}


class JobTests(Exam):
    @before
    def init_tasks(self):
        @task(self.conductor, name='bokchoy.tasks.message', max_retries=3, retry_interval=60)
        def message(text, *args, **kwargs):
            _state['message'] = text

        self.message = message

        @task(self.conductor, name='bokchoy.tasks.error', max_retries=3, retry_interval=60, topic='test')
        def error(text, *args, **kwargs):
            raise Exception('test')

        self.error = error

    @before
    def init_result(self):
        self.result.flush()

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

        task = job.task

        for i in range(task.max_retries):
            assert self.conductor.handle(job) is False
            assert job.is_failed() is True

            job = job.child

            assert job is not None
            assert job.is_queued() is True
            assert job is not None

            assert job.max_retries - (i + 1)

        assert self.conductor.handle(job) is False
        assert job.child is None

    def test_consume_job(self):
        job = self.message.delay('test')

        assert self.conductor.handle(job) is True

        assert 'test' not in _state
