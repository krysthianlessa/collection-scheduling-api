from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Creates a superuser."

    def handle(self, *args, **options):
        create = (
            not User.objects.filter(username=settings.DJANGO_SUPERUSER_USERNAME).exists()
            and settings.DJANGO_SUPERUSER_USERNAME
            and settings.DJANGO_SUPERUSER_PASSWORD
        )
        if create:
            User.objects.create_superuser(
                username=settings.DJANGO_SUPERUSER_USERNAME,
                password=settings.DJANGO_SUPERUSER_PASSWORD,
            )
        print("Superuser has been created.")
