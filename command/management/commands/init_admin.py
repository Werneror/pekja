from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create init admin user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        user_model = get_user_model()
        if user_model.objects.count() == 0:
            admin = user_model.objects.create_superuser(username=options.get('username'), email=options.get('email'),
                                                        password=options.get('password'))
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no users exist')
