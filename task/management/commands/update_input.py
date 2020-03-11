from django.core.management.base import BaseCommand

from task.cron_task import update_input
from pekja.utils import get_task_by_id


class Command(BaseCommand):
    help = 'Update task input'

    def add_arguments(self, parser):
        parser.add_argument('task_id', type=int)

    def handle(self, *args, **options):
        task = get_task_by_id(options['task_id'])
        if task:
            update_input(task)
