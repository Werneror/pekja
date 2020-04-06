import os
from crontab import CronSlices
from django.core.management.base import BaseCommand
from command.cron_task import set_cron_mail_report


class Command(BaseCommand):
    help = 'Set when to send mail reports'

    def add_arguments(self, parser):
        parser.add_argument('dispatch_file_path', type=str)

    def handle(self, *args, **options):
        file_path = options.get('dispatch_file_path')
        if os.path.exists(file_path):
            with open(file_path) as f:
                dispatch = f.read()
            if CronSlices.is_valid(dispatch):
                set_cron_mail_report(dispatch)
                print('Successfully set the scheduled sending of mail Report.')
            else:
                print('Not a valid cron expression.')
        else:
            print('The file does not exist.')
