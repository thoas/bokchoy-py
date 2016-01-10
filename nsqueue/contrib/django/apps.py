from django.utils.module_loading import autodiscover_modules
from django.apps import AppConfig


class NSQueueConfig(AppConfig):
    name = 'nsqueue.contrib.django'
    verbose_name = 'NSQueue'

    def ready(self):
        super(NSQueueConfig, self).ready()

        autodiscover_modules('tasks')
