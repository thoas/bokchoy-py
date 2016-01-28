from django.core.management.base import BaseCommand


class Command(BaseCommand):
    options = BaseCommand.option_list

    def add_arguments(self, parser):
        parser.add_argument('--topic',
                            dest='topic',
                            type=str)

        parser.add_argument('--channel',
                            dest='channel',
                            default='default',
                            type=str)

    def handle(self, *args, **options):
        from bokchoy.contrib.django.app import conductor

        conductor.consume(options['topic'].split(','),
                          options['channel'])
