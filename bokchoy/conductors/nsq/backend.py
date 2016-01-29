from bokchoy.conductors import base
from bokchoy.job import Job
from bokchoy.compat import as_text

import nsq

from .connection import ConnectionPool


class NSQBackend(base.Backend):
    def __init__(self, *args, **kwargs):
        self.tcp_addresses = kwargs.pop('tcp_addresses')
        self.http_addresses = kwargs.pop('http_addresses')

        super(NSQBackend, self).__init__(*args, **kwargs)

        self.writer = nsq.Writer(self.tcp_addresses)
        self.writer.conns = {'pool': ConnectionPool(self.tcp_addresses)}

    def _publish(self, job, *args, **kwargs):
        self.writer.pub(job.task.topic, job.key)

    def consume(self, topics, channel):
        self.logger.info("NSQ worker started, topics: {}, channel:{}, addresses:{}".format(','.join(topics), channel, ','.join(self.http_addresses)))

        for t in topics:
            nsq.Reader(message_handler=self.handle,
                       lookupd_http_addresses=self.http_addresses,
                       topic=t, channel=channel,
                       lookupd_poll_interval=15)
        nsq.run()

    def _handle(self, message):
        return Job.fetch(key=as_text(message.body),
                         backend=self.result,
                         serializer=self.serializer)

    def retry(self, job, message):
        message.requeue(delay=job.task.retry_interval / 60.0)  # we need it in seconds
