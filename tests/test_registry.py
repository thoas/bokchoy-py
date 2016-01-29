import unittest

from bokchoy.tasks import task
from bokchoy.registry import registry

from exam import before, Exam


class RegistryTests(Exam, unittest.TestCase):
    @before
    def init_tasks(self):
        @task(name='bokchoy.tasks.message', max_retries=3, retry_interval=60)
        def message(text, *args, **kwargs):
            print(text)

    def test_registry(self):
        assert registry.get_registered('bokchoy.tasks.message') is not None
