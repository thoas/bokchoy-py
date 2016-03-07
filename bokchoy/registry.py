from bokchoy.utils.log import base_logger


class Registry(object):
    def __init__(self):
        self._registry = {}

    def register(self, task):
        self._registry[task.name] = task

        base_logger.debug('<Task: {}> registered'.format(task.name))

    def get_registered(self, task_name):
        task = self._registry.get(task_name)

        if task is None:
            raise LookupError(
                "Task '%s' not registered." % (task_name))

        return task


registry = Registry()
