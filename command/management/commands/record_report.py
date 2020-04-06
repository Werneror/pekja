import datetime

from django.core.management.base import BaseCommand

from command.report import generate_new_record_report
from command.report import send_report_by_mail


class Command(BaseCommand):
    help = 'Generate record report and email'

    def add_arguments(self, parser):
        parser.add_argument('date', type=str, nargs='?')

    def handle(self, *args, **options):
        try:
            date = datetime.datetime.strptime('' if options.get('date') is None else options.get('date'), '%Y-%m-%d')
        except ValueError:
            date = datetime.datetime.now()
        report = generate_new_record_report(date)
        send_report_by_mail(date, report)
