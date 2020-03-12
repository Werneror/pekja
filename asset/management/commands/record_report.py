from django.core.management.base import BaseCommand

from pekja.utils import validate_date_str
from pekja.utils import get_today
from asset.report import generate_new_record_report


class Command(BaseCommand):
    help = 'Generate record report and email'

    def add_arguments(self, parser):
        parser.add_argument('date', type=str, nargs='?')

    def handle(self, *args, **options):
        date = options['date']
        if date is None or not validate_date_str(date):
            date = get_today()
        report = generate_new_record_report(date)
        # Todo: 邮件发送报告
