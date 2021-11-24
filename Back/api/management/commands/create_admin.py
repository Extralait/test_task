from django.core.management import BaseCommand

from Config import settings
from api.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            for admin in settings.ADMINS:
                User.objects.create_superuser(**admin)
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
