from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = 'admin2@admin.com'
        password = 'admin'
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь {email} успешно создан'))
        else:
            self.stdout.write(self.style.WARNING(f'Пользователь с email {email} уже существует'))
