from bokchoy.job import Job
from bokchoy.utils.log import base_logger

import traceback
import sys
import time

from bokchoy import signals


class Conductor(object):
    def __init__(self, serializer, result, logger=None):
        self.serializer = serializer
        self.result = result
        self.logger = logger or base_logger

    def publish(self, task, *args, **kwargs):
        job = Job(task=task,
                  args=args,
                  kwargs=kwargs,
                  serializer=self.serializer,
                  backend=self.result)
        job.save()

        self._publish(job, *args, **kwargs)

        self.logger.info('%r published' % job)

        signals.job_published.send(job)

        return job

    def handle(self, message):
        job = self._handle(message)
        job.refresh()

        signals.job_received.send(job)

        self.logger.info('%r received' % job)

        ts = time.time()

        result = None

        try:
            result = job()
        except Exception:
            exc_string = self.handle_exception(job, *sys.exc_info())

            job.error = exc_string

            laps = time.time() - ts

            job.exec_time = laps
            job.set_status_failed(commit=False)

            self.logger.warning('%r failed in %2.3f seconds' % (job, laps))

            if job.can_retry():
                job.child = self.retry(job, message)

                signals.job_retried.send(job)

            job.save()

            signals.job_failed.send(job)
            signals.job_finished.send(job)

            return False
        else:
            laps = time.time() - ts

            job.set_status_succeeded(commit=False)
            job.exec_time = laps
            job.result = result
            job.save()

            signals.job_succeeded.send(job)
            signals.job_finished.send(job)

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

    def retry(self, job, message):
        new_job = job.retry()
        new_job.save()

        self.logger.warning('%r will be retried in %2.3f seconds via %r, still %d retries' % (
            job,
            job.retry_interval / 60.0,
            new_job,
            job.max_retries
        ))

        self._retry(new_job, message)

        return new_job

    def _retry(self, job, message):
        raise NotImplementedError

    def _publish(self, job):
        raise NotImplementedError

    def _handle(self, message):
        raise NotImplementedError
