from django.core.management.base import BaseCommand

from task.cron_task import run_parse


class Command(BaseCommand):
    help = 'Parse the output of a task'

    def add_arguments(self, parser):
        parser.add_argument('task_id', type=int)

    def handle(self, *args, **options):
        run_parse(options['task_id'])
