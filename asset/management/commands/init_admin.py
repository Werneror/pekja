from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from pekja.settings import INIT_ADMIN_USER
from pekja.settings import INIT_ADMIN_EMAIL
from pekja.settings import INIT_ADMIN_PASSWORD


class Command(BaseCommand):
    help = 'Create init admin user'

    def handle(self, *args, **options):
        user_model = get_user_model()
        if user_model.objects.count() == 0:
            if INIT_ADMIN_USER is not None:
                admin = user_model.objects.create_superuser(username=INIT_ADMIN_USER, email=INIT_ADMIN_EMAIL,
                                                            password=INIT_ADMIN_PASSWORD)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
            else:
                print('Initialization admin user not found in settings file')
        else:
            print('Admin accounts can only be initialized if no users exist')
