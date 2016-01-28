import six
import logging


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


def logger_isa(l, p, max=1000):
    this, seen = l, set()
    for _ in range(max):
        if this == p:
            return True
        else:
            if this in seen:
                raise RuntimeError(
                    'Logger {0!r} parents recursive'.format(l),
                )
            seen.add(this)
            this = this.parent
            if not this:
                break
    else:  # pragma: no cover
        raise RuntimeError('Logger hierarchy exceeds {0}'.format(max))
    return False


def _get_logger(logger):
    if isinstance(logger, six.string_types):
        logger = logging.getLogger(logger)

    if not logger.handlers:
        logger.addHandler(NullHandler())

    return logger


def get_logger(name):
    l = _get_logger(name)

    if logging.root not in (l, l.parent) and l is not base_logger:
        if not logger_isa(l, base_logger):  # pragma: no cover
            l.parent = base_logger

    return l


base_logger = logger = _get_logger('bokchoy')
task_logger = get_logger('bokchoy.task')
worker_logger = get_logger('bokchoy.worker')


def get_task_logger(name):
    logger = get_logger(name)

    if not logger_isa(logger, task_logger):
        logger.parent = task_logger

    return logger
