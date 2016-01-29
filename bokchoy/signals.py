from blinker import Namespace


signals = Namespace()

job_received = signals.signal('job_received')

job_finished = signals.signal('job_finished')

job_failed = signals.signal('job_failed')

job_retried = signals.signal('job_retried')

job_succeeded = signals.signal('job_succeeded')

job_published = signals.signal('job_published')
