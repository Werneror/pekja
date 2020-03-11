from django.core.management.base import BaseCommand

from asset.models import Record


class Command(BaseCommand):
    help = 'Generate record report and email'

    def handle(self, *args, **options):
        pass
        # Todo: 生成记录报告并通过邮件发送
