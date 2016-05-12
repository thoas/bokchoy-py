from bokchoy.conductors import base


class DummyConductor(base.Conductor):
    def __init__(self, *args, **kwargs):
        self.jobs = []

        super(DummyConductor, self).__init__(*args, **kwargs)

    def _publish(self, job, *args, **kwargs):
        self.jobs.append(job.key)

    def consume(self, topics, channel):
        while True:
            self.handle(self.jobs.pop())

    def _get_job_id(self, message):
        return message.key

    def _retry(self, job, message):
        self.jobs.append(job.key)
