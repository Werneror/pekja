from django.core.management.base import BaseCommand

from entities.models import Task
from entities.models import BatchTask
from command.cron_task import set_cron_task
from command.cron_task import set_cron_batch_task


class Command(BaseCommand):
    help = 'Add all tasks to crontab'

    def handle(self, *args, **options):
        for task in Task.objects.all():
            set_cron_task(task)
        for batch_task in BatchTask.objects.all():
            set_cron_batch_task(batch_task)
