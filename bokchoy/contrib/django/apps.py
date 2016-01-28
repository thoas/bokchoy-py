from django.utils.module_loading import autodiscover_modules
from django.apps import AppConfig


class BokchoyConfig(AppConfig):
    name = 'bokchoy.contrib.django'
    verbose_name = 'Bok Choy'

    def ready(self):
        super(BokchoyConfig, self).ready()

        autodiscover_modules('tasks')
