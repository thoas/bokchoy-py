from bokchoy.conductors import base


class DummyConductor(base.Conductor):
    def __init__(self, *args, **kwargs):
        self.jobs = []

        super(DummyConductor, self).__init__(*args, **kwargs)

    def _publish(self, job, *args, **kwargs):
        self.jobs.append(job)

    def consume(self, topics, channel):
        while True:
            self._handle(self.jobs.pop())

    def _handle(self, message):
        return message

    def _retry(self, job, message):
        self.jobs.append(job)
