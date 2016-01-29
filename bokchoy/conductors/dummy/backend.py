from bokchoy.conductors import base


class DummyConductor(base.Conductor):
    def _publish(self, job, *args, **kwargs):
        pass

    def consume(self, topics, channel):
        pass

    def _handle(self, message):
        pass

    def retry(self, job, message):
        pass
