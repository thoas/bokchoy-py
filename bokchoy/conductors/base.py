from .job import Job

import traceback
import sys
import time


class Backend(object):
    def __init__(self, serializer, logger, result):
        self.serializer = serializer
        self.logger = logger
        self.result = result

        self._registry = {}

    def register_task(self, task):
        self._registry[task.name] = task

    def get_registered_task(self, task_name):
        task = self._registry.get(task_name)

        if task is None:
            raise LookupError(
                "Task '%s' not registered." % (task_name))

        return task

    def publish(self, task, *args, **kwargs):
        job = Job(task=task,
                  args=args,
                  kwargs=kwargs,
                  serializer=self.serializer,
                  backend=self.result)
        job.save()

        self._publish(job, *args, **kwargs)

        self.logger.info('%r published' % job)

        return job

    def handle(self, message):
        job = self._handle(message)
        job.refresh()
        job.task = self.get_registered_task(job.name)

        self.logger.info('%r received' % job)

        ts = time.time()

        result = None

        try:
            result = job()
        except Exception:
            exc_string = self.handle_exception(job, *sys.exc_info())

            job.error = exc_string

            max_retries = job.max_retries

            laps = time.time() - ts

            if max_retries > 0:
                job.max_retries = max_retries - 1

                self.logger.warning('%r failed in %2.3f seconds' % (job, laps))
                self.logger.warning('%r will be retried in %d seconds, still %d retries' % (job, job.task.retry_interval / 60.0), job.max_retries)

                self.retry(job, message)
            else:
                job.set_status_failed(commit=False)

                self.logger.warning('%r failed in %2.3f seconds' % (job, laps))

            job.save()

            return False
        else:
            job.set_status_succeeded(commit=False)
            job.result = result
            job.save()

            laps = time.time() - ts

            self.logger.warning('%r succeeded in %2.3f seconds' % (job, laps))

            return True

    def handle_exception(self, job, *exc_info):
        exc_string = ''.join(traceback.format_exception_only(*exc_info[:2]) +
                             traceback.format_exception(*exc_info))

        self.logger.error(exc_string, exc_info=True, extra={
            'func': job.name,
            'arguments': job.args,
            'kwargs': job.kwargs,
        })

        return exc_string

    def consume(self, *args, **kwargs):
        raise NotImplementedError

    def retry(self):
        raise NotImplementedError

    def _publish(self, job):
        raise NotImplementedError

    def _handle(self, message):
        raise NotImplementedError
