from django.core.management.base import BaseCommand

from task.models import Tool


class Command(BaseCommand):
    help = 'Is the tool table empty'

    def handle(self, *args, **options):
        if Tool.objects.count() == 0:
            print('Yes')
            exit(0)
        else:
            print('No')
            exit(-1)
