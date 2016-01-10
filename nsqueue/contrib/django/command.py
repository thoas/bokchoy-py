from django.core.management.base import BaseCommand


class WorkerCommand(BaseCommand):
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
        from kolkt.queue import publisher
        publisher.consume(options['topic'].split(','),
                          options['channel'])
