from django.core.management.base import BaseCommand

from command.cron_task import run_parse
from pekja.utils import get_task_by_id


class Command(BaseCommand):
    help = 'Parse the output of a task'

    def add_arguments(self, parser):
        parser.add_argument('task_id', type=int)

    def handle(self, *args, **options):
        task = get_task_by_id(options['task_id'])
        if task:
            run_parse(task)
